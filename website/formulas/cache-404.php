<?php
include '../init.php';
$base = basename($_SERVER['REQUEST_URI'], ".svg");
$a = explode("-", $base);
$formula_id = $a[0];
$rendering_id = $a[1];

$sql = "SELECT svg FROM `wm_renderings` WHERE id=:rid";
$stmt = $pdo->prepare($sql);
$stmt->bindParam(':rid', $rendering_id, PDO::PARAM_INT);
$stmt->execute();
$svg_obj = $stmt->fetchObject();
if ($svg_obj) {
    $svg = $svg_obj->svg;
} else {
    $svg = "";
}


if (strlen($svg) > 50) {
    file_put_contents ("../formulas/$formula_id-$rendering_id.svg", $svg);
    header("Location: ../formulas/$formula_id-$rendering_id.svg");
}
?>