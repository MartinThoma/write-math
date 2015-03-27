<?php
include_once '../init.php';
require_once '../classification.php';
require_once '../svg.php';

if (!is_logged_in()) {
    header("Location: ../login");
}

if (isset($_POST['recording_id'])) {
    $response = array();

    $raw_data_id = intval($_POST['recording_id']);
    $response['recording_id'] = $raw_data_id;
    $segmentation = $_POST['segmentation'];
    $segmentation = str_replace('"', "", $segmentation);
    $segmentation = str_replace("'", "", $segmentation);

    $sql = "SELECT `data` FROM `wm_raw_draw_data` WHERE id=:id";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':id', $raw_data_id, PDO::PARAM_INT);
    $stmt->execute();
    $obj = $stmt->fetchObject();
    $recording_point_list = pointLineList($obj->data);
    $segmentation = make_valid_segmentation($recording_point_list, json_decode($segmentation));
    $segmentation = json_encode($segmentation);
    $response['segmentation'] = $segmentation;
    $response['segmentation_type'] = gettype($segmentation);

    # Update segmentation of recording
    $sql = "UPDATE `wm_raw_draw_data` ".
           "SET `segmentation` = :segmentation ".
           "WHERE `id` = :raw_data_id AND (`user_id` = :uid OR :uid=10);"; // TODO: Set to admin group
    $stmt = $pdo->prepare($sql);
    $uid = get_uid();
    $response['uid'] = $uid;
    $stmt->bindParam(':raw_data_id', $raw_data_id, PDO::PARAM_INT);
    $stmt->bindParam(':segmentation', $segmentation);
    $stmt->bindParam(':uid', $uid, PDO::PARAM_INT);
    $result = $stmt->execute();
    $response['result'] = $result;

    if (get_uid() == 10) {
        $filename = dirname(dirname(__FILE__))."/raw-data/$raw_data_id.svg";
        if (file_exists($filename)) {
            unlink($filename);
        }
    }


    echo json_encode($response);
} else {
    echo "{'error': 'No recording_id'}";
}

?>