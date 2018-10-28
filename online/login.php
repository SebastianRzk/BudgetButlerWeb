<?php
require_once('layout.php');
$start = '<html>';
$startBody = '<body class="smallbody">
	<div class="mainimage"><img src="logo.png" class="bblogo" alt="BudgetButlerWeb" width="100%"></div>
	<div class="content">';
$end = '</div></body></html>';

require_once('creds.php');
   try {
	$auth = getAuth();
	if( isset($_POST['email']) and isset($_POST['password'])){
		$auth->login($_POST['email'], $_POST['password']);
	}

	if ($auth->isLoggedIn()) {
		header('Location: /dashboard.php');
		die();
	}

	echo $start;
	head('Login');
	echo '<body class="smallbody">
		<div class="mainimage"><img src="logo.png" class="bblogo" alt="BudgetButlerWeb" width="100%"></div>
		<div class="content">
		<form action="/login.php" method="post">
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
	// wrong email address
	echo  $start;
	head('Wrong Email');
	echo $startBody;
	echo "wrong email<br>";
	echo '<a href="/login.php">Einloggen</a>';
	echo $end;
}
catch (\Delight\Auth\InvalidPasswordException $e) {
	echo  $start;
	head('Wrong Password');
	echo $startBody;
	echo "wrong pass<br>";
	echo '<a href="/login.php">Einloggen</a>';
	echo $end;
}
catch (\Delight\Auth\EmailNotVerifiedException $e) {
	// email not verified
	echo  $start;
	head('Not verified');
	echo $startBody;
	echo "email not verified<br>";
	echo '<a href="/login.php">Einloggen</a>';
	echo $end;
}
catch (\Delight\Auth\TooManyRequestsException $e) {
    // too many requests
	echo  $start;
	head('Too many requests');
	echo $startBody;
	echo "Too many requests<br>";
	echo '<a href="/login.php">Einloggen</a>';
	echo $end;
}


?>

