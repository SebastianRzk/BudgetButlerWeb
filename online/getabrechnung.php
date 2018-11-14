<?php
require_once('creds.php');
try {
	if( isset($_POST['email']) and isset($_POST['password'])){
		$auth = getAuth();
		$auth->login($_POST['email'], $_POST['password']);
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
	}
}
catch (\Delight\Auth\InvalidEmailException $e) {
	echo "failed";
}
catch (\Delight\Auth\InvalidPasswordException $e) {
	echo "failed";
}
catch (\Delight\Auth\EmailNotVerifiedException $e) {
	echo "failed";
}
catch (\Delight\Auth\TooManyRequestsException $e) {
	echo "failed";
}


?>
