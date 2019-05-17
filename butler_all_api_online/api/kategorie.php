<?php


class Topic {
	public $name = "undefined";
	public $id = 0;
	public $habits = array();
}

require_once(__DIR__.'/creds.php');

authenticated(function(){
	$auth = getAuth();
	$sql = "SELECT DISTINCT kategorie FROM `einzelbuchungen` WHERE user = :user";
	$sth = getPDO()->prepare($sql);
	$sth->execute(array(':user' => $auth->getUsername()));

	$sqlkategorien = $sth->fetchAll();
	$result = array();

	foreach($sqlkategorien as $sqlkategorie) {
		array_push($result, $sqlkategorie['kategorie']);
	}
	echo json_encode($result);
});


?>
