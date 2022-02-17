#!/usr/bin/env python3

import os
from http.server import HTTPServer, CGIHTTPRequestHandler

os.chdir("./docs")

port = int(os.getenv("PORT", 8000))
server_object = HTTPServer(server_address=("", port), RequestHandlerClass=CGIHTTPRequestHandler)
print(f"Starting simple http server on port %d" % port)
server_object.serve_forever()
