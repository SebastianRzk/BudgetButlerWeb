<?php
require_once(__DIR__.'/util/creds.php');
require_once(__DIR__.'/model.php');
authenticated(function(){
	$auth = getAuth();
	$dbh = getPDO();
	$partnerstatus =  get_partnerstatus($auth, $dbh);

	echo '\n\n';
	if ($partnerstatus->confirmed){
		echo "Connection confirmed \r\n";
		$sql = "SELECT * FROM `gemeinsamebuchungen` WHERE user = :user OR user = :partner";
		$sth = $dbh->prepare($sql);
		$sth->execute(array(	':user' => $auth->getUsername(),
					':partner' => $partnerstatus->partnername));
		$alldata = $sth->fetchAll();
	}
	else {
		// Wenn nicht gegeben
		echo "Connection not confirmed \r\n";
		$sql = "SELECT * FROM `gemeinsamebuchungen` WHERE user = :user";
		$sth = $dbh->prepare($sql);
		$sth->execute(array(':user' => $auth->getUsername()));
		$alldata = $sth->fetchAll();
	}

	$result = "#######MaschinenimportStart\r\nDatum,Kategorie,Name,Wert,Person,Dynamisch";
	foreach($alldata as $item) {
		$row = $item['datum'].','.str_replace(',',' ',$item['kategorie']).','.str_replace(',',' ',$item['name']).','.str_replace(',','.',$item['wert']). ','. str_replace(',','.',$item['zielperson']).',False';
		$result = $result."\r\n".$row;
	}
	$result = $result."\r\n#######MaschinenimportEnd\r\n\r\n";
	echo $result;
});
?>
