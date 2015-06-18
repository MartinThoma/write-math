<?php
include '../init.php';
include '../svg.php';

if (!is_logged_in()) {
    header("Location: ../login");
}

function get_tag_name() {
    $url = explode("/tags/", $_SERVER['REQUEST_URI']);
    array_shift($url);
    $tag_name = explode("/", $url[0])[0];
    return $tag_name;
}

$tag_name = get_tag_name();

if (strlen($tag_name) > 0) {
    $sql = "SELECT `id`, `tag_name`, `description` ".
           "FROM `wm_tags` WHERE `tag_name`=:tag_name LIMIT 1";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':tag_name', $tag_name, PDO::PARAM_STR);
    $stmt->execute();
    $tag_info = $stmt->fetch();

    // Get all symbols
    $sql = "SELECT * ".
           "FROM `wm_tags2symbols` ".
           "JOIN `wm_formula` ON `wm_formula`.`id` = `symbol_id` ".
           "WHERE `tag_id`=:tag_id ".
           "ORDER BY `unicode_dec`, `variant_of`, `wm_formula`.`id` ASC";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':tag_id', $tag_info['id'], PDO::PARAM_STR);
    $stmt->execute();
    $symbols = $stmt->fetchAll();

    $Parsedown = new Parsedown();
    $tag_info['description'] = $Parsedown->text($tag_info['description']);

    echo $twig->render('tag.twig', array('heading' => 'Tag: '.$tag_name.' ('.count($symbols).' symbols)',
                                         'logged_in' => is_logged_in(),
                                         'display_name' => $_SESSION['display_name'],
                                         'file'=> "tag",
                                         'tag_info' => $tag_info,
                                         'symbols' => $symbols,
                                         )
                      );
} else {
    // Get all tags
    $sql = "SELECT * ".
           "FROM `wm_tags` ".
           "ORDER BY `tag_name` ASC";
    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    $tags = $stmt->fetchAll();
    echo $twig->render('tags_overview.twig',
                       array('heading' => 'Tags ('.count($tags).')',
                             'logged_in' => is_logged_in(),
                             'display_name' => $_SESSION['display_name'],
                             'file'=> "tag",
                             'tags' => $tags,
                                         )
                      );
}


?>