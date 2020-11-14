<?php

require_once(__DIR__.'/creds.php');


function init() {
	$pdo = getPDO();

	$val = $pdo->prepare('select 1 from `einzelbuchungen` LIMIT 1');

	if ( $val->execute() ) {
	    // db initialized
	} else {
	    $sql = file_get_contents(__DIR__.'/sql/base.sql');
	    $pdo->exec($sql);
	}
}
