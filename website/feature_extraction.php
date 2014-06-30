<?php

function squared_dist($p1, $p2) {
    return pow($p1['x'] - $p2['x'], 2) + pow($p1['y'] - $p2['y'], 2);
}

function get_max_distance($L) {
    if (count($L) <= 1) {
        return -1;
    } else {
        $max_dist = squared_dist($L[0], $L[1]);
        for ($i=0; $i < count($L)-1; $i++) { 
            for ($j=$i+1; $j < count($L); $j++) { 
                $max_dist = max(squared_dist($L[$i], $L[$j]), $max_dist);
            }
        }
        return $max_dist;
    }
}

function get_point_count($data) {
    // TODO: Probably data should get scaled before
    $sum = 0;
    if (!is_array($data)) {
        # TODO: This should not happen
        error_log($data);
        return -1;
    }
    foreach ($data as $line) {
        if (get_max_distance($line) < 100) {
            $sum += 1;
        }
    }
    return $sum;
}

?>