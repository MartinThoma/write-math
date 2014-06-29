<?php
require_once 'init.php';
require_once 'classification.php';
require_once '../../render/functions.php';
require_once '../../view/functions.php';

function get_lines($data) {
    return count($data);
}

$sql = "SELECT `id`, `data`, `nr_of_symbols`, `accepted_formula_id` FROM `wm_raw_draw_data`";
$stmt = $pdo->prepare($sql);
$stmt->execute();
$datasets = $stmt->fetchAll();
foreach ($datasets as $key => $dataset) {
    $sql = "INSERT INTO `wm_dtw_worker_data` (`id` , ".
           "`data` , ".
           "`preprocessed_data` , ".
           "`nr_of_symbols` , ".
           "`accepted_formula_id` , ".
           "`nr_of_lines` , ".
           "`nr_of_points` ".
           ") VALUES (:id, :data, :preprocessed, :nr_of_symbols, :aid, :lines, :points)";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':id', $dataset->id, PDO::PARAM_INT);
    $stmt->bindParam(':data', $dataset->data, PDO::PARAM_STR);
    $data = $dataset->data;
    // scale and center
    $data = json_encode(scale_and_shift(json_decode($data, true), true));

    // Douglas peucker
    $data = json_encode(apply_douglas_peucker(json_decode($data, true), $epsilon));

    // Cubic spline
    $pointlist = json_decode($data, true);
    $pointlist = calculate_spline_points($pointlist, $cubic_spline_points);
    $data = json_encode($pointlist);

    // Scale and center again
    $data = json_encode(scale_and_shift(json_decode($data, true), true));

    $stmt->bindParam(':preprocessed', $data, PDO::PARAM_STR);
    $stmt->bindParam(':data', $dataset->data, PDO::PARAM_STR);
    $stmt->bindParam(':nr_of_symbols', $dataset->nr_of_symbols, PDO::PARAM_INT);
    $stmt->bindParam(':aid', $dataset->accepted_formula_id, PDO::PARAM_INT);

    $lines = get_lines($data);
    $stmt->bindParam(':lines', $lines, PDO::PARAM_INT);

    $points = get_points($data);
    $stmt->bindParam(':points', $points, PDO::PARAM_INT);

    $stmt->execute();
    $datasets = $stmt->fetchAll();
}

?>