<?php
require_once(__DIR__.'/util/creds.php');
require_once(__DIR__.'/model.php');



authenticated(function($auth){
	$dbh = getPDO();

	if($_SERVER['REQUEST_METHOD'] === 'PUT'){
		delete_existing($auth, $dbh);
		put_element($auth, $dbh);
		$result = new Result();
		$result->message = "Partner erfolgreich gesetzt.";
		echo json_encode($result);
	}else if($_SERVER['REQUEST_METHOD'] === 'DELETE'){
		delete_existing($auth, $dbh);
		$result = new Result();
		$result->message = "Verknüpfung erfolgreich entfernt.";
		echo json_encode($result);
	}
	else {
		echo json_encode(get_partnerstatus($auth, $dbh));
	}
});


function delete_existing($auth, $dbh){
	$sql = "DELETE FROM `partner` WHERE `user` = :user";
	$sth = $dbh->prepare($sql);
	$sth->execute(array(
		':user' => $auth->getUsername(),
		));
}

function put_element($auth, $dbh){
	$jsondata = file_get_contents('php://input');
	$partnerData = json_decode($jsondata, true);

	$sql = "INSERT INTO `partner`(`user`, `partner`, `erweiterteRechte`) VALUES (:user,:partner,:erweiterteRechte)";
	$sth = $dbh->prepare($sql);
	$sth->execute(array(
		':user' => $auth->getUsername(),
		':partner' => $partnerData['partnername'],
		':erweiterteRechte' => 1
		));
}
?>
