import datetime
import settings


# global constants
# log level
LEVEL_TRACE = "T"
LEVEL_DEBUG = "D"
LEVEL_INFO = "I"
LEVEL_WARNING = "W"
LEVEL_ERROR = "E"

# global variables
_level = LEVEL_INFO

def _checkLevel( level ):
	global _level
	if _level == LEVEL_TRACE:
		return True
	if _level == LEVEL_DEBUG:
		return level != LEVEL_TRACE
	if _level == LEVEL_INFO:
		return level != LEVEL_TRACE and level != LEVEL_DEBUG
	if _level == LEVEL_WARNING:
		return level == LEVEL_WARNING or level == LEVEL_ERROR
	if _level == LEVEL_ERROR:
		return level == level == LEVEL_ERROR
	

def setLevel( level ):
	global _level
	_level = level
	add( LEVEL_INFO, "New log level: {}".format(_level) )
	
	
def add( level, msg ):
	if not _checkLevel( level ):
		return
	
	# replace illegal chars in message
	msg = msg.replace( "/", "\\" )
	msg = msg.replace( "\n", " " )
	# compose log string
	logStr = datetime.datetime.now().isoformat()
	logStr += "/" + level + "/"
	logStr += msg
	logStr += "\n"
	# write to file, stdout if not yet initialized
	with open( settings.getLogFile(), "a") as f:
		f.write( logStr )
