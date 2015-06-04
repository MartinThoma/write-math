<?php

require_once '../view/submit_answer.php';

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


function get_answer_id($raw_data_id, $symbol_id, $strokes) {
    global $pdo;
    global $msg;

    // get strokes
    if ($strokes == 'ALL') {
        $total_strokes = get_stroke_count($raw_data_id);
        $strokes = implode(',', range(0, $total_strokes-1));
    }
    $total_strokes = get_stroke_count($raw_data_id);
    $strokes = implode(',', range(0, $total_strokes-1));
    $user_id = get_uid();
    add_partial_classification_pure($user_id, $raw_data_id, $symbol_id, $strokes);

    $sql = "SELECT `id` ".
           "FROM `wm_partial_answer` ".
           "WHERE `recording_id` = :recording_id AND ".
           "`symbol_id` = :symbol_id LIMIT 1";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':recording_id', $raw_data_id, PDO::PARAM_INT);
    $stmt->bindParam(':symbol_id', $symbol_id, PDO::PARAM_INT);
    $stmt->execute();
    $answer = $stmt->fetchObject();
    return $answer->id;
}

?>