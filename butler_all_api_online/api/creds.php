<?php
require __DIR__ . '/vendor/autoload.php';

function getPDO(){
	$config_array  = parse_ini_file('db.ini');
	return new PDO('mysql:dbname='.$config_array['db_name'].';host=localhost;charset=utf8mb4', $config_array['db_usr'], $config_array['db_pw']);
}

function getAuth(){
    //ini_set('session.cookie_secure', 1);
  //  ini_set('session.cookie_httponly', 1);
    //ini_set('session.cookie_path', '/');
    //ini_set('session.cookie_domain', $_SERVER['HTTP_HOST']);
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
?>