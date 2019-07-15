import ConfigParser
import datetime
import calendar


SETTINGS_FILE = ".settings"

config = ConfigParser.ConfigParser()


def init():
	global config
	config.read( SETTINGS_FILE )

def write():
	global config
	with open( SETTINGS_FILE, "wb" ) as configFile:
		config.write( configFile )
	# re-read
	config.read( SETTINGS_FILE )

def toString():
	result = ""
	with open( SETTINGS_FILE, "r" ) as configFile:
		result = configFile.read()
	return result

def fromString( str ):
    global config
    with open( SETTINGS_FILE, "wb" ) as configFile:
        configFile.write( str )
    # re-read
    config.read( SETTINGS_FILE )

def getLatitude():
	return config.getfloat( "position", "latitude" )

def setLatitude( lat ):
	config.set( "position", "latitude", lat )

def getLongitude():
	return config.getfloat( "position", "longitude" )

def setLongitude( lng ):
	config.set( "position", "longitude", lng )

def getTimeZone():
	return config.get( "position", "timezone" )

def setTimeZone( tz ):
	config.set( "position", "timezone", tz )

def getSunsetEnabled():
	return config.getboolean( "sunset", "enabled" )

def setSunsetEnabled( enabled ):
	config.set( "sunset", "enabled", enabled )

def getSunsetOnTimeDelta():
	diffMinutes = config.getint( "sunset", "on_diff_minutes" )
	return datetime.timedelta( minutes = diffMinutes )

def setSunsetOnTimeDelta( onDiff ):
	config.set( "sunset", "on_diff_minutes", onDiff )

def getSunsetOffTime( wday ):
	dayName = calendar.day_abbr[ wday ]
	settingName = "off_time_{}".format( dayName ).lower()
	timeStr = config.get( "sunset", settingName )
	return datetime.datetime.strptime( timeStr, "%H:%M:%S" ).time()

def setSunsetOffTime( dayAbbr, timeStr ):
	settingName = "off_time_{}".format( dayAbbr ).lower()
	if len( timeStr ) == 5:
		timeStr += ":00"
	config.set( "sunset", settingName, timeStr )

def getSunriseEnabled():
	return config.getboolean( "sunrise", "enabled" )

def setSunriseEnabled( enabled ):
	config.set( "sunrise", "enabled", enabled )

def getSunriseOffTimeDelta():
	diffMinutes = config.getint( "sunrise", "off_diff_minutes" )
	return datetime.timedelta( minutes = diffMinutes )

def setSunriseOffTimeDelta( offDiff ):
	config.set( "sunrise", "off_diff_minutes", offDiff )

def getSunriseOnTime( wday ):
	dayName = calendar.day_abbr[ wday ]
	settingName = "on_time_{}".format( dayName ).lower()
	timeStr = config.get( "sunrise", settingName )
	return datetime.datetime.strptime( timeStr, "%H:%M:%S" ).time()

def setSunriseOnTime( dayAbbr, timeStr ):
	settingName = "on_time_{}".format( dayAbbr ).lower()
	if len( timeStr ) == 5:
		timeStr += ":00"
	config.set( "sunrise", settingName, timeStr )

def getTimerEnabled():
	return config.getboolean( "timer", "enabled" )

def getTimerOnTime( index ):
	settingName = "on_time_{}".format( index )
	timeStr = config.get( "timer", settingName )
	return datetime.datetime.strptime( timeStr, "%H:%M:%S" ).time()

def getTimerOffTime( index ):
	settingName = "off_time_{}".format( index )
	timeStr = config.get( "timer", settingName )
	return datetime.datetime.strptime( timeStr, "%H:%M:%S" ).time()

def getTimerDays( index ):
	settingName = "days_{}".format( index )
	return config.getint( "timer", settingName )

def getGpioOutPins():
	pinStr = config.get( "gpio", "pins" )
	result = []
	splitStr = pinStr.split()
	for s in splitStr:
		result.append( int(s) )
	return result

def getOnValue():
	return config.getint( "gpio", "on_value" )

def getOffValue():
	return config.getint( "gpio", "off_value" )

def getUpdateTimerIntervalSec():
	return config.getint( "interval", "update_timer_sec" )

def getCheckWifiIntervalSec():
	return config.getint( "interval", "check_wifi_sec" )

def getLogFile():
	return config.get( "files", "log_file" )

def getCheckWifiFile():
	return config.get( "files", "wifi_check_script" )

def getRestartWifiFile():
	return config.get( "files", "wifi_restart_script" )

def getSocketPort():
	return config.getint( "socket", "port" )

def getSocketIp():
	val = config.get( "socket", "ip" )
	if ( val == "0" ):
		return ""
	return val


if __name__ == "__main__":
	init()
	print( getSocketIp( ) )

