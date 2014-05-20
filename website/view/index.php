<?php
require_once '../svg.php';
require_once '../classification.php';
include '../init.php';

function add_classification($user_id, $raw_data_id, $latex, $mode="mathmode", 
                            $packages="") {
    global $pdo;

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
               "`formula_in_latex`, `mode`".
               ") VALUES (:latex, :mode);";
        $stmt = $pdo->prepare($sql);
        $latex = trim($latex);

        $stmt->bindParam(':latex', $latex, PDO::PARAM_STR);
        $stmt->bindParam(':mode', $mode, PDO::PARAM_STR);
        $stmt->execute();
        $formula_id = $pdo->lastInsertId;
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

if (isset($_GET['delete'])) {
    $sql = "DELETE FROM `wm_raw_draw_data` ".
           "WHERE `wm_raw_draw_data`.`id` = :raw_id AND user_id = :user_id";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':raw_id', $_GET['delete'], PDO::PARAM_INT);
    $stmt->bindParam(':user_id', get_uid(), PDO::PARAM_INT);
    $stmt->execute();
    header("Location: ../gallery/");
} elseif (isset($_GET['flag'])) {
    $sql = "INSERT INTO `wm_flags` (`user_id`, `raw_data_id`)".
           "VALUES (:uid,  :raw_data_id);";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':uid', get_uid(), PDO::PARAM_INT);
    $stmt->bindParam(':uid', $_GET['flag'], PDO::PARAM_INT);
    try {
        $result = $stmt->execute();
    } catch (Exception $e) {
        var_dump($e);
    }

    if ($result) {
        mail ("themoosemind@gmail.com", "[Write-Math] flagged symbol",
              "Hallo Martin,\ngerade wurde das Symbol '".intval($_GET['flag']).
              "' geflaggt.");
        $msg[] = array("class" => "alert-info",
                        "text" => "Thank you for flagging this symbol. A ".
                                  "moderator will take a look at it soon.");
    } else {
        $msg[] = array("class" => "alert-warning",
                        "text" => "Flagging did not work. Did you probably ".
                                  "already flag it?");
    }
}

if (isset($_GET['raw_data_id'])) {
    if (isset($_GET['accept'])) {
        $sql = "UPDATE `wm_raw_draw_data` ".
               "SET `accepted_formula_id` = :accepted_id ".
               "WHERE `wm_raw_draw_data`.`id` = :raw_data_id AND ".
               "`user_id` = :uid";
        $stmt = $pdo->prepare($sql);
        $uid = get_uid();
        $stmt->bindParam(':uid', $uid, PDO::PARAM_INT);
        $stmt->bindParam(':accepted_id', $_GET['accept'], PDO::PARAM_INT);
        $stmt->bindParam(':raw_data_id', $_GET['raw_data_id'], PDO::PARAM_INT);
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
        }
    } elseif (isset($_GET['vote'])) {
        // TODO: Check if user has right to vote
        
        $vote = intval($_GET['vote']);
        $id = intval($_GET['raw_data2formula_id']);
        if ($vote == 1 || $vote == -1) {
            try {
                $sql = "INSERT INTO `wm_votes` ".
                        "(`user_id`, `raw_data2formula_id`, `vote`)".
                        "VALUES (:uid,  :raw_data2formula_id, :vote);";
                $stmt = $pdo->prepare($sql);
                $uid = get_uid();
                $stmt->bindParam(':uid', $uid, PDO::PARAM_INT);
                $stmt->bindParam(':raw_data2formula_id', $id, PDO::PARAM_INT);
                $stmt->bindParam(':vote', $vote, PDO::PARAM_INT);
                $stmt->execute();
            } catch (Exception $e) {
                $msg[] = array("class" => "alert-warning",
                               "text" => "You've already casted a vote.");
            }
        }
    }

    $raw_data_id = $_GET['raw_data_id'];
    $sql = "SELECT `user_id`, `display_name`, `data`, ".
           "`creation_date`, `accepted_formula_id` ".
           "FROM `wm_raw_draw_data` ".
           "JOIN `wm_users` ON `wm_users`.`id` = `user_id`".
           "WHERE `wm_raw_draw_data`.`id` = :id";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':id', $_GET['raw_data_id'], PDO::PARAM_INT);
    $stmt->execute();
    $image_data = $stmt->fetchObject();

    // Add a new classification
    if (isset($_POST['latex'])) {
        $user_id = get_uid();
        $latex = $_POST['latex'];
        $raw_data_id = $_GET['raw_data_id'];
        $mode = $_POST['mode'];
        $packages = $_POST['packages'];
        add_classification($user_id, $raw_data_id, $latex, $mode, $packages);
    }

    // Get all probable classifications
    $sql = "SELECT `wm_raw_data2formula`.`id`, `display_name`, ".
           "`formula_in_latex`, `package`, `mode`, `formula_id`, ".
           "`formula_type`, `best_rendering`, ".
           "COALESCE(sum(`vote`), 0) as `votes` ".
           "FROM `wm_raw_data2formula` ".
           "LEFT JOIN `wm_votes` ".
              "ON `wm_votes`.`raw_data2formula_id` = `wm_raw_data2formula`.`id` ".
           "LEFT JOIN `wm_raw_draw_data` ".
              "ON `wm_raw_draw_data`.`id` = `wm_raw_data2formula`.`raw_data_id` ".
          "LEFT JOIN `wm_users` ON `wm_raw_data2formula`.`user_id` = `wm_users`.`id` ".
          "LEFT JOIN `wm_formula` ON `wm_raw_data2formula`.`formula_id` = `wm_formula`.`id` ".
          "WHERE raw_data_id=:id ".
          "GROUP BY `formula_id`";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':id', $_GET['raw_data_id'], PDO::PARAM_INT);
    $stmt->execute();
    $answers = $stmt->fetchAll();
}

$epsilon = isset($_POST['epsilon']) ? $_POST['epsilon'] : 0;

$path = get_path($image_data->data, $epsilon);
$lines_nr = substr_count($path, 'M');
$control_points = substr_count($path, 'L') + $lines_nr;
if ($epsilon > 0) {
    $result_path = apply_douglas_peucker(pointLineList($image_data->data), $epsilon);
} else {
    $result_path = pointLineList($image_data->data);
}
$bounding_box = get_dimensions(list_of_pointlists2pointlist($result_path));
$time_resolution = get_time_resolution(list_of_pointlists2pointlist($result_path), $lines_nr);

// Get all automatic classificaitons:
$sql = "SELECT `formula_id`, `formula_name`, `formula_in_latex`, ".
       "`mode`, `package`, ROUND(`probability`*100, 2) as `probability`, ".
       "`worker_id`, `worker_name`, `best_rendering` ".
       "FROM `wm_worker_answers`  ".
       "JOIN `wm_workers` ON `wm_workers`.`id` = `worker_id` ".
       "JOIN `wm_formula` ON `wm_formula`.`id` = `formula_id` ".
       "WHERE `raw_data_id` = :raw_data_id ".
       "ORDER BY `probability` DESC";
$stmt = $pdo->prepare($sql);
$stmt->bindParam(':raw_data_id', $_GET['raw_data_id'], PDO::PARAM_INT);
$stmt->execute();
$automatic_answers = $stmt->fetchAll();

echo $twig->render('view.twig', array('heading' => 'View',
                                       'logged_in' => is_logged_in(),
                                       'display_name' => $_SESSION['display_name'],
                                       'file' => "view",
                                       'path' => $path,
                                       'image_data' => $image_data,
                                       'raw_data_id' => $raw_data_id,
                                       'answers' => $answers,
                                       'epsilon' => $epsilon,
                                       'msg' => $msg,
                                       'uid' => $_SESSION['uid'],
                                       'lines_nr' => $lines_nr,
                                       'control_points' => $control_points,
                                       'bounding_box' => $bounding_box,
                                       'automatic_answers' => $automatic_answers,
                                       'time_resolution' => $time_resolution
                                       )
                  );

?>