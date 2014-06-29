<?php
include '../init.php';
include '../svg.php';
include 'functions.php';

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