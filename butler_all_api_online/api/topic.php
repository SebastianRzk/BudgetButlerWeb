<?php


class Topic {
	public $name = "undefined";
	public $id = 0;
	public $habits = array();
}

class Habit {
	public $name = "undefined";
	public $id = 0;
	public $type = "undefined";
}

require_once(__DIR__.'/creds.php');

authenticated(function(){
	$auth = getAuth();
	$dbh = getPDO();

	if($_SERVER['REQUEST_METHOD'] === 'PUT'){
		handle_put($auth, $dbh);
	}else if($_SERVER['REQUEST_METHOD'] === 'DELETE'){
		handle_delete($auth, $dbh);
	}
	else {

		$sql = "SELECT * FROM `topics` WHERE user = :user";
		$sth = $dbh->prepare($sql);
		$sth->execute(array(':user' => $auth->getUsername()));

		$sqltopics = $sth->fetchAll();

		$result = array();

		foreach($sqltopics as $sqltopic) {
			$newTopic = new Topic();
			$newTopic->name = $sqltopic['name'];
			$newTopic->id = $sqltopic['id'];
			array_push($result, $newTopic);



			$sql = "SELECT * FROM `habits` WHERE topic_id = :topic_id";
			$sth = $dbh->prepare($sql);
			$sth->execute(array(':topic_id' => $newTopic->id));
			$habits = $sth->fetchAll();
			foreach($habits as $sqlhabit){
				$newHabit = new Habit();
				$newHabit->name = $sqlhabit['name'];
				$newHabit->id = $sqlhabit['id'];
				$newHabit->type = $sqlhabit['type'];
				array_push($newTopic->habits, $newHabit);
			}
		}
		echo json_encode($result);
	}
});


function handle_delete($auth, $dbh){
	$jsondata = file_get_contents('php://input');
	$requestedTopic = json_decode($jsondata, true);


	//delete habit-elements
	$sql = "DELETE FROM habit_elements WHERE EXISTS ".
		"(SELECT * FROM ( topics INNER JOIN habits on habits.topic_id = topics.id) ".
		"WHERE  habits.topic_id = :id AND habits.id = habit_elements.habit_id AND topics.user = :user)";

	$sth = $dbh->prepare($sql);
	$sth->execute(array(
		':user' => $auth->getUsername(),
		':id' => $requestedTopic['id']
		));


	//delete habits
	$sql = "DELETE FROM habits WHERE EXISTS (".
				    " SELECT *".
				    " FROM topics".
				    " Where habits.topic_id = :id AND".
				    " topics.user = :user".
				   " )";

	$sth = $dbh->prepare($sql);
	$sth->execute(array(
		':user' => $auth->getUsername(),
		':id' => $requestedTopic['id']
		));



	//delete topic
	$sql = "DELETE FROM topics WHERE ".
				    " id = :id AND".
				    " user = :user";

	$sth = $dbh->prepare($sql);
	$sth->execute(array(
		':user' => $auth->getUsername(),
		':id' => $requestedTopic['id']
		));
}


function handle_put($auth, $dbh){
	$jsondata = file_get_contents('php://input');
	$requestedTopic = json_decode($jsondata, true);

	$sql = "INSERT INTO `topics`(`user`, `name`) VALUES (:user,:name)";

	$sth = $dbh->prepare($sql);
	$sth->execute(array(':user' => $auth->getUsername(),
			    ':name' => $requestedTopic['name']));
}

?>