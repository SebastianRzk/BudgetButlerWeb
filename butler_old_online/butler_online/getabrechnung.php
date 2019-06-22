<?php
require_once(__DIR__.'/creds.php');
authenticated(function(){
	$auth = getAuth();
	echo "well done!\r\n\r\n";
	$dbh = getPDO();

	$sql = "SELECT * FROM `eintraege` WHERE person = :person";
	$sth = $dbh->prepare($sql);
	$sth->execute(array(':person' => $auth->getUsername()));
	$alldata = $sth->fetchAll();


	$result = "#######MaschinenimportStart\r\nDatum,Kategorie,Name,Wert,Dynamisch";
	foreach($alldata as $item) {
		$row = $item['datum'].','.str_replace(',',' ',$item['kategorie']).','.str_replace(',',' ',$item['name']).','.str_replace(',','.',$item['wert']).',False';
		$result = $result."\r\n".$row;
	}
	$result = $result."\n#######MaschinenimportEnd\r\n\r\n";
	echo $result;
});
?>