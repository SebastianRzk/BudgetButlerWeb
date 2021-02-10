<?php
require_once(__DIR__.'/util/creds.php');
require_once(__DIR__.'/model.php');
require_once(__DIR__.'/entityManager.php');
require_once(__DIR__.'/src/GemeinsameBuchung.php');


authenticated(function($auth){
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
			$query = getEntityManager()->createQuery('SELECT u FROM GemeinsameBuchung u WHERE u.user = :username ORDER BY u.datum');
			$query->setParameter('username', $auth->getUsername());
		} else {
			$query = getEntityManager()->createQuery('SELECT u FROM GemeinsameBuchung u WHERE u.user = :username OR u.user = :partner ORDER BY u.datum');
			$query->setParameter('username', $auth->getUsername());
			$query->setParameter(':partner', $partnerstatus->partnername);
		}
		$dtos = array_map(function ($x){ return $x->asDto();},$query->getResult());
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
	$requestedBuchung = json_decode($jsondata, true)['id'];

	$entityManager = getEntityManager();
	$partnerstatus =  get_partnerstatus($auth, $dbh);

	$query = getEntityManager()->createQuery('DELETE GemeinsameBuchung u WHERE ( u.user = :username OR u.user = :partner ) AND u.id = :id');
	$query->setParameter('username', $auth->getUsername());
	$query->setParameter('partner', $partnerstatus->partnername);
	$query->setParameter('id', $requestedBuchung);
	$query->execute();

	$result = new Result();
	$result->message = "Buchung erfolgreich gelöscht";
	echo json_encode($result);
}


function handle_put($auth, $dbh){
	$jsondata = file_get_contents('php://input');
	$requestedBuchung = json_decode($jsondata, true);

	if (!isset($requestedBuchung['name'])) {
		# compute list;
		echo json_encode(handle_put_list($auth, $dbh, $requestedBuchung));
	}
	else
	{
		# compute single element
		echo json_encode(handle_put_single($auth, $dbh, $requestedBuchung));
	}
}


function handle_put_single($auth, $dbh, $requestedBuchung){
	$neueBuchung = new GemeinsameBuchung();
	$neueBuchung->setUser($auth->getUsername());
	$neueBuchung->setDatum(date_create(getOrDefault($requestedBuchung, 'datum', '01-01-2019')));
	$neueBuchung->setName(getOrDefault($requestedBuchung, 'name', 'kein Name angegeben'));
	$neueBuchung->setKategorie(getOrDefault($requestedBuchung, 'kategorie', 'keine Kategorie angegeben'));
	$neueBuchung->setWert(getOrDefault($requestedBuchung, 'wert', 0));

	if (strcmp($requestedBuchung['zielperson'], $auth->getUsername()) == 0) {
		$neueBuchung->setZielperson($auth->getUsername());
	} else {
		$partnerstatus = get_partnerstatus($auth, $dbh);
		$neueBuchung->setZielperson($partnerstatus->partnername);
	}

	$entityManager = getEntityManager();
	$entityManager->persist($neueBuchung);
	$entityManager->flush();

	$result = new Result();
	$result->message = "Buchung erfolgreich hinzugefügt";
	return $result;
}


function handle_put_list($auth, $dbh, $liste){
	foreach ($liste as $item){
		handle_put_single($auth, $dbh, $item);
	}

	$result = new Result();
	$result->message = "Buchung erfolgreich hinzugefügt";
	return $result;
}


?>
