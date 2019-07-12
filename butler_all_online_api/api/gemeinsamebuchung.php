<?php


class GemeinsameBuchung {
	public $id = 0;
	public $datum = "";
	public $name = "undefined";
	public $user = "undefined";
	public $zielperson = "undefined";
	public $kategorie = "undefined";
	public $wert = "undefined";
}

require_once(__DIR__.'/util/creds.php');
require_once(__DIR__.'/model.php');

authenticated(function(){
	$auth = getAuth();
	$dbh = getPDO();

	if($_SERVER['REQUEST_METHOD'] === 'PUT'){
		handle_put($auth, $dbh);
	}else if($_SERVER['REQUEST_METHOD'] === 'DELETE'){
		handle_delete($auth, $dbh);
	}
	else {
		$sth = "";
		$partnerstatus =  get_partnerstatus($auth, $dbh);
		if ($partnerstatus->confirmed == false) {
			$sql = "SELECT * FROM `gemeinsamebuchungen` WHERE user = :user ORDER BY `datum`";
			$sth = $dbh->prepare($sql);
			$sth->execute(array(':user' => $auth->getUsername()));
		} else {
			$sql = "SELECT * FROM `gemeinsamebuchungen` WHERE user = :user OR user = :partner ORDER BY `datum`";
			$sth = $dbh->prepare($sql);
			$sth->execute(array(':user' => $auth->getUsername(),
			':partner' => $partnerstatus->partnername));
		}

		$sqlbuchungen = $sth->fetchAll();

		$result = array();

		foreach($sqlbuchungen as $sqlbuchung) {
			$gemeinsameBuchung = new GemeinsameBuchung();
			$gemeinsameBuchung->id = $sqlbuchung['id'];
			$gemeinsameBuchung->datum = $sqlbuchung['datum'];
			$gemeinsameBuchung->user = $sqlbuchung['user'];
			$gemeinsameBuchung->zielperson = $sqlbuchung['zielperson'];
			$gemeinsameBuchung->name = $sqlbuchung['name'];
			$gemeinsameBuchung->kategorie = $sqlbuchung['kategorie'];
			$gemeinsameBuchung->wert = $sqlbuchung['wert'];
			array_push($result, $gemeinsameBuchung);
		}
		echo json_encode($result);
	}
});

function getOrDefault($param, $key, $default){
	if(isset($param[$key])){
		return $param[$key];
	}
	return $default;
}


function handle_delete($auth, $dbh){
	$jsondata = file_get_contents('php://input');
	$requestetBuchung = json_decode($jsondata, true);

	$sql = "DELETE FROM `gemeinsamebuchungen` WHERE `id` = :id AND `user` = :user";
	$sth = $dbh->prepare($sql);
	$sth->execute(array(
		':user' => $auth->getUsername(),
		':id' => (int) $requestetBuchung['id']
		));

	$partnerstatus =  get_partnerstatus($auth, $dbh);
	$sql = "DELETE FROM `gemeinsamebuchungen` WHERE `id` = :id AND `user` = :user";
	if ($partnerstatus->erweiterteRechteBekommen) {
		$sth = $dbh->prepare($sql);
		$sth->execute(array(
			':user' => $partnerstatus->partnername,
			':id' => (int) $requestetBuchung['id']
			));
	}


	$result = new Result();
	$result->message = "Buchung erfolgreich gelöscht";
	echo json_encode($result);
}


function handle_put($auth, $dbh){
	$jsondata = file_get_contents('php://input');
	$requestetBuchung = json_decode($jsondata, true);
	if (strcmp($requestetBuchung['zielperson'], $auth->getUsername()) == 0) {
		$sql = "INSERT INTO `gemeinsamebuchungen`(`user`, `zielperson` ,`datum`, `name`, `kategorie`, `wert`) VALUES (:user,:zielperson, :datum,:name,:kategorie,:wert)";

		$sth = $dbh->prepare($sql);
		$sth->execute(array(':user' => $auth->getUsername(),
				    ':zielperson' => $auth->getUsername(),
				    ':datum' => getOrDefault($requestetBuchung, 'datum', '01-01-2019'),
				    ':name' => getOrDefault($requestetBuchung, 'name', 'kein Name angegeben'),
				    ':kategorie' => getOrDefault($requestetBuchung, 'kategorie', 'keine Kategorie angegeben'),
				    ':wert' => getOrDefault($requestetBuchung, 'wert', 0)));
	} else {
		$partnerstatus = get_partnerstatus($auth, $dbh);
		$sql = "INSERT INTO `gemeinsamebuchungen`(`user`, `zielperson` ,`datum`, `name`, `kategorie`, `wert`) VALUES (:user,:zielperson, :datum,:name,:kategorie,:wert)";

		$sth = $dbh->prepare($sql);
		$sth->execute(array(':zielperson' => $partnerstatus->partnername,
				    ':user' => $auth->getUsername(),
				    ':datum' => getOrDefault($requestetBuchung, 'datum', '01-01-2019'),
				    ':name' => getOrDefault($requestetBuchung, 'name', 'kein Name angegeben'),
				    ':kategorie' => getOrDefault($requestetBuchung, 'kategorie', 'keine Kategorie angegeben'),
				    ':wert' => getOrDefault($requestetBuchung, 'wert', 0)));
	}
	$result = new Result();
	$result->message = "Buchung erfolgreich hinzugefügt";
	echo json_encode($result);
}

?>
