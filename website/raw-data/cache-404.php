<?php
include '../init.php';
require_once '../svg.php';
$raw_data_id = basename($_SERVER['REQUEST_URI'], ".svg");

$sql = "SELECT `data` FROM `wm_raw_draw_data` WHERE id=:did";
$stmt = $pdo->prepare($sql);
$stmt->bindParam(':did', $raw_data_id, PDO::PARAM_INT);
$stmt->execute();
$data = $stmt->fetchObject()->data;

create_raw_data_svg($raw_data_id, $data);
header("Location: ../raw-data/$raw_data_id.svg");
?>