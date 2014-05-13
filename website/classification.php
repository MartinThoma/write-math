<?php

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
?>