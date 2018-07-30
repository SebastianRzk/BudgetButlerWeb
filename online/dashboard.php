<html>
<head><link rel="stylesheet" type="text/css" href="style.css"></head>
<body class="fullsizebody">
<div class="fullsizecontent">
<div class="mainimage"><img src="logo.png" class="bblogo" alt="BudgetButlerWeb" width="100%"></div>
<?php

require_once('creds.php');
    function showOk($auth)
    {
    	$dbh = getPDO();
	$sql = 'SELECT name
	FROM kategorien
	WHERE person = :person';
	$sth = $dbh->prepare($sql, array(PDO::ATTR_CURSOR => PDO::CURSOR_FWDONLY));
	$sth->execute(array(':person' => $auth->getUsername()));
	$kategorien = $sth->fetchAll();



	echo "<h2> Hallo ";
	echo $auth->getUsername();
	echo ' </h2>
	<a href="/logout.php">Ausloggen</a>

	<h2> Neue Ausgabe erfassen </h2>
	<form action="/dashboard.php" method="post">
	<div>Datum: <input type="date" required="required" name="date" id="date" value="';
	echo date("Y-m-j");
	echo '"> </div>
	<div>Name: <input type="text" required="required" name="name" id="name"> </div>
	<div>Kategorie <select id="kategorie" name="kategorie">
	';

	foreach($kategorien as $k) {
		echo '<option>';
		echo $k['name'];
		echo '</option>';
	}

	echo '
	</select></div>
	<div>Wert: <input type="text" name="wert" required="required" id="wert" pattern="[0-9]+([\.,][0-9]+)?" step="0.01"> </div>
	<button type="submit" class="rightbutton">Speichern</button>
	</form>
	<h2> Passwort ändern </h2>
	<form action="/dashboard.php" method="post">
		<div> Altes Passwort <input type="password" required="required" name="oldPassword" ></input> </div>
		<div> Neues Passwort <input type="password" required="required" name="newPassword" ></input> </div>
		<button type=submit class="rightbutton">Password ändern </button>
	</form>
	';
    }

    function showAdmin(){
	echo '
	<h2> Nutzer registrieren</h2>
	<form action="/dashboard.php" method="post">
	  <div>
	  Nutzername: <input type="text" id="username" name="username"></input>
	  </div>
	  <div>
	  Email: <input type="text" id="email" name="email"></input>
	  </div>
	  <div>
	  Passwort: <input type="password" id="password" name="password"></input>
	  </div>
	  <button type="submit" class="rightbutton">Abschicken</button>
	  </form>';
    }

$auth = getAuth();

if ($auth->isLoggedIn()) {

	if( isset($_POST['oldPassword']) )
	{
		$auth->changePassword($_POST['oldPassword'], $_POST['newPassword']);
		echo "<h2>Passwort geändert</h2>";
	}
	if( isset($_POST['date']) ){
		$dbh = new PDO('mysql:dbname=delight;host=localhost;charset=utf8mb4', 'root', '');
		$sql = "INSERT INTO `eintraege` (`person`, `name`, `kategorie`, `wert`, `datum`) VALUES (:person, :name , :kategorie , :wert , :datum )";
		$sth = $dbh->prepare($sql);
		$sth->execute(array(
				':person' => $auth->getUsername(),
				':name' => (string)$_POST['name'],
				':kategorie' => (string)$_POST['kategorie'],
				':datum' => (string)$_POST['date'],
				':wert' => (string)$_POST['wert']));
		echo "<h2>Eintrag hinzugefügt</h2>";
	}


	showOK($auth);
	if (strcmp($auth->getUsername(), 'admin') == 0){
		showAdmin();
		if( isset($_POST['email']) and isset($_POST['username']) and isset($_POST['password'])){
					try {
			    $userId = $auth->register($_POST['email'], $_POST['password'], $_POST['username'], function ($selector, $token) {});
			    echo "well done";
			}
			catch (\Delight\Auth\InvalidEmailException $e) {
			    // invalid email address
			    echo "invalid email";
			}
			catch (\Delight\Auth\InvalidPasswordException $e) {
			    // invalid password
			    echo "invalid pw";
			}
			catch (\Delight\Auth\UserAlreadyExistsException $e) {
			    // user already exists
				echo "user already exists";
			}
			catch (\Delight\Auth\TooManyRequestsException $e) {
			    // too many requests
			    echo "to many requests";
			}
		}
	}

} else {
	echo "<p> <a href=\"/login.html\">Einloggen </a> <p>";
}
?>
</div>
</body>
</html>