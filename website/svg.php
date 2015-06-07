<?php
require_once 'preprocessing.php';
require_once 'classification.php';
require_once 'segmentation.php';

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


function get_colors($segmentation) {
    $symbol_count = count($segmentation);
    $num_colors = $symbol_count;

    // See
    // http://stackoverflow.com/a/20298116/562769
    $color_array = array(
        "#000000", "#FFFF00", "#1CE6FF", "#FF34FF", "#FF4A46", "#008941", "#006FA6", "#A30059",
        "#FFDBE5", "#7A4900", "#0000A6", "#63FFAC", "#B79762", "#004D43", "#8FB0FF", "#997D87",
        "#5A0007", "#809693", "#FEFFE6", "#1B4400", "#4FC601", "#3B5DFF", "#4A3B53", "#FF2F80",
        "#61615A", "#BA0900", "#6B7900", "#00C2A0", "#FFAA92", "#FF90C9", "#B903AA", "#D16100",
        "#DDEFFF", "#000035", "#7B4F4B", "#A1C299", "#300018", "#0AA6D8", "#013349", "#00846F",
        "#372101", "#FFB500", "#C2FFED", "#A079BF", "#CC0744", "#C0B9B2", "#C2FF99", "#001E09",
        "#00489C", "#6F0062", "#0CBD66", "#EEC3FF", "#456D75", "#B77B68", "#7A87A1", "#788D66",
        "#885578", "#FAD09F", "#FF8A9A", "#D157A0", "#BEC459", "#456648", "#0086ED", "#886F4C",

        "#34362D", "#B4A8BD", "#00A6AA", "#452C2C", "#636375", "#A3C8C9", "#FF913F", "#938A81",
        "#575329", "#00FECF", "#B05B6F", "#8CD0FF", "#3B9700", "#04F757", "#C8A1A1", "#1E6E00",
        "#7900D7", "#A77500", "#6367A9", "#A05837", "#6B002C", "#772600", "#D790FF", "#9B9700",
        "#549E79", "#FFF69F", "#201625", "#72418F", "#BC23FF", "#99ADC0", "#3A2465", "#922329",
        "#5B4534", "#FDE8DC", "#404E55", "#0089A3", "#CB7E98", "#A4E804", "#324E72", "#6A3A4C",
        "#83AB58", "#001C1E", "#D1F7CE", "#004B28", "#C8D0F6", "#A3A489", "#806C66", "#222800",
        "#BF5650", "#E83000", "#66796D", "#DA007C", "#FF1A59", "#8ADBB4", "#1E0200", "#5B4E51",
        "#C895C5", "#320033", "#FF6832", "#66E1D3", "#CFCDAC", "#D0AC94", "#7ED379", "#012C58");

    // Apply a little trick to make sure we have enough colors, no matter
    // how many symbols are in one recording.
    // This simply appends the color array as long as necessary to get enough
    // colors
    $newArray = $color_array;
    while(count($newArray) <= $num_colors){
        $newArray = array_merge($newArray, $color_array);
    }

    return array_slice($newArray, 0, $num_colors);
}

function search_symbol_nr_by_stroke_id($stroke_id, $segmentation) {
   foreach ($segmentation as $symbol_nr => $strokes) {
       foreach ($strokes as $stroke_id_in_symbol) {
           if ($stroke_id_in_symbol === $stroke_id) {
               return $symbol_nr;
           }
       }
   }
   return null;
}


function create_raw_data_svg($raw_data_id, $data, $segmentation=NULL) {
    assert(is_null($segmentation)||is_array($segmentation),
           '$segmentation is neither NULL nor array. '.
           'It is '.gettype($segmentation).".");

    # Move drawing so that the smallest x-value is 0 and the smallest y value
    # is 0.
    $recording_point_list = pointLineList($data);
    $b = get_bounding_box($recording_point_list);
    extract($b);
    $width_stroke = 5;
    $width  = $width_stroke*3 + $maxx - $minx;
    $height = $width_stroke*3 + $maxy - $miny;
    $dots = "";

    $segmentation = make_valid_segmentation($recording_point_list, $segmentation);
    $colors = get_colors($segmentation);

    $new_list = array();
    $i = 0;
    foreach ($recording_point_list as $stroke_id=>$stroke) {
        $symbol_nr = search_symbol_nr_by_stroke_id($stroke_id, $segmentation);
        $new_stroke = array();
        foreach ($stroke as $point) {
            $newx = $width_stroke + $point["x"] - $minx;
            $newy = $width_stroke + $point["y"] - $miny;
            $new_stroke[] = array("x" => $newx,
                                  "y" => $newy,
                                  "time" => $point["time"],
                                  "color" => $colors[$symbol_nr]);
        }
        if (count($stroke) == 1) {
            $dots .= '<circle id="stroke'.$i.'" cx="'.$newx.'" cy="'.$newy.'" r="2" style="fill:'.$colors[$symbol_nr].';stroke:'.$colors[$symbol_nr].';"/>';
        }
        $new_list[] = $new_stroke;
        $i += 1;
    }

    $path = get_path(json_encode($new_list), 0, $height);

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

function get_path_pure($data, $epsilon=0) {
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

function get_path($data, $epsilon=0, $height=1000) {
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

    $first = true;

    $stroke_nr = 0;
    foreach ($data as $line) {
        //if (count($line) > 1) {
            foreach ($line as $i => $point) {
                if (!$first && $i == 0) {
                    $path .= '" />'."\n";
                }

                if ($i == 0) {
                    $first = false;
                    $stroke_width = 5;
                    if ($height > 1000) {
                        $stroke_width = $height / 50.0;
                    }
                    $path .= "<path id='stroke".$stroke_nr."' style=\"fill:none;stroke:".$point['color'].";stroke-width:$stroke_width;stroke-linecap:round;\" d=\"  M ".$point['x']." ".$point['y'];
                } else {
                    $path .= " L ".$point['x']." ".$point['y'];
                }
            }
        //}
        $stroke_nr += 1;
    }
    $path .= '" />'."\n";

    return $path;
}

?>