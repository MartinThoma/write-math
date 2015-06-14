<?php
include '../init.php';
include '../svg.php';

if (!is_logged_in()) {
    header("Location: ../login");
}


// Code does the same for each tab
if (isset($_GET['tab']) && $_GET['tab'] == 'unclassified') {
    $tab = "unclassified";
    $select = "SELECT `wm_raw_draw_data`.`id`, `data` as `image`, ".
              "`creation_date`, ".
              "`user_answers_count` as `answers`,  ".
              "`automated_answers_count` as `answers2` ".
              "FROM `wm_raw_draw_data` ".
              "WHERE `accepted_formula_id` IS NULL AND `is_image`=0 AND ".
              "`classifiable`=1 AND `stroke_segmentable`=1 ".
              "AND `nr_of_symbols` = 1 AND ".
              "(`user_answers_count` > 0 OR `automated_answers_count` > 0)";
              # "ORDER BY `probability` DESC "

    // Get total number of elements for pagination
    $sql = "SELECT COUNT(*) as `counter` FROM ($select) AS T";
    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    $row = $stmt->fetchObject();
    $total = $row->counter;

    // Get all raw data of this user
    $currentPage = isset($_GET['page']) ? intval($_GET['page']) : 1;
    $sql = $select." LIMIT ".(($currentPage-1)*14).", 14";
    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    $userimages = $stmt->fetchAll();
} elseif (isset($_GET['tab']) && $_GET['tab'] == 'unclassified_multiple') {
    $tab = "unclassified_multiple";
    $select = "SELECT `wm_raw_draw_data`.`id`, `data` as `image`, ".
              "`creation_date`, ".
              "`user_answers_count` as `answers`,  ".
              "`automated_answers_count` as `answers2` ".
              "FROM `wm_raw_draw_data` ".
              "WHERE `accepted_formula_id` IS NULL AND `is_image`=0 ".
              "AND `classifiable`=1 AND `stroke_segmentable`=1 ".
              "AND `nr_of_symbols` > 1 ".
              "AND (`user_answers_count` > 0 OR `automated_answers_count` > 0) ".
              "ORDER BY `creation_date` DESC ";

    // Get total number of elements for pagination
    $sql = "SELECT COUNT(*) as `counter` FROM ($select) AS T";
    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    $row = $stmt->fetchObject();
    $total = $row->counter;

    // Get all raw data of this user
    $currentPage = isset($_GET['page']) ? intval($_GET['page']) : 1;
    $sql = $select."LIMIT ".(($currentPage-1)*14).", 14";
    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    $userimages = $stmt->fetchAll();
} elseif (isset($_GET['tab']) && $_GET['tab'] == 'unanswered') {
    $tab = "unanswered";
    $select = "SELECT `wm_raw_draw_data`.`id`, `data` as `image`, ".
              "`creation_date`, ".
              "`user_answers_count` as `answers`,  ".
              "`automated_answers_count` as `answers2` ".
              "FROM `wm_raw_draw_data` ".
              "WHERE `accepted_formula_id` IS NULL AND `is_image`=0 AND ".
              "`classifiable`=1 AND `stroke_segmentable`=1 ".
              "AND (`user_answers_count` = 0 AND `automated_answers_count` = 0) ".
              "ORDER BY `creation_date` DESC ";

    // Get total number of elements for pagination
    $sql = "SELECT COUNT(*) as `counter` FROM ($select) AS T";
    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    $row = $stmt->fetchObject();
    $total = $row->counter;

    // Get all raw data of this user
    $currentPage = isset($_GET['page']) ? intval($_GET['page']) : 1;
    $sql = $select." LIMIT ".(($currentPage-1)*14).", 14";
    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    $userimages = $stmt->fetchAll();
} elseif (isset($_GET['tab']) && $_GET['tab'] == 'all') {
    $tab = "all";
    $select = "SELECT `id`, `data` as `image`, `creation_date` ".
              "FROM `wm_raw_draw_data` ".
              "ORDER BY `creation_date` DESC ";

    // Get total number of elements for pagination
    $sql = "SELECT COUNT(*) as `counter` FROM ($select) AS T";
    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    $row = $stmt->fetchObject();
    $total = $row->counter;

    // Get all raw data of this user
    $currentPage = isset($_GET['page']) ? intval($_GET['page']) : 1;
    $sql = $select." LIMIT ".(($currentPage-1)*14).", 14";
    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    $userimages = $stmt->fetchAll();
} else {
    $tab = "my_raw_data";
    $select = "SELECT `id`, `data` as `image`, `creation_date` ".
              "FROM `wm_raw_draw_data` ".
              "WHERE `user_id` = :uid ".
              "ORDER BY `creation_date` DESC ";

    // Get total number of elements for pagination
    $sql = "SELECT COUNT(*) as `counter` FROM ($select) AS T";
    $stmt = $pdo->prepare($sql);
    $uid = get_uid();
    $stmt->bindParam(':uid', $uid, PDO::PARAM_STR);
    $stmt->execute();
    $row = $stmt->fetchObject();
    $total = $row->counter;

    // Get all raw data of this user
    $currentPage = isset($_GET['page']) ? intval($_GET['page']) : 1;
    $sql = $select." LIMIT ".(($currentPage-1)*14).", 14";
    $stmt = $pdo->prepare($sql);
    $uid = get_uid();
    $stmt->bindParam(':uid', $uid, PDO::PARAM_STR);
    $stmt->execute();
    $userimages = $stmt->fetchAll();
}

echo $twig->render('gallery.twig', array('heading' => 'Gallery',
                                         'logged_in' => is_logged_in(),
                                         'display_name' => $_SESSION['display_name'],
                                         'file'=> "gallery",
                                         'userimages' => $userimages,
                                         'total' => $total,
                                         'pages' => ceil(($total)/14),
                                         'currentPage' => $currentPage,
                                         'tab' => $tab
                                        )
                  );

?>