<?php

function add_classification($user_id, $raw_data_id, $latex, $mode="mathmode", 
                            $packages="") {
    global $pdo;

    // Get formula id if it is already in the database
    $sql = "SELECT `id` FROM `wm_formula` ".
           "WHERE `formula_in_latex` = :latex";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':latex', $latex, PDO::PARAM_STR);
    $stmt->execute();
    $formula_id = $stmt->fetchObject()->id;

    if($formula_id == 0 || $formula_id == null) {
        // it was not in the database. Add it.
        $sql = "INSERT INTO `wm_formula` (".
               "`formula_name`, `formula_in_latex`, `mode`, `package` ".
               ") VALUES (:latex, :latex, :mode, :package);";
        $stmt = $pdo->prepare($sql);
        $latex = trim($latex);

        $stmt->bindParam(':latex', $latex, PDO::PARAM_STR);
        $stmt->bindParam(':mode', $mode, PDO::PARAM_STR);
        $stmt->bindParam(':package', $packages, PDO::PARAM_STR);
        $stmt->execute();
        $formula_id = $pdo->lastInsertId('id');
    }

    $sql = "INSERT INTO `wm_raw_data2formula` (".
           "`raw_data_id` ,".
           "`formula_id` ,".
           "`user_id`".
           ") VALUES (".
           ":raw_data_id, :formula_id, :user_id".
           ");";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':raw_data_id', $raw_data_id, PDO::PARAM_INT);
    $stmt->bindParam(':formula_id', $formula_id, PDO::PARAM_INT);
    $uid = get_uid();
    $stmt->bindParam(':user_id', $uid, PDO::PARAM_INT);
    $stmt->execute();
}

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

?>