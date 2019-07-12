<?php
// list_products.php
require_once "entityManager.php";
$entityManager = entityManager();
$productRepository = $entityManager->getRepository('einzelbuchung');
$dtos = array_map(function ($x){ return $x->asDTO();},$productRepository->findAll());
echo json_encode($dtos);
