<?php
include '../init.php';
include '../svg.php';

if (!is_logged_in()) {
    header("Location: ../login");
}

// Get all raw data of this user
$sql = "SELECT `id`, `data` as `image`, `creation_date` FROM `wm_raw_draw_data` ".
       "WHERE `user_id` = :uid";
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
                                         'userimages' => $userimages
                                        )
                  );

?>