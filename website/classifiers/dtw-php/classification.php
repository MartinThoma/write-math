<?php

function scale_and_center($pointlist, $center = false) {
    global $msg;

    extract(get_bounding_box($pointlist));

    $width = $maxx - $minx;
    $height = $maxy - $miny;

    $factorX = 1;
    $factorY = 1;
    if ($width != 0) {
        $factorX = 1./$width;
    }

    if ($height != 0) {
        $factorY = 1./$height;
    }

    $factor = min($factorX, $factorY);
    $addx = 0;
    $addy = 0;

    if ($center) {
        $add = (1 - (max($factorX, $factorY) / $factor)) / 2;
    
        if ($factor == $factorX) {
            $addy = $add;
        } else {
            $addx = $add;
        }
    }

    foreach ($pointlist as $key => $p) {
        $pointlist[$key] = array("x" => ($p["x"] - $minx)*$factor + $addx,
                                 "y" => ($p["y"] - $miny)*$factor + $addy);
    }

    return $pointlist;
}

/**
 * Calculate the squared eucliden distance of two points.
 * @param  associative array $p1 first point
 * @param  associative array $p2 second point
 * @return float
 */
function d($p1, $p2) {
    $dx = $p1["x"] - $p2["x"];
    $dy = $p1["y"] - $p2["y"];
    return sqrt($dx*$dx + $dy*$dy); // TODO: try sqrt
}

function maximum_dtw($var, $threshold=20) {
    if ($threshold == 0) {
        return true;
    } else {
        return ($var['dtw'] < $threshold);
    }
}

/**
 * Calculate distance of $A and $B by greedy dynamic time warping.
 * @param  array $A list of points
 * @param  array $B list of points
 * @return float    Minimal distance you have to move points from A to get B
 */
function greedyMatchingDTW($A, $B) {
    $a = array_shift($A);
    $b = array_shift($B);
    $d = d($a, $b);
    $as = array_shift($A);
    $bs = array_shift($B);
    while (count($A) > 0 && count($B) > 0) {
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

/**
 * Calculate the distance from $p3 to the line defined by $p1 and $p2.
 * @param array $p1 associative array with "x" and "y" (start of line)
 * @param array $p2 associative array with "x" and "y" (end of line)
 * @param array $p3 associative array with "x" and "y" (point)
 */
function LotrechterAbstand($p1, $p2, $p3) {
    $x3 = $p3['x'];
    $y3 = $p3['y'];

    $px = $p2['x']-$p1['x'];
    $py = $p2['y']-$p1['y'];

    $something = $px*$px + $py*$py;
    if ($something == 0) {
        // TODO: really?
        return 0;
    }

    $u =  (($x3 - $p1['x']) * $px + ($y3 - $p1['y']) * $py) / $something;

    if ($u > 1) {
        $u = 1;
    } elseif ($u < 0) {
        $u = 0;
    }

    $x = $p1['x'] + $u * $px;
    $y = $p1['y'] + $u * $py;

    $dx = $x - $x3;
    $dy = $y - $y3;

    # Note: If the actual distance does not matter,
    # if you only want to compare what this function
    # returns to other results of this function, you
    # can just return the squared distance instead
    # (i.e. remove the sqrt) to gain a little performance

    $dist = sqrt($dx*$dx + $dy*$dy);
    return $dist;
}

function DouglasPeucker($PointList, $epsilon) {
    // Finde den Punkt mit dem größten Abstand
    $dmax = 0;
    $index = 0;
    for ($i = 1; $i < count($PointList); $i++) {
            $d = LotrechterAbstand($PointList[0], end($PointList), $PointList[$i]);
            if ($d > $dmax) {
                $index = $i;
                $dmax = $d;
            }
    }
 
    // Wenn die maximale Entfernung größer als Epsilon ist, dann rekursiv vereinfachen
    if ($dmax >= $epsilon){
            // Recursive call
            $recResults1 = DouglasPeucker(array_slice($PointList, 0, $index), $epsilon);
            $recResults2 = DouglasPeucker(array_slice($PointList, $index, -1), $epsilon);
     
            // Ergebnisliste aufbauen
            $ResultList = array_merge(array_slice($recResults1, 0, -1), $recResults2);
    } else{
            $ResultList = array($PointList[0], end($PointList));
    }
 
    // Ergebnis zurückgeben
    return $ResultList;
}

/**
 * Apply the Douglas-Peucker algorithm to each line of $pointlist seperately.
 * @param  array $pointlist see pointList()
 * @return pointlist
 */
function apply_douglas_peucker($pointlist, $epsilon) {
    for ($i=0; $i < count($pointlist); $i++) {
        $pointlist[$i] = DouglasPeucker($pointlist[$i], $epsilon);
    }
    return $pointlist;
}

function get_path($data, $epsilon=0) {
    $path = "";
    $data = pointLineList($data);
    if (!is_array($data)) {
        echo "This was not an array!"; // TODO debug message
        var_dump($data);
        return false;
    }
    if ($epsilon > 0) {
        $data = apply_douglas_peucker($data, $epsilon);
    }

    foreach ($data as $line) {
        foreach ($line as $i => $point) {
            if ($i == 0) {
                $path .= " M ".$point['x']." ".$point['y'];
            } else {
                $path .= " L ".$point['x']." ".$point['y'];
            }
        }
    }

    return $path;
}

function pointLineList($linelistP) {
    global $msg;

    $linelist = json_decode($linelistP);
    $pointlist = array();
    foreach ($linelist as $line) {
        $l = array();
        foreach ($line as $p) {
            $l[] = array("x"=>$p->x, "y"=>$p->y);
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

function get_bounding_box($pointlist) {
    $minx = $pointlist[0]["x"];
    $maxx = $pointlist[0]["x"];
    $miny = $pointlist[0]["y"];
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
    return array("minx" => $minx, "maxx" => $maxx,
                 "miny" => $miny, "maxy" => $maxy);
}

function list_of_pointlists2pointlist($data) {
    $result = array();
    foreach ($data as $line) {
        $result = array_merge($result, $line);
    }
    return $result;
}

function get_dimensions($pointlist) {
    extract(get_bounding_box($pointlist));
    return array("width" => $maxx - $minx, "height" => $maxy - $miny);
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
function classify($datasets, $A, $epsilon = 0) {
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

?>