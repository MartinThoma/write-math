<?php

require_once('../latex.php');

function add_classification($user_id, $raw_data_id, $latex, $mode="mathmode",
                            $packages="") {
    global $pdo;
    global $msg;

    // Very simple spam check (TODO: improve)
    if (strpos($latex,'http://') !== false || strpos($latex,'https://') !== false) {
        return '';
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
        $stmt->bindParam(':mode', $mode, PDO::PARAM_STR);
        $stmt->bindParam(':package', $packages, PDO::PARAM_STR);
        $uid = get_uid();
        $stmt->bindParam(':uid', $uid, PDO::PARAM_INT);
        $stmt->execute();
        $formula_id = $pdo->lastInsertId('id');
    }

    $sql = "INSERT INTO `wm_raw_data2formula` (".
           "`raw_data_id` ,".
           "`formula_id` ,".
           "`user_id`".
           ") VALUES (".
           ":raw_data_id, :formula_id, :user_id".
           ");";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':raw_data_id', $raw_data_id, PDO::PARAM_INT);
    $stmt->bindParam(':formula_id', $formula_id, PDO::PARAM_INT);
    $uid = get_uid();
    $stmt->bindParam(':user_id', $uid, PDO::PARAM_INT);
    $stmt->execute();
}

function add_partial_classification($user_id, $raw_data_id, $latex, $strokes) {
    global $pdo;
    global $msg;

    // Very simple spam check (TODO: improve)
    if (strpos($latex,'http://') !== false || strpos($latex,'https://') !== false) {
        return '';
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
            $msg[] = array("class" => "alert-warning",
                            "text" => "This classification does already ".
                                      "exist.");
        } else {
            $msg[] = array("class" => "alert-error",
                            "text" => implode(":", $e->errorInfo()));
        }
    }
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

function remove_usepackage($package) {
    if (0 === strpos($package, '\usepackage{') && substr($package, -1) == '}') {
        $package = substr($package, strlen('\usepackage{'));
        $package = rtrim($package, '}');
    }
    return $package;
}

function sanitize_packages($packages) {
    if (strpos($packages, ';') !== false) {
        $packages = explode(';', $packages);
    } else {
        $packages = array($packages);
    }

    $packages = array_map(trim, $packages);
    $packages = array_map(remove_usepackage, $packages);

    return $packages;
}

function endsWith($haystack, $needle) {
    return $needle === "" || substr($haystack, -strlen($needle)) === $needle;
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
            $msg[] = array("class" => "alert-warning",
                           "text" => "You cannot accept this answer, as you ".
                                     "have accepted another answer which ".
                                     "classifies stroke '$stroke_nr', too.");
            return false;
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

    if ($stmt->rowCount() == 1) {
        $msg[] = array("class" => "alert-success",
                       "text" => "Thank you for accepting an answer. ".
                                 "This helps getting better automatic ".
                                 "classifications.");
    } else {
        $msg[] = array("class" => "alert-warning",
                       "text" => "You could not accept that answer. ".
                                 "This happens when you try to accept ".
                                 "a classification of a formula you ".
                                 "did not write. ".
                                 "Or multiple form submission.");
        return false;
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


// Returns
// -------
// boolean :
//     true if it was successful, otherwise false
function unaccept_partial_answer($answer_id) {
    global $pdo;
    global $msg;

    $sql = "UPDATE `wm_partial_answer` ".
           "SET `is_accepted` = 0 ".
           "WHERE `id` = :answer_id ".
           "AND (`user_id` = :user_id OR :user_id = 10) ";  # TODO: Change to admin-group check
           "LIMIT 1;";
    $stmt = $pdo->prepare($sql);
    $uid = get_uid();
    $stmt->bindParam(':user_id', $uid, PDO::PARAM_INT);
    $stmt->bindParam(':answer_id', $answer_id, PDO::PARAM_INT);
    $stmt->execute();

    if ($stmt->rowCount() == 1) {
        $msg[] = array("class" => "alert-success",
                       "text" => "The answer was unaccepted.");
        return true;
    } else {
        $msg[] = array("class" => "alert-warning",
                       "text" => "You could not accept that answer. ".
                                 "This happens when you try to accept ".
                                 "a classification of a formula you ".
                                 "did not write. ".
                                 "Or multiple form submission.");
        return false;
    }
}

?>