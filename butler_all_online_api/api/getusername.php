<?php
require_once(__DIR__.'/util/creds.php');
authenticated(function(){
	$auth = getAuth();
	echo $auth->getUsername();
});
