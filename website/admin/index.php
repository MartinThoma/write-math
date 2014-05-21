<?php
require_once '../svg.php';
include '../init.php';
require_once '../classification.php';

if (!is_logged_in() || get_uid() != 10) {
    header("Location: ../login");
}

$sql = "SELECT `id`, `data`, `creation_date` ".
       "FROM `wm_raw_draw_data`";
$stmt = $pdo->prepare($sql);
$stmt->execute();
$images = $stmt->fetchAll();

$many_lines = array();
foreach ($images as $image) {
    $data = pointLineList($image['data']);
    if (count($data) > 3) {
        $many_lines[] = array("lines" => count($data), "id" => $image['id']);
    }
}

$sql = "SELECT `wm_flags`.`id`, `user_id`, `raw_data_id`, `display_name` ".
       "FROM `wm_flags` ".
       "JOIN `wm_users` ON `wm_users`.`id` = `user_id`";
$stmt = $pdo->prepare($sql);
$stmt->execute();
$flags = $stmt->fetchAll();

echo $twig->render('admin.twig', array('heading' => 'Admin Tools',
                                       'file' => "admin",
                                       'logged_in' => is_logged_in(),
                                       'display_name' => $_SESSION['display_name'],
                                       'user_id' => $user->id,
                                       'many_lines' => $many_lines,
                                       'flags' => $flags
                                       )
                  );

?>