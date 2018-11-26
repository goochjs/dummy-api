# dummy-api

This script uses [bottle](https://bottlepy.org/docs/dev/) to provide a simple API, which will react to GET, POST, PATCH and DELETE.  It was originally developed to assist in some performance testing of an API gateway.

You can simply execute it without any parameters, and it will provide an endpoint on http://localhost:555/thing.  Run the script with the `--help` flag for more options (e.g. larger responses to GETs or to add delays in processing).

A Swagger file is included, to describe the API methods.

__

https://github.com/goochjs/dummy-api
