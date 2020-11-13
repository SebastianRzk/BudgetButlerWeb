<?php
require_once(__DIR__.'/util/creds.php');
require_once(__DIR__.'/entityManager.php');
require_once(__DIR__.'/model.php');
require_once(__DIR__.'/src/Einzelbuchung.php');


authenticated(function($auth){
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
	$requestedEinzelbuchung = json_decode(file_get_contents('php://input'), true);
	$entityManager = getEntityManager();
	$einzelbuchung = $entityManager->getRepository('Einzelbuchung')->findOneBy(array('user' => $auth->getUsername(), 'id' => $requestedEinzelbuchung['id']));
	$entityManager->remove($einzelbuchung);
	$entityManager->flush();

	$result = new Result();
	$result->message = "Buchung erfolgreich gelöscht";
	echo json_encode($result);
}


function handle_put($auth, $dbh){
	$requestedEinzelbuchung = json_decode(file_get_contents('php://input'), true);

	$neueBuchung = new Einzelbuchung();
	$neueBuchung->setUser($auth->getUsername());
	$neueBuchung->setDatum(date_create(getOrDefault($requestedEinzelbuchung, 'datum', '01-01-2019')));
	$neueBuchung->setName(getOrDefault($requestedEinzelbuchung, 'name', 'kein Name angegeben'));
	$neueBuchung->setKategorie(getOrDefault($requestedEinzelbuchung, 'kategorie', 'keine Kategorie angegeben'));
	$neueBuchung->setWert(getOrDefault($requestedEinzelbuchung, 'wert', 0));

	$entityManager = getEntityManager();
	$entityManager->persist($neueBuchung);
	$entityManager->flush();

	$result = new Result();
	$result->message = "Buchung erfolgreich hinzugefügt";
	echo json_encode($result);
}

?>
