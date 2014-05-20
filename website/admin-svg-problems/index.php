<?php
require_once '../svg.php';
include '../init.php';

if (!is_logged_in() || get_uid() != 10) {
    header("Location: ../login");
}

$problematic_formuas = "";

if (isset($_GET['is_ok']) && isset($_GET['formula_id'])) {
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

if (isset($_GET['formula_id'])) {
    $sql = "SELECT `id`, `formula_name`, `description`, `mode`, ".
           "`best_rendering` ".
           "FROM  `wm_formula` WHERE  `id` = :id;";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':id', $_GET['formula_id'], PDO::PARAM_INT);
    $stmt->execute();
    $formula = $stmt->fetchObject();
} else {
    $sql = "SELECT `formula_id`, `problem_type` ".
           "FROM `wm_formula_svg_missing`";
    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    $problematic_formulas = $stmt->fetchAll();
}

echo $twig->render('admin-svg-problems.twig', array('heading' => 'SVG Problems',
                                       'file' => "user",
                                       'logged_in' => is_logged_in(),
                                       'display_name' => $_SESSION['display_name'],
                                       'user_id' => $user->id,
                                       'problematic_formulas' => $problematic_formulas,
                                       'formula' => $formula
                                       )
                  );

?>