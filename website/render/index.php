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
    $scale_and_shift = isset($_GET["scale_and_shift"]) && $_GET["scale_and_shift"] == "on";
    $cubic_spline = isset($_GET["cubic_spline"]) && $_GET["cubic_spline"] == "on";
    $douglas_peucker = isset($_GET["douglas_peucker"]) && $_GET["douglas_peucker"] == "on";
    $dot_reduction = isset($_GET["dot_reduction"]) && $_GET["dot_reduction"] == "on";
    $dehooking = isset($_GET["dehooking"]) && $_GET["dehooking"] == "on";
    $minimum_time_delay_filter = isset($_GET["minimum_time_delay_filter"]) && $_GET["minimum_time_delay_filter"] == "on";
    $dot_reduction_threshold = isset($_GET['dot_reduction_threshold']) ? $_GET['dot_reduction_threshold'] : 0.2;
    $dehooking_threshold = isset($_GET['dehooking_threshold']) ? $_GET['dehooking_threshold'] : 20;
    $minimum_time_delay_filter_constant = isset($_GET['minimum_time_delay_filter_constant']) ? $_GET['minimum_time_delay_filter_constant'] : 10;
    $show_raw = isset($_GET["show_raw"]) && $_GET["show_raw"] == "on";
    $smoothing_applications = isset($_GET['smoothing_applications']) ? $_GET['smoothing_applications'] : 1;
    if ($smoothing_applications > 30) {
        $smoothing_applications = 30;
    } elseif ($smoothing_applications < 0) {
        $smoothing_applications = 0;
    }
    $smooth1 = isset($_GET['smooth1']) ? $_GET['smooth1'] : 0;
    $smooth2 = isset($_GET['smooth2']) ? $_GET['smooth2'] : 1;
    $smooth3 = isset($_GET['smooth3']) ? $_GET['smooth3'] : 0;
    $theta = array($smooth1, $smooth2, $smooth3);

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

    if ($scale_and_shift) {
        $image["data"] = json_encode(scale_and_shift(json_decode($image["data"], true),
                                                     true,
                                                     390)
                                    );
    }

    // Dot reduction
    if ($dot_reduction) {
        $pointlist = dot_reduction(json_decode($image["data"], true),
                                   $dot_reduction_threshold);
        $image["data"] = json_encode($pointlist);
    }

    // Dehooking
    if ($dehooking) {
        $pointlist = dehook_symbol(json_decode($image["data"], true),
                                   $dehooking_threshold);
        $image["data"] = json_encode($pointlist);
    }

    // Minimum time delay filter
    if ($minimum_time_delay_filter) {
        $pointlist = minimum_time_delay_filter(json_decode($image["data"], true),
                                               $minimum_time_delay_filter_constant);
        $image["data"] = json_encode($pointlist);
    }

    // apply weighted moving average
    for ($i=0; $i < $smoothing_applications; $i++) { 
        $pointlist = weighted_average_smoothing(json_decode($image["data"], true),
                                                $theta);
        $image["data"] = json_encode($pointlist);
    }


    // Douglas Peucker
    if ($douglas_peucker) {
        $pointlist = apply_linewise_douglas_peucker(json_decode($image["data"], true), $epsilon);
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
    if ($scale_and_shift) {
        $image["data"] = json_encode(scale_and_shift(json_decode($image["data"], true),
                                                     true,
                                                     390)
                                    );
    }

    // Calculate path for fabric.js
    $image["path"] = get_path($image["data"]);
    $dots = get_dots($image["data"]);

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

echo $twig->render('render.twig', array('heading' => 'Interactive Preprocessing Experiments',
                                       'file'=> "render",
                                       'logged_in' => is_logged_in(),
                                       'display_name' => $_SESSION['display_name'],
                                       'msg' => $msg,
                                       'image' => $image,
                                       'dots' => $dots,
                                       'points' => json_encode($points),
                                       'show_points' => $show_points,
                                       'scale_and_shift' => $scale_and_shift,
                                       'douglas_peucker' => $douglas_peucker,
                                       'epsilon' => $epsilon,
                                       'cubic_spline' => $cubic_spline,
                                       'cubic_spline_points' => $cubic_spline_points,
                                       'smooth1' => $smooth1,
                                       'smooth2' => $smooth2,
                                       'smooth3' => $smooth3,
                                       'show_raw' => $show_raw,
                                       'dot_reduction' => $dot_reduction,
                                       'dot_reduction_threshold' => $dot_reduction_threshold,
                                       'minimum_time_delay_filter' => $minimum_time_delay_filter,
                                       'minimum_time_delay_filter_constant' => $minimum_time_delay_filter_constant,
                                       'dehooking' => $dehooking,
                                       'dehooking_threshold' => $dehooking_threshold,
                                       'smoothing_applications' => $smoothing_applications
                                       )
                  );