<?php
require_once(__DIR__.'/util/creds.php');
require_once(__DIR__.'/entityManager.php');
require_once(__DIR__.'/model.php');
require_once(__DIR__.'/src/Einzelbuchung.php');


authenticated(function(){
	$auth = getAuth();
	$dbh = getPDO();

	if($_SERVER['REQUEST_METHOD'] === 'PUT'){
		handle_put($auth, $dbh);
	}else if($_SERVER['REQUEST_METHOD'] === 'DELETE'){
		handle_delete($auth, $dbh);
	}
	else {
		$query = getEntityManager()->createQuery('SELECT u FROM Einzelbuchung u WHERE u.user = :username ORDER BY u.datum');
		$query->setParameter('username', $auth->getUsername());
		$einzelbuchungen = $query->getResult();
		$dtos = array_map(function ($x){ return $x->asDto();},$einzelbuchungen);
		echo json_encode($dtos);
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
	$entityManager = getEntityManager();
	$einzelbuchung = $entityManager->getRepository('Einzelbuchung')->findOneBy(array('user' => $auth->getUsername(), 'id' => $requestedEinzelbuchung['id']));
	$entityManager->remove($einzelbuchung);
	$entityManager->flush();

	$result = new Result();
	$result->message = "Buchung erfolgreich gelöscht";
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
    $result->message = "Buchung erfolgreich hinzugefügt";
    echo json_encode($result);
}

?>
