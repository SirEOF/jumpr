import socket
from urlparse import urlparse
import thread
import sys


TO_PORT=80

def handleRequest(conn):
    request = ""
    while 1:
        data = conn.recv(1024)
        request += data
        if len(data) != 1024:
            break
    request.strip()
    if len(request) == 0:
        print "EMPTY REQUEST?"
        return conn.close()

    print request

    host = parseHost(request)
    print "HOST", host
    response = retrieveData(host, request)
    print response
    conn.send(response)
    conn.close()

def retrieveData(host, request):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, TO_PORT))
    s.sendall(request)
    response = ""
    while 1:
        data = s.recv(2048)
        print data
        response += data
        if not data:
            print "NOT DATA"
            break

    s.close()
    return response

def resolveHost(host):
    return socket.gethostbyname(str(host.strip()))

def parseHost(request):
    line = request.split('\n')[0].split(' ')

    try:
        host = urlparse(line[1]).netloc
    except:
        print request
        print "Unexpected error:", sys.exc_info()[0]

    return host.strip()

def server():
    HOST = ''                 # Symbolic name meaning the local host
    PORT = 1337               # Arbitrary non-privileged port
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(50)
    while True:
        conn, addr = server.accept()
        print 'Connected by', addr

        thread.start_new_thread(handleRequest, (conn,))

if __name__ == "__main__":
    server()
