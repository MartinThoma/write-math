<?php
include '../init.php';

if (!is_logged_in()) {
    header("Location: ../login");
}

function insert_userdrawing($user_id, $data, $formula_id) {
    global $pdo;

    $sql = "INSERT INTO `wm_raw_draw_data` (".
                   "`user_id` ,".
                   "`data` ,".
                   "`creation_date` ,".
                   "`accepted_formula_id`".
                   ") VALUES (:uid, :data, CURRENT_TIMESTAMP , :formula_id);";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':uid', $user_id, PDO::PARAM_INT);
    $stmt->bindParam(':data', $data, PDO::PARAM_STR);
    $stmt->bindParam(':formula_id', $formula_id, PDO::PARAM_INT);
    $stmt->execute();
    return $pdo->lastInsertId;
}

$formula_ids = array();

if (isset($_GET['formula_id'])) {
    $sql = "SELECT `svg` FROM  `wm_formula` WHERE  `id` = :id;";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':id', $_GET['formula_id'], PDO::PARAM_INT);
    $stmt->execute();
    $svg = $stmt->fetchObject()->svg;
} else {
    $sql = "SELECT `id` ,  `formula_name` FROM `wm_formula`";
    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    $formula_ids = $stmt->fetchAll();
}

if (isset($_POST['formula_id'])) {
    insert_userdrawing(get_uid(), $_POST['drawnJSON'], $_POST['formula_id']);
}

echo $twig->render('train.twig', array('heading' => 'Train',
                                       'logged_in' => is_logged_in(),
                                       'display_name' => $_SESSION['display_name'],
                                       'file'=> "train",
                                       'formula_id' => $_GET['formula_id'],
                                       'formula_ids' => $formula_ids
                                       )
                  );

?>