import socket
import settings
import log
import threading


_cbOn = None
_cbOff = None


def init( cbOn, cbOff ):
	log.Add( log.LEVEL_DEBUG, "Start socket thread")
	global _cbOn
	_cbOn = cbOn
	global _cbOff
	_cbOff = cbOff
	t = threading.Thread(target=_serverThread)
	t.start()


def _handleReq( data ):
	data = data.strip()
	if data == "SWITCH=ON":
		log.Add( log.LEVEL_DEBUG, "Notify switch on from external interface")
		if _cbOn:
			_cbOn()
	elif data == "SWITCH=OFF":
		log.Add( log.LEVEL_DEBUG, "Notify switch off from external interface")
		if _cbOff:
			_cbOff()
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
