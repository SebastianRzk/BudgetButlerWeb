<?php

class Auth {
	public $token = "";
	public $username = "";
}

require_once(__DIR__.'/creds.php');
try {
	$auth = getAuth();
	if( isset($_POST['email']) and isset($_POST['password'])){
		$auth->login($_POST['email'], $_POST['password']);
	}
	if ($auth->isLoggedIn()) {
		$result = new Auth();
		$result->token = $_COOKIE["PHPSESSID"];
		$result->username = $auth->getUsername();
		echo json_encode($result);
	}
}
catch (\Delight\Auth\InvalidEmailException $e) {
}
catch (\Delight\Auth\InvalidPasswordException $e) {
}
catch (\Delight\Auth\EmailNotVerifiedException $e) {
}
catch (\Delight\Auth\TooManyRequestsException $e) {
}
?>
