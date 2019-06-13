<?php
require __DIR__ . '/vendor/autoload.php';
require_once(__DIR__.'/model.php');

function getPDO(){
	$config_array  = parse_ini_file('db.ini');
	return new PDO('mysql:dbname='.$config_array['db_name'].';host=localhost;charset=utf8mb4', $config_array['db_usr'], $config_array['db_pw']);
}

function online(){
	return false;
}

function getAuth(){
	if(online()){
		ini_set('session.cookie_secure', 1);
		ini_set('session.cookie_httponly', 1);
		ini_set('session.cookie_path', '/');
		ini_set('session.cookie_domain', $_SERVER['HTTP_HOST']);
	}

	$config_array  = parse_ini_file('db.ini');
	// $db = new \PDO('mysql:dbname=my-database;host=localhost;charset=utf8mb4', 'my-username', 'my-password');
	// or
	// $db = new \PDO('pgsql:dbname=my-database;host=localhost;port=5432', 'my-username', 'my-password');
	// or
	// $db = new \PDO('sqlite:../Databases/my-database.sqlite');
	// or
	 $db = new \Delight\Db\PdoDsn('mysql:dbname='.$config_array['db_name'].';host=localhost;charset=utf8mb4', $config_array['db_usr'], $config_array['db_pw']);
	// or
	// $db = new \Delight\Db\PdoDsn('pgsql:dbname=my-database;host=localhost;port=5432', 'my-username', 'my-password');
	// or
	// $db = new \Delight\Db\PdoDsn('sqlite:../Databases/my-database.sqlite');
	return new \Delight\Auth\Auth($db);
}

function authenticated($myfunc){
	try {
		if (getAuth()->isLoggedIn()) {
			$myfunc();
		} else {
			if( isset($_POST['email']) and isset($_POST['password'])){
				$auth = getAuth();
				$auth->login($_POST['email'], $_POST['password']);
				$myfunc();
			} else {
				header('Location: login.php');
				die();
			}
		}
	}
	catch (\Delight\Auth\InvalidEmailException $e) {
		header('Location: login.php');
		die();
	}
	catch (\Delight\Auth\InvalidPasswordException $e) {
		header('Location: login.php');
		die();
	}
	catch (\Delight\Auth\EmailNotVerifiedException $e) {
		header('Location: login.php');
		die();
	}
	catch (\Delight\Auth\TooManyRequestsException $e) {
		header('Location: login.php');
		die();
	}
}

class Auth {
	public $token = "";
	public $username = "";
	public $role = "user";
}

function getUserAuth($auth){
	$result = new Auth();
	$result->token = $_COOKIE["PHPSESSID"];
	$result->username = $auth->getUsername();

	if ($auth->getUsername() == "admin"){
		$result->role = "admin";
	}
	return $result;
}


function get_partnerstatus($auth, $dbh) {
	$sql = 'select partner, erweiterteRechte from partner where user = :user';
	$sth = $dbh->prepare($sql, array(PDO::ATTR_CURSOR => PDO::CURSOR_FWDONLY));
	$sth->execute(array(':user' => $auth->getUsername()));
	$other = $sth->fetchAll();

	$other_person_confirmed = false;
	$erweiterteRechteGeben = false;
	$erweiterteRechteBekommen = false;
	$other_name = '';

	if (sizeof($other) > 0){
		$other_name = array_values($other)[0]['partner'];
		$erweiterteRechteGeben = array_values($other)[0]['erweiterteRechte'] == 1;

		$sql = 'select partner, erweiterteRechte from partner where user = :user';
		$sth = $dbh->prepare($sql, array(PDO::ATTR_CURSOR => PDO::CURSOR_FWDONLY));
		$sth->execute(array(':user' => $other_name));
		$sourceperson = $sth->fetchAll();
		if (sizeof($sourceperson) > 0) {
			$sourceperson_name = array_values($sourceperson)[0]['partner'];
			if (strcmp($sourceperson_name, $auth->getUsername()) == 0){
				$other_person_confirmed = true;
				$erweiterteRechteBekommen = array_values($sourceperson)[0]['erweiterteRechte'] == 1;
			}
		}
	}
	$result = new PartnerInfo();
	$result->partnername = $other_name;
  	$result->confirmed = $other_person_confirmed;
	$result->erweiterteRechteGeben = $erweiterteRechteGeben;
	$result->erweiterteRechteBekommen = $erweiterteRechteBekommen;
	return $result;
}
?>
