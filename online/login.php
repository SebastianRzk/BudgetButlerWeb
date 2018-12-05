<?php
require_once(__DIR__.'/layout.php');
$start = '<html>';
$startBody = '<body>
	<header><img src="logo.png" alt="BudgetButlerWeb"></header>
	<div class="content">';
$end = '</div></body></html>';

function auth_failed() {
	$start = '<html>';
	$startBody = '<body>
		<header><img src="logo.png" alt="BudgetButlerWeb"></header>
		<div class="content">';
	$end = '</div></body></html>';
	echo  $start;
	head('Anmeldung fehlgeschlagen');
	echo $startBody;
	echo "Anmeldung fehlgeschlagen<br>";
	echo '<a href="login.php">Einloggen</a>';
	echo $end;
}

require_once(__DIR__.'/creds.php');
try {
	$auth = getAuth();
	if( isset($_POST['email']) and isset($_POST['password'])){
		$auth->login($_POST['email'], $_POST['password']);
	}

	if ($auth->isLoggedIn()) {
		header('Location: dashboard.php');
		die();
	}

	echo $start;
	head('Login');
	echo '<body>
		<header><img src="logo.png" class="bblogo" alt="BudgetButlerWeb"></header>
		<div class="content">
		<form action="login.php" method="post">
		<div>
		Email: <input type="text" name="email" id="email"></input>
		</div>
		<div>
		Passwort: <input type="password" name="password" id="password"></input>
		</div>
		<button class="rightbutton" id="btn_login" type="submit">Login</button>
		</form>';
	echo $end;

}
catch (\Delight\Auth\InvalidEmailException $e) {
	auth_failed();
}
catch (\Delight\Auth\InvalidPasswordException $e) {
	auth_failed();
}
catch (\Delight\Auth\EmailNotVerifiedException $e) {
	auth_failed();
}
catch (\Delight\Auth\TooManyRequestsException $e) {
	auth_failed();
}
?>