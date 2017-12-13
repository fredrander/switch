<?php

require 'switchsock.php';


$switchName = $_GET[ "s" ];
$cmdStr = "SWITCH?";
$rsp =  socket_req_rsp( $switchName, $cmdStr );

echo json_encode( $rsp );
?>
