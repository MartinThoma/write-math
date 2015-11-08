<?php

require_once('../latex.php');

function endsWith($haystack, $needle) {
    return $needle === "" || substr($haystack, -strlen($needle)) === $needle;
}

function getPackageTags() {
    global $pdo;
    $sql = "SELECT `id`, `tag_name`, `is_package` FROM `wm_tags`";
    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    $tags = $stmt->fetchAll();
    $tagsById = array();
    foreach ($tags as $tag) {
        $tagsById[$tag['id']] = array("tag_name" => $tag['tag_name'],
                                      "is_package" => $tag['is_package']);
    }
    return $tagsById;
}

function addTagIds($answers, $tagsById) {
    global $pdo;
    for($i = 0; $i < count($answers); $i++) {
        $symbol_id = $answers[$i]['symbol_id'];
        $answers[$i]['tag_ids'] = array();
        $answers[$i]['packages'] = array();
        // Get tag IDs of this answer
        $sql = "SELECT  `tag_id` ".
               "FROM  `wm_tags2symbols` ".
               "WHERE  `symbol_id` = :symbol_id";
        $stmt = $pdo->prepare($sql);
        $stmt->bindParam(':symbol_id', $symbol_id, PDO::PARAM_INT);
        $stmt->execute();
        $tag_ids = $stmt->fetchAll();
        foreach ($tag_ids as $key => $value) {
            $answers[$i]['tag_ids'][] = $tagsById[$value['tag_id']];
            if ($tagsById[$value['tag_id']]['is_package']) {
                $answers[$i]['packages'][] = $tagsById[$value['tag_id']]['tag_name'];
            }
        }
    }
    return $answers;
}

?>