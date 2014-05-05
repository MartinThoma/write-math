<?php
require_once '../svg.php';
include '../init.php';

$sql = "SELECT  `language_code` ,  `english_language_name` 
FROM  `wm_languages` 
ORDER BY  `english_language_name` ASC";
$stmt = $pdo->prepare($sql);
$stmt->execute();
$languages =$stmt->fetchAll();

if (isset($_POST['language'])) {
    $lang = $_POST['language'];
    $handedness = $_POST['handedness'];

    if ($lang == 'NULL') {
        $sql = "UPDATE `wm_users` SET `language` =  NULL WHERE `id` = :uid;";
        $stmt = $pdo->prepare($sql);
        $stmt->bindParam(':uid', get_uid(), PDO::PARAM_INT);
        $stmt->execute();
    } else {
        $sql = "UPDATE `wm_users` SET `language` =  :lang WHERE `id` = :uid;";
        $stmt = $pdo->prepare($sql);
        $stmt->bindParam(':lang', $lang, PDO::PARAM_STR);
        $stmt->bindParam(':uid', get_uid(), PDO::PARAM_INT);
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
        $stmt->bindParam(':uid', get_uid(), PDO::PARAM_INT);
        $stmt->execute();
    }
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
                                       'languages' => $languages
                                       )
                  );

?>