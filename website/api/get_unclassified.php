<?php
include '../init.php';
include '../svg.php';
require_once 'api.functions.php';

function insert_worker_answers($user_id, $raw_data_id, $answer_json) {
    global $pdo;
    // Delete all answers regarding this raw_data_id from the current
    // worker
    $sql = "DELETE FROM `wm_partial_answer` WHERE `user_id` = :wid ".
           "AND `recording_id` = :recording_id;";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':wid', $user_id, PDO::PARAM_INT);
    $stmt->bindParam(':recording_id', $raw_data_id, PDO::PARAM_INT);
    $stmt->execute();
    $delta = -$stmt->rowCount();
    adjust_automatic_answer_count($raw_data_id, $delta);
    // Insert new data
    foreach ($answer_json as $key => $object) {
        // Each object is like
        //    {'probability': 0.9876,
        //     'segmentation': [[0, 1], [2, 4], [3]],
        //     'symbols': [{'id': 543,               <- length has to match
        //                  'probability': 0.123}]      length of segmentation
        //    }
        if (count($object['segmentation']) == 0) {
            echo '{"error": "No valid segmentation given."}';
            return;
        }
        if (count($object['segmentation']) != count($object['symbols'])) {
            echo '{"error": "The number of symbols does not match the '.
                 'segmentation."}';
            return;
        }

        for ($i=0; $i < count($object['segmentation']); $i++) {
            $strokes = implode(',', $object['segmentation'][$i]);
            $symbol = $object['symbols'][$i];
            $symbol_id = $symbol['id'];
            $symbol_prob = $symbol['probability'];
            $sql = "INSERT INTO `wm_partial_answer` (".
                    "`user_id` , ".
                    "`recording_id` , ".
                    "`strokes`, ".
                    "`symbol_id` , ".
                    "`probability`, ".
                    "`is_worker_answer` ".
                    ") VALUES (:wid, :recording_id, :strokes, :formula_id, ".
                    ":probability, 1)";
            $stmt = $pdo->prepare($sql);
            $stmt->bindParam(':wid', $user_id, PDO::PARAM_INT);
            $stmt->bindParam(':recording_id', $raw_data_id, PDO::PARAM_INT);
            $stmt->bindParam(':formula_id', $symbol_id, PDO::PARAM_INT);
            $stmt->bindParam(':probability', $symbol_prob, PDO::PARAM_STR);
            $stmt->bindParam(':strokes', $strokes, PDO::PARAM_STR);
            try {
                $stmt->execute();
                adjust_automatic_answer_count($raw_data_id, 1);
            } catch (Exception $e) {
                var_dump($e);
            }
        }
    }
}


if (isset($_POST['recording_id'])) { // Add a new classification
    // Check if this new classification was made by somebody who is
    // known and identifiable
    // Required Payload:
    // POST
    //    recording_id : int
    //        The raw data item which got classified
    //    api_key : str
    //        Identifier for the workder
    //    results : list of dicts
    //        List of possible classifications with scores for the recording_id
    $sql = "SELECT `id`, `has_user_id` FROM `wm_workers` ".
           "WHERE `API_key` =:api_key ".
           "LIMIT 1";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':api_key', $_POST['api_key'], PDO::PARAM_INT);
    $stmt->execute();
    $row = $stmt->fetch();
    $user_id = $row['has_user_id'];
    if ($user_id != 0) {
        $raw_data_id = intval($_POST['recording_id']);
        $answer_json = json_decode($_POST['results'], true);
        insert_worker_answers($user_id, $raw_data_id, $answer_json);
        echo '{"success": "true"}';
    } else {
        echo '{"error": "api_key \''.$_POST['api_key'].'\' does not exist"}';
    }
} else { // Show recording which needs classification
    $sql = "SELECT `wm_raw_draw_data`.`id`, `data` as `recording`, ".
           "`creation_date`, COUNT(`recording_id`) as `answers` ".
           "FROM `wm_raw_draw_data` ".
           "LEFT OUTER JOIN `wm_partial_answer` ".
                "ON (`recording_id` = `wm_raw_draw_data`.`id`) ".
           "WHERE `accepted_formula_id` IS NULL AND `is_image`=0 ".
           "GROUP BY `wm_raw_draw_data`.`id` ".
           "HAVING `answers` = 0 ".
           "ORDER BY `creation_date` DESC ".
           "LIMIT 1";
    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    $dbrecord = $stmt->fetch();
    echo json_encode($dbrecord);
}



?>