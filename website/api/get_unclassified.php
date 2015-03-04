<?php
include '../init.php';
include '../svg.php';

function insert_worker_answers($worker_id, $raw_data_id, $answer_json) {
    global $pdo;
    // Delete all answers regarding this raw_data_id from the current
    // worker
    $sql = "DELETE FROM `wm_worker_answers` WHERE `worker_id` = :wid ".
           "AND `raw_data_id` = :raw_data_id;";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':wid', $worker_id, PDO::PARAM_INT);
    $stmt->bindParam(':raw_data_id', $raw_data_id, PDO::PARAM_INT);
    $stmt->execute();
    // Insert new data
    foreach ($answer_json as $key => $object) {
        var_dump($object);
        $formula_id = array_keys($object)[0];
        $probability = $object[$formula_id];
        $sql = "INSERT INTO `wm_worker_answers` (".
                "`worker_id` , ".
                "`raw_data_id` , ".
                "`formula_id` , ".
                "`probability` ".
                ") VALUES (:wid, :raw_data_id, :formula_id, :probability)";
        $stmt = $pdo->prepare($sql);
        $stmt->bindParam(':wid', $worker_id, PDO::PARAM_INT);
        $stmt->bindParam(':raw_data_id', $raw_data_id, PDO::PARAM_INT);
        $stmt->bindParam(':formula_id', $formula_id, PDO::PARAM_INT);
        $stmt->bindParam(':probability', $probability, PDO::PARAM_STR);
        try {
          $stmt->execute();
        } catch (Exception $e) {
          var_dump($e);
        }
    }
}

if (isset($_POST['recording_id'])) {
    $sql = "SELECT `id` FROM `wm_workers` ".
           "WHERE `API_key` =:api_key ".
           "LIMIT 1";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':api_key', $_POST['api_key'], PDO::PARAM_INT);
    $stmt->execute();
    $row = $stmt->fetch();
    $worker_id = $row['id'];
    if ($worker_id != 0) {
        $raw_data_id = intval($_POST['recording_id']);
        $answer_json = json_decode($_POST['results'], true);
        insert_worker_answers($worker_id, $raw_data_id, $answer_json);
    } else {
        echo "api_key '".$_POST['api_key']."' does not exist";
    }
} else {
    $sql = "SELECT `wm_raw_draw_data`.`id`, `data` as `recording`, ".
           "`creation_date`, COUNT(`raw_data_id`) as `answers` ".
           "FROM `wm_raw_draw_data` ".
           "LEFT OUTER JOIN `wm_worker_answers` ".
                "ON (`raw_data_id` = `wm_raw_draw_data`.`id`) ".
           "WHERE `accepted_formula_id` IS NULL AND `is_image`=0 ".
           "GROUP BY `wm_raw_draw_data`.`id` ".
           "HAVING `answers` = 0 ".
           "ORDER BY `creation_date` DESC ".
           "LIMIT 1";
    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    $dbrecord = $stmt->fetch();
    echo json_encode($dbrecord);
}



?>