<?php
include '../init.php';
include '../svg.php';

if (!is_logged_in()) {
    header("Location: ../login");
}

if (isset($_GET['tab']) && $_GET['tab'] == 'unclassified') {
    // Get total number of elements for pagination
    $sql = "SELECT COUNT(*) as `counter` FROM ".
           "(SELECT `wm_raw_draw_data`.`id`, `data` as `image`, ".
           "`creation_date`, ".
           "COUNT(`wm_raw_data2formula`.`raw_data_id`) as `answers`,  ".
           "COUNT(`wm_worker_answers`.`raw_data_id`) as `answers2` ".
           "FROM `wm_raw_draw_data` ".
           "LEFT OUTER JOIN `wm_raw_data2formula`  ".
                "ON (`raw_data_id` = `wm_raw_draw_data`.`id`) ".
           "LEFT OUTER JOIN `wm_worker_answers`  ".
                "ON (`wm_worker_answers`.`raw_data_id` = `wm_raw_draw_data`.`id`) ".
           "WHERE `accepted_formula_id` IS NULL AND `is_image`=0 ".
           "GROUP BY `wm_raw_draw_data`.`id` ".
           "HAVING `answers` > 0 OR `answers2` > 0 ".
           "ORDER BY `creation_date` DESC) AS T";
    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    $row = $stmt->fetchObject();
    $total = $row->counter;

    // Get all raw data of this user
    $currentPage = isset($_GET['page']) ? intval($_GET['page']) : 1;
    $sql = "SELECT `wm_raw_draw_data`.`id`, `data` as `image`, ".
           "`creation_date`, ".
           "COUNT(`wm_raw_data2formula`.`raw_data_id`) as `answers`,  ".
           "COUNT(`wm_worker_answers`.`raw_data_id`) as `answers2` ".
           "FROM `wm_raw_draw_data` ".
           "LEFT OUTER JOIN `wm_raw_data2formula` ".
                "ON (`raw_data_id` = `wm_raw_draw_data`.`id`) ".
           "LEFT OUTER JOIN `wm_worker_answers`  ".
                "ON (`wm_worker_answers`.`raw_data_id` = `wm_raw_draw_data`.`id`) ".
           "WHERE `accepted_formula_id` IS NULL AND `is_image`=0 ".
           "GROUP BY `wm_raw_draw_data`.`id` ".
           "HAVING `answers` > 0 OR `answers2` > 0 ".
           "ORDER BY `creation_date` DESC ".
           "LIMIT ".(($currentPage-1)*14).", 14";
    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    $userimages = $stmt->fetchAll();

    $tab = "unclassified";
} elseif (isset($_GET['tab']) && $_GET['tab'] == 'unanswered') {
    // Get total number of elements for pagination
    $sql = "SELECT COUNT(*) as `counter` FROM ".
           "(SELECT `wm_raw_draw_data`.`id`, `data` as `image`, ".
           "`creation_date`, ".
           "COUNT(`wm_raw_data2formula`.`raw_data_id`) as `answers`,  ".
           "COUNT(`wm_worker_answers`.`raw_data_id`) as `answers2` ".
           "FROM `wm_raw_draw_data` ".
           "LEFT OUTER JOIN `wm_raw_data2formula`  ".
                "ON (`wm_raw_data2formula`.`raw_data_id` = `wm_raw_draw_data`.`id`) ".
           "LEFT OUTER JOIN `wm_worker_answers`  ".
                "ON (`wm_worker_answers`.`raw_data_id` = `wm_raw_draw_data`.`id`) ".
           "WHERE `accepted_formula_id` IS NULL AND `is_image`=0 ".
           "GROUP BY `wm_raw_draw_data`.`id` ".
           "HAVING `answers` = 0 AND `answers2` = 0 ".
           "ORDER BY `creation_date` DESC) AS T";
    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    $row = $stmt->fetchObject();
    $total = $row->counter;

    // Get all raw data of this user
    $currentPage = isset($_GET['page']) ? intval($_GET['page']) : 1;
    $sql = "SELECT `wm_raw_draw_data`.`id`, `data` as `image`, ".
           "`creation_date`, ".
           "COUNT(`wm_raw_data2formula`.`raw_data_id`) as `answers`,  ".
           "COUNT(`wm_worker_answers`.`raw_data_id`) as `answers2` ".
           "FROM `wm_raw_draw_data` ".
           "LEFT OUTER JOIN `wm_raw_data2formula`  ".
                "ON (`wm_raw_data2formula`.`raw_data_id` = `wm_raw_draw_data`.`id`) ".
           "LEFT OUTER JOIN `wm_worker_answers`  ".
                "ON (`wm_worker_answers`.`raw_data_id` = `wm_raw_draw_data`.`id`) ".
           "WHERE `accepted_formula_id` IS NULL AND `is_image`=0 ".
           "GROUP BY `wm_raw_draw_data`.`id` ".
           "HAVING `answers` = 0 AND `answers2` = 0 ".
           "ORDER BY `creation_date` DESC ".
           "LIMIT ".(($currentPage-1)*14).", 14";
    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    $userimages = $stmt->fetchAll();

    $tab = "unanswered";
} elseif (isset($_GET['tab']) && $_GET['tab'] == 'all') {
    // Get total number of elements for pagination
    $sql = "SELECT COUNT(`id`) as counter FROM `wm_raw_draw_data` ";
    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    $row = $stmt->fetchObject();
    $total = $row->counter;

    // Get all raw data of this user
    $currentPage = isset($_GET['page']) ? intval($_GET['page']) : 1;
    $sql = "SELECT `id`, `data` as `image`, `creation_date` ".
           "FROM `wm_raw_draw_data` ".
           "ORDER BY `creation_date` DESC ".
           "LIMIT ".(($currentPage-1)*14).", 14";
    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    $userimages = $stmt->fetchAll();

    $tab = "all";
} else {
    // Get total number of elements for pagination
    $sql = "SELECT COUNT(`id`) as counter FROM `wm_raw_draw_data` ".
           "WHERE `user_id` = :uid";
    $stmt = $pdo->prepare($sql);
    $uid = get_uid();
    $stmt->bindParam(':uid', $uid, PDO::PARAM_STR);
    $stmt->execute();
    $row = $stmt->fetchObject();
    $total = $row->counter;

    // Get all raw data of this user
    $currentPage = isset($_GET['page']) ? intval($_GET['page']) : 1;
    $sql = "SELECT `id`, `data` as `image`, `creation_date` ".
           "FROM `wm_raw_draw_data` ".
           "WHERE `user_id` = :uid ".
           "ORDER BY `creation_date` DESC ".
           "LIMIT ".(($currentPage-1)*14).", 14";
    $stmt = $pdo->prepare($sql);
    $uid = get_uid();
    $stmt->bindParam(':uid', $uid, PDO::PARAM_STR);
    $stmt->execute();
    $userimages = $stmt->fetchAll();
    
    $tab = "my_raw_data";
}

echo $twig->render('gallery.twig', array('heading' => 'Gallery',
                                         'logged_in' => is_logged_in(),
                                         'display_name' => $_SESSION['display_name'],
                                         'file'=> "gallery",
                                         'userimages' => $userimages,
                                         'total' => $total,
                                         'pages' => floor(($total)/14),
                                         'currentPage' => $currentPage,
                                         'tab' => $tab
                                        )
                  );

?>