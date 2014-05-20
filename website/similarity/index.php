<?php
include '../init.php';

if (isset($_POST['base_symbol_id'])) {
    $sql = "INSERT INTO `wm_similarity` (".
           "`base_symbol` , ".
           "`similar_symbol` , ".
           "`comment_choice` ".
           ") VALUES (:base_symbol, :similar_symbol, :comment);";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':base_symbol', $_POST['base_symbol_id'], PDO::PARAM_INT);
    $stmt->bindParam(':similar_symbol', $_POST['similar_symbol_id'], PDO::PARAM_INT);
    $stmt->bindParam(':comment', $_POST['description'], PDO::PARAM_STR);
    $stmt->execute();
}

$sql = "SELECT `base_symbol`, `similar_symbol`, `comment_choice` ".
       "FROM `wm_similarity` ".
       "ORDER BY `base_symbol` ASC";
$stmt = $pdo->prepare($sql);
$stmt->execute();
$symbols = $stmt->fetchAll();

echo $twig->render('similarity.twig', array('heading' => 'Symbol similarity',
                                       'file'=> "similarity",
                                       'logged_in' => is_logged_in(),
                                       'display_name' => $_SESSION['display_name'],
                                       'msg' => $msg,
                                       'symbols' => $symbols
                                       )
                  );