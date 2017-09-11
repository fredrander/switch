<?php

$mode=$_GET["mode"];

$cmdStr="";
if ($mode=="1") {
	$cmdStr="SWITCH=ON";
} else if ($mode=="0") {
	$cmdStr="SWITCH=OFF";
} else if ($mode=="2") {
	$cmdStr="SWITCH=TIMER";
}

$s=socket_create( AF_INET, SOCK_STREAM, SOL_TCP );
socket_connect( $s, "10.0.1.112", 49444 ) or die("Failed to connect socket");
socket_write( $s, $cmdStr );
socket_shutdown( $s );
?>
