<?php

function get_stroke_count($raw_data_id) {
    global $pdo;
    global $msg;

    // Get total number of strokes
    $sql = "SELECT `data` ".
           "FROM `wm_raw_draw_data` ".
           "WHERE `wm_raw_draw_data`.`id` = :recording_id";

    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':recording_id', $raw_data_id, PDO::PARAM_INT);
    $stmt->execute();
    $image_data = $stmt->fetchObject();
    $total_strokes = count(json_decode($image_data->data));
    return $total_strokes;
}

?>