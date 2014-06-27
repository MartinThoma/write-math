<?php
include '../init.php';
include '../svg.php';

function scale_and_center($pointlist, $center = false) {
    global $msg;

    extract(get_bounding_box2($pointlist));

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

    $factor = min($factorX, $factorY)*390;
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
 * Gaussian elimination
 * @param  array $A matrix
 * @param  array $x vector
 * @return array    solution vector
 */
function gauss($A, $x) {
    # Just make a single matrix
    for ($i=0; $i < count($A); $i++) { 
        $A[$i][] = $x[$i];
    }
    $n = count($A);
 
    for ($i=0; $i < $n; $i++) { 
        # Search for maximum in this column
        $maxEl = abs($A[$i][$i]);
        $maxRow = $i;
        for ($k=$i+1; $k < $n; $k++) { 
            if (abs($A[$k][$i]) > $maxEl) {
                $maxEl = abs($A[$k][$i]);
                $maxRow = $k;
            }
        }

 
        # Swap maximum row with current row (column by column)
        for ($k=$i; $k < $n+1; $k++) { 
            $tmp = $A[$maxRow][$k];
            $A[$maxRow][$k] = $A[$i][$k];
            $A[$i][$k] = $tmp;
        }

        # Make all rows below this one 0 in current column
        for ($k=$i+1; $k < $n; $k++) { 
            $c = -$A[$k][$i]/$A[$i][$i];
            for ($j=$i; $j < $n+1; $j++) { 
                if ($i==$j) {
                    $A[$k][$j] = 0;
                } else {
                    $A[$k][$j] += $c * $A[$i][$j];
                }
            }
        }
    }

    # Solve equation Ax=b for an upper triangular matrix $A
    $x = array_fill(0, $n, 0);
    for ($i=$n-1; $i > -1; $i--) { 
        $x[$i] = $A[$i][$n]/$A[$i][$i];
        for ($k=$i-1; $k > -1; $k--) { 
            $A[$k][$n] -= $A[$k][$i] * $x[$i];
        }
    }

    return $x;
}


/**
 * Calculate the parameters of a cubic spline that interpolates $points
 * @param  array $points list of points with "x" and "y" coordinates
 * @return array         parameters of a cubic spline (array of arrays)
 */
function get_spline($points) {
    // sort points by x value
    ksort($points);

    $n = count($points) - 1;

    # Set up a system of equations of form Ax=b
    $A = array_fill(0 , 4*$n, array_fill(0, 4*$n, 0));
    $b = array_fill(0, 4*$n, 0);

    for ($i=0; $i < $n; $i++) { 
        # 2n equations from condtions (S2)
        $A[$i][4*$i+0] = pow($points[$i]["x"], 3);
        $A[$i][4*$i+1] = pow($points[$i]["x"], 2);
        $A[$i][4*$i+2] = $points[$i]["x"];
        $A[$i][4*$i+3] = 1;
        $b[$i] = $points[$i]["y"];

        $A[$n+$i][4*$i+0] = pow($points[$i+1]["x"], 3);
        $A[$n+$i][4*$i+1] = pow($points[$i+1]["x"], 2);
        $A[$n+$i][4*$i+2] = $points[$i+1]["x"];
        $A[$n+$i][4*$i+3] = 1;
        $b[$n+$i] = $points[$i+1]["y"];

        # 2n-2 equations for (S3):
        if ($i == 0) {
            continue;
        }

        # point $i is an inner point
        $A[2*$n+($i-1)][4*($i-1)+0] = 3*pow($points[$i]["x"], 2);
        $A[2*$n+($i-1)][4*($i-1)+1] = 2*$points[$i]["x"];
        $A[2*$n+($i-1)][4*($i-1)+2] = 1;
        $A[2*$n+($i-1)][4*($i-1)+0+4] = -3*pow($points[$i]["x"], 2);
        $A[2*$n+($i-1)][4*($i-1)+1+4] = -2*$points[$i]["x"];
        $A[2*$n+($i-1)][4*($i-1)+2+4] = -1;
        $b[2*$n+($i-1)] = 0;

        $A[3*$n+($i-1)][4*($i-1)+0] = 6*$points[$i]["x"];
        $A[3*$n+($i-1)][4*($i-1)+1] = 2;
        $A[3*$n+($i-1)][4*($i-1)+0+4] = -6*$points[$i]["x"];
        $A[3*$n+($i-1)][4*($i-1)+1+4] = -2;
        $b[3*$n+($i-1)] = 0;
    }



    # Natural spline:
    $A[3*$n-1+0][0+0] += 6*$points[0]["x"];
    $A[3*$n-1+0][0+1] += 2;
    $b[3*$n-1+0] += 0;

    $A[3*$n+$n-1][4*($n-1)+0] += 6*$points[$n]["x"];
    $A[3*$n+$n-1][4*($n-1)+1] += 2;
    $b[3*$n+$n-1] += 0;

    $x = gauss($A, $b);
    $spline = array();
    for ($i=0; $i < $n; $i++) { 
        $spline[] = array("u" => $points[$i]["x"], 
                          "v" => $points[$i+1]["x"],
                          "a" => $x[4*$i+0],
                          "b" => $x[4*$i+1],
                          "c" => $x[4*$i+2],
                          "d" => $x[4*$i+3]);
    }

    return $spline;
}

function evaluate_spline($spline, $x) {
    foreach ($spline as $t) {
        if ($t['u'] <= $x and $x <= $t['v']) {
            return $t['a']*pow($x, 3)
                 + $t['b']*pow($x, 2)
                 + $t['c']*$x
                 + $t['d'];
        }
    }
}

/**
 * Calculate an equidistant list of points
 * @param  array $pointlist           point list with lines
 * @param  array $interpolationpoints how many points you want to get
 * @return array                      points on a cubic spline
 */
function calculate_spline_points($pointlist, $interpolationpoints) {
    $new_points = array();
    foreach ($pointlist as $key => $line) {
        $new_line = array();
        $x = array();
        $y = array();
        foreach ($line as $p) {
            $x[] = array("x" => $p['time'], "y" => $p['x']);
            $y[] = array("x" => $p['time'], "y" => $p['y']);
        }

        $spline_x = get_spline($x);
        $spline_y = get_spline($y);
        $mint = $spline_x[0]['u'];
        $maxt = end($spline_x)['v'];
        for ($i=0; $i < $interpolationpoints; $i++) {
            $t = $mint + $i*($maxt - $mint) /($interpolationpoints-1);
            $new_x = evaluate_spline($spline_x, $t);
            $new_y = evaluate_spline($spline_y, $t);
            $new_line[] = array("x" => $new_x, "y" => $new_y, "time" => $t);
        }
        $new_points[] = $new_line;
    }
    return $new_points;
}

function count_points($pointlist) {
    $counter = 0;
    foreach ($pointlist as $line) {
        foreach ($line as $p) {
            $counter += 1;
        }
    }
    return $counter;
}

if (isset($_GET['raw_data_id'])) {
    $sql = "SELECT `id`, `data` FROM `wm_raw_draw_data` WHERE `id` = :rid";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':rid', $_GET['raw_data_id'], PDO::PARAM_INT);
    $stmt->execute();
    $image = $stmt->fetch(PDO::FETCH_ASSOC);
    $show_points = isset($_GET["show_points"]) && $_GET["show_points"] == "on";
    $scale_and_center = isset($_GET["scale_and_center"]) && $_GET["scale_and_center"] == "on";
    $cubic_spline = isset($_GET["cubic_spline"]) && $_GET["cubic_spline"] == "on";
    $douglas_peucker = isset($_GET["douglas_peucker"]) && $_GET["douglas_peucker"] == "on";

    if (isset($_GET["epsilon"]) && $_GET["epsilon"] > 0) {
        $epsilon = $_GET["epsilon"];
    } else {
        $epsilon = 10;
    }

    if (isset($_GET["cubic_spline_points"]) && $_GET["cubic_spline_points"] >= 2) {
        $cubic_spline_points = $_GET["cubic_spline_points"];
    } else {
        $cubic_spline_points = 20;
    }

    if ($cubic_spline_points > 100 && get_uid() != 10) {
        $cubic_spline_points = 100;
    }

    if ($scale_and_center) {
        $image["data"] = json_encode(scale_and_center(json_decode($image["data"], true), true));
    }

    if ($douglas_peucker) {
        $pointlist = apply_douglas_peucker(json_decode($image["data"], true), $epsilon);
        $image["data"] = json_encode($pointlist);
    }

    // Cubic spline interpolation
    if($cubic_spline) { #TODO: Fix bugs
        $pointlist = json_decode($image["data"], true);
        if (count_points($pointlist) > 100) {
            $msg[] = array("class" => "alert-warning",
                       "text" => "This symbol has too many points (".count_points($pointlist).">100) to ".
                                 "apply a cubic spline directly in the ".
                                 "cubic spline directly online. ".
                                 "You should apply the Douglas-Peucker ".
                                 "algorithm in that case. ");
        } else {
            $pointlist = calculate_spline_points($pointlist, $cubic_spline_points);
            $image["data"] = json_encode($pointlist);
        }
    }

    // Make sure it's still within the border
    if ($scale_and_center) {
        $image["data"] = json_encode(scale_and_center(json_decode($image["data"], true), true));
    }

    // Calculate path for fabric.js
    $image["path"] = get_path($image["data"]);

    // Draw points
    $points = array();
    if ($show_points) {
        $pointlist = json_decode($image["data"], true);
        if (count_points($pointlist) > 500) {
            $msg[] = array("class" => "alert-warning",
                       "text" => "This symbol has many points (".
                                 count_points($pointlist)."> 500). ".
                                 "Although they can easily be calculated, ".
                                 "you should not display them. ".
                                 "To keep your performance, this option ".
                                 "was disabled automatically.");
            $show_points = false;
        } else {
            $data = json_decode($image["data"]);
            foreach ($data as $line) {
                foreach ($line as $point) {
                    $points[] = $point;
                }
            }
        }
    }
} else {
    echo "Specify the raw_data_id you want to use for your experiments.<br/>";
    echo '<a href="?raw_data_id=31">render/?raw_data_id=31</a>';
    exit (0);
}

echo $twig->render('render.twig', array('heading' => 'Render',
                                       'file'=> "render",
                                       'logged_in' => is_logged_in(),
                                       'display_name' => $_SESSION['display_name'],
                                       'msg' => $msg,
                                       'image' => $image,
                                       'points' => json_encode($points),
                                       'show_points' => $show_points,
                                       'scale_and_center' => $scale_and_center,
                                       'douglas_peucker' => $douglas_peucker,
                                       'epsilon' => $epsilon,
                                       'cubic_spline' => $cubic_spline,
                                       'cubic_spline_points' => $cubic_spline_points
                                       )
                  );