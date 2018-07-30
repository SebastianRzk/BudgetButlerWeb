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
			$row = $item['datum'].','.$item['kategorie'].','.$item['name'].','.str_replace(',','.',$item['wert']).',False';
			$result = $result."\r\n".$row;
		}
		$result = $result."\n#######MaschinenimportEnd\r\n\r\n";
		echo $result;


		$sql = "DELETE FROM `eintraege` WHERE person = :person";
		$sth = $dbh->prepare($sql);
		$sth->execute(array(':person' => $auth->getUsername()));

	}
}
catch (\Delight\Auth\InvalidEmailException $e) {
    // wrong email address
    echo "wrong email";
}
catch (\Delight\Auth\InvalidPasswordException $e) {
	echo "wrong pass";
}
catch (\Delight\Auth\EmailNotVerifiedException $e) {
    // email not verified
	echo "email not verified";
}
catch (\Delight\Auth\TooManyRequestsException $e) {
    // too many requests
    echo "too many requests";
}


?>
