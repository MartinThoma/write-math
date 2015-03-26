<?php
require_once 'init.php';

function add_segmentation($recording_id) {
    global $pdo;
    $sql = "SELECT `data` ".
           "FROM `wm_raw_draw_data` ".
           "WHERE `id` = :id";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':id', $recording_id, PDO::PARAM_INT);
    $stmt->execute();
    $image_data = $stmt->fetchObject();
    $raw_data = $image_data->data;
    $strokes = count(json_decode($raw_data, true));

    // Assume it is one symbol
    $segmentation = "";
    for ($i=0; $i < $strokes-1; $i++) {
        $segmentation .= "0";
    }

    $sql = "UPDATE `wm_raw_draw_data` SET `segmentation` = :segmentation ".
           "WHERE `id` = :id;";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':id', $recording_id, PDO::PARAM_INT);
    $stmt->bindParam(':segmentation', $segmentation);
    $stmt->execute();
}


/**
 * $segmentation should be a string of 0s and 1s
 * of length (number of strokes-1)
 * A 0 means two strokes are connected to one symbol, a 1 menas a new symbol
 * begins
 *
 * If no segmentation data is given, it is assumed that the recording is one
 * symbol.
 *
 * Return the segmentation string
 */
function make_valid_segmentation($recording_point_list, $segmentation) {
    global $pdo;
    $required_chars = count($recording_point_list) - 1;
    if (is_null($segmentation)) {
        $segmentation = "";
        for ($i=0; $i < $required_chars; $i++) { 
            $segmentation .= "0";
        }
    } else {
        if (strlen($segmentation) > $required_chars) {
            $segmentation = substr($segmentation, 0, $required_chars);
        } elseif (strlen($segmentation) < $required_chars) {
            for ($i=strlen($segmentation); $i < $required_chars; $i++) { 
                $segmentation .= "0";
            }
        } else {
            // It was already valid
            return $segmentation;
        }
    }

    // Segmentation was invalid. Update in DB
    $sql = "UPDATE `wm_raw_draw_data` SET `segmentation` = :segmentation ".
           "WHERE `id` = :id;";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':id', $recording_id, PDO::PARAM_INT);
    $stmt->bindParam(':segmentation', $segmentation);
    $stmt->execute();

    return $segmentation;
}

?>