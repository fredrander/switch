import settings
import log
import subprocess


def check():
    log.add( log.LEVEL_DEBUG, "Check wifi" )
    exitCode = subprocess.call( settings.WIFI_CHECK_SCRIPT )
    result = exitCode == 0
    if result:
        log.add( log.LEVEL_DEBUG, "Wifi up" )
    else:
        log.add( log.LEVEL_DEBUG, "Wifi down" )
    return result


def restart():
    log.add( log.LEVEL_DEBUG, "Restart wifi" )
    exitCode = subprocess.call( settings.WIFI_RESTART_SCRIPT )
    result = exitCode == 0
    if result:
        log.add( log.LEVEL_DEBUG, "Wifi restarted" )
    else:
        log.add( log.LEVEL_DEBUG, "Failed to restart wifi" )
    return result


if __name__ == "__main__":
    if not check():
        log.add( log.LEVEL_WARNING, "Wifi is down" )
        restart()

