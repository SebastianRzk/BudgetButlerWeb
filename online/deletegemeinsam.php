<?php
require_once('creds.php');

authenticated(function(){
	$auth = getAuth();
	$dbh = getPDO();

	$sql = "DELETE FROM `gemeinsame_eintraege` WHERE person = :person";
	$sth = $dbh->prepare($sql);
	$sth->execute(array(':person' => $auth->getUsername()));

	// Test, ob Verknüpfung mit anderer Person gegeben
	$other_person_selected = false;
	$other_person_confirmed = false;
	$other_name = 'undef';

	$sql = 'select DestinationPerson from gemeinsam_zuordnung where SourcePerson = :sourceperson';
	$sth = $dbh->prepare($sql, array(PDO::ATTR_CURSOR => PDO::CURSOR_FWDONLY));
	$sth->execute(array(':sourceperson' => $auth->getUsername()));
	$other = $sth->fetchAll();

	if (sizeof($other) > 0){
		$other_person_selected = true;
		$other_name = array_values($other)[0]['DestinationPerson'];

		$sql = 'select DestinationPerson from gemeinsam_zuordnung where SourcePerson = :sourceperson';
		$sth = $dbh->prepare($sql, array(PDO::ATTR_CURSOR => PDO::CURSOR_FWDONLY));
		$sth->execute(array(':sourceperson' => $other_name));
		$sourceperson = $sth->fetchAll();
		if (sizeof($sourceperson) > 0) {
			$sourceperson_name = array_values($sourceperson)[0]['DestinationPerson'];
			if (strcmp($sourceperson_name, $auth->getUsername()) == 0){
				$other_person_confirmed = true;
			}
		}
	}
	if ($other_person_confirmed){
		$sql = "DELETE FROM `gemeinsame_eintraege` WHERE person = :person";
		$sth = $dbh->prepare($sql);
		$sth->execute(array(':person' => $other_name));
		echo 'all deleted';
	} else {
		echo 'own deleted';
	}
});

?>