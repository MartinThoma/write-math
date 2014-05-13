<?php
require_once '../svg.php';
include '../init.php';

if (!is_logged_in()) {
    header("Location: ../login");
}

function validate_display_name($name) {
    return preg_match('/^[A-Za-z]{1}[A-Za-z0-9_ ]{1,}[A-Za-z0-9]{1}$/',$name);
}

$sql = "SELECT  `language_code` ,  `english_language_name` 
FROM  `wm_languages` 
ORDER BY  `english_language_name` ASC";
$stmt = $pdo->prepare($sql);
$stmt->execute();
$languages =$stmt->fetchAll();

if (isset($_POST['language'])) {
    $lang = $_POST['language'];
    $handedness = $_POST['handedness'];

    if (validate_display_name($_POST['display_name'])) {
        $sql = "UPDATE `wm_users` SET ".
               "`display_name` = :display_name ".
               "WHERE `id` = :uid;";
        $stmt = $pdo->prepare($sql);
        $uid = get_uid();
        $stmt->bindParam(':uid', $uid, PDO::PARAM_INT);
        $stmt->bindParam(':display_name', $_POST['display_name'], PDO::PARAM_STR);
        $stmt->execute();
    }

    if (isset($_POST['password']) && $_POST['password'] != "") {
        if (strlen($_POST['password']) < 6) {
            $msg[] = array("class" => "alert-danger",
                           "text" => "Your password has to have 6 characters.");
        } elseif ($_POST['password'] != $_POST['passwordconf']) {
            $msg[] = array("class" => "alert-danger",
                           "text" => "Your passwords did not match.");
        } else {
            $sql = "UPDATE `wm_users` SET `password` = :password ".
                   "WHERE `id` = :uid;";
            $stmt = $pdo->prepare($sql);
            $uid = get_uid();
            $stmt->bindParam(':uid', $uid, PDO::PARAM_INT);
            $hash = password_hash($_POST['password'], PASSWORD_BCRYPT, array("cost" => 10));
            $stmt->bindParam(':password', $hash, PDO::PARAM_STR);
            $stmt->execute();
            header("Location: ../login");
        }
    }

    if ($lang == 'NULL') {
        $sql = "UPDATE `wm_users` SET `language` =  NULL WHERE `id` = :uid;";
        $stmt = $pdo->prepare($sql);
        $uid = get_uid();
        $stmt->bindParam(':uid', $uid, PDO::PARAM_INT);
        $stmt->execute();
    } else {
        $sql = "UPDATE `wm_users` SET `language` =  :lang WHERE `id` = :uid;";
        $stmt = $pdo->prepare($sql);
        $stmt->bindParam(':lang', $lang, PDO::PARAM_STR);
        $uid = get_uid();
        $stmt->bindParam(':uid', $uid, PDO::PARAM_INT);
        $stmt->execute();
    }

    if ($handedness == 'NULL') {
        $sql = "UPDATE `wm_users` SET `handedness` =  NULL WHERE `id` = :uid;";
        $stmt = $pdo->prepare($sql);
        $stmt->bindParam(':uid', get_uid(), PDO::PARAM_INT);
        $stmt->execute();
    } else {
        $sql = "UPDATE `wm_users` SET `handedness` =  :hand WHERE `id` = :uid;";
        $stmt = $pdo->prepare($sql);
        $stmt->bindParam(':hand', $handedness, PDO::PARAM_STR);
        $uid = get_uid();
        $stmt->bindParam(':uid', $uid, PDO::PARAM_INT);
        $stmt->execute();
    }
}


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

echo $twig->render('profile.twig', array('heading' => 'Profile',
                                       'file' => "profile",
                                       'logged_in' => is_logged_in(),
                                       'display_name' => $_SESSION['display_name'],
                                       'user_id' => get_uid(),
                                       'email' => get_email(),
                                       'gravatar' => "http://www.gravatar.com/avatar/".md5(get_email()),
                                       'language' => get_language(),
                                       'handedness' => get_handedness(),
                                       'languages' => $languages,
                                       'userimages' => $userimages,
                                       'total' => $total,
                                       'pages' => floor(($total)/14),
                                       'currentPage' => $currentPage,
                                       )
                  );

?>