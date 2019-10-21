<?php
require_once(__DIR__.'/util/creds.php');
require_once(__DIR__.'/model.php');
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
	$result = new Result();
	$result->result = "Fehler";
	$result->message = "Fehler beim Login";
	echo json_encode($result);
}
catch (\Delight\Auth\InvalidPasswordException $e) {
	$result = new Result();
	$result->result = "Fehler";
	$result->message = "Fehler beim Login";
	echo json_encode($result);
}
catch (\Delight\Auth\EmailNotVerifiedException $e) {
	$result = new Result();
	$result->result = "Fehler";
	$result->message = "Fehler beim Login";
	echo json_encode($result);
}
catch (\Delight\Auth\TooManyRequestsException $e) {
	$result = new Result();
	$result->result = "Fehler";
	$result->message = "Fehler beim Login";
	echo json_encode($result);
}
?>
