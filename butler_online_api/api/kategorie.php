<?php
require_once(__DIR__.'/util/creds.php');
require_once(__DIR__.'/entityManager.php');

authenticated(function(){
	$auth = getAuth();
	$query = getEntityManager()->createQuery('SELECT u FROM Kategorie u WHERE u.user = :username');
	$query->setParameter('username', $auth->getUsername());
	$kategorien = $query->getResult();
	$dtos = array_map(function ($x){ return $x->asDto();},$kategorien);
	echo json_encode($dtos);
});


?>
