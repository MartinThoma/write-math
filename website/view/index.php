<?php
require_once '../vendor/autoload.php';
require_once '../svg.php';
include '../init.php';

$loader = new Twig_Loader_Filesystem('../templates');
$twig = new Twig_Environment($loader, array(
    'cache' => '../cache',
));

if (isset($_GET['id'])) {
    if (!($stmt = $mysqli->prepare("SELECT `user_id`, `data`, `creation_date`, ".
                                   "`accepted_formula_id` ".
                                   "FROM `wm_raw_draw_data` WHERE `id` = ?"))) {
        echo "Prepare failed: (" . $mysqli->errno . ") " . $mysqli->error;
    }

    if (!$stmt->bind_param("i", $_GET['id'])) {
        echo "Binding parameters failed: (" . $stmt->errno . ") " . $stmt->error;
    }

    if (!$stmt->execute()) {
        echo "Execute failed: (" . $stmt->errno . ") " . $stmt->error;
    } else {
        $stmt->bind_result($user_id, $data, $creation_date, $accepted_formula_id);
        $stmt->fetch();
    }

    $stmt -> close();
}

echo $twig->render('view.twig', array('heading' => 'View',
                                       'logged_in' => is_logged_in(),
                                       'display_name' => $_SESSION['display_name'],
                                       'file' => "view",
                                       'path' => get_path($data),
                                       'user_id' => $user_id,
                                       'creation_date' => $creation_date,
                                       'accepted_formula_id' => $accepted_formula_id
                                       )
                  );

?>