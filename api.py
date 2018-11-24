"""
This script provides a dummy endpoint, which responds to HTTP calls as if it's a RESTful API.
"""

# --- LIBRARIES --------------------------------------------------------------

import bottle
import argparse
import enum
import os
import sys
import datetime
import routes
from time import sleep
from random import choice
from string import ascii_uppercase
from bottle import HTTPResponse


# --- FUNCTIONS --------------------------------------------------------------

def process_options():
    opts = argparse.ArgumentParser(description="A dummy API")

    CustomEnumType = enum.Enum("CustomEnumType", ("SMALL", "BIG"))

    opts.add_argument("--server", "-s",
                      required=False,
                      default="0.0.0.0",
                      help="Hostname")
    opts.add_argument("--port", "-p",
                      required=False,
                      default=5555,
                      help="Port on which to run the API")
    opts.add_argument("--wait", "-w",
                      required=False,
                      default=0,
                      type=int,
                      help="Millisecond delay in response")
    opts.add_argument("--size", "-z",
                      required=False,
                      default=CustomEnumType.SMALL.name.lower(),
                      choices=tuple(t.name.lower() for t in CustomEnumType),
                      help="API response size [big|small]")
    opts.add_argument("--debug", "-d",
                      required=False,
                      default=False,
                      action="store_true",
                      help="Enable more verbose output in the console window")
    options = opts.parse_args()

    if options.debug:
        bottle.debug(True)
        
    return(
        options.server,
        options.port,
        options.wait,
        options.size
    )


# --- START OF MAIN ----------------------------------------------------------

if __name__ == '__main__':
    (hostname, portnumber, delay, size) = process_options()


    @bottle.route('/thing/:id', method='GET')
    def get_thing(id):
        if size == "small":
            response_json = {
                'data': {
                    'type': 'thing',
                    'id': id,
                    'meta': {
                        'date_retrieved': datetime.datetime.now().isoformat()
                    }
                }
            }
        elif size == "big":
            junk = ''.join(choice(ascii_uppercase) for i in range(10000))

            response_json = {
                'data': {
                    'type': 'thing',
                    'id': id,
                    'attributes': {
                        'stuff': junk
                    },
                    'meta': {
                        'date_retrieved': datetime.datetime.now().isoformat()
                    }
                }
            }


        delayseconds = delay/1000
        sleep(delayseconds)

        bottle.response.headers['Cache-Control'] = 'public,max-age=0'
        return HTTPResponse(status=200, body=response_json)


    @bottle.route('/thing/:id', method='DELETE')
    def delete_thing(id):
        return HTTPResponse(status=204)


    # Starts a local test server.
    bottle.run(server='cherrypy', host=hostname, port=portnumber)