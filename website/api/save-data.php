<?php
include '../init.php';

if (!is_logged_in()) {
    header("Location: ../login");
}

if (isset($_POST['data'])) {
    $record_id = intval($_POST['record_id']);
    $data = $_POST['data'];
    $secret = $_POST['secret'];

    $linelist = json_decode($data, true);

    if (count($linelist) == 0 || count($linelist[0]) == 0) {
        echo "Not even a single point";
    } else {
        if ($record_id == 0) {
            # Insert dataset
            $sql = "INSERT INTO `wm_raw_draw_data` (".
                   "`user_id`, ".
                   "`data`, ".
                   "`md5data`, ".
                   "`creation_date`, ".
                   "`user_agent`, ".
                   "`accepted_formula_id`, ".
                   "`secret`".
                   ") VALUES (:user_id, :data, MD5(data), ".
                   "CURRENT_TIMESTAMP, :user_agent, NULL, :secret);";
            $stmt = $pdo->prepare($sql);
            $uid = get_uid();
            $stmt->bindParam(':user_id', $uid, PDO::PARAM_INT);
            $stmt->bindParam(':data', $data, PDO::PARAM_STR);
            $stmt->bindParam(':user_agent',
                             $_SERVER['HTTP_USER_AGENT'],
                             PDO::PARAM_STR);
            $stmt->bindParam(':secret', $secret, PDO::PARAM_STR);
            $stmt->execute();
            $record_id = $pdo->lastInsertId();
            echo json_encode($record_id);
        } else {
            # Insert dataset
            $sql = "UPDATE `wm_raw_draw_data` ".
                   "SET `data` = :data ".
                   "WHERE `id` = :rid AND `secret` = :secret AND ".
                   "UNIX_TIMESTAMP(NOW())-".
                   "UNIX_TIMESTAMP(`creation_date`) < 60*5;";
            $stmt = $pdo->prepare($sql);
            $uid = get_uid();
            $stmt->bindParam(':rid', $record_id, PDO::PARAM_INT);
            $stmt->bindParam(':data', $data, PDO::PARAM_STR);
            $stmt->bindParam(':secret', $secret, PDO::PARAM_STR);
            $stmt->execute();
            echo json_encode($record_id);
        }
    }
} else {
    echo json_encode("No data received via POST.");
}

?>