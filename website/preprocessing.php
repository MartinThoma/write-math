<?php

/**
 * Scale a list of points so that they fit into a unit square and shift the
 * points into [0, 1] x [0, 1].
 * @param  array   $pointlist A list of lines. Lines themselfs are lists of
 *                            associative arrays.
 * @param  boolean $center    Should the symbol be centered within [0,1]x[0,1]
 * @return array              Pointlist
 */
function scale_and_shift($pointlist, $center=false, $square_base_size=1) {
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

    $factor = min($factorX, $factorY)*$square_base_size;
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

    foreach ($pointlist as $key1 => $line) {
        foreach ($line as $key2 => $p) {
            $pointlist[$key1][$key2] = array("x" => ($p["x"] - $minx)*$factor + $addx,
                                     "y" => ($p["y"] - $miny)*$factor + $addy,
                                     "time" => $p["time"]-$mint);
        }
    }

    return $pointlist;
}


/**
 * Get the bounding box (space and time) for
 * @param  array $pointlist A list of lines. Lines themselfs are lists of
 *                          associative arrays.
 * @return array            Return an associative array with 'minx', 'maxx'
 *                          'miny', 'maxy', 'mint', 'maxt'
 */
function get_bounding_box($pointlist) {
    $minx = $pointlist[0][0]["x"];
    $maxx = $pointlist[0][0]["x"];
    $miny = $pointlist[0][0]["y"];
    $maxy = $pointlist[0][0]["y"];
    $mint = $pointlist[0][0]["time"];
    $maxt = $pointlist[0][0]["time"];

    foreach ($pointlist as $line) {
        foreach ($line as $p) {
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
            if ($p["time"] < $mint) {
                $mint = $p["time"];
            }
            if ($p["time"] > $maxt) {
                $maxt = $p["time"];
            }
        }
    }
    return array("minx" => $minx, "maxx" => $maxx,
                 "miny" => $miny, "maxy" => $maxy,
                 "mint" => $mint, "maxt" => $maxt);
}

/**
 * Get width and height of a list of points.
 * @param  array $pointlist A list of lines. Lines themselfs are lists of
 *                          associative arrays.
 * @return array            Associative array with 'width' and 'height'.
 */
function get_dimensions($pointlist) {
    extract(get_bounding_box($pointlist));
    return array("width" => $maxx - $minx, "height" => $maxy - $miny);
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

/**
 * Apply the Douglas Peucker algorithm to reduce the number of points.
 * @param array $flat_pointlist A list of points (not a list of lines!)
 * @param float $epsilon        maximum distance a point may have
 * @return  pointlist Reduced number of points
 */
function DouglasPeucker($flat_pointlist, $epsilon) {
    // Finde den Punkt mit dem größten Abstand
    $dmax = 0;
    $index = 0;
    for ($i = 1; $i < count($flat_pointlist); $i++) {
            $d = LotrechterAbstand($flat_pointlist[0],
                                   end($flat_pointlist),
                                   $flat_pointlist[$i]);
            if ($d > $dmax) {
                $index = $i;
                $dmax = $d;
            }
    }
 
    // Wenn die maximale Entfernung größer als Epsilon ist, dann rekursiv vereinfachen
    if ($dmax >= $epsilon){
            // Recursive call
            $recResults1 = DouglasPeucker(array_slice($flat_pointlist, 0, $index),
                                          $epsilon);
            $recResults2 = DouglasPeucker(array_slice($flat_pointlist, $index, -1),
                                          $epsilon);
     
            // Ergebnisliste aufbauen
            $ResultList = array_merge(array_slice($recResults1, 0, -1), $recResults2);
    } else{
            $ResultList = array($flat_pointlist[0], end($flat_pointlist));
    }
 
    // Ergebnis zurückgeben
    return $ResultList;
}

/**
 * Apply the Douglas-Peucker algorithm to each line of $pointlist seperately.
 * @param  array     $pointlist A list of lines. Lines themselfs are lists of
 *                              associative arrays.
 * @return pointlist
 */
function apply_linewise_douglas_peucker($pointlist, $epsilon) {
    for ($i=0; $i < count($pointlist); $i++) {
        $pointlist[$i] = DouglasPeucker($pointlist[$i], $epsilon);
    }
    return $pointlist;
}
?>