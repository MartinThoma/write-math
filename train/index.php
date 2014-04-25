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

function insert_userdrawing($user_id, $data, $formula_id) {
    global $mysqli;

    if (!($stmt = $mysqli->prepare("INSERT INTO  `write-math`.`wm_raw_draw_data` (".
                                   "`user_id` ,".
                                   "`data` ,".
                                   "`creation_date` ,".
                                   "`accepted_formula_id`".
                                   ") VALUES (?, ?, CURRENT_TIMESTAMP , ?);"
                                   )
          )
       ) {
        echo "Prepare failed: (" . $mysqli->errno . ") " . $mysqli->error;
    }

    if (!$stmt->bind_param("isi", $user_id, $data, $formula_id)) {
        echo "Binding parameters failed: (" . $stmt->errno . ") " . $stmt->error;
        return 0;
    }

    if (!$stmt->execute()) {
        echo "Execute failed: (" . $stmt->errno . ") " . $stmt->error;
        return 0;
    }
    return $mysqli->insert_id;
}

if (!($stmt = $mysqli->prepare("SELECT `svg` FROM  `wm_symbols` WHERE  `id` = ?;"))) {
    echo "Prepare failed: (" . $mysqli->errno . ") " . $mysqli->error;
}

if (!$stmt->bind_param("i", $_GET['symbol_id'])) {
    echo "Binding parameters failed: (" . $stmt->errno . ") " . $stmt->error;
}

if (!$stmt->execute()) {
    echo "Execute failed: (" . $stmt->errno . ") " . $stmt->error;
} else {
  /* Bind results */
  $stmt -> bind_result($svg);

  /* Fetch the value */
  $stmt -> fetch();
}
//$stmt->close();

if (isset($_POST['formula_id'])) {
    insert_userdrawing(get_uid(), $_POST['drawnJSON'], $_POST['formula_id']);
}

echo $twig->render('train.twig', array('heading' => 'Train',
                                       'logged_in' => is_logged_in(),
                                       'display_name' => $_SESSION['display_name'],
                                       'file'=> "train",
                                       'symbol_id' => $_GET['formula_id'],
                                       'formula_id' => $_GET['formula_id']
                                       )
                  );

?>