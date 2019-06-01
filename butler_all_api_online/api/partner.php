<?php
require_once(__DIR__.'/creds.php');
require_once(__DIR__.'/model.php');



authenticated(function(){
	$auth = getAuth();
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


function get_partnerstatus($auth, $dbh) {
	$sql = 'select partner, erweiterteRechte from partner where user = :user';
	$sth = $dbh->prepare($sql, array(PDO::ATTR_CURSOR => PDO::CURSOR_FWDONLY));
	$sth->execute(array(':user' => $auth->getUsername()));
	$other = $sth->fetchAll();

	$other_person_selected = false;
	$other_person_confirmed = false;
	$erweiterteRechteGeben = false;
	$erweiterteRechteBekommen = false;
	$other_name = '';

	if (sizeof($other) > 0){
		$other_person_selected = true;
		$other_name = array_values($other)[0]['partner'];
		$erweiterteRechteGeben = array_values($other)[0]['erweiterteRechte'];

		$sql = 'select partner, erweiterteRechte from partner where user = :user';
		$sth = $dbh->prepare($sql, array(PDO::ATTR_CURSOR => PDO::CURSOR_FWDONLY));
		$sth->execute(array(':user' => $other_name));
		$sourceperson = $sth->fetchAll();
		if (sizeof($sourceperson) > 0) {
			$sourceperson_name = array_values($sourceperson)[0]['partner'];
			$erweiterteRechteBekommen = array_values($sourceperson)[0]['erweiterteRechte'];
			if (strcmp($sourceperson_name, $auth->getUsername()) == 0){
				$other_person_confirmed = true;
			}
		}
	}
	$result = new PartnerInfo();
	$result->partnername = $other_name;
  	$result->confirmed = $other_person_confirmed;
	$result->erweiterteRechteGeben = $erweiterteRechteGeben;
	$result->erweiterteRechteBekommen = $erweiterteRechteBekommen;
	return $result;
}

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
		':erweiterteRechte' => $partnerData['erweiterteRechteGeben'],
		));
}
?>
