<?php
function head($pagetitle){
	echo '<head>';
	echo '<link rel="stylesheet" type="text/css" href="style.css">';
	echo '<meta content="text/html; charset=UTF-8; X-Content-Type-Options=nosniff" http-equiv="Content-Type" />';
	echo '<title>BudgetButlerWeb - ';
	echo $pagetitle;
	echo '</title>';
	header('X-Frame-Options: DENY');
	echo '<link rel="shortcut icon" type="image/png" href="/logo.png">';
	echo '</head>';
}
?>