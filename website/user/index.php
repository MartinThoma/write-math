<?php
require_once '../svg.php';
include '../init.php';

$sql = "SELECT `id`, `email`, `display_name`, `language`, `handedness` ".
       "FROM `wm_users` WHERE `id` = :uid";
$stmt = $pdo->prepare($sql);
$stmt->bindParam(':uid', $_GET['id'], PDO::PARAM_INT);
$stmt->execute();
$user =$stmt->fetchObject();


$sql = "SELECT  `language_code` ,  `english_language_name` 
FROM  `wm_languages` 
ORDER BY  `english_language_name` ASC";
$stmt = $pdo->prepare($sql);
$stmt->execute();
$languages =$stmt->fetchAll();

echo $twig->render('user.twig', array('heading' => 'User',
                                       'file' => "user",
                                       'logged_in' => is_logged_in(),
                                       'display_name' => $_SESSION['display_name'],
                                       'user_id' => $user->id,
                                       'gravatar' => "http://www.gravatar.com/avatar/".md5($user->email),
                                       'user' => $user,
                                       'languages' => $languages
                                       )
                  );

?>