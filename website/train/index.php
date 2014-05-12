<?php
include '../init.php';

if (!is_logged_in()) {
    header("Location: ../login");
}

$challenge_id = "";
$i = "";
$formula_id = "";
$formula_name = "";
$formula_description = "";
$random_mode = false;

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

$formula_ids = array();

if (isset($_POST['formula_id'])) {
    insert_userdrawing(get_uid(), $_POST['drawnJSON'], $_POST['formula_id']);
}

if (isset($_GET['rand'])) {
    $random_mode = true;
    $sql = "SELECT `id`, `formula_name`, `description`, `svg` ".
           "FROM  `wm_formula` ORDER BY RAND( ) LIMIT 0, 1";
    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    $formula = $stmt->fetchObject();
    $svg = $formula->svg;
    $formula_id = $formula->id;
    $formula_name = $formula->formula_name;
    $formula_description = $formula->description;
} elseif (isset($_GET['formula_id'])) {
    $formula_id = $_GET['formula_id'];
    $sql = "SELECT `formula_name`, `description`, `svg` ".
           "FROM  `wm_formula` WHERE  `id` = :id;";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':id', $_GET['formula_id'], PDO::PARAM_INT);
    $stmt->execute();
    $formula = $stmt->fetchObject();
    $svg = $formula->svg;
    $formula_name = $formula->formula_name;
    $formula_description = $formula->description;
} elseif (isset($_GET['challenge_id']) && isset($_GET['i'])) {
    $i = intval($_GET['i']);
    $challenge_id = intval($_GET['challenge_id']);

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
            header("Location: ..");
        }

        $formula_id = $formula_id->formula_id;

        if ($formula_id == 0) {
            // This challenge is finished!
            header("Location: ..");
        }

        // Has the user already written this symbol?
        $sql = "SELECT `raw_data_id` FROM `wm_raw_data2formula` ".
               "WHERE `formula_id` = :fid AND `user_id` = :uid LIMIT 0, 1";
        $stmt = $pdo->prepare($sql);
        $stmt->bindParam(':fid', $formula_id, PDO::PARAM_INT);
        $stmt->bindParam(':uid', get_uid(), PDO::PARAM_INT);
        $stmt->execute();
        $raw_data_id = $stmt->fetchObject()->raw_data_id;

        if ($raw_data_id > 0) {
            $i += 1;
        } else {
            break;
        }
    }

    $sql = "SELECT `svg` FROM  `wm_formula` WHERE  `id` = :id;";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':id', $formula_id, PDO::PARAM_INT);
    $stmt->execute();
    $svg = $stmt->fetchObject()->svg;

    $challenge_id = intval($_GET['challenge_id']);
} else {
    $uid = get_uid();
    $sql = "SELECT `wm_formula`.`id` ,  `formula_name`, ".
           "COUNT(`wm_raw_data2formula`.`id`) as `counter` ".
           "FROM `wm_formula` ".
           "LEFT JOIN `wm_raw_data2formula` ".
           "ON `formula_id` = `wm_formula`.`id` AND `user_id` = :uid ".
           "GROUP BY formula_name ".
           "ORDER BY `wm_formula`.`id` ASC";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':uid', $uid, PDO::PARAM_INT);
    $stmt->execute();
    $formula_ids = $stmt->fetchAll();

    $sql = "SELECT `wm_challenges`.`id` , `challenge_name`, ".
           "sum(case when `raw_data_id` is null then 1 else 0 end) as `missing` ".
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

echo $twig->render('train.twig', array('heading' => 'Train',
                                       'logged_in' => is_logged_in(),
                                       'display_name' => $_SESSION['display_name'],
                                       'file'=> "train",
                                       'formula_id' => $formula_id,
                                       'formula_ids' => $formula_ids,
                                       'challenges' => $challenges,
                                       'i' => ($i+1),
                                       'challenge_id' => $challenge_id,
                                       'formula_name' => $formula_name,
                                       'formula_description' => $formula_description,
                                       'random_mode' => $random_mode
                                       )
                  );

?>