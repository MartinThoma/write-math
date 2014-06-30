<?php

require_once('preprocessing.php');

/**
 * Classify $A with data from $datasets and smoothing of $epsilon.
 * @param  array $datasets array(
 *                             array('data' => ..., 
 *                                   'accepted_formula_id' => ...,
 *                                   'id' => ...,
 *                                   'formula_in_latex' => ...,
 *                                  )
 *                         )
 * @param  array $A        List of points
 * @return array           List of possible classifications, ordered DESC by
 *                              likelines
 */
function classify_with_greedy_matching($datasets, $A, $epsilon = 0) {
    $results = array();

    foreach ($datasets as $key => $dataset) {
        $B = $dataset['data'];
        if ($epsilon > 0) {
            $B = apply_linewise_douglas_peucker(pointLineList($B), $epsilon);
        } else {
            $B = pointLineList($B);
        }
        $B = scale_and_shift($B);
        $results[] = array("dtw" => apply_greedy_matching_dtw_linewise($A, $B),
                           "latex" => $dataset['accepted_formula_id'],
                           "id" => $dataset['id'],
                           "latex" => $dataset['formula_in_latex'],
                           "formula_id" => $dataset['formula_id']);
    }

    $dtw = array();
    foreach ($results as $key => $row) {
        $dtw[$key] = $row['dtw'];
    }
    array_multisort($dtw, SORT_ASC, $results);
    $results = array_filter($results, "maximum_dtw");

    // get only best match for each single symbol
    $results2 = array();
    foreach ($results as $key => $row) {
        if (array_key_exists($row['formula_id'], $results2)) {
            $results2[$row['formula_id']] = min($results2[$row['formula_id']], $row['dtw']);
        } else {
            $results2[$row['formula_id']] = $row['dtw'];
        }
    }

    $results = $results2;
    $results = array_slice($results, 0, 10, true);

    $results = get_probability_from_distance($results);
    return $results;
}

function d($p1, $p2) {
    $dx = $p1["x"] - $p2["x"];
    $dy = $p1["y"] - $p2["y"];
    return $dx*$dx + $dy*$dy;
}

function apply_greedy_matching_dtw_linewise($A, $B) {
    if (count($A) != count($B)) {
        # If they have a different count of lines, they are different
        return 1.8e200;
    } else {
        $dist = 0;
        for ($i=0; $i < count($A); $i++) { 
            $dist += greedyMatchingDTW($A[$i], $B[$i]);
        }
        return $dist;
    }
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

function pointLineList($linelistP) {
    global $msg;

    $linelist = json_decode($linelistP);
    $pointlist = array();
    foreach ($linelist as $line) {
        $l = array();
        foreach ($line as $p) {
            $l[] = array("x"=>$p->x, "y"=>$p->y, "time"=>$p->time);
        }
        $pointlist[] = $l;
    }

    if (count($pointlist) == 0) {
        $msg[] = array("class" => "alert-warning",
                       "text" => "Pointlist was empty. Search for '".
                                 $linelistP."' in `wm_raw_draw_data`.");
    }
    return $pointlist;
}

function pointList($linelistP) {
    global $msg;

    $linelist = json_decode($linelistP);
    $pointlist = array();
    foreach ($linelist as $line) {
        foreach ($line as $p) {
            $pointlist[] = array("x"=>$p->x, "y"=>$p->y);
        }
    }

    if (count($pointlist) == 0) {
        $msg[] = array("class" => "alert-warning",
                       "text" => "Pointlist was empty. Search for '".
                                 $linelistP."' in `wm_raw_draw_data`.");
    }

    return $pointlist;
}

function list_of_pointlists2pointlist($data) {
    $result = array();
    foreach ($data as $line) {
        $result = array_merge($result, $line);
    }
    return $result;
}

function get_time_resolution($pointlist, $lines_nr) {
    $min_time_resolution = $pointlist[1]["time"]-$pointlist[0]["time"];
    $max_time_resolution = $min_time_resolution;

    $n = count($pointlist);
    $timesum = 0.0;
    $counter = 0;

    for ($i= $n-1; $i >= 1; $i--) {
        $delta = $pointlist[$i]["time"] - $pointlist[$i-1]["time"];
        if ($delta < 0) {
            continue;
        }
        $timesum += $delta;
        $counter += 1;
        if ($delta < $min_time_resolution) {
            $min_time_resolution = $delta;
        }
        if ($delta > $max_time_resolution) {
            $max_time_resolution = $delta;
        }
    }

    $divisor = $n-$lines_nr;

    if ($divisor == 0) {
        $avg_time_resolution = 0;
        $min_time_resolution = 0;
        $max_time_resolution = 0;
    } else {
        $avg_time_resolution = $timesum / $divisor;
    }

    return array("min_time_resolution" => $min_time_resolution,
                 "max_time_resolution" => $max_time_resolution,
                 "average_time_resolution" => $avg_time_resolution);
}

function maximum_dtw($var, $threshold=20) {
    if ($threshold == 0) {
        return true;
    } else {
        return ($var['dtw'] < $threshold);
    }
}

function get_probability_from_distance($results) {
    if (count($results) == 0) {
        return array();
    }
    // check if one distance is 0 and meanwhile build sum of distances.
    $sum = 0.0;
    $modified = array();
    foreach ($results as $formula_id => $dtw) {
        if ($dtw == 0) {
            return array(array($formula_id => 1));
        } else {
            $modified[$formula_id] = exp(-$dtw);
            $sum += $modified[$formula_id];
        }
    }

    $results = $modified;

    $probabilities = array();
    foreach ($results as $formula_id => $p) {
        $probabilities[] = array($formula_id => $p / $sum);
    }
    return $probabilities;
}

?>