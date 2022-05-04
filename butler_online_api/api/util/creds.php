<?php
require __DIR__ . '/../vendor/autoload.php';
require_once(__DIR__.'/../model.php');



function choose($key, $config_from_env, $config_from_ini, $default_value){
	if (isset($config_from_env[$key])){
		return $config_from_env[$key];
	}
	if (isset($config_from_ini[$key])){
		return $config_from_ini[$key];
	}
	return $default_value;
}


function getConfig() {
	$config_from_ini  = parse_ini_file(__DIR__.'/../db.ini');
	$config_from_env = getenv();
	return array(
		'db_name' => choose('db_name', $config_from_env, $config_from_ini, 'butler'),
		'db_usr' => choose('db_usr', $config_from_env, $config_from_ini, 'butler'),
		'db_pw' => choose('db_pw', $config_from_env, $config_from_ini, 'butler'),
		'db_host' => choose('db_host', $config_from_env, $config_from_ini, 'localhost')
	);
}

function getPDO(){
	$config_array = getConfig();
	return new PDO('mysql:dbname='.$config_array['db_name'].';host='.$config_array['db_host'].';charset=utf8mb4', $config_array['db_usr'], $config_array['db_pw']);
}

function online(){
	return true;
}

function getAuth(){
	if(online()){
		ini_set('session.cookie_secure', 1);
		ini_set('session.cookie_httponly', 1);
		ini_set('session.cookie_path', '/');
		ini_set('session.cookie_domain', $_SERVER['HTTP_HOST']);
	}

	$config_array  = getConfig();
	// $db = new \PDO('mysql:dbname=my-database;host=localhost;charset=utf8mb4', 'my-username', 'my-password');
	// or
	// $db = new \PDO('pgsql:dbname=my-database;host=localhost;port=5432', 'my-username', 'my-password');
	// or
	// $db = new \PDO('sqlite:../Databases/my-database.sqlite');
	// or
	 $db = new \Delight\Db\PdoDsn('mysql:dbname='.$config_array['db_name'].';host='.$config_array['db_host'].';charset=utf8mb4', $config_array['db_usr'], $config_array['db_pw']);
	// or
	// $db = new \Delight\Db\PdoDsn('pgsql:dbname=my-database;host=localhost;port=5432', 'my-username', 'my-password');
	// or
	// $db = new \Delight\Db\PdoDsn('sqlite:../Databases/my-database.sqlite');
	return new \Delight\Auth\Auth($db);
}

function authenticated($myfunc){
	try {
		$auth = getAuth();
		if ($auth->isLoggedIn()) {
			$myfunc($auth);
		} else {
			if( isset($_POST['email']) and isset($_POST['password'])){
				$auth->login($_POST['email'], $_POST['password']);
				$myfunc($auth);
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
	public $username = "";
	public $role = "user";
}

function getUserAuth($auth){
	$result = new Auth();
	$result->username = $auth->getUsername();

	if ($auth->getUsername() == "admin"){
		$result->role = "admin";
	}
	return $result;
}


function get_partnerstatus($auth, $dbh) {
	$sql = 'select partner from partner where user = :user';
	$sth = $dbh->prepare($sql, array(PDO::ATTR_CURSOR => PDO::CURSOR_FWDONLY));
	$sth->execute(array(':user' => $auth->getUsername()));
	$other = $sth->fetchAll();

	$other_person_confirmed = false;
	$other_name = '';

	if (sizeof($other) > 0){
		$other_name = array_values($other)[0]['partner'];
		$sql = 'select partner from partner where user = :user';
		$sth = $dbh->prepare($sql, array(PDO::ATTR_CURSOR => PDO::CURSOR_FWDONLY));
		$sth->execute(array(':user' => $other_name));
		$sourceperson = $sth->fetchAll();
		if (sizeof($sourceperson) > 0) {
			$sourceperson_name = array_values($sourceperson)[0]['partner'];
			if (strcmp($sourceperson_name, $auth->getUsername()) == 0){
				$other_person_confirmed = true;
			}
		}
	}
	$result = new PartnerInfo();
	$result->partnername = $other_name;
  	$result->confirmed = $other_person_confirmed;
	return $result;
}

function doctrineConnection() {
	$config = new \Doctrine\DBAL\Configuration();
	$config_array  = getConfig();
	$connectionParams = array(
	    'dbname' => $config_array['db_name'],
	    'user' => $config_array['db_usr'],
	    'password' => $config_array['db_pw'],
	    'host' => $config_array['db_host'],
	    'driver' => 'pdo_mysql',
	    'charset'  => 'utf8mb4'
	);
	return \Doctrine\DBAL\DriverManager::getConnection($connectionParams, $config);
}

?>
