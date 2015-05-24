<?php
function add_partial_classification($user_id, $raw_data_id, $latex, $strokes) {
    global $pdo;
    global $msg;

    // Very simple spam check (TODO: improve)
    if (strpos($latex,'http://') !== false || strpos($latex,'https://') !== false) {
        return '{"error": "failed spam check"}';
    }

    // Normalize
    $latex_new = normalize($latex);
    if ($latex != $latex_new) {
        $msg[] = array("class" => "alert-info",
                        "text" => "LaTex was normalized from '$latex' to '$latex_new'.");
        $latex = $latex_new;
    }

    // Get formula id if it is already in the database
    $sql = "SELECT `id` FROM `wm_formula` ".
           "WHERE `formula_in_latex` = :latex";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':latex', $latex, PDO::PARAM_STR);
    $stmt->execute();
    $formula_id = $stmt->fetchObject()->id;

    if($formula_id == 0 || $formula_id == null) {
        // it was not in the database. Add it.
        $sql = "INSERT INTO `wm_formula` (".
               "`formula_name`, `formula_in_latex`, `mode`, `package`, `user_id` ".
               ") VALUES (:latex, :latex, :mode, :package, :uid);";
        $stmt = $pdo->prepare($sql);
        $latex = trim($latex);

        $stmt->bindParam(':latex', $latex, PDO::PARAM_STR);
        $mode = 'bothmodes';
        $stmt->bindParam(':mode', $mode, PDO::PARAM_STR);
        $stmt->bindParam(':package', $packages, PDO::PARAM_STR);
        $uid = get_uid();
        $stmt->bindParam(':uid', $uid, PDO::PARAM_INT);
        $stmt->execute();
        $formula_id = $pdo->lastInsertId('id');
    }

    $sql = "INSERT INTO `wm_partial_answer` (".
           "`user_id` ,".
           "`recording_id` ,".
           "`strokes`, ".
           "`symbol_id`".
           ") VALUES (".
           ":user_id, :raw_data_id, :strokes, :symbol_id".
           ");";
    $stmt = $pdo->prepare($sql);
    $uid = get_uid();
    $stmt->bindParam(':user_id', $uid, PDO::PARAM_INT);
    $stmt->bindParam(':raw_data_id', $raw_data_id, PDO::PARAM_INT);
    $stmt->bindParam(':strokes', $strokes, PDO::PARAM_STR);
    $stmt->bindParam(':symbol_id', $formula_id, PDO::PARAM_INT);
    try {
        $stmt->execute();
    } catch (PDOException $e) {
        if ($e->errorInfo[1] == 1062) {
            // duplicate entry, do something else
            return '{"error": "This classification does already exist."}';
        } else {
            return '{"error": ".'.implode(":", $e->errorInfo()).'}';
        }
    }
    return json_encode(1);
}

function filter_strokes($strokes, $total_strokes) {
    $strokes = explode(",", $strokes);
    $filtered_strokes = array();
    foreach ($strokes as $stroke) {
        if (is_numeric($stroke)) {
            $stroke_nr = intval($stroke);
            if (0 <= $stroke_nr && $stroke_nr < $total_strokes) {
                $filtered_strokes[] = $stroke_nr;
            }
        }
    }
    return $filtered_strokes;
}

?>