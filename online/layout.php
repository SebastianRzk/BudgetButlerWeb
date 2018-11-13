<?php
function head($pagetitle){
	echo '<head>';
	echo '<link rel="stylesheet" type="text/css" href="style.css">';
	echo '<meta content="text/html; charset=UTF-8; X-Content-Type-Options=nosniff" http-equiv="Content-Type" />';
	echo '<meta http-equiv="Content-Security-Policy" content="default-src: https:">';
	echo '<meta name="referer" content="no-referer"/>';
	echo '<title>BudgetButlerWeb - ';
	echo $pagetitle;
	echo '</title>';
	header('X-Frame-Options: DENY');
	header("X-XSS-Protection: 1; mode=block");
	echo '<link rel="shortcut icon" type="image/png" href="/logo.png">';
	echo '</head>';
}
?>
