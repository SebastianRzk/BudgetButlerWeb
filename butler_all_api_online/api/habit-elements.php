<?php


class HabitElement {
	public $date = "undefined";
	public $type = "undefined";
	public $value = "";
	public $id = 0;
	public $habitid = 0;
}


require_once(__DIR__.'/creds.php');

authenticated(function(){
	$auth = getAuth();
	$dbh = getPDO();

	if($_SERVER['REQUEST_METHOD'] === 'PUT'){
		handle_put($auth, $dbh);
	}
	else {
		if (isset($_POST['weeks'])) {
			$weeks = json_decode($_POST['weeks'], true);
			$result = array();
			foreach ($weeks as $day) {
				array_push($result, handle_get_item($auth, $dbh, $day, (int) $_POST['habitid']));
			}
			echo json_encode($result);

		} else {
			echo json_encode(handle_get_item($auth, $dbh, $_POST['date'], (int) $_POST['habitid']));
		}
	}
});


function handle_get_item($auth, $dbh, $date, $habitid){
	$sql = "SELECT habits.type, habit_elements.id, habit_elements.date, habit_elements.value".
			" FROM ((habit_elements".
      				" INNER JOIN habits on habits.id = habit_elements.habit_id)".
     				" INNER JOIN topics on topics.id = habits.topic_id)".
				" WHERE (topics.user = :user AND habits.id = :habitid AND habit_elements.date = :date )";


	$sth = $dbh->prepare($sql);
	$sth->execute(array(':user' => $auth->getUsername(),
			    ':habitid' => $habitid,
			    ':date' => $date));

	$sqlHabitElement = $sth->fetchAll();
	if(count($sqlHabitElement) == 1){
		$sqlElement = $sqlHabitElement[0];
		$result = new HabitElement();
		$result->date = $sqlElement['date'];
		$result->type = $sqlElement['type'];
		$result->value = $sqlElement['value'];
		$result->id = $sqlElement['id'];
		$result->habitid = $habitid;
		return $result;
		echo json_encode($result);
	}
	else {
		$sql = "SELECT habits.type".
				" FROM (habits".
	     				" INNER JOIN topics on topics.id = habits.topic_id)".
					" WHERE (topics.user = :user AND habits.id = :habitid)";

		$sth = $dbh->prepare($sql);
		$sth->execute(array(':user' => $auth->getUsername(),
				    ':habitid' => $habitid));
		$sqlHabit = $sth->fetchAll();
		if(count($sqlHabit) == 1){
			$result = new HabitElement();
			$result->date = $date;
			$result->type = $sqlHabit[0]['type'];
			$result->habitid = $habitid;
			return $result;
		}

	}
}

function handle_put($auth, $dbh){


	$jsondata = file_get_contents('php://input');
	$requestedHabitElement = json_decode($jsondata, true);

	$sql = "SELECT habits.type".
			" FROM (habits".
     				" INNER JOIN topics on topics.id = habits.topic_id)".
				" WHERE (topics.user = :user AND habits.id = :habitid)";

	$sth = $dbh->prepare($sql);
	$sth->execute(array(':user' => $auth->getUsername(),
			    ':habitid' => (int) $requestedHabitElement['habitid']));
	$sqlHabit = $sth->fetchAll();
	if(count($sqlHabit) == 1){
		$value = var_export($requestedHabitElement['value'], true);
		if ($requestedHabitElement['type'] == 'string'){
			$value = $requestedHabitElement['value'];
		}
		// habit belongs to the user
		if(isset($requestedHabitElement['id']) and $requestedHabitElement['id'] != 0){
			// habit element should be updated
			$sql = "SELECT habits.type, habit_elements.id, habit_elements.date, habit_elements.value".
				" FROM ((habit_elements".
	      				" INNER JOIN habits on habits.id = habit_elements.habit_id)".
	     				" INNER JOIN topics on topics.id = habits.topic_id)".
					" WHERE (topics.user = :user AND habits.id = :habitid AND habit_elements.id = :id )";


			$sth = $dbh->prepare($sql);
			$sth->execute(array(':user' => $auth->getUsername(),
					    ':habitid' => (int) $requestedHabitElement['habitid'],
					    ':id' => $requestedHabitElement['id']));

			$sqlHabitElement = $sth->fetchAll();
			if(count($sqlHabitElement) == 1){
				// habit element belongs to the user
				$sql = "UPDATE `habit_elements` SET `value`= :value WHERE `id` = :id";

				$sth = $dbh->prepare($sql);
				$sth->execute(array(':value' => $value,
						    ':id' => $requestedHabitElement['id']));
			}

		}else {
			//habit element should be created
			$sql = "INSERT INTO `habit_elements`(`habit_id`, `date`, `value`) VALUES (:habitid,:date,:value)";

			$sth = $dbh->prepare($sql);
			$sth->execute(array(':value' => $value,
					    ':habitid' => (int) $requestedHabitElement['habitid'],
					    ':date' => $requestedHabitElement['date']));
		}
	}

}

?>