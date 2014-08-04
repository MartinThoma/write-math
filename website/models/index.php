<?php
include '../init.php';
include '../svg.php';

if (!is_logged_in()) {
    header("Location: ../login");
}

if (isset($_GET['create_new_model']) && is_admin()) {
    $name = $_GET['name'];
    $sql = "INSERT INTO `wm_models` (`name` , `topology` , ".
           "`details`, `parent`) ".
           "VALUES (:name, :topology, :details, :parent);";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':name', $_POST['name'], PDO::PARAM_STR);
    $stmt->bindParam(':topology', $_POST['topology'], PDO::PARAM_STR);
    $stmt->bindParam(':details', $_POST['details'], PDO::PARAM_STR);
    if ($_POST['parent'] == "") {
        $stmt->bindParam(':parent', NULL, PDO::PARAM_STR);
    } else {
        $stmt->bindParam(':parent', $_POST['parent'], PDO::PARAM_STR);
    }
    $stmt->execute();
} elseif (isset($_POST['id']) && is_admin()) {
    $sql = "UPDATE `wm_models` SET  ".
           "`name` = :name, ".
           "`topology` = :topology, ".
           "`testresult` = :testresult, ".
           "`preprocessing` = :preprocessing, ".
           "`features` = :features, ".
           "`training` = :training, ".
           "`details` = :details ".
           "WHERE  `wm_models`.`id` = :id;";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':name', $_POST['name'], PDO::PARAM_STR);
    $stmt->bindParam(':topology', $_POST['topology'], PDO::PARAM_STR);
    $stmt->bindParam(':testresult', $_POST['testresult'], PDO::PARAM_STR);
    $stmt->bindParam(':preprocessing', $_POST['preprocessing'], PDO::PARAM_STR);
    $stmt->bindParam(':features', $_POST['features'], PDO::PARAM_STR);
    $stmt->bindParam(':training', $_POST['training'], PDO::PARAM_STR);
    $stmt->bindParam(':testresult', $_POST['testresult'], PDO::PARAM_STR);
    $stmt->bindParam(':details', $_POST['details'], PDO::PARAM_STR);
    $stmt->bindParam(':id', $_POST['id'], PDO::PARAM_STR);
    $stmt->execute();
}

if (isset($_GET['details'])) {
    $sql = "SELECT `id`, `name`, `topology`, `parent`, `testresult`, ".
           "`preprocessing`, `features`, `training`, `details` ".
           "FROM `wm_models` WHERE `id` = :mid";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':mid', $_GET['details'], PDO::PARAM_INT);
    $stmt->execute();
    $model_detailed = $stmt->fetchObject();
}

// Get all models
$currentPage = isset($_GET['page']) ? intval($_GET['page']) : 1;
$sql = "SELECT `id`, `name`, `topology`, `parent`, `testresult` ".
       "FROM `wm_models`";
$stmt = $pdo->prepare($sql);
$stmt->execute();
$models = $stmt->fetchAll();

echo $twig->render('models.twig', array('heading' => 'Models',
                                         'logged_in' => is_logged_in(),
                                         'uid' => $_SESSION['uid'],
                                         'display_name' => $_SESSION['display_name'],
                                         'file'=> "models",
                                         'models' => $models,
                                         'model_detailed' => $model_detailed
                                        )
                  );

?>