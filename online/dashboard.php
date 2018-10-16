<html>
<?php
require_once('layout.php');
head('Dashboard');
echo '<body class="fullsizebody">
<div class="fullsizecontent">
<div class="mainimage"><img src="logo.png" class="bblogo" alt="BudgetButlerWeb" width="100%"></div>
';

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

	$sql = 'select DestinationPerson from gemeinsam_zuordnung where SourcePerson = :sourceperson';
	$sth = $dbh->prepare($sql, array(PDO::ATTR_CURSOR => PDO::CURSOR_FWDONLY));
	$sth->execute(array(':sourceperson' => $auth->getUsername()));
	$other = $sth->fetchAll();


	$other_person_selected = false;
	$other_person_confirmed = false;

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

	echo '<h2> Hallo ';
	echo $auth->getUsername();
	echo ' </h2>
	<a href="/logout.php">Ausloggen</a>';

	if(sizeof($kategorien) == 0) {
		echo '<h2> Noch nicht eingerichtet </h2>
		Bitte synchonisieren Sie ihre locale BudgetButlerWeb installation mit BudgetButlerWeb Online <br>
		Menüpunnkt: "Import / Export" im Feld "Online Kategorien installieren"';
	}
	else {
		echo ' <h2> Neue Ausgabe erfassen </h2>
		<form action="/dashboard.php" method="post">
		<div>Datum: <input type="date" required="required" name="date" id="date" value="';
		echo date('Y-m-d');
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
		</select></div>';
		if ($other_person_confirmed){
			echo '<div>Gemeinsame Buchung<input type="checkbox" name="gemeinsam" value="gemeinsam" title="Gemeinsame Buchung" class="mycheckbox"></div>';
		}
		echo '<div>Wert: <input type="number" name="wert" required="required" id="wert" pattern="[0-9]+([\.,][0-9]+)?" step="0.01"> </div>
		<button type="submit" class="rightbutton">Speichern</button>
		</form>';
	}
	echo '
	<h2> Passwort ändern </h2>
	<form action="/dashboard.php" method="post">
		<div> Altes Passwort <input type="password" required="required" name="oldPassword" ></input> </div>
		<div> Neues Passwort <input type="password" required="required" name="newPassword" ></input> </div>
		<button type=submit class="rightbutton">Password ändern </button>
	</form>
	';

	echo '<p>
			<h2> Gemeinsame Buchungen aktivieren </h2>';

	if ($other_person_selected){
		if ($other_person_confirmed){
			echo '<p id="gemeinschaftsstatus">Gemeinsschaft bestätigt. Gemeinsame Buchungen aktiv.</p>';
		} else {
			echo '<p id="gemeinschaftsstatus">Warten auf Partner.</p>';
		}
		echo '
			<form action="/dashboard.php" method="post">
				<input type="hidden" required="required" name="delete_other" ></input>
				<button type=submit class="rightbutton", id="btn_delete_other">Verknüpfung für gemeinsame Buchungen löschen</button>
			</form>';
	}
	else
	{
		echo '
			<form action="/dashboard.php" method="post" id="other_person_form">
				<div> Andere Person <input type="text" required="required" name="other_person" ></input> </div>
				<button type=submit class="rightbutton" id="add_other_person">Verknüpfung für gemeinsame Buchungen erzeugen</button>
			</form>';
	}
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
	  <button type="submit" class="rightbutton" id="btn_add_user">Abschicken</button>
	  </form>';
    }

$auth = getAuth();

if ($auth->isLoggedIn()) {
	$dbh = getPDO();

	if( isset($_POST['oldPassword']) )
	{
		$auth->changePassword($_POST['oldPassword'], $_POST['newPassword']);
		echo '<h2>Passwort geändert</h2>';
	}


	if( isset($_POST['delete_other']) ){
		$sql = 'DELETE FROM `gemeinsam_zuordnung` WHERE SourcePerson = :sourceperson';
		$sth = $dbh->prepare($sql);
		$sth->execute(array(
				':sourceperson' => $auth->getUsername()));
		echo '<h2> Verknüpfung gelöscht </h2>';
	}

	if( isset($_POST['other_person']) )
	{
		$sql = 'INSERT INTO `gemeinsam_zuordnung` (`SourcePerson`, `DestinationPerson`) VALUES (:source, :destination)';
		$sth = $dbh->prepare($sql);
		$sth->execute(array(
				':source' => $auth->getUsername(),
				':destination' => (string)$_POST['other_person']));
		echo '<h2>Verknüpfung gesetzt</h2>';
	}


	if( isset($_POST['date']) ){
		$sql = 'INSERT INTO `eintraege` (`person`, `name`, `kategorie`, `wert`, `datum`) VALUES (:person, :name , :kategorie , :wert , :datum )';

		if (isset($_POST['gemeinsam'])){
			$sql = 'INSERT INTO `gemeinsame_eintraege` (`person`, `name`, `kategorie`, `wert`, `datum`) VALUES (:person, :name , :kategorie , :wert , :datum )';
		}

		$sth = $dbh->prepare($sql);
		$sth->execute(array(
				':person' => $auth->getUsername(),
				':name' => (string)$_POST['name'],
				':kategorie' => (string)$_POST['kategorie'],
				':datum' => (string)$_POST['date'],
				':wert' => '-'.((string)$_POST['wert'])));

		if  (isset($_POST['gemeinsam'])){
			echo '<h2> Gemeinsame Buchung hinzugefügt</h2>';
		}
		else {
			echo '<h2>Eintrag hinzugefügt</h2>';
		}
	}

	showOK($auth);
	if (strcmp($auth->getUsername(), 'admin') == 0){
		showAdmin();
		if( isset($_POST['email']) and isset($_POST['username']) and isset($_POST['password'])){
					try {
		 		$userId = $auth->register($_POST['email'], $_POST['password'], $_POST['username'],
		 			function ($selector, $token) {
		 				getAuth()->confirmEmail($selector, $token);
		 			});
			    echo 'well done';
			}
			catch (\Delight\Auth\InvalidEmailException $e) {
			    // invalid email address
			    echo 'invalid email';
			}
			catch (\Delight\Auth\InvalidPasswordException $e) {
			    // invalid password
			    echo 'invalid pw';
			}
			catch (\Delight\Auth\UserAlreadyExistsException $e) {
			    // user already exists
				echo 'user already exists';
			}
			catch (\Delight\Auth\TooManyRequestsException $e) {
			    // too many requests
			    echo 'to many requests';
			}
		}
	}

} else {
	echo '<p> <a href="/login.php">Einloggen </a> <p>';
}
?>
</div>
</body>
</html>