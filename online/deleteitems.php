<?php
require_once(__DIR__.'/creds.php');
authenticated(function(){
	$auth = getAuth();
	$dbh = getPDO();

	$sql = "DELETE FROM `eintraege` WHERE person = :person";
	$sth = $dbh->prepare($sql);
	$sth->execute(array(':person' => $auth->getUsername()));
});
?>