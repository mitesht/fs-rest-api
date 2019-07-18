#!/usr/bin/env python
import web
import ESL
import json

urls = (
    '/api/call', 'call',
    '/api/call_list', 'call_list',
    '/api/hangup', 'hangup'
)

app = web.application(urls, globals())

# Make a call and play when the call is answered
class call:
    def POST(self):
        if not web.data():
            # No data. Return 500 - call error
            print("No data found in the request")
            web.header('Content-Type', 'application/json','unique=True')
            raise web.InternalError("{\"message\": \"call error\"}")
        else:
            data = json.loads(web.data())
            if not data:
                # No JSON. Return 500 - call error
                print("No JSON data found in the request")
                web.header('Content-Type', 'application/json','unique=True')
                raise web.InternalError("{\"message\": \"call error\"}")
            else:
                # Fetch destination from JSON
                destination = data["destination"]
                print("Destination: "+destination)
                if not destination:
                    # Destination not found in request JSON. Return 500 - call error
                    web.header('Content-Type', 'application/json','unique=True')
                    raise web.InternalError("{\"message\": \"call error\"}")

        con = ESL.ESLconnection('127.0.0.1', '8021', 'ClueCon')
        if not con.connected():
            # Unable to connect FreeSWITCH
            print("Unable to connect FreeSWITCH")
            web.header('Content-Type', 'application/json','unique=True')
            raise web.InternalError("{\"message\": \"call error\"}")

        temp = "{'origination_caller_id_number=3024561011'}user/"+destination+" &playback(http://s3.amazonaws.com/plivocloud/music.mp3)" 
        cmd = str(temp) 
        
        # Sending command to FreeSWITCH
        print("Initiating Call.. ")
        e = con.api("originate", cmd)
        if e:
            res = e.getBody()
            if (res.find("OK") != -1):
                # Call Successful. Return 201 -ok
                print("Call Successful")
                web.header('Content-Type', 'application/json','unique=True')
                raise web.created("{\"message\": \"ok\"}")
            else:
                # Call Failed. Return 500 - call error
                print("Call Failed")
                web.header('Content-Type', 'application/json','unique=True')
                raise web.InternalError("{\"message\": \"call error\"}")

# Active Call List
class call_list:
    def GET(self):
        con = ESL.ESLconnection('127.0.0.1', '8021', 'ClueCon')
        if not con.connected():
            # Unable to connect FreeSWITCH
            print("Unable to connect FreeSWITCH")
            web.header('Content-Type', 'application/json','unique=True')
            raise web.InternalError("{\"message\": \"active call list error\"}")

        #Sending command to FreeSWITCH
        print("Sending command to FreeSWITCH for call list")
        e = con.api("show calls as json")
        if e:
            # Found active calls. Prasing and makeing list of call uuid. Sending response 200 - ok with list of call uuids in JSON
            print("Active calls found")
            web.header('Content-Type', 'application/json','unique=True')
            calls_str = json.loads(e.getBody())

            arr_call_uuids = []
            if calls_str['row_count'] > 0:
                for call in calls_str['rows']:
                    arr_call_uuids.append(call['call_uuid'])
            raise web.ok(json.dumps(arr_call_uuids))
        else:
            web.header('Content-Type', 'application/json','unique=True')
            raise web.InternalError("{\"message\": \"active call list error\"}")

# Hangup the call
class hangup:
    def POST(self):
        if not web.data():
            # No data. Return 500 - hangup error
            print("No data found in the request")
            web.header('Content-Type', 'application/json','unique=True')
            raise web.InternalError("{\"message\": \"hangup error\"}")
        else:
            data = json.loads(web.data())
            if not data:
                # No JSON. Return 500 - hangup error
                print("No JSON data found in the request")
                web.header('Content-Type', 'application/json','unique=True')
                raise web.InternalError("{\"message\": \"hangup error\"}")
            else:
                # Fetch uuid from JSON
                uuid = data["uuid"]
                if not uuid:
                    # UUID not found in request JSON. Return 500 - hangup error
                    print("UUID not found in JSON")
                    web.header('Content-Type', 'application/json','unique=True')
                    raise web.InternalError("{\"message\": \"hangup error\"}")

        con = ESL.ESLconnection('127.0.0.1', '8021', 'ClueCon')
        if not con.connected():
            # Unable to connect FreeSWITCH
            print("Unable to connect FreeSWITCH")
            web.header('Content-Type', 'application/json','unique=True')
            raise web.InternalError("{\"message\": \"call error\"}")

        # Check if mentioned call exists
        e = con.api(str("uuid_exists "+uuid))
        if (e.getBody() != 'true'):
            # Call does not exists. Return 404 - call not found
            print("Call not found for call uuid:"+uuid)
            web.header('Content-Type', 'application/json','unique=True')
            raise web.notfound("{\"message\": \"call not found\"}")
        else:
            # Call found. Sending command for hangup to FreeSWITCH
            print("Call found. Hanging up..")
            e = con.api(str("uuid_kill "+uuid))

            if (e.getBody().find("OK") != -1):
                # Call hangup Successfully. Return 202 - ok
                print("Call hangup sucessfully. Call UUID:"+uuid)
                web.header('Content-Type', 'application/json','unique=True')
                raise web.accepted("{\"message\": \"ok\"}")
            else:
                # Call hangup failed
                print("Call hangup failed")
                web.header('Content-Type', 'application/json','unique=True')
                raise web.InternalError("{\"message\": \"hangup error\"}")

if __name__ == "__main__":
    app.run()
