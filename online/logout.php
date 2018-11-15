<html>
<?php
require_once(__DIR__.'/layout.php');
head('Logout');
echo '<body class="smallbody">
  <div class="mainimage"><img src="logo.png" class="bblogo" alt="BudgetButlerWeb" width="100%"></div>
  <div class="content">
  <h2>Tschüüs!</h2>';

require_once(__DIR__.'/creds.php');
getAuth()->logOut();
echo '<a href="login.php">Einloggen</a>';
?>
</div>
</body>
</html>