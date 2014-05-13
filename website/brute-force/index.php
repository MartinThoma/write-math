<?php

require_once '../svg.php';
require_once '../classification.php';
include '../init.php';

$A = "";
$results = "";

function scale_and_center($pointlist) {
    global $msg;

    extract(get_bounding_box($pointlist));

    $width = $maxx - $minx;
    $height = $maxy - $miny;

    $factorX = 1;
    $factorY = 1;
    if ($width == 0) {
        $msg[] = array("class" => "alert-warning",
                       "text" => "Width was 0!"); // TODO: fix this! 
    } else {
        $factorX = 1./$width;
    }

    if ($height == 0) {
        $msg[] = array("class" => "alert-warning",
                       "text" => "Width was 0!"); // TODO: fix this! 
    } else {
        $factorY = 1./$height;
    }

    $factor = min($factorX, $factorY);
    $addx = 0;
    $addy = 0;

/*    $add = (1 - (max($factorX, $factorY) / $factor)) / 2;

    if ($factor == $factorX) {
        $addy = $add; //TODO
    } else {
        $addx = $add; //TODO
    }*/

    foreach ($pointlist as $key => $p) {
        $pointlist[$key] = array("x" => ($p["x"] - $minx)*$factor + $addx,
                                 "y" => ($p["y"] - $miny)*$factor + $addy);
    }

    return $pointlist;
}

function d($p1, $p2) {
    $dx = $p1["x"] - $p2["x"];
    $dy = $p1["y"] - $p2["y"];
    return $dx*$dx + $dy*$dy;
}

function maximum_dtw($var) {
    return($var['dtw'] < 20);
}

function greedyMatchingDTW($A, $B) {
    $a = array_shift($A);
    $b = array_shift($B);
    $d = d($a, $b);
    $as = array_shift($A);
    $bs = array_shift($B);
    while (count($A) > 0 && count($B)) {
        $l = d($as, $b);
        $m = d($as, $bs);
        $r = d($a, $bs);
        $mu = min($l, $m, $r);
        $d = $d + $mu;
        if ($l == $mu) {
            $a = $as;
            $as = array_shift($A);
        } elseif ($r == $mu) {
            $b = $bs;
            $bs = array_shift($B);
        } else {
            $a = $as;
            $b = $bs;
            $as = array_shift($A);
            $bs = array_shift($B);
        }
    }
    if (count($A) == 0) {
        foreach ($B as $p) {
            $d = $d + d($as, $p);
        }
    } elseif (count($B) == 0) {
        foreach ($A as $p) {
            $d = $d + d($bs, $p);
        }
    }
    return $d;
}

if (!is_logged_in()) {
    header("Location: ../login");
}

$epsilon = isset($_POST['epsilon']) ? $_POST['epsilon'] : 0;

if (!isset($_GET['A'])) {
    $msg[] = array("class" => "alert-warning",
                   "text" => "Please provide 'A' and 'B' with a raw_data_id. ".
                             'e.g. <a href="?A=300">like this</a> or '.
                             '<a href="?A=300">like that</a>.');
} else {
    $sql = "SELECT `id`, `data` FROM `wm_raw_draw_data` ".
           "WHERE `id` = :ida";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':ida', $_GET['A'], PDO::PARAM_INT);
    $stmt->execute();

    $A_data = $stmt->fetchObject()->data;
    if ($epsilon > 0) {
        $result_path = apply_douglas_peucker(pointLineList($A_data), $epsilon);
    } else {
        $result_path = pointLineList($A_data);
    }
    $A = scale_and_center(list_of_pointlists2pointlist($result_path));

    # Check all other stuff
    $sql = "SELECT `wm_raw_draw_data`.`id`, `data`, `accepted_formula_id`, `formula_in_latex` ".
           "FROM `wm_raw_draw_data` ".
           "JOIN  `wm_formula` ON  `wm_formula`.`id` =  `accepted_formula_id` ";
    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    $datasets = $stmt->fetchAll();

    $results = array();

    foreach ($datasets as $key => $dataset) {
        $B = $dataset['data'];
        if ($epsilon > 0) {
            $B = apply_douglas_peucker(pointLineList($B), $epsilon);
        } else {
            $B = pointLineList($B);
        }
        $B = scale_and_center(list_of_pointlists2pointlist($B));
        $results[] = array("dtw" => greedyMatchingDTW($A, $B),
                           "latex" => $dataset['accepted_formula_id'],
                           "id" => $dataset['id'],
                           "latex" => $dataset['formula_in_latex']);
    }

    $dtw = array();
    foreach ($results as $key => $row) {
        $dtw[$key] = $row['dtw'];
    }
    array_multisort($dtw, SORT_ASC, $results);
    $results = array_filter($results, "maximum_dtw");
}

echo $twig->render('brute-force.twig', array('heading' => 'Brute Force DTW',
                                         'file'=> 'brute-force',
                                         'logged_in' => is_logged_in(),
                                         'display_name' => $_SESSION['display_name'],
                                         'msg' => $msg,
                                         'pathA' => get_path($A_data, $epsilon),
                                         'epsilon' => $epsilon,
                                         'results' => $results
                                       )
                  );

?>