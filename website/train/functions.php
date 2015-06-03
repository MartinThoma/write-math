<?php

function insert_recording($user_id, $data, $formula_id) {
    global $pdo, $msg;

    if (strpos($data, "[]") === false) {
        // Search dataset in database to prevent the database from throwing an
        // error to the user if its already present (e.g. multiple form submission)
        $sql = "SELECT `id` FROM `wm_raw_draw_data` ".
               "WHERE `md5data` = MD5(:data);";
        $stmt = $pdo->prepare($sql);
        $stmt->bindParam(':data', $data, PDO::PARAM_STR);
        $stmt->execute();
        $raw_data_set = $stmt->fetchObject();
        if ($raw_data_set === False) {
            $sql = "INSERT INTO `wm_raw_draw_data` (".
                           "`user_id`, ".
                           "`data`, ".
                           "`md5data`, ".
                           "`creation_date`, ".
                           "`user_agent`, ".
                           "`accepted_formula_id`".
                           ") VALUES (:uid, :data, MD5(:data), ".
                           "CURRENT_TIMESTAMP, :user_agent, :formula_id);";
            $stmt = $pdo->prepare($sql);
            $stmt->bindParam(':uid', $user_id, PDO::PARAM_INT);
            $stmt->bindParam(':data', $data, PDO::PARAM_STR);
            $stmt->bindParam(':formula_id', $formula_id, PDO::PARAM_INT);
            $stmt->bindParam(':user_agent', $_SERVER['HTTP_USER_AGENT'], PDO::PARAM_STR);
            $stmt->execute();
            $raw_data_id = $pdo->lastInsertId('id');

            $sql = "INSERT INTO `wm_partial_answer` (".
                           "`recording_id` ,".
                           "`symbol_id` ,".
                           "`user_id`, ".
                           "`strokes` ".
                           ") VALUES (".
                           ":raw_data_id, :formula_id, :uid, :strokes);";
            $stmt = $pdo->prepare($sql);
            $stmt->bindParam(':uid', $user_id, PDO::PARAM_INT);
            $stmt->bindParam(':raw_data_id', $raw_data_id, PDO::PARAM_INT);
            $stmt->bindParam(':formula_id', $formula_id, PDO::PARAM_INT);
            $total_strokes = count(json_decode($data));
            $strokes = implode(',', range(0, $total_strokes-1));
            $stmt->bindParam(':strokes', $strokes, PDO::PARAM_INT);
            $stmt->execute();
        } else {
            $msg[] = array("class" => "alert-warning",
                           "text" => "You've already submitted this data. ".
                                     "Please wait 5 seconds. This time is ".
                                     "needed to compare your recording with ".
                                     "4000 others.");
        }
    } else {
        $msg[] = array("class" => "alert-danger",
                       "text" => "This could not be inserted. It didn't even ".
                                 "have a single point. You sent:<br/>".
                                 "<pre>".$data."</pre> ".
                                 "At the moment I have problems with single ".
                                 "points. This might be a symptom of those ".
                                 "problems. See <a href=\"https://github.com/MartinThoma/write-math/issues/6\">issue 6</a>.");
        return false;
    }

}

?>