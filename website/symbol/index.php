<?php
include '../init.php';

$edit_flag = false;

if (isset($_GET['edit'])) {
    $edit_flag = true;
}

if (isset($_GET['delete']) && get_uid() == 10) {
    $sql = "DELETE FROM `wm_formula` WHERE `id` = :id LIMIT 1";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':id', $_GET['delete'], PDO::PARAM_INT);
    $stmt->execute();
    $msg[] = array("class" => "alert-danger",
           "text" => "Symbol was deleted.");
}

if (isset($_POST['id']) && get_uid() == 10) {
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
    $formula_type = trim($_POST['formula_type']);
    $description = trim($_POST['description']);
    $svg = trim($_POST['svg']);

    $sql = "UPDATE `wm_formula` SET ".
           "`formula_name` = :formula_name, ".
           "`description` = :description, ".
           "`mode` = :mode, ".
           "`formula_type` = :formula_type ".
           "WHERE `id` = :id;";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':id', $_POST['id'], PDO::PARAM_INT);
    $stmt->bindParam(':formula_name', $formula_name, PDO::PARAM_STR);
    $stmt->bindParam(':description', $description, PDO::PARAM_STR);
    $stmt->bindParam(':mode', $_POST['mode'], PDO::PARAM_STR);
    $stmt->bindParam(':formula_type', $formula_type, PDO::PARAM_STR);
    $stmt->execute();
}

$sql = "SELECT `wm_formula`.`id`, `formula_name`, `description`, `formula_in_latex`, ".
       "`mode`, `package`, `formula_type`, `best_rendering`, `wm_renderings`.`svg` ".
       "FROM `wm_formula` ".
       "JOIN `wm_renderings` ON `wm_renderings`.`id`=`best_rendering` ".
       "WHERE `wm_formula`.`id` = :id";
$stmt = $pdo->prepare($sql);
$stmt->bindParam(':id', $_GET['id'], PDO::PARAM_INT);
$stmt->execute();
$formula = $stmt->fetchObject();

echo $twig->render('symbol.twig', array('heading' => 'Symbol',
                                       'logged_in' => is_logged_in(),
                                       'display_name' => $_SESSION['display_name'],
                                       'uid' => get_uid(),
                                       'file'=> "symbol",
                                       'msg' => $msg,
                                       'formula' => $formula,
                                       'edit_flag' => $edit_flag
                                       )
                  );

?>