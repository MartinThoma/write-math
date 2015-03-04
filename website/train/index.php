<?php
include '../init.php';
require_once 'functions.php';

if (!is_logged_in()) {
    header("Location: ../login");
}

$heading_html = 'Train';
$challenge_id = "";
$i = "";
$formula_id = "";
$random_mode = false;
$formula_ids = array();
$formula = null;
$challenges = null;

if (isset($_POST['formula_id'])) {
    insert_recording(get_uid(), $_POST['drawnJSON'], $_POST['formula_id']);
}

if (isset($_GET['missing_formula_id']) || isset($_GET['wrong_rendering_id'])) {
    if($_GET['wrong_rendering_id']) {
        $ptype = 'rendering wrong';
        $fid = $_GET['wrong_rendering_id'];
    } else {
        $ptype = 'svg missing';
        $fid = $_GET['missing_formula_id'];
    }

    $sql = "INSERT INTO `wm_formula_svg_missing` (".
           "`user_id`, ".
           "`formula_id`, ".
           "`time`, ".
           "`useragent`, ".
           "`problem_type` ".
           ")".
           "VALUES (:uid, :fid, CURRENT_TIMESTAMP, :user_agent, :ptype);";
    $stmt = $pdo->prepare($sql);
    $user_id = get_uid();
    $stmt->bindParam(':uid', $user_id, PDO::PARAM_INT);
    $stmt->bindParam(':fid', $fid, PDO::PARAM_INT);
    $stmt->bindParam(':user_agent', $_SERVER['HTTP_USER_AGENT'], PDO::PARAM_STR);
    $stmt->bindParam(':ptype', $ptype, PDO::PARAM_STR);
    try {
        $stmt->execute();
        $msg[] = array("class" => "alert-success",
                   "text" => "Your notice has been recorded and a moderator ".
                             "will fix the issue as soon as possible. I'm ".
                             "sorry for the inconvenience.");
    } catch (Exception $e) {
        if ($ptype == 'svg missing') {
          $msg[] = array("class" => "alert-warning",
              "text" => "You've already mentioned that this symbol is missing.");
        } else {
          $msg[] = array("class" => "alert-warning",
              "text" => "You've already mentioned this looks wrong.");
        }
    }
} elseif (isset($_GET['unknown_formula_id'])) {
    $sql = "INSERT INTO `wm_user_unknown_formula` (".
           "`user_id` , `formula_id` , `time`) ".
           "VALUES (:uid, :fid, CURRENT_TIMESTAMP)";
    $stmt = $pdo->prepare($sql);
    $user_id = get_uid();
    $stmt->bindParam(':uid', $user_id, PDO::PARAM_INT);
    $stmt->bindParam(':fid', $_GET['unknown_formula_id'], PDO::PARAM_INT);
    try {
        $stmt->execute();
        $msg[] = array("class" => "alert-success",
                   "text" => "Thank you for mentioning that you don't know ".
                             "this symbol. It's better to mention it than ".
                             "trying to draw it, because this way I get more ".
                             "of the 'important' symbols and less crap that ".
                             "nobody needs.");
    } catch (Exception $e) {
        $msg[] = array("class" => "alert-warning",
            "text" => "You've already mentioned that you don't know this symbol.");
    }
}

if (isset($_GET['rand'])) {
    $random_mode = true;
    $sql = "SELECT `id`, `formula_name`, `description`, `mode`, `best_rendering` ".
           "FROM  `wm_formula` ".
           "WHERE `id` NOT IN ( ".
               "SELECT `formula_id` ".
               "FROM  `wm_raw_data2formula` ".
               "WHERE `user_id` = :uid".
           ") AND `id` NOT IN ( ".
                "SELECT `wm_formula`.`id` ".
                "FROM  `wm_raw_draw_data` ".
                "JOIN  `wm_formula` ON  `wm_formula`.`id` =  `accepted_formula_id` ".
                "GROUP BY `accepted_formula_id` ".
                "HAVING COUNT(`wm_formula`.`id`) < 20 OR COUNT(`wm_formula`.`id` ) > 100 ".
           ") AND `id` NOT IN ( ".
               "SELECT `formula_id` ".
               "FROM  `wm_user_unknown_formula` ".
               "WHERE `user_id` = :uid".
            ") AND `formula_type` = 'single symbol' ".
           "ORDER BY RAND( ) LIMIT 0, 1";
    $stmt = $pdo->prepare($sql);
    $user_id = get_uid();
    $stmt->bindParam(':uid', $user_id, PDO::PARAM_INT);
    $stmt->execute();
    $formula = $stmt->fetchObject();
    if (!$formula) {
        $sql = "SELECT `id`, `formula_name`, `description`, `mode`, `best_rendering` ".
               "FROM  `wm_formula` ".
               "WHERE `id` NOT IN ( ".
                "SELECT `wm_formula`.`id` ".
                "FROM  `wm_raw_draw_data` ".
                "JOIN  `wm_formula` ON  `wm_formula`.`id` =  `accepted_formula_id` ".
                "GROUP BY `accepted_formula_id` ".
                "HAVING COUNT(`wm_formula`.`id`) < 20 OR COUNT(`wm_formula`.`id` ) > 100 ".
               ") AND `id` NOT IN ( ".
                   "SELECT `formula_id` ".
                   "FROM  `wm_user_unknown_formula` ".
                   "WHERE `user_id` = :uid".
               ") AND `formula_type` = 'single symbol' ".
               "ORDER BY RAND( ) LIMIT 0, 1";
        $stmt = $pdo->prepare($sql);
        $user_id = get_uid();
        $stmt->bindParam(':uid', $user_id, PDO::PARAM_INT);
        $stmt->execute();
        $formula = $stmt->fetchObject();
    }
} elseif (isset($_GET['formula_id'])) {
    $formula_id = $_GET['formula_id'];
    $sql = "SELECT `wm_formula`.`id`, `formula_name`, `description`, ".
           "`mode`, `best_rendering`,".
           "COUNT(`wm_raw_data2formula`.`id`) as `counter` ".
           "FROM `wm_formula` ".
           "LEFT JOIN `wm_raw_data2formula` ".
           "ON `formula_id` = `wm_formula`.`id` AND `wm_formula`.`user_id` = :uid ".
           "WHERE `wm_formula`.`id` = :id;";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':id', $_GET['formula_id'], PDO::PARAM_INT);
    $user_id = get_uid();
    $stmt->bindParam(':uid', $user_id, PDO::PARAM_INT);
    $stmt->execute();
    $formula = $stmt->fetchObject();
} elseif (isset($_GET['challenge_id']) && isset($_GET['i'])) {
    $i = intval($_GET['i']);
    $challenge_id = intval($_GET['challenge_id']);

    # TODO: Fix this shit
    while (true) {
        $sql = "SELECT `formula_id` FROM `wm_formula2challenge` ".
               "WHERE `challenge_id` = :challenge_id ".
               "ORDER BY `formula_id` LIMIT $i, 1";
        $stmt = $pdo->prepare($sql);
        $stmt->bindParam(':challenge_id', $challenge_id, PDO::PARAM_INT);
        $stmt->execute();
        $formula_id = $stmt->fetchObject();

        if (empty($formula_id)) {
            // This challenge is finished!
            header("Location: ../train/");
        }

        $formula_id = $formula_id->formula_id;

        if ($formula_id == 0) {
            // This challenge is finished!
            header("Location: ../train/");
        }

        // Has the user already written this symbol?
        $sql = "SELECT `raw_data_id` FROM `wm_raw_data2formula` ".
               "WHERE `formula_id` = :fid AND `user_id` = :uid LIMIT 0, 1";
        $stmt = $pdo->prepare($sql);
        $stmt->bindParam(':fid', $formula_id, PDO::PARAM_INT);
        $user_id = get_uid();
        $stmt->bindParam(':uid', $user_id, PDO::PARAM_INT);
        $stmt->execute();
        $raw_data_id = $stmt->fetchObject()->raw_data_id;

        if ($raw_data_id > 0) {
            $i += 1;
        } else {
            break;
        }
    }

    $sql = "SELECT `id`, `best_rendering`, `formula_name`, `description`, ".
           "`mode` FROM  `wm_formula` WHERE  `id` = :id;";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':id', $formula_id, PDO::PARAM_INT);
    $stmt->execute();
    $formula = $stmt->fetchObject();

    $challenge_id = intval($_GET['challenge_id']);
} else {
    $uid = get_uid();
    $sql = "SELECT `wm_formula`.`id` ,  `formula_name`, ".
           "COUNT(`wm_raw_data2formula`.`id`) as `counter` ".
           "FROM `wm_formula` ".
           "LEFT JOIN `wm_raw_data2formula` ".
           "ON `formula_id` = `wm_formula`.`id` AND `wm_formula`.`user_id` = :uid ".
           "WHERE `formula_type` = 'single symbol' ".
           "GROUP BY formula_name ".
           "ORDER BY `wm_formula`.`id` ASC";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':uid', $uid, PDO::PARAM_INT);
    $stmt->execute();
    $formula_ids = $stmt->fetchAll();

    $sql = "SELECT `wm_challenges`.`id` , `challenge_name`, ".
           "sum(case when `raw_data_id` is null then 1 else 0 end) as `missing`, ".
           "sum(case when `raw_data_id` is null then 1 else 1 end) as `total` ".
           "FROM `wm_challenges` ".
           "JOIN `wm_formula2challenge` ".
           "ON `challenge_id` = `wm_challenges`.`id` ".
           "LEFT JOIN `wm_raw_data2formula` ".
           "ON `wm_raw_data2formula`.`formula_id` = `wm_formula2challenge`.`formula_id` ".
           "AND `user_id` = :uid ".
           "GROUP BY `challenge_name` ".
           "ORDER BY `challenge_name` ASC";

    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':uid', $uid, PDO::PARAM_INT);
    $stmt->execute();
    $challenges = $stmt->fetchAll();
}

echo $twig->render('train.twig', array('heading' => $heading_html,
                                       'logged_in' => is_logged_in(),
                                       'display_name' => $_SESSION['display_name'],
                                       'file'=> "train",
                                       'msg' => $msg,
                                       'formula_id' => $formula_id,
                                       'formula_ids' => $formula_ids,
                                       'challenges' => $challenges,
                                       'i' => ($i+1),
                                       'challenge_id' => $challenge_id,
                                       'formula' => $formula,
                                       'random_mode' => $random_mode,
                                       'useragentstring' => $_SERVER['HTTP_USER_AGENT']
                                       )
                  );

?>