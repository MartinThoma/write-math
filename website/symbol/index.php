<?php
include '../init.php';

$edit_flag = false;

if (isset($_GET['edit'])) {
    $edit_flag = true;
}

if (isset($_POST['id']) && get_uid() == 10) {
    $sql = "UPDATE `wm_formula` SET ".
           "`formula_name` = :formula_name, ".
           "`description` = :description, ".
           "`mode` = :mode, ".
           "`svg` = :svg, ".
           "`formula_type` = :formula_type ".
           "WHERE `id` = :id;";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':id', $_POST['id'], PDO::PARAM_INT);#
    $stmt->bindParam(':formula_name', trim($_POST['formula_name']), PDO::PARAM_STR);
    $stmt->bindParam(':description', trim($_POST['description']), PDO::PARAM_STR);
    $stmt->bindParam(':mode', $_POST['mode'], PDO::PARAM_STR);
    $stmt->bindParam(':svg', trim($_POST['svg']), PDO::PARAM_STR);
    $stmt->bindParam(':formula_type', trim($_POST['formula_type']), PDO::PARAM_STR);
    $stmt->execute();
}

$sql = "SELECT `id`, `formula_name`, `description`, `formula_in_latex`, ".
       "`mode`, `package`, `formula_type`, `svg` ".
       "FROM `wm_formula` WHERE `id` = :id";
$stmt = $pdo->prepare($sql);
$stmt->bindParam(':id', $_GET['id'], PDO::PARAM_INT);
$stmt->execute();
$formula = $stmt->fetchObject();

echo $twig->render('symbol.twig', array('heading' => 'Symbol',
                                       'logged_in' => is_logged_in(),
                                       'display_name' => $_SESSION['display_name'],
                                       'file'=> "symbol",
                                       'msg' => $msg,
                                       'formula' => $formula,
                                       'edit_flag' => $edit_flag
                                       )
                  );

?>