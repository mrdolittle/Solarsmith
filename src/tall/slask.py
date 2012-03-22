'''
Created on Mar 21, 2012

@author: jonas
'''
[].s
#from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
#from SocketServer import ThreadingMixIn
#
#
#class ThreadingServer(ThreadingMixIn, HTTPServer):
#    # Ctrl-C will cleanly kill all spawned threads
#    daemon_threads = True
#    # much faster rebinding
#    allow_reuse_address = True
#
#
#class RequestHandler(BaseHTTPRequestHandler):
#    def _writeheaders(self):
#        self.send_response(200)
#        self.send_header('Content-type', 'text/html')
#        self.end_headers()
#
#    def do_HEAD(self):
#        self._writeheaders()
#
#    def do_GET(self):
#        self._writeheaders()
#        self.wfile.write("""<HTML><HEAD><TITLE>Sample Page</TITLE></HEAD>
#        <BODY>This is a sample HTML page.</BODY></HTML>""")
#
#
## main
#serveraddr = ('', 8001)
#srvr = ThreadingServer(serveraddr, RequestHandler)
#srvr.serve_forever()


