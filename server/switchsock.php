<?php


function socket_req_rsp( $switchName, $reqStr ) {

	$switchIni = parse_ini_file( "switch.ini", true );
	$switchIp = $switchIni[ $switchName ][ "ip" ];
	$switchPort = $switchIni[ $switchName ][ "port" ];

	$s = socket_create( AF_INET, SOCK_STREAM, SOL_TCP );
	socket_connect( $s, $switchIp, $switchPort ) or die("Failed to connect socket ".$switchIp.":".$switchPort);
	socket_write( $s, $reqStr );
	$rsp = socket_read( $s, 32768 );
	socket_shutdown( $s );

	return $rsp;
}


?>
