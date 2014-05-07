<?php
include '../init.php';

$sql = "SELECT `svg` FROM  `wm_formula` WHERE  `id` = :id;";
$stmt = $pdo->prepare($sql);
$stmt->bindParam(':id', $_GET['id'], PDO::PARAM_INT);
$stmt->execute();
$svg = $stmt->fetchObject();

if (empty($svg)) {
    // TODO: is there a better way?
    echo "empty";
} else {
    $svg = $svg->svg;
}

if ($svg == "") {
	// TODO
    echo "oh";
} else {
    header('Content-type: image/svg+xml');
    echo $svg;
}
?>