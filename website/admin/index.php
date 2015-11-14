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

function merge_formulas($fid_a, $fid_b) {
    global $pdo;
    global $msg;
    // a gets deleted, b remains
    $sql = "SELECT `id`, `formula_type`, `is_important` ".
           "FROM `wm_formula` ".
           "WHERE `id`=:ida OR `id`=:idb AND ".
           "`is_important`=0 AND ".
           "(NOT (`formula_type`='single symbol') OR `formula_type` IS NULL)";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':ida', $fid_a, PDO::PARAM_INT);
    $stmt->bindParam(':idb', $fid_b, PDO::PARAM_INT);
    $stmt->execute();
    $formulas = $stmt->fetchAll();

    $i = 0;
    foreach ($formulas as $formula) {
        $i += 1;
    }

    if ($i != 2) {
        $msg[] = array("class" => "alert-warning",
                       "text" => "Could not be merged. One was not a formula.");
        return -1;
    }

    // Adjust accepted ids
    $sql = "UPDATE `wm_raw_draw_data` SET `accepted_formula_id` = :idb ".
           "WHERE  `accepted_formula_id` = :ida LIMIT 20;";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':ida', $fid_a, PDO::PARAM_INT);
    $stmt->bindParam(':idb', $fid_b, PDO::PARAM_INT);
    $stmt->execute();

    // Adjust peoples answers
    $sql = "UPDATE `wm_partial_answer` SET `symbol_id` = :ida ".
           "WHERE  `symbol_id` = :idb LIMIT 20;";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':ida', $fid_a, PDO::PARAM_INT);
    $stmt->bindParam(':idb', $fid_b, PDO::PARAM_INT);
    $stmt->execute();
    // The normalized answer could already exist. TODO: Deal with it.
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
} elseif (isset($_GET['delete_phraselist'])) {
    unlink('../cache-data/phraselist.js');
    header("Location: ../admin");
} elseif (isset($_GET['remove_worker_answers'])) {
    $sql = "DELETE FROM `wm_partial_answer` WHERE `is_worker_answer` = 1 ".
           "AND `is_accepted`=0 ";
    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    $sql = "UPDATE `wm_raw_draw_data` ".
           "SET  `automated_answers_count` =  '0';";
    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    header("Location: ../admin");
}

if (isset($_GET['delete_formula'])) {
    $sql = "DELETE FROM `wm_formula` WHERE `id` = :fid AND :fid > 1000 LIMIT 1";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':fid', $_GET['delete_formula'], PDO::PARAM_STR);
    $stmt->execute();
    header("Location: ../admin");
}

if (isset($_GET['delete'])) {
    $sql = "DELETE FROM `wm_flags` WHERE `wm_flags`.`id` = :id LIMIT 1";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':id', $_GET['delete'], PDO::PARAM_STR);
    $stmt->execute();
    header("Location: ../admin");
}

if (isset($_GET['delete_inactive_user'])) {
    $sql = "DELETE FROM `wm_users` WHERE `wm_users`.`id` = :uid ".
           "AND `account_type` = 'IP-User' LIMIT 1";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':uid', $_GET['delete_inactive_user'], PDO::PARAM_STR);
    $stmt->execute();
    header("Location: ../admin");
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
                   "text" => "Your have deleted all inactive users.");
}

if (isset($_GET['many_lines'])) {
    $sql = "SELECT `id`, `data`, `creation_date` ".
           "FROM `wm_raw_draw_data` ".
           "WHERE `is_image`=0 AND `nr_of_symbols`=1 AND `accepted_formula_id`!=1 ".
           "LIMIT ".rand (1, 300000).", 500";
    echo $sql;
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

// Merge formulas
$formulaA = '';
$formulaB = '';
if (isset($_GET['formulaA']) && isset($_GET['formulaB'])) {
    $a_id = $_GET['formulaA'];
    $b_id = $_GET['formulaB'];
    $ret_code = merge_formulas($a_id, $b_id);
    if ($ret_code != -1) {
        $msg[] = array("class" => "alert-success",
                       "text" => "Your have merged formula id $a_id ".
                                 "to formula id $b_id.");
        ;
    }
}


// Merge user accounts
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

// Get symbols/formulas which don't have any example
$sql = "SELECT * FROM `wm_formula` ".
       "WHERE `id` NOT IN (".
       "SELECT DISTINCT `wm_raw_draw_data`.`accepted_formula_id` ".
       "FROM `wm_raw_draw_data` ".
       "WHERE `wm_raw_draw_data`.`accepted_formula_id` IS NOT NULL) ".
       "AND `id` NOT IN (".
       "SELECT DISTINCT `symbol_id` ".
       "FROM `wm_partial_answer` WHERE `is_accepted` = 1)".
       "ORDER BY `user_id` ASC";
$stmt = $pdo->prepare($sql);
$stmt->execute();
$without_example = $stmt->fetchAll();

$formula_answers = array();
foreach ($without_example as $key => $formula) {
    $sql = "SELECT `recording_id`  FROM `wm_partial_answer` ".
           "WHERE `symbol_id` = :fid";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':fid', $formula['id'], PDO::PARAM_INT);
    $stmt->execute();
    $answers = $stmt->fetchAll();
    $formula_answers[$formula['id']] = $answers;
}

// New tag
if (isset($_POST['tag_name_new'])) {
    $sql = "INSERT INTO `wm_tags` (`tag_name` ,`description`) ".
           "VALUES (:tag_name, :tag_description);";
    $stmt = $pdo->prepare($sql);
    $tag_name = $_POST['tag_name_new'];
    $tag_name = strtolower($tag_name);
    $tag_name = str_replace(" ", "-", $tag_name);
    $stmt->bindParam(':tag_name', $tag_name, PDO::PARAM_STR);
    $stmt->bindParam(':tag_description', $_POST['description'], PDO::PARAM_STR);
    $stmt->execute();
}

// Get all tags
$sql = "SELECT `id`, `tag_name`, `description` FROM `wm_tags` ".
       "ORDER BY `tag_name` ASC";
$stmt = $pdo->prepare($sql);
$stmt->execute();
$tags = $stmt->fetchAll();


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
                                       'without_unicode' => $without_unicode,
                                       'without_example' => $without_example,
                                       'formula_answers' => $formula_answers,
                                       'tags' => $tags
                                       )
                  );

?>