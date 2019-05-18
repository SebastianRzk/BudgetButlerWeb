<?php
require_once(__DIR__.'/creds.php');
authenticated(function(){
	$auth = getAuth();
	$dbh = getPDO();

	$sql = "DELETE FROM `einzelbuchungen` WHERE user = :user";
	$sth = $dbh->prepare($sql);
	$sth->execute(array(':user' => $auth->getUsername()));
});
?>
