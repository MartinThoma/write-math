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

    $segmentation = create_initial_segmentation($raw_data);

    $sql = "UPDATE `wm_raw_draw_data` SET `segmentation` = :segmentation ".
           "WHERE `id` = :id;";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':id', $recording_id, PDO::PARAM_INT);
    $stmt->bindParam(':segmentation', json_encode($segmentation));
    $stmt->execute();
}

function array_delete($array, $element) {
    return array_diff($array, [$element]);
}


function create_initial_segmentation($recording_point_list) {
    $stroke_count = count($recording_point_list);
    // Assume it is exactly one symbol in the recording.
    $segmentation = array(array());
    for ($i=0; $i < $stroke_count; $i++) {
        $segmentation[0][] = $i;
    }
    return $segmentation;
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
    assert(is_null($segmentation)||is_array($segmentation),
           '$segmentation is neither NULL nor array. '.
           'It is '.gettype($segmentation).".");
    $was_invalid = false;
    if (is_null($segmentation) || count($segmentation) == 0) {
        $segmentation = create_initial_segmentation($recording_point_list);
        $was_invalid = true;
    } else {
        $stroke_count = count($recording_point_list);

        // Get rid of everything not in 0...$stroke_count-1
        $new_segmentation = array();
        for ($symbol_i=0; $symbol_i < count($segmentation); $symbol_i++) {
            $new_symbol = array();
            $symbol = $segmentation[$symbol_i];
            for ($stroke_i=0; $stroke_i < count($symbol); $stroke_i++) {
                $stroke_id = $symbol[$stroke_i];
                if (0 <= $stroke_id && $stroke_id < $stroke_count) {
                    $new_symbol[] = $stroke_id;
                } else {
                    $was_invalid = true;
                }
            }
            if (count($new_symbol) > 0) {
                $new_segmentation[] = $new_symbol;
            } else {
                $was_invalid = true;
            }
        }

        if (count($segmentation) == 0) {
            $was_invalid = true;
            $segmentation = create_initial_segmentation($recording_point_list);
        }

        // Now we know we don't have too much in our segmentation.
        // Lets make sure we have enough in it.
        // Make sure that the numbers 0...$stroke_count are in the
        // segmentation.

        // Get a list of keys 0...$stroke_count which we want to see
        // in the segmentation
        $required_keys = array();
        for ($stroke_i=0; $stroke_i < $stroke_count; $stroke_i++) {
            $required_keys[] = $stroke_i;
        }

        for ($symbol_i=0; $symbol_i < count($segmentation); $symbol_i++) {
            $new_symbol = array();
            $symbol = $segmentation[$symbol_i];
            for ($stroke_i=0; $stroke_i < count($symbol); $stroke_i++) {
                $stroke_id = $symbol[$stroke_i];
                $required_keys = array_delete($required_keys, $stroke_id);
            }
        }

        if (count($required_keys) > 0) {
            $was_invalid = true;
            // There are still some stroke keys left. Lets assume they all
            // belong to one symbol.
            $segmentation[] = array_values($required_keys);
        }
    }

    // Sort it
    for ($i=0; $i < count($segmentation); $i++) { 
        sort($segmentation[$i]);
    }
    usort($segmentation, function($a, $b) {
        return $a[0] > $b[0];
    });
    $was_invalid = true; // TODO: Check if sorting changed

    if ($was_invalid) {
        // Segmentation was invalid. Update in DB
        $sql = "UPDATE `wm_raw_draw_data` SET `segmentation` = :segmentation ".
               "WHERE `id` = :id;";
        $stmt = $pdo->prepare($sql);
        $stmt->bindParam(':id', $recording_id, PDO::PARAM_INT);
        $json_segmentation = json_encode($segmentation);
        $stmt->bindParam(':segmentation', $json_segmentation);
        $stmt->execute();
    }

    return $segmentation;
}

?>