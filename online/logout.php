<html>
<head>
  <link rel="stylesheet" type="text/css" href="style.css">
</head>
<body class="smallbody">
  <div class="mainimage"><img src="logo.png" class="bblogo" alt="BudgetButlerWeb" width="100%"></div>
  <div class="content">
  <h2>Tschüüs!</h2>

<?php


require_once('creds.php');
$auth = getAuth();

$auth->logOut();
echo '<a href="/login.html">Einloggen</a>';
?>
</div>
</body>
</html>