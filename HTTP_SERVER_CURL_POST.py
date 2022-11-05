

from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
import json

class WebServerHandler(BaseHTTPRequestHandler):

   try:
       def do_GET(self):
           if self.path.endswith("/hello"):
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
               return

           else:
               self.send_error(404, 'File Not Found:')

       def do_POST(self):
           data = self.rfile.read(int(self.headers.get('Content-Length')))
           data = str(data)
           print(data)
           if 'good' in data:
               self.send_response(200)
               self.send_header('Content-type', 'text/html/json')
               self.end_headers()
               output = {"output": {"status": "SUCCESS",
                                    "vnmsha-dtails": {"mgmt-ip-address": "192.10.10.5", "enabled": "true",
                                                      "designated-master": "true", "mode": "master"}}}
               jsondata = json.dumps(output)
               # output = "Received"
               self.wfile.write(jsondata.encode(encoding="utf_8"))

           else:
               self.send_response(501)
               self.send_header('Content-type', 'text/html')
               self.end_headers()
               output = "Failed Attempt"
               self.wfile.write(output.encode(encoding="utf_8"))

   except:
       pass

def main():
    try:
        port = 6443
        server = HTTPServer(('10.229.205.38', port), WebServerHandler)
        print ("Web Server running on port: 6443")
        server.serve_forever()
    except KeyboardInterrupt:
        print (" ^C entered, stopping web server....")
        server.socket.close()


if __name__ == '__main__':
    main()