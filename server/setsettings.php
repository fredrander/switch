<?php


require 'switchsock.php';


$switchName = $_POST[ "s" ];
$settings = $_POST[ "settings" ];

$rsp = socket_req_rsp( $switchName, $settings );

?>
