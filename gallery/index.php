<?php
require_once '../vendor/autoload.php';
include '../init.php';

$loader = new Twig_Loader_Filesystem('../templates');
$twig = new Twig_Environment($loader, array(
    'cache' => '../cache',
));

if (!($stmt = $mysqli->prepare("SELECT `data`, `creation_date` FROM `wm_raw_draw_data` WHERE `user_id` = ?"))) {
    echo "Prepare failed: (" . $mysqli->errno . ") " . $mysqli->error;
}


// TODO: Here is an error...
var_dump(get_uid());

if (!$stmt->bind_param("i", get_uid())) {
    echo "Binding parameters failed: (" . $stmt->errno . ") " . $stmt->error;
}

if (!$stmt->execute()) {
    echo "Execute failed: (" . $stmt->errno . ") " . $stmt->error;
} else {

echo "fetch";
  /* Fetch the value */
  while ($row = $stmt->fetch()) {
    var_dump($row);
  }

  var_dump($result);
}

$stmt -> close();

echo $twig->render('gallery.twig', array('heading' => 'Gallery',
                                       'logged_in' => is_logged_in(),
                                       'username' => $_SESSION['uname'],
                                       'file'=> "gallery",
                                       'userimages' => $result
                                       )
                  );

?>