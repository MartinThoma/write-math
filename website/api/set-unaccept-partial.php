<?php
include '../init.php';

if (!is_logged_in()) {
    header("Location: ../login");
}

// Returns
// -------
// boolean :
//     true if it was successful, otherwise false
function unaccept_partial_answer($answer_id) {
    global $pdo;
    global $msg;

    $sql = "UPDATE `wm_partial_answer` ".
           "SET `is_accepted` = 0 ".
           "WHERE `id` = :answer_id ".
           "AND (`user_id` = :user_id OR :user_id = 10) ";  # TODO: Change to admin-group check
           "LIMIT 1;";
    $stmt = $pdo->prepare($sql);
    $uid = get_uid();
    $stmt->bindParam(':user_id', $uid, PDO::PARAM_INT);
    $stmt->bindParam(':answer_id', $answer_id, PDO::PARAM_INT);
    $stmt->execute();

    if ($stmt->rowCount() == 1) {
        $msg[] = array("class" => "alert-success",
                       "text" => "The answer was unaccepted.");
        return true;
    } else {
        $msg[] = array("class" => "alert-warning",
                       "text" => "You could not accept that answer. ".
                                 "This happens when you try to accept ".
                                 "a classification of a formula you ".
                                 "did not write. ".
                                 "Or multiple form submission.");
        return false;
    }
}

if (isset($_POST['partial_answer_id'])) {
    $answer_id = intval($_POST['partial_answer_id']);

    $success = unaccept_partial_answer($answer_id);
    if ($success) {
        echo json_encode(1);
    } else {
        echo json_encode(0);
    }
} else {
    echo "{'error': 'Not POSTed partial_answer_id'}";
}

?>