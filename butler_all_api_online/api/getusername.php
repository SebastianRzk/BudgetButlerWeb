<?php
require_once(__DIR__.'/creds.php');
authenticated(function(){
	$auth = getAuth();
	echo $auth->getUsername();
});
