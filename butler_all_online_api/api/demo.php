<?php
require_once "entityManager.php";
$entityManager = getEntityManager();
$buchungRepository = $entityManager->getRepository('Einzelbuchung');
echo json_encode($buchungRepository->findAll());
$dtos = array_map(function ($x){ return $x->asDto();},$buchungRepository->findAll());
echo json_encode($dtos);

echo "\n\n\n<br><br>";

$entityMappter = function ($x){return $x->asDto(); };

$query = $entityManager->createQuery('SELECT u FROM Einzelbuchung u WHERE u.user = :username ORDER BY u.datum');
$query->setParameter('username', 'admin');
$einzelbuchungen = $query->getResult();
$dtos = array_map(function ($x){ return $x->asDto();},$einzelbuchungen);
echo print_r($dtos);
echo json_encode($dtos);

echo json_encode($einzelbuchungen);
echo json_encode($dtos, JSON_UNESCAPED_UNICODE);
echo json_last_error();

