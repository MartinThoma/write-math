<?php
require_once 'preprocessing.php';
require_once 'classification.php';

function get_dots($data) {
    $dots = array();
    $pointList = pointLineList($data);
    foreach ($pointList as $line) {
        if (count($line) == 1) {
            $dots[] = array('x'=> $line[0]["x"],
                            'y'=> $line[0]["y"],
                            'time'=> $line[0]["time"]);
        }
    }
    return $dots;
}

function create_raw_data_svg($raw_data_id, $data) {
    # Move drawing so that the smallest x-value is 0 and the smallest y value
    # is 0.
    $pointList = pointLineList($data);
    $b = get_bounding_box($pointList);
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
            $newLine[] = array("x" => $newx,
                               "y" => $newy,
                               "time" => $point["time"]);
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

function get_path($data, $epsilon=0) {
    $path = "";
    $data = pointLineList($data);
    if (!is_array($data)) {
		echo "This was not an array!"; // TODO debug message
        var_dump($data);
        return false;
    }
    if ($epsilon > 0) {
        $data = apply_linewise_douglas_peucker($data, $epsilon);
    }

    foreach ($data as $line) {
        //if (count($line) > 1) {
            foreach ($line as $i => $point) {
                if ($i == 0) {
                    $path .= " M ".$point['x']." ".$point['y'];
                } else {
                    $path .= " L ".$point['x']." ".$point['y'];
                }
            }
        //}
    }

    return $path;
}

?>