<?php
require_once(__DIR__.'/layout.php');

function auth_failed() {
	head('Anmeldung fehlgeschlagen');
	echo "Anmeldung fehlgeschlagen<br>";
	echo '<a href="login.php">Einloggen</a>';
	echo endBodyAndHtml();
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

	head('Login');
	echo '<form action="login.php" method="post">
		<div>
		Email: <input type="email" name="email" id="email"></input>
		</div>
		<div>
		Passwort: <input type="password" name="password" id="password"></input>
		</div>
		<button class="rightbutton" id="btn_login" type="submit">Login</button>
		</form>';
	echo endBodyAndHtml();

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