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

    $result = new Result();
    $result->message = "Ausgaben erfolgreich gelöscht";
    echo json_encode($result);
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
    $result = new Result();
    $result->message = "Ausgaben erfolgreich hinzugefügt";
    echo json_encode($result);
}

?>
