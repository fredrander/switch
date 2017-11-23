import socket
import settings
import log
import threading


_callback = {}

def init( callback ):
	log.add( log.LEVEL_DEBUG, "Start socket thread" )
	global _callback
	_callback = callback
	t = threading.Thread(target=_serverThread)
	t.start()


def _handleReq( data ):
	data = data.strip()
	handler = ""
	if data == "SWITCH=ON":
		log.add( log.LEVEL_DEBUG, "Notify switch on from external interface" )
		handler = "on"
	elif data == "SWITCH=OFF":
		log.add( log.LEVEL_DEBUG, "Notify switch off from external interface" )
		handler = "off"
	elif data == "SWITCH=TIMER":
		log.add( log.LEVEL_DEBUG, "Notify timer mode from external interface" )
		handler = "timer"
	elif data == "SWITCH?":
		log.add( log.LEVEL_DEBUG, "Query switch status from external interface" )
		handler = "?"
	elif data == "SETTINGS?":
		log.add( log.LEVEL_DEBUG, "Request settings from external interface" )
		handler = "settings"
	elif data.startswith( "SETTINGS;" ):
		log.add( log.LEVEL_DEBUG, "New settings from external interface" )
		handler = "set_settings"
	else:
		log.add( log.LEVEL_WARNING, "Unknown req. on external interface: {}".format(data) )

	rsp = "ERROR"
	if handler in _callback:
		rsp = _callback[handler]( data )
   	return rsp

 
def _serverThread():
	log.add( log.LEVEL_DEBUG, "Setup server socket on {}:{}".format( settings.getSocketIp(), settings.getSocketPort() ))
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.bind(( settings.getSocketIp(), settings.getSocketPort() ))
	s.listen(1)
	while True:
		conn, addr = s.accept()
		log.add( log.LEVEL_DEBUG, "Socket connection from {}".format( addr ))
		data = conn.recv(8192)
		if len(data) > 0:
			log.add( log.LEVEL_DEBUG, "Incoming req: {}".format( data ))
			rsp = _handleReq( data )
			if rsp and len(rsp) > 0:
				log.add( log.LEVEL_DEBUG, "Send rsp: {}".format( rsp ))
				conn.send( rsp )
		conn.close()
		log.add( log.LEVEL_DEBUG, "Closed connection" )
    
if __name__ == "__main__":
	init()
