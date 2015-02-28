<?php
include '../init.php';
require_once '../classification.php';
require_once '../svg.php';
require_once 'functions.php';

$raw_data_id = "";

if (!is_logged_in()) {
    header("Location: ../login");
}


$formula_ids = array();

if (isset($_POST['drawnJSON'])) {
    $raw_data_id = insert_userdrawing(get_uid(), $_POST['drawnJSON']);
    if (!($raw_data_id == false)) {
        classify($raw_data_id, $_POST['drawnJSON']);
    }
}

echo $twig->render('classify.twig', array('heading' => 'Classify',
                                       'file'=> "classify",
                                       'logged_in' => is_logged_in(),
                                       'display_name' => $_SESSION['display_name'],
                                       'formula_ids' => $formula_ids,
                                       'raw_data_id' => $raw_data_id,
                                       'msg' => $msg,
                                       'useragentstring' => $_SERVER['HTTP_USER_AGENT']
                                       )
                  );

?>