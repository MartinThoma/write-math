<?php
include '../init.php';
require_once '../svg.php';
$raw_data_id = basename($_SERVER['REQUEST_URI'], ".svg");
if (strpos($raw_data_id,'?') !== false) {
    $raw_data_id = array_shift(explode('?', $raw_data_id));
    $raw_data_id = basename($raw_data_id, ".svg");
}
$sql = "SELECT `data`, `segmentation` FROM `wm_raw_draw_data` WHERE id=:did";
$stmt = $pdo->prepare($sql);
$stmt->bindParam(':did', $raw_data_id, PDO::PARAM_INT);
$stmt->execute();
$obj = $stmt->fetchObject();
$data = $obj->data;
$segmentation = $obj->segmentation;

create_raw_data_svg($raw_data_id, $data, $segmentation);
header("Location: ../raw-data/$raw_data_id.svg");
?>