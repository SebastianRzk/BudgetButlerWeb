<html>
<?php
require_once(__DIR__.'/layout.php');
head('Logout');
echo '<h2>Tschüüs!</h2>';

require_once(__DIR__.'/creds.php');
getAuth()->logOut();
echo '<nav><a href="login.php">Einloggen</a></nav>';
endBodyAndHtml();
?>
