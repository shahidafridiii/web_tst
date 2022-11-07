# taken from http://www.piware.de/2011/01/creating-an-https-server-in-python/
# generate server.pem with the following command:
#    openssl req -new -x509 -keyout key.pem -out server.pem -days 365 -nodes
# run as follows:
#    python simple-https-server.py
# then in your browser, visit:
#    https://localhost:4443


import http.server
from http.server import BaseHTTPRequestHandler, HTTPServer
import ssl
import json

class WebServerHandler(BaseHTTPRequestHandler):

   try:
       def do_GET(self):
           data = self.headers.items()
           print('')
           print(10 * '#' + " Request Header Received as GET " + 10 * '#')
           for l in data:
               print(l)
           print(10 * '#' + " Request Header End " + 10 * '#')
           if self.path.endswith("/wrongpage"):
               self.send_error(404, 'File Not Found:')
           else:
               self.send_response(200)
               self.send_header('Content-type', 'text/html')
               self.end_headers()
               output = ""
               output += "<html><body>"
               output += "<h2> How's it going?</h2>"
               output += "<form method = 'POST' enctype='multipart/form-data' action='/hello'> What would you like me to say?</h2><input name = 'message' type = 'text'> <input type = 'submit' value = 'Submit'></form>"
               output += "</body></html>"
               self.wfile.write(output.encode(encoding='utf_8'))
               print(output)

       def do_POST(self):
           # use below 3 lines to get data from post req
           data = self.headers.items()
           print('')
           print(10*'#' + " Request Header Received as POST " + 10*'#')
           for l in data:
               print(l)
           print(10 * '#' + " Request Header End " + 10 * '#')
           # if 'good' in data:
           if self.path.endswith("/get-vnmsha-details") or self.path.endswith("/hello"):
               self.send_response(200)
               self.send_header('Content-type', 'text/html/json')
               self.send_header('accept', 'application/vnd.yang.data+json')
               self.send_header('Accept-Encoding', 'deflate')
               self.end_headers()
               output = {"output": {"status": "SUCCESS",
                                    "vnmsha-dtails": {"mgmt-ip-address": "192.10.10.5", "enabled": "true",
                                                      "designated-master": "true", "mode": "master"}}}
               jsondata = json.dumps(output)
               self.wfile.write(jsondata.encode(encoding="utf_8"))
               print('')
               print(10 * '#' + " Response Header  " + 10 * '#')
               print(jsondata)

           else:
               self.send_response(501)
               self.send_header('Content-type', 'text/json')
               self.end_headers()
               output = "Failed Attempt"
               self.wfile.write(output.encode(encoding="utf_8"))
               print('')
               print(10 * '#' + " Response_info " + 10 * '#')
               print(output)
   except:
       pass


def main():
    try:
        server_address = ('10.229.205.38', 6443)
        httpd = http.server.HTTPServer(server_address, WebServerHandler)
        httpd.socket = ssl.wrap_socket(httpd.socket,
                                       server_side=True,
                                       certfile="my.cer",
                                       keyfile="my.key",
                                       ssl_version=ssl.PROTOCOL_TLS)
        print("Web Server running on port: 6443")
        httpd.serve_forever()
    except KeyboardInterrupt:
        print(" ^C entered, stopping web server....")
        httpd.socket.close()


if __name__ == '__main__':
    main()