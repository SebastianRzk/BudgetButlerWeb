<?php
require_once('creds.php');
authenticated(function(){
	$auth = getAuth();
	echo "well done!";
	$dbh = getPDO();

	$sql = "DELETE FROM `kategorien` WHERE person = :person";
	$sth = $dbh->prepare($sql);
	$sth->execute(array(':person' => $auth->getUsername()));

	$kategorien = explode(',', $_POST['kategorien']);

	foreach($kategorien as $k) {
	$sql = "INSERT INTO `kategorien`(`person`, `name`) VALUES (:person,:kategorie)";
	$sth = $dbh->prepare($sql);
	$sth->execute(array(':person' => $auth->getUsername(),
			':kategorie' => $k));
	}
});
?>