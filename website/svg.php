<?php
require_once '../classification.php';

function create_raw_data_svg($raw_data_id, $data) {
    # Move drawing so that the smallest x-value is 0 and the smallest y value
    # is 0.
    $pointList = pointLineList($data);
    $a = list_of_pointlists2pointlist($pointList);
    $b = get_bounding_box($a);
    extract($b);
    $linewidth = 5;
    $width  = $linewidth*3 + $maxx - $minx;
    $height = $linewidth*3 + $maxy - $miny;
    $dots = "";

    $newList = array();
    foreach ($pointList as $line) {
        $newLine = array();
        foreach ($line as $point) {
            $newx = $linewidth + $point["x"] - $minx;
            $newy = $linewidth + $point["y"] - $miny;
            $newLine[] = array("x" => $newx, "y" => $newy);
        }
        if (count($line) == 1) {
            $dots .= '<circle cx="'.$newx.'" cy="'.$newy.'" r="2" style="fill:#ff0000;stroke:#ff0000;"/>';
        }
        $newList[] = $newLine;
    }

    $path = get_path(json_encode($newList));

    # Create SVG and store it for later usage
    $filename = "../classify/svg-template.svg";
    $handle = fopen($filename, "r");
    $contents = fread($handle, filesize($filename));
    fclose($handle);

    $contents = str_replace("{{ width }}", $width, $contents);
    $contents = str_replace("{{ height }}", $height, $contents);
    $contents = str_replace("{{ path }}", $path, $contents);
    $contents = str_replace("{{ dots }}", $dots, $contents);

    file_put_contents ("../raw-data/$raw_data_id.svg", $contents);
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

?>