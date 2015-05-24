<?php
include '../init.php';
require_once('../latex.php');
require_once('../view/submit_answer.php');

if (!is_logged_in()) {
    header("Location: ../login");
}

if (isset($_POST['latex_partial'])) {
    $user_id = get_uid();
    $latex = trim($_POST['latex_partial']);
    $raw_data_id = $_POST['raw_data_id'];
    $sql = "SELECT `data` ".
           "FROM `wm_raw_draw_data` ".
           "WHERE `id` = :id";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':id', $raw_data_id, PDO::PARAM_INT);
    $stmt->execute();
    $image_data = $stmt->fetchObject();
    $total_strokes = count(json_decode($image_data->data));
    $filtered_strokes = filter_strokes($_POST['strokes'], $total_strokes);
    if (count($filtered_strokes) > 0) {
        $strokes = implode(",", $filtered_strokes);
        echo add_partial_classification($user_id, $raw_data_id, $latex, $strokes);
    } else {
        echo '{"error": "Filtered strokes: '.count($filtered_strokes).' (total: '.$total_strokes.')"}';
    }
} else {
    echo json_encode('{"error": "Not POSTed latex_partial"}');
}

?>