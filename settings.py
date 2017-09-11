import datetime

LATITUDE=57.743703
LONGITUDE=14.383779
TIME_ZONE="Europe/Stockholm"

UPDATE_INTERVAL_SEC=60

ON_TIME_DIFF_SUNSET=datetime.timedelta( minutes = 0 )
OFF_TIME_DAY_LIST=[ 
	datetime.time(23, 30), 
	datetime.time(23, 30), 
	datetime.time(23, 30),
	datetime.time(23, 30),
	datetime.time(0, 30),
	datetime.time(0, 30),
	datetime.time(23, 30) ] 
LOG_FILE="/home/switch/log/switch.log"

GPIO_1_OUT_PIN=3
GPIO_2_OUT_PIN=5
GPIO_CONTROLLED_OUT_PINS=[GPIO_2_OUT_PIN]

SOCKET_IP=""
SOCKET_PORT=49444
