<?php
function head($pagetitle){
	echo '<head>';
	echo '<link rel="stylesheet" type="text/css" href="style.css">';
	echo '<title>BudgetButlerWeb - ';
	echo $pagetitle;
	echo '</title>';
	echo '<link rel="shortcut icon" type="image/png" href="/logo.png">';
	echo '</head>';
}
?>