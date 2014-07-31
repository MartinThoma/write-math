<?php
require_once '../svg.php';
include '../init.php';

$problematic_formuas = "";

if (isset($_GET['is_ok']) && isset($_GET['formula_id']) && is_admin()) {
    $sql = "DELETE FROM `wm_formula_svg_missing` ".
           "WHERE `wm_formula_svg_missing`.`formula_id` = :fid";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':fid', $_GET['formula_id'], PDO::PARAM_INT);
    $stmt->execute();

    $sql = "SELECT `formula_id` ".
           "FROM `wm_formula_svg_missing` ORDER BY formula_id";
    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    $id = $stmt->fetchObject()->formula_id;
    $str = "Location: ../admin-svg-problems/?formula_id=$id";
    header($str);
}

$sql = "SELECT `formula_id`, `problem_type` ".
       "FROM `wm_formula_svg_missing`";
$stmt = $pdo->prepare($sql);
$stmt->execute();
$problematic_formulas = $stmt->fetchAll();

echo $twig->render('svg-problems.twig', array('heading' => 'SVG Problems',
                                       'file' => "user",
                                       'logged_in' => is_logged_in(),
                                       'display_name' => $_SESSION['display_name'],
                                       'user_id' => $user->id,
                                       'problematic_formulas' => $problematic_formulas,
                                       'formula' => $formula,
                                       'is_admin' => is_admin()
                                       )
                  );

?>