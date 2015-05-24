<?php
include '../init.php';

if (!is_logged_in()) {
    header("Location: ../login");
}

// Returns
// -------
// boolean :
//     true if it was successful, otherwise false
function accept_partial_answer($raw_data_id, $answer_id) {
    global $pdo;
    global $msg;

    // Check if this answer conflicts with other partial answers
    $sql = "SELECT `wm_partial_answer`.`id`, `formula_name`, `strokes`, ".
           "`symbol_id` ".
           "FROM `wm_partial_answer` ".
           "JOIN `wm_formula` ON (`symbol_id` = `wm_formula`.`id`) ".
           "WHERE ".
           "(`is_accepted` = 1 OR `wm_partial_answer`.`id` = :answer_id) ".
           "AND `recording_id` = :recording_id";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':answer_id', $answer_id, PDO::PARAM_INT);
    $stmt->bindParam(':recording_id', $raw_data_id, PDO::PARAM_INT);
    $stmt->execute();
    $partial_answers = $stmt->fetchAll();

    $new_answer = null;
    $aa_strokes = array();
    $aa_symbols = array();
    foreach ($partial_answers as $answer) {
        $answer['strokes'] = explode(',', $answer['strokes']);
        $aa_symbols[] = array('name' => $answer['formula_name'],
                              'id' => $answer['symbol_id']);
        if ($answer['id'] == $answer_id) {
            $new_answer = $answer['strokes'];
        } else {
            $aa_strokes = array_merge($aa_strokes, $answer['strokes']);
            $aa_strokes = array_unique($aa_strokes);
        }
    }

    foreach ($new_answer as $stroke_nr) {
        if (in_array($stroke_nr, $aa_strokes)) {
            // There is an collision
            return '{"error": "You cannot accept this answer, as you '.
                   'have accepted another answer which '.
                   'classifies stroke '.$stroke_nr.', too."}';
        }
    }

    $sql = "UPDATE `wm_partial_answer` ".
           "SET `is_accepted` = 1 ".
           "WHERE `id` = :answer_id ".
           "AND (`user_id` = :user_id OR :user_id = 10) ";  # TODO: Change to admin-group check
           "LIMIT 1;";
    $stmt = $pdo->prepare($sql);
    $uid = get_uid();
    $stmt->bindParam(':user_id', $uid, PDO::PARAM_INT);
    $stmt->bindParam(':answer_id', $answer_id, PDO::PARAM_INT);
    $stmt->execute();

    if ($stmt->rowCount() != 1) {
        return '{"error": "'.$stmt->rowCount().'.'.$uid.'.'.$answer_id.': You could not accept that answer. '.
               "This happens when you try to accept ".
               "a classification of a formula you ".
               "did not write. ".
               "Or multiple form submission: $sql.\"}";
    }

    // Check if this answer classified the whole recording. If that is the case
    // then write the answer in wm_raw_draw_data.accepted_formula_id

    // Get total number of strokes
    $sql = "SELECT `data` ".
           "FROM `wm_raw_draw_data` ".
           "WHERE `wm_raw_draw_data`.`id` = :recording_id";

    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':recording_id', $raw_data_id, PDO::PARAM_INT);
    $stmt->execute();
    $image_data = $stmt->fetchObject();
    $total_strokes = count(json_decode($image_data->data));

    if (count($aa_strokes) + count($new_answer) == $total_strokes) {
        // All strokes were classified and accepted as some symbol

        // Check if there is more then one accepted formula / symbol
        // (excluding WILDPOINT)
        // If there are more, then we are still missing the geometry
        // information
        $other = 0;
        $last_formula_id = 0;
        foreach ($aa_symbols as $symbol) {
            if ($symbol['name'] != 'WILDPOINT' && $symbol['name'] != 'TRASH') {
                $other += 1;
                $last_formula_id = $symbol['id'];
            }
        }

        if ($other == 1) {
            $sql = "UPDATE `wm_raw_draw_data` ".
                   "SET `accepted_formula_id` = :fid ".
                   "WHERE `id` = :raw_data_id AND ".
                   "(`user_id` = :uid OR :uid = 10) LIMIT 1;";  # TODO: Change to admin-group check
            $stmt = $pdo->prepare($sql);
            $uid = get_uid();
            $stmt->bindParam(':uid', $uid, PDO::PARAM_INT);
            $stmt->bindParam(':raw_data_id', $raw_data_id, PDO::PARAM_INT);
            $stmt->bindParam(':fid', $last_formula_id, PDO::PARAM_INT);
            $stmt->execute();
        }
    }
    return true;
}

if (isset($_POST['raw_data_id'])) {
    $raw_data_id = intval($_POST['raw_data_id']);
    $answer_id = intval($_POST['partial_answer_id']);

    $return = accept_partial_answer($raw_data_id, $answer_id);
    if ($return == '') {
        echo json_encode(1);
    } else {
        echo $return;
    }
} else {
    echo json_encode('{"error": "Not POSTed raw_data_id"}');
}

?>