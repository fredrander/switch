import socket
import settings
import log
import threading


def init():
    log.Add( log.LEVEL_DEBUG, "Start socket thread")
    t = threading.Thread(target=_serverThread)
    t.start()


def _handleReq( data ):
    data = data.strip()
    if data == "SWITCH=ON":
        log.Add( log.LEVEL_INFO, "Switch on from external interface")
    elif data == "SWITCH=OFF":
        log.Add( log.LEVEL_INFO, "Switch off from external interface")
    else:
        log.Add( log.LEVEL_WARNING, "Unknown req. on external interface: {}".format(data) )
    
def _serverThread():
    log.Add( log.LEVEL_DEBUG, "Setup server socket on {}:{}".format( settings.SOCKET_IP, settings.SOCKET_PORT ))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((settings.SOCKET_IP, settings.SOCKET_PORT))
    s.listen(1)
    while True:
        conn, addr = s.accept()
        log.Add( log.LEVEL_DEBUG, "Socket connection from {}".format( addr ))
        data = conn.recv(1024)
        if len(data) > 0:
            log.Add( log.LEVEL_DEBUG, "Incoming req. {}".format( data ))
            _handleReq( data )
        conn.close()
        log.Add( log.LEVEL_DEBUG, "Closed connection" )
    
if __name__ == "__main__":
    init()
