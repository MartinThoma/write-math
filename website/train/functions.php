<?php

function insert_userdrawing($user_id, $data, $formula_id) {
    global $pdo;

    $sql = "INSERT INTO `wm_raw_draw_data` (".
                   "`user_id` ,".
                   "`data` ,".
                   "`creation_date` ,".
                   "`user_agent`, ".
                   "`accepted_formula_id`".
                   ") VALUES (:uid, :data, CURRENT_TIMESTAMP, :user_agent, :formula_id);";
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
}

?>