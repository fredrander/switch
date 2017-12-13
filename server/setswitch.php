<?php


require 'switchsock.php';


$switchName = $_GET[ "s" ];
$mode = $_GET[ "mode" ];

$cmdStr = "";
if ($mode=="1") {
	$cmdStr="SWITCH=ON";
} else if ($mode=="0") {
	$cmdStr="SWITCH=OFF";
} else if ($mode=="2") {
	$cmdStr="SWITCH=TIMER";
}

$rsp = socket_req_rsp( $switchName, $cmdStr );


?>
