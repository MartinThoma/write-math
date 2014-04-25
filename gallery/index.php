<?php
require_once '../vendor/autoload.php';
include '../init.php';

$loader = new Twig_Loader_Filesystem('../templates');
$twig = new Twig_Environment($loader, array(
    'cache' => '../cache',
));

if (!is_logged_in()) {
    header("Location: ../login");
}

if (!($stmt = $mysqli->prepare("SELECT `data`, `creation_date` FROM `wm_raw_draw_data` WHERE `user_id` = ?"))) {
    echo "Prepare failed: (" . $mysqli->errno . ") " . $mysqli->error;
}

if (!$stmt->bind_param("i", get_uid())) {
    echo "Binding parameters failed: (" . $stmt->errno . ") " . $stmt->error;
}

if (!$stmt->execute()) {
    echo "Execute failed: (" . $stmt->errno . ") " . $stmt->error;
} else {

  $stmt -> bind_result($data, $creation_date);
  $userimages = array();

  while ($row = $stmt->fetch()) {
    array_push($userimages, array("image" => $data, "creation_date" => $creation_date));
  }
}

$stmt -> close();

echo $twig->render('gallery.twig', array('heading' => 'Gallery',
                                       'logged_in' => is_logged_in(),
                                       'display_name' => $_SESSION['display_name'],
                                       'file'=> "gallery",
                                       'userimages' => $userimages
                                       )
                  );

?>