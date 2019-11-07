<?php
require_once(__DIR__.'/util/creds.php');
require_once(__DIR__.'/model.php');
require_once(__DIR__.'/entityManager.php');
require_once(__DIR__.'/src/GemeinsameBuchung.php');


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

	if ($partnerstatus->erweiterteRechteBekommen) {
		$query = getEntityManager()->createQuery('DELETE GemeinsameBuchung u WHERE ( u.user = :username OR u.user = :partner ) AND u.id = :id');
		$query->setParameter('username', $auth->getUsername());
		$query->setParameter('partner', $partnerstatus->partnername);
		$query->setParameter('id', $requestedBuchung);
		$query->execute();
	} else {
		$einzelbuchung = $entityManager->getRepository('GemeinsameBuchung')->findOneBy(array('user' => $auth->getUsername(), 'id' => $requestedBuchung));
		$entityManager->remove($einzelbuchung);
		$entityManager->flush();
	}

	$result = new Result();
	$result->message = "Buchung erfolgreich gelöscht";
	echo json_encode($result);
}


function handle_put($auth, $dbh){
	$jsondata = file_get_contents('php://input');
	$requestetBuchung = json_decode($jsondata, true);


	$neueBuchung = new GemeinsameBuchung();
	$neueBuchung->setUser($auth->getUsername());
	$neueBuchung->setDatum(date_create(getOrDefault($requestetBuchung, 'datum', '01-01-2019')));
	$neueBuchung->setName(getOrDefault($requestetBuchung, 'name', 'kein Name angegeben'));
	$neueBuchung->setKategorie(getOrDefault($requestetBuchung, 'kategorie', 'keine Kategorie angegeben'));
	$neueBuchung->setWert(getOrDefault($requestetBuchung, 'wert', 0));

	if (strcmp($requestetBuchung['zielperson'], $auth->getUsername()) == 0) {
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
	echo json_encode($result);
}

?>