<?php

function insert_userdrawing($user_id, $data, $formula_id) {
    global $pdo, $msg;

    if (strpos($data, "[]") === false) {
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

        $sql = "INSERT INTO `wm_raw_data2formula` (".
                       "`raw_data_id` ,".
                       "`formula_id` ,".
                       "`user_id`".
                       ") VALUES (".
                       ":raw_data_id, :formula_id, :uid);";
        $stmt = $pdo->prepare($sql);
        $stmt->bindParam(':uid', $user_id, PDO::PARAM_INT);
        $stmt->bindParam(':raw_data_id', $raw_data_id, PDO::PARAM_INT);
        $stmt->bindParam(':formula_id', $formula_id, PDO::PARAM_INT);
        $stmt->execute();
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