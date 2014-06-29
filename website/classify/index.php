<?php
include '../init.php';
require_once '../classification.php';
require_once '../svg.php';
require_once 'functions.php';

$raw_data_id = "";

if (!is_logged_in()) {
    header("Location: ../login");
}

# solution for < PHP 5.5.0
if (!function_exists('json_last_error_msg')) {
    function json_last_error_msg() {
        switch (json_last_error()) {
            default:
                return;
            case JSON_ERROR_DEPTH:
                $error = 'Maximum stack depth exceeded';
            break;
            case JSON_ERROR_STATE_MISMATCH:
                $error = 'Underflow or the modes mismatch';
            break;
            case JSON_ERROR_CTRL_CHAR:
                $error = 'Unexpected control character found';
            break;
            case JSON_ERROR_SYNTAX:
                $error = 'Syntax error, malformed JSON';
            break;
            case JSON_ERROR_UTF8:
                $error = 'Malformed UTF-8 characters, possibly incorrectly encoded';
            break;
        }
        return $error;
    }
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