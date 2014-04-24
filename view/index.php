<?php
require_once '../vendor/autoload.php';
include '../init.php';

$loader = new Twig_Loader_Filesystem('../templates');
$twig = new Twig_Environment($loader, array(
    'cache' => '../cache',
));

if (!($stmt = $mysqli->prepare("SELECT `svg` FROM  `wm_symbols` WHERE  `id` = ?;"))) {
    echo "Prepare failed: (" . $mysqli->errno . ") " . $mysqli->error;
    return false;
}

if (!$stmt->bind_param("i", $_GET['id'])) {
    echo "Binding parameters failed: (" . $stmt->errno . ") " . $stmt->error;
    return false;
}

if (!$stmt->execute()) {
    echo "Execute failed: (" . $stmt->errno . ") " . $stmt->error;
    return false;
} else {
  /* Bind results */
  $stmt -> bind_result($svg);

  /* Fetch the value */
  $stmt -> fetch();
}
$stmt->close();
header('Content-type: image/svg+xml');
echo $svg

?>