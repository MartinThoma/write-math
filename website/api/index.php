<?php
include '../init.php';

$tasks = array("list-unclassified", "view-raw-data", "view-formula", "delete");

if (!isset($_GET['task']) || !in_array($_GET['task'], $tasks)) {
    echo "You have to provide a valid task. Valid tasks are: ";
    echo "<ul>";
    foreach ($tasks as $task) {
        echo "<li><a href=\"?task=$task\">$task</a></li>";
    }
    echo "</ul>";
    exit (-1);
}

if ($_GET['task'] == "list-unclassified") {
    $sql = "SELECT `id` FROM `wm_raw_draw_data` WHERE `accepted_formula_id` IS NULL";
    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    $unclassified = $stmt->fetchAll(PDO::FETCH_COLUMN);
    echo json_encode($unclassified);
} elseif ($_GET['task'] == "view-raw-data") {
    if (!isset($_GET['id'])) {
        echo "You have to specify an id. Some of the valid ids are:";
        $sql = "SELECT `id` FROM `wm_raw_draw_data` LIMIT 0, 7";
        $stmt = $pdo->prepare($sql);
        $stmt->execute();
        $ids = $stmt->fetchAll(PDO::FETCH_COLUMN);
        foreach ($ids as $id) {
            $url = "?task=view-raw-data&id=$id";
            echo "<li><a href=\"$url\">$url</a></li>";
        }
        exit(-1);
    }

    $formats = array("svg", "path", "pointlist");
    if (!isset($_GET['format']) || !in_array($_GET['format'], $formats)) {
        echo "<p>You have to note which format you want to see.</p>";
        echo "<p>Valid formats are:</p>";
        echo "<ul>";
        foreach ($formats as $format) {
            $url = "?task=view-raw-data&id=".$_GET['id']."&format=$format";
            echo "<li><a href=\"$url\">$format</a></li>";
        }
        echo "</ul>";
        exit (-1);
    }

    if ($_GET['format'] == "pointlist") {
        $sql = "SELECT `data` FROM `wm_raw_draw_data` WHERE `id` = :id";
        $stmt = $pdo->prepare($sql);
        $stmt->bindParam(':id', $_GET['id'], PDO::PARAM_INT);
        $stmt->execute();
        $row = $stmt->fetchObject();
        echo $row->data;
    } else {
        echo "Format not implemented yet.";
    }
} else {
    echo "Task is not implemented yet.";
}

?>