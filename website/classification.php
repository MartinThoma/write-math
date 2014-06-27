<?php

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

function get_bounding_box2($pointLinelist) {
    $minx = $pointLinelist[0][0]["x"];
    $maxx = $pointLinelist[0][0]["x"];
    $miny = $pointLinelist[0][0]["y"];
    $maxy = $pointLinelist[0][0]["y"];
    $mint = $pointLinelist[0][0]["time"];
    $maxt = $pointLinelist[0][0]["time"];
    foreach ($pointLinelist as $line) {
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
?>