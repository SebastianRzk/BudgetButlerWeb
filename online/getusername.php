<?php
require_once('creds.php');
authenticated(function(){
	$auth = getAuth();
	echo $auth->getUsername();
});