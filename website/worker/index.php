<?php
require_once '../svg.php';
include '../init.php';

if (isset($_GET['id'])) {
    $sql = "SELECT `wm_workers`.`id` as `woker_id`, `user_id`, ".
           "`wm_workers`.`display_name` as `worker_name`, ".
           "`wm_workers`.`description`, `url`, ".
           "`latest_heartbeat`, ".
           "`wm_users`.`display_name` ".
           "FROM `wm_workers` ".
           "JOIN `wm_users` ON `user_id` = `wm_users`.`id`".
           "WHERE `wm_workers`.`id` = :wid";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':wid', $_GET['id'], PDO::PARAM_INT);
    $stmt->execute();
    $worker = $stmt->fetchObject();
}

echo $twig->render('worker.twig', array('heading' => 'Worker',
                                       'file' => "worker",
                                       'logged_in' => is_logged_in(),
                                       'display_name' => $_SESSION['display_name'],
                                       'user_id' => $user->id,
                                       'worker' => $worker
                                       )
                  );

?>