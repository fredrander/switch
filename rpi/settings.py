import datetime

LATITUDE=57.743703
LONGITUDE=14.383779
TIME_ZONE="Europe/Stockholm"

UPDATE_INTERVAL_SEC=60
CHECK_WIFI_INTERVAL_SEC=20

SUNSET_TIMER_ACTIVE=True
SUNSET_ON_TIME_DIFF=datetime.timedelta( minutes = 0 )
SUNSET_OFF_TIME_DAY_LIST=[ 
	datetime.time(23, 30), 
	datetime.time(23, 30), 
	datetime.time(23, 30),
	datetime.time(23, 30),
	datetime.time(0, 30),
	datetime.time(0, 30),
	datetime.time(23, 30) ] 

SUNRISE_TIMER_ACTIVE=True
SUNRISE_OFF_TIME_DIFF=datetime.timedelta( minutes = 0 )
SUNRISE_ON_TIME_DAY_LIST=[ 
	datetime.time(6, 30), 
	datetime.time(6, 30), 
	datetime.time(6, 30),
	datetime.time(6, 30),
	datetime.time(6, 30),
	datetime.time(8, 0),
	datetime.time(8, 0) ] 

LOG_FILE="/home/switch/log/switch.log"

GPIO_1_OUT_PIN=3
GPIO_2_OUT_PIN=5
GPIO_CONTROLLED_OUT_PINS=[GPIO_2_OUT_PIN]

SOCKET_IP=""
SOCKET_PORT=49444

WIFI_CHECK_SCRIPT="/home/switch/checkwifi.sh"
WIFI_RESTART_SCRIPT="/home/switch/restartwifi.sh"

