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

// Get total number of elements for pagination
$sql = "SELECT COUNT(`id`) as counter FROM `wm_raw_draw_data` ".
       "WHERE `user_id` = :uid";
$stmt = $pdo->prepare($sql);
$uid = get_uid();
$stmt->bindParam(':uid', $_GET['id'], PDO::PARAM_STR);
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
$stmt->bindParam(':uid', $_GET['id'], PDO::PARAM_STR);
$stmt->execute();
$userimages = $stmt->fetchAll();

echo $twig->render('user.twig', array('heading' => 'User \''.$user->display_name.'\'',
                                      'file' => "user",
                                      'logged_in' => is_logged_in(),
                                      'display_name' => $_SESSION['display_name'],
                                      'user_id' => $user->id,
                                      'gravatar' => "http://www.gravatar.com/avatar/".md5($user->email),
                                      'user' => $user,
                                      'languages' => $languages,
                                      'userimages' => $userimages,
                                      'total' => $total,
                                      'pages' => floor(($total)/14),
                                      'currentPage' => $currentPage
                                      )
                  );

?>