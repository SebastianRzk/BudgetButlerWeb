<?php


class Einzelbuchung {
	public $id = 0;
	public $datum = "";
	public $name = "undefined";
	public $kategorie = "undefined";
	public $wert = "undefined";
}

class Result {
	public $result = "OK";
	public $message = "";
}

require_once(__DIR__.'/creds.php');

authenticated(function(){
	$auth = getAuth();
	$dbh = getPDO();

	if($_SERVER['REQUEST_METHOD'] === 'PUT'){
		handle_put($auth, $dbh);
	}else if($_SERVER['REQUEST_METHOD'] === 'DELETE'){
		handle_delete($auth, $dbh);
	}
	else {
		$sql = "SELECT * FROM `einzelbuchungen` WHERE user = :user";
		$sth = $dbh->prepare($sql);
		$sth->execute(array(':user' => $auth->getUsername()));

		$sqlbuchungen = $sth->fetchAll();

		$result = array();

		foreach($sqlbuchungen as $sqlbuchung) {
			$einzelbuchung = new Einzelbuchung();
			$einzelbuchung->id = $sqlbuchung['id'];
			$einzelbuchung->datum = $sqlbuchung['datum'];
			$einzelbuchung->name = $sqlbuchung['name'];
			$einzelbuchung->kategorie = $sqlbuchung['kategorie'];
			$einzelbuchung->wert = $sqlbuchung['wert'];
			array_push($result, $einzelbuchung);
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
	$requestedEinzelbuchung = json_decode($jsondata, true);

	$sql = "DELETE FROM `einzelbuchungen` WHERE `id` = :id AND `user` = :user";
	$sth = $dbh->prepare($sql);
	$sth->execute(array(
		':user' => $auth->getUsername(),
		':id' => (int) $requestedEinzelbuchung['id']
		));
	echo json_encode(new Result());
}

function handle_edit($auth, $dbh){
	$jsondata = file_get_contents('php://input');
	$requestedEinzelbuchung = json_decode($jsondata, true);

	$sql = "SELECT id FROM einzelbuchungen WHERE  einzelbuchungen.id = :id AND einzelbuchungen.user = :user";

	$sth = $dbh->prepare($sql);
	$sth->execute(array(':user' => $auth->getUsername(),
			    ':id' => (int) $requestedEinzelbuchung['id']));
	$sqlHabit = $sth->fetchAll();
	if(count($sqlHabit) == 1){
		$sql = "UPDATE `einzelbuchungen` SET `datum`= :datum, `name` = :name, `kategorie` = :kategorie, `wert` = :wert WHERE `id` = :id";
		$sth = $dbh->prepare($sql);
	$sth->execute(array(':user' => $auth->getUsername(),
			    ':datum' => $requestedEinzelbuchung['datum'],
			    ':name' => $requestedEinzelbuchung['name'],
			    ':kategorie' => $requestedEinzelbuchung['kategorie'],
			    ':wert' => $requestedEinzelbuchung['wert']));
	}

	echo json_encode(new Result());
}


function handle_put($auth, $dbh){
	$jsondata = file_get_contents('php://input');
	$requestedEinzelbuchung = json_decode($jsondata, true);

	$sql = "INSERT INTO `einzelbuchungen`(`user`, `datum`, `name`, `kategorie`, `wert`) VALUES (:user,:datum,:name,:kategorie,:wert)";

	$sth = $dbh->prepare($sql);
	$sth->execute(array(':user' => $auth->getUsername(),
			    ':datum' => getOrDefault($requestedEinzelbuchung, 'datum', '01-01-2019'),
			    ':name' => getOrDefault($requestedEinzelbuchung, 'name', 'kein Name angegeben'),
			    ':kategorie' => getOrDefault($requestedEinzelbuchung, 'kategorie', 'keine Kategorie angegeben'),
			    ':wert' => getOrDefault($requestedEinzelbuchung, 'wert', 0)));
	echo json_encode(new Result());
}

?>
