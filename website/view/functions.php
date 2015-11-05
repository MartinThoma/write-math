<?php

require_once('../latex.php');

function remove_usepackage($package) {
    if (0 === strpos($package, '\usepackage{') && substr($package, -1) == '}') {
        $package = substr($package, strlen('\usepackage{'));
        $package = rtrim($package, '}');
    }
    return $package;
}

function sanitize_packages($packages) {
    if (strpos($packages, ';') !== false) {
        $packages = explode(';', $packages);
    } else {
        $packages = array($packages);
    }

    $packages = array_map(trim, $packages);
    $packages = array_map(remove_usepackage, $packages);

    return $packages;
}

function endsWith($haystack, $needle) {
    return $needle === "" || substr($haystack, -strlen($needle)) === $needle;
}

function annotate_wildpoints($raw_data_id) {
    // Get number of dots in image and get expected number of WILDPOINTs
    # Get raw data
    $sql = "SELECT `data`, `wild_point_count` ".
           "FROM `wm_raw_draw_data` ".
           "WHERE `id` = :id";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':id', $raw_data_id, PDO::PARAM_INT);
    $stmt->execute();
    $image_data = $stmt->fetchObject();
    $wild_point_count = $image_data->wild_point_count;
    # Get list of stroke indices for strokes which are dots
    $raw_data = $image_data->data;
    # TODO: if ($wild_point_count == count($wild_point_indices)) {submit wildpoints to db}

}

?>