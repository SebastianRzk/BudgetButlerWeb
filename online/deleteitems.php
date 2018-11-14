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
	echo "failed";
}
catch (\Delight\Auth\InvalidPasswordException $e) {
	echo "failed";
}
catch (\Delight\Auth\EmailNotVerifiedException $e) {
	echo "failed";
}
catch (\Delight\Auth\TooManyRequestsException $e) {
	echo "failed";
}

?>
