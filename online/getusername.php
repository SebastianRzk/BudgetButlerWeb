<?php
require_once('creds.php');
if( isset($_POST['email']) and isset($_POST['password'])){
	$auth = getAuth();
	$auth->login($_POST['email'], $_POST['password']);
	echo $auth->getUsername();
}