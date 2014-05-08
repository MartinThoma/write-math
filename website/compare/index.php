<?php
require_once '../svg.php';
include '../init.php';

function pointList($linelist) {
    $linelist = json_decode($linelist);
    $pointlist = array();
    foreach ($linelist as $line) {
        foreach ($line as $p) {
            print_r($point);
            $pointlist[] = array("x"=>$p->x, "y"=>$p->y);
        }
    }
    return $pointlist;
}

function scale_and_center($pointlist) {
    $minx = $pointlist[0]["x"];
    $maxx = $pointlist[0]["x"];
    $mixy = $pointlist[0]["y"];
    $maxy = $pointlist[0]["y"];
    foreach ($pointlist as $p) {
        if ($p["x"] < $minx) {
            $minx = $p["x"];
        }
        if ($p["x"] > $maxx) {
            $maxx = $p["x"];
        }
        if ($p["y"] < $miny) {
            $miny = $p["y"];
        }
        if ($p["y"] > $maxy) {
            $maxy = $p["y"];
        }
    }

    $width = $maxx - $minx;
    $height = $maxy - $miny;
    $factorX = 1./$width;
    $factorY = 1./$height;
    $factor = min($factorX, $factorY);

    foreach ($pointlist as $key => $p) {
        $pointlist[$key] = array("x" => ($p["x"] - $minx)*$factor,
                                 "y" => ($p["y"] - $miny)*$factor);
    }

    return $pointlist;
}

function d($p1, $p2) {
    $dx = $p1["x"] - $p2["x"];
    $dy = $p1["y"] - $p2["y"];
    return $dx*$dx + $dy*$dy;
}

function greedyMatchingDTW($A, $B) {
    $A = scale_and_center(pointList($A));
    $B = scale_and_center(pointList($B));
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

if (!isset($_GET['A']) || !isset($_GET['B'])) {
    $msg[] = array("class" => "alert-warning",
                   "text" => "Please provide 'A' and 'B' with a raw_data_id.");
} else {
    $sql = "SELECT `id`, `data` FROM `wm_raw_draw_data` ".
           "WHERE `id` = :ida OR `id` = :idb";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':ida', $_GET['A'], PDO::PARAM_INT);
    $stmt->bindParam(':idb', $_GET['B'], PDO::PARAM_INT);
    $stmt->execute();
    $data = $stmt->fetchAll(PDO::FETCH_ASSOC);
}

$epsilon = isset($_POST['epsilon']) ? $_POST['epsilon'] : 0;
$A = $data[0]['data'];
$B = $data[1]['data'];

echo $twig->render('compare.twig', array('heading' => 'Compare',
                                         'file'=> 'compare',
                                         'logged_in' => is_logged_in(),
                                         'display_name' => $_SESSION['display_name'],
                                         'msg' => $msg,
                                         'pathA' => get_path($A, $epsilon),
                                         'pathB' => get_path($B, $epsilon),
                                         'epsilon' => $epsilon,
                                         'dtw_distance' => greedyMatchingDTW($A, $B)
                                       )
                  );

?>