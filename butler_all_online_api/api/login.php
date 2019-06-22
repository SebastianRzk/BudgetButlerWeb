<?php
require_once(__DIR__.'/creds.php');

try {
	$auth = getAuth();
	if( isset($_POST['email']) and isset($_POST['password'])){
		$auth->login($_POST['email'], $_POST['password']);
	}
	if ($auth->isLoggedIn()) {

		echo json_encode(getUserAuth($auth));
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
