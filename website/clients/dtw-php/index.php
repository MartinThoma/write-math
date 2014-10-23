<?php
require_once 'init.php';
require_once '../../classification.php';

$epsilon = isset($_POST['epsilon']) ? $_POST['epsilon'] : 0;

if (isset($_GET['heartbeat'])) {
    echo $_GET['heartbeat'];
} elseif (isset($_POST['classify'])) {
    $raw_draw_data = $_POST['classify'];

    // Classification
    if ($epsilon > 0) {
        $result_path = apply_linewise_douglas_peucker(pointLineList($raw_draw_data),
                                                      $epsilon);
    } else {
        $result_path = pointLineList($raw_draw_data);
    }
    $A = scale_and_shift($result_path);

    // Get the first 2000 known formulas
    $sql = "SELECT `wm_raw_draw_data`.`id`, `data`, `accepted_formula_id`, ".
           "`formula_in_latex`, `accepted_formula_id` as `formula_id`".
           "FROM `wm_raw_draw_data` ".
           "JOIN  `wm_formula` ON  `wm_formula`.`id` =  `accepted_formula_id` ".
           "LIMIT 2000";
    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    $datasets = $stmt->fetchAll();

    $results = classify_with_greedy_matching($datasets, $A);
    echo json_encode($results);
}

?>