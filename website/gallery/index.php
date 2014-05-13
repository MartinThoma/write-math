<?php
include '../init.php';
include '../svg.php';

if (!is_logged_in()) {
    header("Location: ../login");
}

if (isset($_GET['tab']) && $_GET['tab'] == 'unclassified') {
    // Get total number of elements for pagination
    $sql = "SELECT COUNT(`id`) as counter FROM `wm_raw_draw_data` ".
           "WHERE `accepted_formula_id` IS NULL ";
    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    $row = $stmt->fetchObject();
    $total = $row->counter;

    // Get all raw data of this user
    $currentPage = isset($_GET['page']) ? intval($_GET['page']) : 1;
    $sql = "SELECT `id`, `data` as `image`, `creation_date` ".
           "FROM `wm_raw_draw_data` ".
           "WHERE `accepted_formula_id` IS NULL ".
           "ORDER BY `creation_date` DESC ".
           "LIMIT ".(($currentPage-1)*14).", 14";
    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    $userimages = $stmt->fetchAll();

    foreach ($userimages as $key => $value) {
        $userimages[$key]["path"] = get_path($value["image"]);
    }
    $tab = "unclassified";
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

    foreach ($userimages as $key => $value) {
        $userimages[$key]["path"] = get_path($value["image"]);
    }
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

    foreach ($userimages as $key => $value) {
        $userimages[$key]["path"] = get_path($value["image"]);
    }
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