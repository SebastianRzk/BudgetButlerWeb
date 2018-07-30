<?php
require_once('creds.php');
try {
	if( isset($_POST['email']) and isset($_POST['password'])){
		$auth = getAuth();
		$auth->login($_POST['email'], $_POST['password']);
		$dbh = getPDO();


		$sql = "DELETE FROM `eintraege` WHERE person = :person";
		$sth = $dbh->prepare($sql);
		$sth->execute(array(':person' => $auth->getUsername()));

	}
}
catch (\Delight\Auth\InvalidEmailException $e) {
    // wrong email address
    echo "wrong email";
}
catch (\Delight\Auth\InvalidPasswordException $e) {
	echo "wrong pass";
}
catch (\Delight\Auth\EmailNotVerifiedException $e) {
    // email not verified
	echo "email not verified";
}
catch (\Delight\Auth\TooManyRequestsException $e) {
    // too many requests
    echo "too many requests";
}


?>
