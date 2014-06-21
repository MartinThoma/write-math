<?php
require_once 'init.php';
require_once 'classification.php';

$epsilon = isset($_POST['epsilon']) ? $_POST['epsilon'] : 0;

if (isset($_GET['heartbeat'])) {
    echo $_GET['heartbeat'];
} elseif (isset($_POST['classify'])) {
    $raw_data_id = $_POST['raw_data_id'];
    $raw_draw_data = $_POST['classify'];

    // Classification
    if ($epsilon > 0) {
        $result_path = apply_douglas_peucker(pointLineList($raw_draw_data), $epsilon);
    } else {
        $result_path = pointLineList($raw_draw_data);
    }
    $A = scale_and_center(list_of_pointlists2pointlist($result_path));

    // Get the first 4000 known formulas
    $sql = "SELECT `wm_raw_draw_data`.`id`, `data`, `accepted_formula_id`, ".
           "`formula_in_latex`, `accepted_formula_id` as `formula_id`".
           "FROM `wm_raw_draw_data` ".
           "JOIN  `wm_formula` ON  `wm_formula`.`id` =  `accepted_formula_id` ".
           "LIMIT 4000";
    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    $datasets = $stmt->fetchAll();

    $results = classify($datasets, $A);
    echo json_encode($results);
}

?>