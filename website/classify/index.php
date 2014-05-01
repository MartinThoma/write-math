<?php
include '../init.php';

if (!is_logged_in()) {
    header("Location: ../login");
}

function insert_userdrawing($user_id, $data) {
    global $pdo;

    $sql = "INSERT INTO `wm_raw_draw_data` (".
           "`user_id` ,".
           "`data` ,".
           "`creation_date` ,".
           "`accepted_formula_id`".
           ") VALUES (:user_id, :data, CURRENT_TIMESTAMP , NULL);";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':user_id', get_uid(), PDO::PARAM_INT);
    $stmt->bindParam(':data', $data, PDO::PARAM_STR);
    $stmt->execute();

    return $pdo->lastInsertId();
}

$formula_ids = array();

if (isset($_POST['drawnJSON'])) {
    insert_userdrawing(get_uid(), $_POST['drawnJSON']);
}

echo $twig->render('classify.twig', array('heading' => 'Classify',
                                       'file'=> "classify",
                                       'logged_in' => is_logged_in(),
                                       'display_name' => $_SESSION['display_name'],
                                       'formula_id' => $_GET['formula_id'],
                                       'formula_ids' => $formula_ids
                                       )
                  );

?>