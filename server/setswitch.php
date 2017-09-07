<?php

$on=$_GET["on"];

$cmdStr="";
if ($on=="true" or $on=="1") {
	$cmdStr="SWITCH=ON";
} else {
	$cmdStr="SWITCH=OFF";
}

$s=socket_create( AF_INET, SOCK_STREAM, SOL_TCP );
socket_connect( $s, "10.0.1.112", 49444 ) or die("Failed to connect socket");
socket_write( $s, $cmdStr );
socket_shutdown( $s );
?>
