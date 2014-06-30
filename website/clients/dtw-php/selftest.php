<?php
set_time_limit (6*60*60);
require_once 'init.php';
require_once '../../classification.php';

// Parameters for self-testing
define("MIN_OCCURENCES", 10);
define("K_FOLD", 10);
define("EPSILON", 0);
define("CENTER", false);

// Prepare crossvalidation data set
$crossvalidation = array(
        array(),
        array(),
        array(),
        array(),
        array(),
        array(),
        array(),
        array(),
        array(),
        array()
    );

$sql = "SELECT id, formula_in_latex FROM `wm_formula`";
$stmt = $pdo->prepare($sql);
$stmt->execute();
$datasets = $stmt->fetchAll();

$symbol_counter = 0;
$raw_data_counter = 0;
$symbols = array();

foreach ($datasets as $key => $dataset) {
    $id = $dataset['id'];
    $sql = "SELECT id, data FROM `wm_raw_draw_data` WHERE `accepted_formula_id` = :fid";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':fid', $id, PDO::PARAM_INT);
    $stmt->execute();
    $raw_datasets = $stmt->fetchAll();
    if (count($raw_datasets) >= MIN_OCCURENCES) {
        $symbol_counter += 1;
        $symbols[] = $dataset['formula_in_latex'];
        echo $dataset['formula_in_latex']." (".count($raw_datasets)."), ";
        $i = 0;
        foreach ($raw_datasets as $key => $raw_data) {
            $raw_data_counter += 1;
            $crossvalidation[$i][] = array('data' => $raw_data['data'],
                                           'id' => $raw_data['id'],
                                           'formula_id' => $dataset['id'],
                                           'accepted_formula_id' => $id,
                                           'formula_in_latex' => $dataset['formula_in_latex']
                                          );
            $i = ($i + 1) % K_FOLD;
        }
    }
}

// Start getting validation results
$classification_accuracy = array();
echo "\n\n";
$execution_time = array();

function is_in_top_ten($id, $data) {
    $keys = array();
    foreach ($data as $key => $value) {
        $keys[] = key($value);
    }
    return in_array($id, $keys);
}

for ($testset=0; $testset < K_FOLD; $testset++) {
    $classification_accuracy[] = array('correct' => 0,
                                       'wrong' => 0,
                                       'c10' => 0,
                                       'w10' => 0);
    foreach ($crossvalidation[$testset] as $testdata) {
        $start = microtime (true);
        $raw_draw_data = $testdata['data'];
        if (EPSILON > 0) {
            $result_path = apply_linewise_douglas_peucker(pointLineList($raw_draw_data),
                                                          EPSILON);
        } else {
            $result_path = pointLineList($raw_draw_data);
        }
        $A = scale_and_shift($result_path, CENTER);

        // Prepare datasets the algorithm may use
        $datasets = array();
        foreach ($crossvalidation as $key => $value) {
            if ($key == $testset) {
                continue;
            } else {
                $datasets = array_merge($datasets, $value);
            }
        }

        $results = classify_with_greedy_matching($datasets, $A, EPSILON);
        $end = microtime (true);
        $execution_time[] = $end - $start;

        reset($results);
        $answer_id = 0;
        if(count($results) == 0 || is_null($results[0])) {
            # That should not happen. Threshold of maximum_dtw might be too
            # high.
            echo "\nRaw_data_id = ".$testdata['id']."\n";
            $answer_id = key($results);
        } else {
            $answer_id = key($results[0]);
        }

        if ($answer_id == $testdata['formula_id']) {
            $classification_accuracy[$testset]['correct'] += 1;
        } else {
            $classification_accuracy[$testset]['wrong'] += 1;
        }

        if (is_in_top_ten($testdata['formula_id'], $results)) {
            $classification_accuracy[$testset]['c10'] += 1;
        } else {
            $classification_accuracy[$testset]['w10'] += 1;
        }
        echo "|";
    }

    $classification_accuracy[$testset]['accuracy'] = $classification_accuracy[$testset]['correct'] / 
        ($classification_accuracy[$testset]['correct'] + $classification_accuracy[$testset]['wrong']);
    $classification_accuracy[$testset]['a10'] = $classification_accuracy[$testset]['c10'] /
        ($classification_accuracy[$testset]['c10'] + $classification_accuracy[$testset]['w10']);
    var_dump($classification_accuracy[$testset]);
    echo "\n";
    echo "Average time:";
    echo array_sum($execution_time)/count($execution_time);
}

var_dump($classification_accuracy);

$t1sum = 0;
$t10sum = 0;

for ($testset=0; $testset < K_FOLD; $testset++) { 
    $t1sum += $classification_accuracy[$testset]['accuracy'];
    $t10sum += $classification_accuracy[$testset]['a10'];
}

echo date("Y-m-d\n")."\n";
echo "The following ".$symbol_counter." symbols with ".$raw_data_counter." raw dataset ".
     "evaluated to\n";
echo implode(", ", $symbols)."\n";
echo "Epsilon: ".EPSILON."\n";
echo "Center: ".CENTER."\n";
echo "* Top-1-Classification (".K_FOLD."-fold cross-validated): ".($t1sum/K_FOLD)."\n";
echo "* Top-10-Classification (".K_FOLD."-fold cross-validated): ".($t10sum/K_FOLD)."\n";
echo "Aveage time: ".(array_sum($execution_time)/count($execution_time))."\n";

?>