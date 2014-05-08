<?php
include '../init.php';
include '../svg.php';

if (!is_logged_in()) {
    header("Location: ../login");
}

// Get total number of elements for pagination
$sql = "SELECT COUNT(`id`) as counter FROM `wm_raw_draw_data` ".
       "WHERE `user_id` = :uid";
$stmt = $pdo->prepare($sql);
$stmt->bindParam(':uid', get_uid(), PDO::PARAM_STR);
$stmt->execute();
$row = $stmt->fetchObject();
$total = $row->counter;

// Get all raw data of this user
$page = isset($_GET['page']) ? intval($_GET['page']) : 1;
$sql = "SELECT `id`, `data` as `image`, `creation_date` ".
       "FROM `wm_raw_draw_data` ".
       "WHERE `user_id` = :uid ".
       "ORDER BY `creation_date` DESC ".
       "LIMIT ".(($page-1)*14).", 14";
$stmt = $pdo->prepare($sql);
$stmt->bindParam(':uid', get_uid(), PDO::PARAM_STR);
$stmt->execute();
$userimages = $stmt->fetchAll();

foreach ($userimages as $key => $value) {
    $userimages[$key]["path"] = get_path($value["image"]);
}

echo $twig->render('gallery.twig', array('heading' => 'Gallery',
                                         'logged_in' => is_logged_in(),
                                         'display_name' => $_SESSION['display_name'],
                                         'file'=> "gallery",
                                         'userimages' => $userimages,
                                         'total' => $total,
                                         'pages' => floor(($total)/14),
                                         'page' => $page
                                        )
                  );

?>