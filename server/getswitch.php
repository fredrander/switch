<?php

$cmdStr="SWITCH?";

$s=socket_create( AF_INET, SOCK_STREAM, SOL_TCP );
socket_connect( $s, "10.0.1.112", 49444 ) or die("Failed to connect socket");
socket_write( $s, $cmdStr );
$rsp = socket_read( $s, 256 );
socket_shutdown( $s );

echo json_encode($rsp);
?>
