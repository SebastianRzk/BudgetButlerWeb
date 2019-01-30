<?php
function head($pagetitle){
	header('X-Frame-Options: DENY');
	header('X-XSS-Protection: 1; mode=block');
	header('X-Content-Type-Options: nosniff');
    startHtml();
	echo '<head>';
	echo '<meta http-equiv="Content-Security-Policy" content="default-src: https:">';
	echo '<link rel="stylesheet" type="text/css" href="style.css">';
	echo '<meta name="referer" content="no-referer"/>';
	echo '<link rel="icon" type="image/png" href="logos/logo16.png" sizes="16x16">';
    echo '<link rel="icon" type="image/png" href="logos/logo32.png" sizes="32x32">';
    echo '<link rel="icon" type="image/png" href="logos/logo96.png" sizes="96x96">';
    echo '<link rel="apple-touch-icon" href="logos/logo120.png">';
    echo '<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=0"/>';
    echo '<link rel="apple-touch-icon" sizes="180x180" href="logos/logo180.png">';
	echo '<title>BudgetButlerWeb - ';
	echo $pagetitle;
	echo '</title>';
	echo '</head>';
    startBody();
}

function startHtml(){
    echo '<html>';
}

function startBody(){
    echo '<body><div class="box">
	<header><img src="logos/logo.svg" class="bblogo" alt="BudgetButlerWeb"></header>
	<div class="content">';
}

function endBodyAndHtml(){
    echo '</div></div></body></html>';
}
?>
