<?php
require_once(__DIR__.'/util/creds.php');

authenticated(function(){
	$auth = getAuth();
	$sql = "SELECT name FROM `kategorie` WHERE user = :user";
	$sth = getPDO()->prepare($sql);
	$sth->execute(array(':user' => $auth->getUsername()));

	$sqlkategorien = $sth->fetchAll();
	$result = array();

	foreach($sqlkategorien as $sqlkategorie) {
		array_push($result, $sqlkategorie['name']);
	}
	echo json_encode($result);
});


?>
