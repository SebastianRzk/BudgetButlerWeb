<?php
use Doctrine\ORM\Tools\Setup;
use Doctrine\ORM\EntityManager;

require_once "vendor/autoload.php";
require_once __DIR__."/util/creds.php";
function entityManager() {
	// Create a simple "default" Doctrine ORM configuration for Annotations
	$isDevMode = true;
	$config = Setup::createAnnotationMetadataConfiguration(array(__DIR__."/src"), $isDevMode);
	// or if you prefer yaml or XML
	//$config = Setup::createXMLMetadataConfiguration(array(__DIR__."/config/xml"), $isDevMode);
	//$config = Setup::createYAMLMetadataConfiguration(array(__DIR__."/config/yaml"), $isDevMode);

	// obtaining the entity manager
	return EntityManager::create(doctrineConnection(), $config);
}

?>
