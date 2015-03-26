<?php
require_once '../svg.php';
require_once '../classification.php';
require_once '../init.php';
require_once 'functions.php';
require_once '../feature_extraction.php';

if (!isset($_GET['raw_data_id'])) {
    header("Location: ../view/?raw_data_id=295093");
}

$answers = null;
$image_data = null;

if (isset($_GET['add_to_testset']) && is_admin()) {
    $sql = "UPDATE `wm_raw_draw_data` ".
           "SET `is_in_testset` =  '1' ".
           "WHERE `wm_raw_draw_data`.`id` = :rid;";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':rid', $_GET['add_to_testset'], PDO::PARAM_INT);
    $stmt->execute();
} elseif (isset($_GET['remove_from_testset']) && is_admin()) {
    $sql = "UPDATE `wm_raw_draw_data` ".
           "SET `is_in_testset` =  '0' ".
           "WHERE `wm_raw_draw_data`.`id` = :rid;";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':rid', $_GET['remove_from_testset'], PDO::PARAM_INT);
    $stmt->execute();
}

/*if (isset($_GET['request_new_classification'])) {
    $raw_data_id = intval($_GET['request_new_classification']);

    // Get raw data
    $sql = "SELECT `data` FROM `wm_raw_draw_data` WHERE `id` = :rid LIMIT 1";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':rid', $raw_data_id, PDO::PARAM_INT);
    $stmt->execute();
    $draw = $stmt->fetchObject()->data;
    classify($raw_data_id, $draw);
}*/

if (isset($_POST['nr_of_lines'])) {
    $sql = "UPDATE `wm_raw_draw_data` ".
           "SET `nr_of_symbols` = :nr ".
           "WHERE `wm_raw_draw_data`.`id` = :raw_id ".
           "AND (`user_id` = :user_id OR :user_id = 10);";  # TODO: Change to admin-group check
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':nr', $_POST['nr_of_lines'], PDO::PARAM_INT);
    $stmt->bindParam(':raw_id', $_POST['raw_id_lines'], PDO::PARAM_INT);
    $uid = get_uid();
    $stmt->bindParam(':user_id', $uid, PDO::PARAM_INT);
    $stmt->execute();
} elseif (isset($_POST['wild_point_count'])) {
    $sql = "UPDATE `wm_raw_draw_data` ".
           "SET `wild_point_count` = :wild_point_count ".
           "WHERE `wm_raw_draw_data`.`id` = :raw_id ".
           "AND (`user_id` = :user_id OR :user_id = 10);";  # TODO: Change to admin-group check
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':wild_point_count', $_POST['wild_point_count'], PDO::PARAM_INT);
    $stmt->bindParam(':raw_id', $_POST['raw_data_id'], PDO::PARAM_INT);
    $uid = get_uid();
    $stmt->bindParam(':user_id', $uid, PDO::PARAM_INT);
    $stmt->execute();
} elseif (isset($_GET['delete'])) {
    $sql = "DELETE FROM `wm_raw_draw_data` ".
           "WHERE `wm_raw_draw_data`.`id` = :raw_id AND ".
           "(user_id = :user_id OR :user_id = 10)";  # TODO: Change to admin-group check
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':raw_id', $_GET['delete'], PDO::PARAM_INT);
    $uid = get_uid();
    $stmt->bindParam(':user_id', $uid, PDO::PARAM_INT);
    $stmt->execute();
    header("Location: ../gallery/");
} elseif (isset($_GET['fix'])) {
    $raw_data_id = intval($_GET['fix']);
    if (get_uid() == 10) {
        # Get raw data
        $sql = "SELECT `data` ".
               "FROM `wm_raw_draw_data` ".
               "WHERE `id` = :id";
        $stmt = $pdo->prepare($sql);
        $stmt->bindParam(':id', $raw_data_id, PDO::PARAM_INT);
        $stmt->execute();
        $image_data = $stmt->fetchObject();
        $raw_data = $image_data->data;

        # Does this dataset need to be fixed?
        if (!endsWith($raw_data, ']]')) {
            $i = -1;
            # Take everything from the back until the first '}' appears
            while (substr($raw_data, $i, 1) != '}' && $i > -strlen($raw_data)) {
                $i -= 1;
            }
            $fixed = substr($raw_data, 0, strlen($raw_data)+$i+1)."]]";
            # Put it in the database
            $sql = "UPDATE `wm_raw_draw_data` ".
                   "SET `data` = :data ".
                   "WHERE `wm_raw_draw_data`.`id` = :rid LIMIT 1; ";
            $stmt = $pdo->prepare($sql);
            $stmt->bindParam(':data', $fixed, PDO::PARAM_STR);
            $stmt->bindParam(':rid', $raw_data_id, PDO::PARAM_INT);
            $stmt->execute();

            # Remove old rendering
            unlink("../raw-data/$raw_data_id.svg");

            # Redirect
            header("Location: ../view/?raw_data_id=$raw_data_id");
        } else {
            $msg[] = array("class" => "alert-info",
                            "text" => "No need to fix anything.");
        }
    }
} elseif (isset($_GET['rerender'])) {
    $raw_data_id = intval($_GET['rerender']);
    if (get_uid() == 10) {
        unlink("../raw-data/$raw_data_id.svg");
    }
} elseif (isset($_GET['trash'])) {
    $sql = "UPDATE `wm_raw_draw_data` ".
           "SET `accepted_formula_id` = 1 ".
           "WHERE `id` = :raw_data_id AND ".
           "(`user_id` = :uid OR :uid = 10) LIMIT 1;";  # TODO: Change to admin-group check
    $stmt = $pdo->prepare($sql);
    $uid = get_uid();
    $stmt->bindParam(':uid', $uid, PDO::PARAM_INT);
    $stmt->bindParam(':raw_data_id', $_GET['trash'], PDO::PARAM_INT);
    $stmt->execute();
} elseif (isset($_GET['missing_line'])) {
    $sql = "UPDATE `wm_raw_draw_data` ".
           "SET `missing_line` = 1 ".
           "WHERE `id` = :raw_data_id AND ".
           "(`user_id` = :uid OR :uid = 10) LIMIT 1;";  # TODO: Change to admin-group check
    $stmt = $pdo->prepare($sql);
    $uid = get_uid();
    $stmt->bindParam(':uid', $uid, PDO::PARAM_INT);
    $stmt->bindParam(':raw_data_id', $_GET['missing_line'], PDO::PARAM_INT);
    $stmt->execute();
} elseif (isset($_GET['has_hook'])) {
    $sql = "UPDATE `wm_raw_draw_data` ".
           "SET `has_hook` = 1 ".
           "WHERE `id` = :raw_data_id AND ".
           "(`user_id` = :uid OR :uid = 10) LIMIT 1;";  # TODO: Change to admin-group check
    $stmt = $pdo->prepare($sql);
    $uid = get_uid();
    $stmt->bindParam(':uid', $uid, PDO::PARAM_INT);
    $stmt->bindParam(':raw_data_id', $_GET['raw_data_id'], PDO::PARAM_INT);
    $stmt->execute();
} elseif (isset($_GET['has_too_long_line'])) {
    $sql = "UPDATE `wm_raw_draw_data` ".
           "SET `has_too_long_line` = 1 ".
           "WHERE `id` = :raw_data_id AND ".
           "(`user_id` = :uid OR :uid = 10) LIMIT 1;";  # TODO: Change to admin-group check
    $stmt = $pdo->prepare($sql);
    $uid = get_uid();
    $stmt->bindParam(':uid', $uid, PDO::PARAM_INT);
    $stmt->bindParam(':raw_data_id', $_GET['raw_data_id'], PDO::PARAM_INT);
    $stmt->execute();
} elseif (isset($_GET['is_image'])) {
    $sql = "UPDATE `wm_raw_draw_data` ".
           "SET `is_image` = 1 ".
           "WHERE `id` = :raw_data_id AND ".
           "(`user_id` = :uid OR :uid = 10) LIMIT 1;";  # TODO: Change to admin-group check
    $stmt = $pdo->prepare($sql);
    $uid = get_uid();
    $stmt->bindParam(':uid', $uid, PDO::PARAM_INT);
    $stmt->bindParam(':raw_data_id', $_GET['is_image'], PDO::PARAM_INT);
    $stmt->execute();
} elseif (isset($_GET['delete_answer'])) {
    $sql = "DELETE FROM `wm_raw_data2formula` ".
           "WHERE `id` = :id AND (user_id = :user_id OR :user_id = 10)";  # TODO: Change to admin-group check
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':id', $_GET['delete_answer'], PDO::PARAM_INT);
    $uid = get_uid();
    $stmt->bindParam(':user_id', $uid, PDO::PARAM_INT);
    $stmt->execute();
    $msg[] = array("class" => "alert-info",
                    "text" => "Your answer was deleted.");
} elseif (isset($_GET['flag']) && $_SESSION['account_type'] != 'IP-User') {
    $sql = "INSERT INTO `wm_flags` (`user_id`, `raw_data_id`)".
           "VALUES (:uid,  :raw_data_id);";
    $stmt = $pdo->prepare($sql);
    $uid = get_uid();
    $stmt->bindParam(':uid', $uid, PDO::PARAM_INT);
    $stmt->bindParam(':raw_data_id', $_GET['flag'], PDO::PARAM_INT);
    try {
        $result = $stmt->execute();
    } catch (Exception $e) {
        var_dump($e);
    }

    if ($result) {
        mail ("themoosemind@gmail.com", "[Write-Math] flagged symbol",
              "Hallo Martin,\ngerade wurde das Symbol '".intval($_GET['flag']).
              "' geflaggt:\n\n".
              "http://write-math.com/view/?raw_data_id=".$_GET['flag']);
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
               "(`user_id` = :uid OR :uid = 10) LIMIT 1;";  # TODO: Change to admin-group check
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
    } elseif (isset($_GET['unaccept'])) {
        $sql = "UPDATE `wm_raw_draw_data` ".
               "SET `accepted_formula_id` = NULL, ".
               "is_in_testset = 0 ".
               "WHERE `wm_raw_draw_data`.`id` = :raw_data_id AND ".
               "(`user_id` = :uid OR :uid = 10) LIMIT 1;";  # TODO: Change to admin-group check
        $stmt = $pdo->prepare($sql);
        $uid = get_uid();
        $stmt->bindParam(':uid', $uid, PDO::PARAM_INT);
        $stmt->bindParam(':raw_data_id', $_GET['raw_data_id'], PDO::PARAM_INT);
        $stmt->execute();
        if ($stmt->rowCount() != 1) {
            $msg[] = array("class" => "alert-warning",
                           "text" => "You could not unaccept that answer. ".
                                     "This happens when you try to unaccept ".
                                     "a classification of a formula you ".
                                     "did not write. ");
        } else {
            # Redirect to prevent multiple submission
            header("Location: ../view/?raw_data_id=".$_GET['raw_data_id']);
        }
    } elseif (isset($_GET['vote'])) {
        // TODO: Check if user has right to vote

        $vote = intval($_GET['vote']);
        $id = intval($_GET['raw_data2formula_id']);
        if ($vote == 1 || $vote == -1) {
            $sql = "SELECT `user_id` FROM `wm_raw_data2formula` ".
                   "WHERE `id` = :id";
            $stmt = $pdo->prepare($sql);
            $stmt->bindParam(':id', $id, PDO::PARAM_INT);
            $stmt->execute();
            $row = $stmt->fetchObject();
            if ($row->user_id == get_uid()) {
                $msg[] = array("class" => "alert-warning",
                               "text" => "You can't upvote your own answer.");
            } else {
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
    }

    $raw_data_id = $_GET['raw_data_id'];
    $sql = "SELECT `user_id`, `display_name`, `data`, ".
           "`creation_date`, `accepted_formula_id`, `nr_of_symbols`, ".
           "`wild_point_count`, `missing_line`, `is_image`, `has_hook`, ".
           "`has_too_long_line`, `is_in_testset` ".
           "FROM `wm_raw_draw_data` ".
           "JOIN `wm_users` ON `wm_users`.`id` = `user_id`".
           "WHERE `wm_raw_draw_data`.`id` = :id";

    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':id', $_GET['raw_data_id'], PDO::PARAM_INT);
    $stmt->execute();
    $image_data = $stmt->fetchObject();

    // Get best rendering of this
    $sql = "SELECT `best_rendering` FROM `wm_formula` WHERE `id` = :fid;";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':fid', $image_data->accepted_formula_id, PDO::PARAM_INT);
    $stmt->execute();
    $image_data_best_rendering = $stmt->fetchObject();
    if ($image_data_best_rendering) {
        $image_data->accepted_formula_id_best_rendering = "-1";
    } else {
        $image_data->accepted_formula_id_best_rendering = $image_data_best_rendering->best_rendering;
    }

    // Add a new classification
    if (isset($_POST['latex'])) {
        $user_id = get_uid();
        $latex = trim($_POST['latex']);
        $raw_data_id = $_GET['raw_data_id'];
        $mode = 'bothmodes';
        //$packages = trim($_POST['packages']);
        add_classification($user_id, $raw_data_id, $latex, $mode);
    }

    // Get all probable classifications
    $sql = "SELECT `wm_raw_data2formula`.`id`, `display_name`, ".
           "`formula_in_latex`, `package`, `mode`, `formula_id`, ".
           "`formula_type`, `best_rendering`, `wm_users`.`id` as `user_id`, ".
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

# TODO: Should I remove the epsilon thing?
# Currently, it is still necessary for the next two lines.
$path = get_path($image_data->data, $epsilon);
$lines_nr = substr_count($path, 'M');
$control_points = substr_count($path, 'L') + $lines_nr;
if ($epsilon > 0) {
    $result_path = apply_linewise_douglas_peucker(pointLineList($image_data->data), $epsilon);
} else {
    $result_path = pointLineList($image_data->data);
}

$bounding_box = get_dimensions($result_path);
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
                                      'points_nr' => get_point_count(json_decode($image_data->data, true)),
                                      'control_points' => $control_points,
                                      'bounding_box' => $bounding_box,
                                      'automatic_answers' => $automatic_answers,
                                      'time_resolution' => $time_resolution
                                      )
                  );

?>