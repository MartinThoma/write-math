<?php
include '../init.php';
require_once '../classification.php';
require_once '../svg.php';

$raw_data_id = "";

if (!is_logged_in()) {
    header("Location: ../login");
}

echo $twig->render('classify-segment.twig', array('heading' => 'Classify with Segmentation',
                                       'file'=> "classify",
                                       'logged_in' => is_logged_in(),
                                       'display_name' => $_SESSION['display_name'],
                                       'msg' => $msg
                                       )
                  );

?>