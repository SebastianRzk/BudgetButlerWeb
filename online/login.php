<?php
$start = '<html>
<head>
  <link rel="stylesheet" type="text/css" href="style.css">
</head>
<body class="smallbody">
  <div class="mainimage"><img src="logo.png" class="bblogo" alt="BudgetButlerWeb" width="100%"></div>
  <div class="content">';

$end = '  </div>
</body>
</html>';

require_once('creds.php');
   try {
	if( isset($_POST['email']) and isset($_POST['password'])){
		$auth = getAuth();
		$auth->login($_POST['email'], $_POST['password']);
		require_once('dashboard.php');
	}
}
catch (\Delight\Auth\InvalidEmailException $e) {
    // wrong email address
    echo  $start;
    echo "wrong email<br>";
    echo '<a href="/login.html">Einloggen</a>';
    echo $end;
}
catch (\Delight\Auth\InvalidPasswordException $e) {
	echo  $start;
	echo "wrong pass<br>";
	echo '<a href="/login.html">Einloggen</a>';
	echo $end;
}
catch (\Delight\Auth\EmailNotVerifiedException $e) {
    // email not verified
       echo  $start;
	echo "email not verified<br>";
	echo '<a href="/login.html">Einloggen</a>';
	echo $end;
}
catch (\Delight\Auth\TooManyRequestsException $e) {
    // too many requests
    echo  $start;
    echo "too many requests<br>";
    echo '<a href="/login.html">Einloggen</a>';
    echo $end;
}


?>


