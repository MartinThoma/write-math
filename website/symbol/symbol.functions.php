<?php

function update_symbol_description($symbol_id, $description) {
    global $pdo;
    global $msg;
    $description = trim($description);

    // Get current revision from `wm_formula`
    $sql = "SELECT `id`, `user_id`, `description`, `for_timestamp` ".
           "FROM `wm_formula` ".
           "WHERE `wm_formula`.`id` = :id LIMIT 1";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':id', $symbol_id, PDO::PARAM_INT);
    $stmt->execute();
    $symbol = $stmt->fetchObject();

    // Put current revision into `wm_formula_old`
    $sql = "INSERT INTO `wm_formula_old` ( ".
           "`formula_id` , ".
           "`description` , ".
           "`user_id` , ".
           "`for_timestamp` ".
           ") VALUES ( ".
           ":symbol_id, :description, :user_id, :timestamp);";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':symbol_id', $symbol->id, PDO::PARAM_INT);
    $stmt->bindParam(':user_id', $symbol->user_id, PDO::PARAM_INT);
    $stmt->bindParam(':description', $symbol->description, PDO::PARAM_STR);
    $stmt->bindParam(':timestamp', $symbol->for_timestamp, PDO::PARAM_STR);
    $stmt->execute();

    // Update current revision
    $sql = "UPDATE `wm_formula` ".
           "SET  `description` = :description, ".
           "`user_id` = :user_id ".
           "WHERE  `wm_formula`.`id` = :symbol_id ".
           "LIMIT 1";
    $uid = get_uid();
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':symbol_id', $symbol_id, PDO::PARAM_INT);
    $stmt->bindParam(':description', $description, PDO::PARAM_STR);
    $stmt->bindParam(':user_id', $uid, PDO::PARAM_INT);
    $stmt->execute();
}

function update_rendering($formula_id, $svg_posted) {
    global $pdo;
    global $msg;
    $sql = "SELECT `wm_renderings`.`svg` ".
           "FROM `wm_formula` ".
           "JOIN `wm_renderings` ON `best_rendering` = `wm_renderings`.`id` ".
           "WHERE `wm_formula`.`id` = :id";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':id', $formula_id, PDO::PARAM_INT);
    $stmt->execute();
    $svg_db = $stmt->fetchObject()->svg;
    $svg_new = trim($svg_posted);
    if ($svg_new != $svg_db) {
        # TODO: Check validity of SVG
        # Insert svg to wm_renderings
        $sql = "INSERT INTO `wm_renderings` (".
               "`formula_id` ,".
               "`user_id` ,".
               "`creation_time` ,".
               "`svg` ".
               ") ".
               "VALUES (:fid, :uid, CURRENT_TIMESTAMP , :svg)";
        $stmt = $pdo->prepare($sql);
        $stmt->bindParam(':fid', $formula_id, PDO::PARAM_INT);
        $uid = get_uid();
        $stmt->bindParam(':uid', $uid, PDO::PARAM_INT);
        $stmt->bindParam(':svg', $svg_new, PDO::PARAM_INT);
        $stmt->execute();
        $rendering_id = $pdo->lastInsertId('id');
        # create svg file
        $return = file_put_contents ("../formulas/$formula_id-$rendering_id.svg", $svg_new);

        if ($return === false) {
            $msg[] = array("class" => "alert-danger",
                   "text" => "Writing was not successful.");
        } else {
            $msg[] = array("class" => "alert-success",
                   "text" => "../formulas/$formula_id-$rendering_id.svg was ".
                             "written successfully");
        }

        # adjust best rendering id
        $sql = "UPDATE `wm_formula` ".
               "SET  `best_rendering` = :rid WHERE `wm_formula`.`id` = :fid;";
        $stmt = $pdo->prepare($sql);
        $stmt->bindParam(':fid', $formula_id, PDO::PARAM_INT);
        $stmt->bindParam(':rid', $rendering_id, PDO::PARAM_INT);
        $stmt->execute();
    }
}


function update_tags($formula_id, $tags_posted) {
    global $pdo;
    global $msg;
    // Delete all previous tags
    $sql = "DELETE FROM `wm_tags2symbols` WHERE `symbol_id` = :symbol_id";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':symbol_id', $formula_id, PDO::PARAM_INT);
    $stmt->execute();

    // Add new tags
    $tags_new = array_unique(explode(" ", $tags_posted));
    // Get a list of all tags
    $sql = "SELECT `id`, `tag_name` FROM  `wm_tags` ";
    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    $tag_list_complete = $stmt->fetchAll();
    $tags_to_id = array();
    foreach ($tag_list_complete as $tag) {
        $tags_to_id[$tag['tag_name']] = $tag['id'];
    }

    foreach ($tags_new as $tag) {
        if (array_key_exists($tag, $tags_to_id)) {
            $sql = "INSERT INTO `wm_tags2symbols` (`tag_id` ,`symbol_id`) ".
                   "VALUES (:tag_id, :symbol_id);";
            $stmt = $pdo->prepare($sql);
            $stmt->bindParam(':tag_id', $tags_to_id[$tag], PDO::PARAM_INT);
            $stmt->bindParam(':symbol_id', $formula_id, PDO::PARAM_INT);
            $stmt->execute();
        }
    }
}

?>