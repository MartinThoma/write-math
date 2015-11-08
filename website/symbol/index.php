<?php
include '../init.php';
require_once 'symbol.functions.php';

$edit_flag = false;
$images = false;

if (!isset($_GET['id'])) {
    header("Location: ?id=1526");
}

if (isset($_GET['delete_reference']) && is_admin()) {
    $sql = "DELETE FROM `wm_formula_in_paper` WHERE `id` = :id LIMIT 1";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':id', $_GET['delete_reference'], PDO::PARAM_INT);
    $stmt->execute();
    $id = intval($_GET['id']);
    header("Location: ?id=".$id);
}

if (isset($_GET['edit'])  && !is_ip_user()) {
    $edit_flag = true;
}

if (isset($_GET['delete']) && is_admin()) {
    $sql = "DELETE FROM `wm_formula` WHERE `id` = :id AND :id > 1556 LIMIT 1";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':id', $_GET['delete'], PDO::PARAM_INT);
    $stmt->execute();
    if ($id > $_GET['delete']) {
        $msg[] = array("class" => "alert-danger",
               "text" => "Symbol was deleted.");
    } else {
        $msg[] = array("class" => "alert-danger",
               "text" => "This block is too dangerous. You have to uncomment"
                        ."it for id<=1556 in symbol/index.php (line 12-19).");
    }
}

if (isset($_POST['id']) && isset($_POST['description']) && !is_ip_user()) {
    $formula_id = $_POST['id'];
    update_symbol_description($formula_id, $_POST['description']);
    if (is_admin()) {
        update_rendering($formula_id, $_POST['svg']);
        update_tags($formula_id, $_POST['tags']);
        $formula_name = trim($_POST['formula_name']);
        $variant_of = trim($_POST['variant_of']);
        if (strlen($variant_of) == 0) {
            $variant_of = NULL;
        }
        $unicode_dec = trim($_POST['unicode_dec']);
        $font = trim($_POST['font']);
        $font_style = trim($_POST['font_style']);
        $formula_type = trim($_POST['formula_type']);
        $svg = trim($_POST['svg']);
        $sql = "UPDATE `wm_formula` SET ".
               "`formula_name` = :formula_name, ".
               "`variant_of` = :variant_of, ".
               "`unicode_dec` = :unicode_dec, ".
               "`font` = :font, ".
               "`font_style` = :font_style, ".
               "`mode` = :mode, ".
               "`formula_type` = :formula_type, ".
               "WHERE `id` = :id;";
        $stmt = $pdo->prepare($sql);
        $stmt->bindParam(':id', $_POST['id'], PDO::PARAM_INT);
        $stmt->bindParam(':formula_name', $formula_name, PDO::PARAM_STR);
        $stmt->bindParam(':variant_of', $variant_of, PDO::PARAM_INT);
        $stmt->bindParam(':unicode_dec', $unicode_dec, PDO::PARAM_INT);
        $stmt->bindParam(':font', $font, PDO::PARAM_STR);
        $stmt->bindParam(':font_style', $font_style, PDO::PARAM_STR);
        $stmt->bindParam(':mode', $_POST['mode'], PDO::PARAM_STR);
        $stmt->bindParam(':formula_type', $formula_type, PDO::PARAM_STR);
        $stmt->execute();
    }
} elseif (isset($_POST['used_by']) && !is_ip_user()) {
    $sql = "INSERT INTO `wm_formula_in_paper` ".
           "(`symbol_id`, `paper`, `inserted_by`, `meaning`) VALUES ".
           "(:sid, :used_by, :uid, :meaning);";
    $stmt = $pdo->prepare($sql);
    $uid = get_uid();
    $stmt->bindParam(':sid', $_POST['id'], PDO::PARAM_INT);
    $stmt->bindParam(':uid', $uid, PDO::PARAM_INT);
    $stmt->bindParam(':used_by', $_POST['used_by'], PDO::PARAM_STR);
    $stmt->bindParam(':meaning', $_POST['meaning'], PDO::PARAM_STR);
    $result = $stmt->execute();
    header("Location: ?id=".$_POST['id']);
}

if (isset($_GET['id'])) {
    $sql = "SELECT `wm_formula`.`id`, `formula_name`, ".
           "`variant_of`, `unicode_dec`, `font`, `font_style`, `description`, ".
           "`formula_in_latex`, `preamble`, ".
           "`mode`, `formula_type`, `best_rendering`, `wm_renderings`.`svg` ".
           "FROM `wm_formula` ".
           "LEFT JOIN `wm_renderings` ON `wm_renderings`.`id`=`best_rendering` ".
           "WHERE `wm_formula`.`id` = :id";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':id', $_GET['id'], PDO::PARAM_INT);
    $stmt->execute();
    $formula = $stmt->fetchObject();

    // Get references
    $sql = "SELECT `id`, `paper`, `meaning` ".
           "FROM `wm_formula_in_paper` ".
           "WHERE `symbol_id` = :id";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':id', $_GET['id'], PDO::PARAM_INT);
    $stmt->execute();
    $references = $stmt->fetchAll();

    $tab = isset($_GET['tab']) ? $_GET['tab'] : "trainingset";
    $is_testset = $tab == "testset";

    // Get total number of elements for pagination
    $sql = "SELECT COUNT(`id`) as counter FROM `wm_raw_draw_data` ".
           "WHERE `accepted_formula_id` = :fid ".
           "AND is_in_testset=:is_in_testset ";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':fid', $_GET['id'], PDO::PARAM_STR);
    $stmt->bindParam(':is_in_testset', $is_testset);
    $stmt->execute();
    $row = $stmt->fetchObject();
    $total = $row->counter;

    // Get all raw data of this user
    $currentPage = isset($_GET['page']) ? intval($_GET['page']) : 1;
    $page_size = 7*4;
    $sql = "SELECT `id`, `data` as `image`, `creation_date` ".
           "FROM `wm_raw_draw_data` ".
           "WHERE `accepted_formula_id` = :fid ".
           "AND is_in_testset=:is_in_testset ".
           "ORDER BY `creation_date` DESC ".
           "LIMIT ".(($currentPage-1)*$page_size).", ".$page_size;
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':fid', $_GET['id'], PDO::PARAM_STR);
    $stmt->bindParam(':is_in_testset', $is_testset);
    $stmt->execute();
    $images = $stmt->fetchAll();

    // Get tags
    $sql = "SELECT  `tag_id` ,  `wm_tags`.`tag_name` ,  `wm_tags`.`description` ".
           "FROM  `wm_tags2symbols` ".
           "JOIN  `wm_tags` ON (  `tag_id` =  `wm_tags`.`id` ) ".
           "WHERE  `symbol_id` = :symbol_id ".
           "ORDER BY `tag_name` ASC";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':symbol_id', $_GET['id'], PDO::PARAM_STR);
    $stmt->execute();
    $tags = $stmt->fetchAll();
} else {
    $msg[] = array("class" => "alert-warning",
                   "text" => "Please set an ID (e.g. <a href=\"../symbol/?id=31\">like this</a>)");
}

if (!$edit_flag) {
    $Parsedown = new Parsedown();
    $formula->description = $Parsedown->text($formula->description);
}

echo $twig->render('symbol.twig', array('heading' => 'Symbol',
                                       'logged_in' => is_logged_in(),
                                       'display_name' => $_SESSION['display_name'],
                                       'uid' => get_uid(),
                                       'file'=> "symbol",
                                       'msg' => $msg,
                                       'formula' => $formula,
                                       'edit_flag' => $edit_flag,
                                       'images' => $images,
                                       'total' => $total,
                                       'pages' => ceil(($total)/$page_size),
                                       'currentPage' => $currentPage,
                                       'tab' => $tab,
                                       'tags' => $tags,
                                       'references' => $references
                                       )
                  );

?>