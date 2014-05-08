<?php
include '../init.php';

$sql = "SELECT COUNT(`id`) as `user_count` FROM `wm_users`";
$stmt = $pdo->prepare($sql);
$stmt->execute();
$user_count = $stmt->fetchObject()->user_count;

$sql = "SELECT COUNT(`id`) as `formula_count` FROM `wm_formula`";
$stmt = $pdo->prepare($sql);
$stmt->execute();
$formula_count = $stmt->fetchObject()->formula_count;

$sql = "SELECT COUNT(`id`) as `raw_data_count` FROM `wm_raw_draw_data`";
$stmt = $pdo->prepare($sql);
$stmt->execute();
$raw_data_count = $stmt->fetchObject()->raw_data_count;

$sql = "SELECT COUNT(`id`) as `unclassified_count` FROM `wm_raw_draw_data` WHERE `accepted_formula_id` IS NULL";
$stmt = $pdo->prepare($sql);
$stmt->execute();
$unclassified_count = $stmt->fetchObject()->unclassified_count;

echo $twig->render('about.twig', array('heading' => 'About',
                                       'file'=> "about",
                                       'logged_in' => is_logged_in(),
                                       'display_name' => $_SESSION['display_name'],
                                       'msg' => $msg,
                                       'user_count' => $user_count,
                                       'formula_count' => $formula_count,
                                       'raw_data_count' => $raw_data_count,
                                       'unclassified_count' => $unclassified_count
                                       )
                  );