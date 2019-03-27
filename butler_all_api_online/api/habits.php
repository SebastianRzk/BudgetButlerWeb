<?php


class HabitElement {
	public $date = "undefined";
	public $type = "undefined";
	public $value = "undefined";
	public $id = 0;
}


require_once(__DIR__.'/creds.php');

authenticated(function(){
	$auth = getAuth();
	$dbh = getPDO();

	if($_SERVER['REQUEST_METHOD'] === 'PUT'){
		handle_put($auth, $dbh);
	} else if ($_SERVER['REQUEST_METHOD'] === 'DELETE'){
		handle_delete_habit($auth, $dbh);
	}
});



function handle_put($auth, $dbh){
	$jsondata = file_get_contents('php://input');
	$requestedHabit = json_decode($jsondata, true);

	if(isset($requestedHabitElement['id']) and $requestedHabitElement['id'] != 0){
		handle_update($auth, $dbh, $jsondata);
	} else {
		handle_new($auth, $dbh, $jsondata);
	}


}

function handle_update($auth, $dbh, $jsondata){

}


function handle_new($auth, $dbh, $jsondata){
	$sql = "SELECT * FROM `topics` WHERE user = :user AND id = :id";

	$sth = $dbh->prepare($sql);
	$sth->execute(array(':user' => $auth->getUsername(),
			    ':id' => (int) $requestedHabit['topicid']));
	$sqlTopic = $sth->fetchAll();
	if(count($sqlTopic) == 1){
		$sql = "INSERT INTO `habits`(`topic_id`, `type`, `name`, `visibility`) VALUES (:topicid,:type,:name, 'visible')";

		$sth = $dbh->prepare($sql);
		$sth->execute(array(':topicid' => $requestedHabit['topicid'],
				    ':type' => $requestedHabit['valueType'] ,
				    ':name' => $requestedHabit['name']));
	}
}


function handle_delete_habit($auth, $dbh){
	$jsondata = file_get_contents('php://input');
	$requestedHabit = json_decode($jsondata, true);


	$sql = "DELETE FROM habit_elements WHERE EXISTS ".
		"(SELECT * FROM ( topics INNER JOIN habits on habits.topic_id = topics.id) ".
		"WHERE habits.id = :id AND habits.id = habit_elements.habit_id AND topics.user = :user)";

	$sth = $dbh->prepare($sql);
	$sth->execute(array(
		':user' => $auth->getUsername(),
		':id' => $requestedHabit['id']
		));


	$sql = "DELETE FROM habits WHERE EXISTS (".
				    " SELECT *".
				    " FROM topics".
				    " Where habits.id = :id AND".
				    " topics.id = habits.topic_id AND".
				    " topics.user = :user".
				   " )";

	$sth = $dbh->prepare($sql);
	$sth->execute(array(
		':user' => $auth->getUsername(),
		':id' => $requestedHabit['id']
		));
}

?>
