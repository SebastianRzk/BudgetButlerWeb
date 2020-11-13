<?php
require_once(__DIR__.'/util/creds.php');
require_once(__DIR__.'/model.php');
authenticated(function($auth){
	$dbh = getPDO();
	$partnerstatus =  get_partnerstatus($auth, $dbh);

	if ($partnerstatus->confirmed) {
		$sql = "DELETE FROM `gemeinsamebuchungen` WHERE user = :user OR user = :partner";
		$sth = $dbh->prepare($sql);
		$sth->execute(array(':user' => $auth->getUsername(),
			':partner' => $partnerstatus->partnername ));
	} else {
		$sql = "DELETE FROM `gemeinsamebuchungen` WHERE user = :user";
		$sth = $dbh->prepare($sql);
		$sth->execute(array(':user' => $auth->getUsername()));
	}

});

?>
