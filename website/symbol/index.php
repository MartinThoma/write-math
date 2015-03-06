<?php
include '../init.php';

$edit_flag = false;
$images = false;

if (!isset($_GET['id'])) {
    header("Location: ?id=1526");
}

if (isset($_GET['edit'])) {
    $edit_flag = true;
}

if (isset($_GET['delete']) && is_admin()) {
    $sql = "DELETE FROM `wm_formula` WHERE `id` = :id AND :id > 1556 LIMIT 1";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':id', $_GET['delete'], PDO::PARAM_INT);
    $stmt->execute();
    $msg[] = array("class" => "alert-danger",
           "text" => "Symbol was deleted.");
    $msg[] = array("class" => "alert-danger",
           "text" => "This block is too dangerous. You have to uncomment"
                    ."it in symbol/index.php (line 12-19).");
}

if (isset($_POST['id']) && is_admin()) {
    $formula_id = $_POST['id'];
    $sql = "SELECT `wm_renderings`.`svg` ".
           "FROM `wm_formula` ".
           "JOIN `wm_renderings` ON `best_rendering` = `wm_renderings`.`id` ".
           "WHERE `wm_formula`.`id` = :id";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':id', $formula_id, PDO::PARAM_INT);
    $stmt->execute();
    $svg_db = $stmt->fetchObject()->svg;
    $svg_new = trim($_POST['svg']);
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

    $formula_name = trim($_POST['formula_name']);
    $unicode_dec = trim($_POST['unicode_dec']);
    $font = trim($_POST['font']);
    $font_style = trim($_POST['font_style']);
    $formula_type = trim($_POST['formula_type']);
    $description = trim($_POST['description']);
    $packages = trim($_POST['packages']);
    $svg = trim($_POST['svg']);

    $sql = "UPDATE `wm_formula` SET ".
           "`formula_name` = :formula_name, ".
           "`unicode_dec` = :unicode_dec, ".
           "`font` = :font, ".
           "`font_style` = :font_style, ".
           "`description` = :description, ".
           "`mode` = :mode, ".
           "`formula_type` = :formula_type, ".
           "`package` = :packages ".
           "WHERE `id` = :id;";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':id', $_POST['id'], PDO::PARAM_INT);
    $stmt->bindParam(':formula_name', $formula_name, PDO::PARAM_STR);
    $stmt->bindParam(':unicode_dec', $unicode_dec, PDO::PARAM_INT);
    $stmt->bindParam(':font', $font, PDO::PARAM_STR);
    $stmt->bindParam(':font_style', $font_style, PDO::PARAM_STR);
    $stmt->bindParam(':description', $description, PDO::PARAM_STR);
    $stmt->bindParam(':mode', $_POST['mode'], PDO::PARAM_STR);
    $stmt->bindParam(':formula_type', $formula_type, PDO::PARAM_STR);
    $stmt->bindParam(':packages', $packages, PDO::PARAM_STR);
    $stmt->execute();
}

if (isset($_GET['id'])) {
    $sql = "SELECT `wm_formula`.`id`, `formula_name`, ".
           "`unicode_dec`, `font`, `font_style`, `description`, ".
           "`formula_in_latex`, `preamble`, ".
           "`mode`, `package`, `formula_type`, `best_rendering`, `wm_renderings`.`svg` ".
           "FROM `wm_formula` ".
           "LEFT JOIN `wm_renderings` ON `wm_renderings`.`id`=`best_rendering` ".
           "WHERE `wm_formula`.`id` = :id";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':id', $_GET['id'], PDO::PARAM_INT);
    $stmt->execute();
    $formula = $stmt->fetchObject();

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
                                       'pages' => floor(($total)/$page_size),
                                       'currentPage' => $currentPage,
                                       'tab' => $tab
                                       )
                  );

?>