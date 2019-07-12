<?php
require_once(__DIR__.'/util/creds.php');
require_once(__DIR__.'/model.php');

authenticated(function(){
	$auth = getAuth();
	$userAuth = getUserAuth($auth);
	if($userAuth->role == 'admin'){
		$jsondata = file_get_contents('php://input');
		$requestedUser = json_decode($jsondata, true);

		$userId = $auth->register($requestedUser['email'], $requestedUser['password'], $requestedUser['username'],
 			function ($selector, $token) {
 				getAuth()->confirmEmail($selector, $token);
 			});
		$result = new Result();
		$result->message = "Account ".$userId." erfolgreich erstellt";
		echo json_encode($result);
	}
	else {
		$result = new Result();
		$result->result = "ERROR";
		$result->message = "Kein Recht";
		echo json_encode($result);
	}
});
