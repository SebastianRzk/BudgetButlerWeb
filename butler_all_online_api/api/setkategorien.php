<?php
require_once(__DIR__.'/util/creds.php');
authenticated(function(){
	$auth = getAuth();
	echo "well done!";
	$dbh = getPDO();

	$sql = "DELETE FROM `kategorie` WHERE user = :user";
	$sth = $dbh->prepare($sql);
	$sth->execute(array(':user' => $auth->getUsername()));

	$kategorien = explode(',', $_POST['kategorien']);

	foreach($kategorien as $k) {
	$sql = "INSERT INTO `kategorie`(`user`, `name`) VALUES (:user,:name)";
	$sth = $dbh->prepare($sql);
	$sth->execute(array(':user' => $auth->getUsername(),
			':name' => $k));
	}
});
?>
