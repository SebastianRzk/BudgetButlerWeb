<?php
require_once('creds.php');
authenticated(function(){
	$auth = getAuth();
	$dbh = getPDO();

	$sql = "DELETE FROM `eintraege` WHERE person = :person";
	$sth = $dbh->prepare($sql);
	$sth->execute(array(':person' => $auth->getUsername()));
});
?>
