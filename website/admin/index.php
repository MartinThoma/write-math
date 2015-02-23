<?php
require_once '../svg.php';
include '../init.php';
require_once '../classification.php';

if (!is_logged_in() || !is_admin()) {
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
        $files = glob('../formulas/*');
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

if (isset($_GET['delete_inactive_user'])) {
    $sql = "DELETE FROM `wm_users` WHERE `wm_users`.`id` = :uid ".
           "AND `account_type` = 'IP-User' LIMIT 1";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':uid', $_GET['delete_inactive_user'], PDO::PARAM_STR);
    $stmt->execute();
} elseif (isset($_GET['delete_all_inactive_users'])) {
    // See http://stackoverflow.com/a/4562797/562769
    $sql = "DELETE FROM `wm_users` WHERE `id` IN ( ".
           "SELECT * FROM ( ".
           "SELECT  `wm_users`.`id` FROM `wm_users`  ".
           "LEFT JOIN `wm_raw_draw_data` ".
           "ON `wm_raw_draw_data`.`user_id` = `wm_users`.`id` ".
           "WHERE `account_type` = 'IP-User' ".
           "AND `wm_raw_draw_data`.`user_id` IS NULL ) AS p)";
    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    $msg[] = array("class" => "alert-success",
                   "text" => "Your have deleted all inactive users ($i).");
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

$accountA = '';
$accountB = '';
if (isset($_GET['accountA']) && isset($_GET['accountB'])
    && !isset($_GET['confirm'])) {
    $sql = "SELECT `id`, `display_name`, `account_type` FROM `wm_users` ".
           "WHERE `id` = :ida";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':ida', $_GET['accountA'], PDO::PARAM_INT);
    $stmt->execute();
    $accountA =$stmt->fetchObject();
    $sql = "SELECT `id`, `display_name`, `account_type` FROM `wm_users` ".
           "WHERE `id` = :idb";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':idb', $_GET['accountB'], PDO::PARAM_INT);
    $stmt->execute();
    $accountB =$stmt->fetchObject();
} elseif (isset($_GET['accountA']) && isset($_GET['accountB'])
    && isset($_GET['confirm'])) {
    $a_id = $_GET['accountA'];
    $b_id = $_GET['accountB'];
    $msg[] = array("class" => "alert-success",
                   "text" => "Your have merged user id $a_id ".
                             "to user id $b_id.");
    merge_accounts($a_id, $b_id);
}


$sql = "SELECT `wm_flags`.`id`, `user_id`, `raw_data_id`, `display_name` ".
       "FROM `wm_flags` ".
       "JOIN `wm_users` ON `wm_users`.`id` = `user_id` ".
       "ORDER BY `display_name` ASC";
$stmt = $pdo->prepare($sql);
$stmt->execute();
$flags = $stmt->fetchAll();

// Get inactive users
$sql = "SELECT  `wm_users`.`id`, `email`, `display_name` FROM `wm_users` ".
       "LEFT JOIN `wm_raw_draw_data` ".
       "ON `wm_raw_draw_data`.`user_id` = `wm_users`.`id` ".
       "WHERE `account_type` = 'IP-User' ".
       "AND `wm_raw_draw_data`.`user_id` IS NULL ".
       "LIMIT ".intval(isset($_GET['page_users'])?isset($_GET['page_users']):0).", 50";
$stmt = $pdo->prepare($sql);
$stmt->execute();
$inactive_users = $stmt->fetchAll();

// Get symbols without unicode
$sql = "SELECT id, `formula_name`, `formula_type`, `unicode_dec` FROM `wm_formula` ".
       "WHERE unicode_dec = 0 ".
       "AND `is_important` = 1 ORDER BY id ASC";
$stmt = $pdo->prepare($sql);
$stmt->execute();
$without_unicode = $stmt->fetchAll();

echo $twig->render('admin.twig', array('heading' => 'Admin Tools',
                                       'file' => "admin",
                                       'logged_in' => is_logged_in(),
                                       'display_name' => $_SESSION['display_name'],
                                       'msg' => $msg,
                                       'many_lines' => $many_lines,
                                       'flags' => $flags,
                                       'accountA' => $accountA,
                                       'accountB' => $accountB,
                                       'inactive_users' => $inactive_users,
                                       'without_unicode' => $without_unicode
                                       )
                  );

?>