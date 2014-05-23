<?php
require_once '../svg.php';
include '../init.php';
require_once '../classification.php';

if (!is_logged_in() || get_uid() != 10) {
    header("Location: ../login");
}

$many_lines = '';

function endsWith($haystack, $needle) {
    $length = strlen($needle);
    if ($length == 0) {
        return true;
    }

    return (substr($haystack, -$length) === $needle);
}

if (isset($_GET['cache-flush'])) {
    if ($_GET['cache-flush'] == 'raw') {
        $files = glob('../raw-data/*');
        foreach($files as $file){
            if(is_file($file) && endsWith($file, ".svg")) {
                unlink($file);
            }
        }
    } elseif ($_GET['cache-flush'] == 'templates') {
        $files = glob('../cache/*'); // get all file names
        foreach($files as $file){ // iterate files and folders
            system('/bin/rm -rf ' . escapeshellarg($file));
        }
    }
}

if (isset($_GET['delete'])) {
    $sql = "DELETE FROM `wm_flags` WHERE `wm_flags`.`id` = :id LIMIT 1";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':id', $_GET['delete'], PDO::PARAM_STR);
    $stmt->execute();
}

if (isset($_GET['many_lines'])) {
    $sql = "SELECT `id`, `data`, `creation_date` ".
           "FROM `wm_raw_draw_data`"; # WHERE `formula_type` = 'single symbol'
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

    function sortByLineNumber($a, $b) {
        return -($a['lines'] - $b['lines']);
    }

    usort($many_lines, 'sortByLineNumber');
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