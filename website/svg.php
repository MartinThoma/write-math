<?php

/**
 * Calculate the distance from $p3 to the line defined by $p1 and $p2.
 * @param array $p1 associative array with "x" and "y" (start of line)
 * @param array $p2 associative array with "x" and "y" (end of line)
 * @param array $p3 associative array with "x" and "y" (point)
 */
function LotrechterAbstand($p1, $p2, $p3) {
    $x3 = $p3->x;
    $y3 = $p3->y;

    $px = $p2->x-$p1->x;
    $py = $p2->y-$p1->y;

    $something = $px*$px + $py*$py;

    $u =  (($x3 - $p1->x) * $px + ($y3 - $p1->y) * $py) / $something;

    if ($u > 1) {
        $u = 1;
    } elseif ($u < 0) {
        $u = 0;
    }

    $x = $p1->x + $u * $px;
    $y = $p1->y + $u * $py;

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

function get_path($data, $epsilon=0) {
    $path = "";
    $data = json_decode($data);
    if ($epsilon > 0) {
        for ($i=0; $i < count($data); $i++) {
            $data[$i] = DouglasPeucker($data[$i], $epsilon);
        }
    }

    foreach ($data as $line) {
        foreach ($line as $i => $point) {
            if ($i == 0) {
                $path .= " M ".$point->x." ".$point->y;
            } else {
                $path .= " L ".$point->x." ".$point->y;
            }
        }
    }

    return $path;
}

?>