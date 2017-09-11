import socket
import settings
import log
import threading


_callback = {}

def init( callback ):
	log.Add( log.LEVEL_DEBUG, "Start socket thread")
	global _callback
	_callback = callback
	t = threading.Thread(target=_serverThread)
	t.start()


def _handleReq( data ):
	data = data.strip()
	handler = ""
	if data == "SWITCH=ON":
		log.Add( log.LEVEL_DEBUG, "Notify switch on from external interface")
		handler = "on"
	elif data == "SWITCH=OFF":
		log.Add( log.LEVEL_DEBUG, "Notify switch off from external interface")
		handler = "off"
	elif data == "SWITCH=TIMER":
		log.Add( log.LEVEL_DEBUG, "Notify timer mode from external interface")
		handler = "timer"
	elif data == "SWITCH?":
		log.Add( log.LEVEL_DEBUG, "Query switch status from external interface")
		handler = "?"
	else:
		log.Add( log.LEVEL_WARNING, "Unknown req. on external interface: {}".format(data) )

	rsp = "ERROR"
	if handler in _callback:
		rsp = _callback[handler]()
   	return rsp

 
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
			log.Add( log.LEVEL_DEBUG, "Incoming req: {}".format( data ))
			rsp = _handleReq( data )
			if rsp and len(rsp) > 0:
				log.Add( log.LEVEL_DEBUG, "Send rsp: {}".format( rsp ))
				conn.send( rsp )
		conn.close()
		log.Add( log.LEVEL_DEBUG, "Closed connection" )
    
if __name__ == "__main__":
	init()
