<?php
include '../init.php';
include '../svg.php';

if (!is_logged_in()) {
    header("Location: ../login");
}

if (isset($_GET['details'])) {
    $sql = "SELECT `id`, `name`, `topology`, `parent`, `testresult`, ".
           "`preprocessing`, `features`, `training`, `details` ".
           "FROM `wm_models` WHERE `id` = :mid";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':mid', $_GET['details'], PDO::PARAM_INT);
    $stmt->execute();
    $model_detailed = $stmt->fetchObject();
} else {
    // Get all raw data of this user
    $currentPage = isset($_GET['page']) ? intval($_GET['page']) : 1;
    $sql = "SELECT `id`, `name`, `topology`, `parent`, `testresult` ".
           "FROM `wm_models`";
    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    $models = $stmt->fetchAll();
}

echo $twig->render('models.twig', array('heading' => 'Models',
                                         'logged_in' => is_logged_in(),
                                         'display_name' => $_SESSION['display_name'],
                                         'file'=> "models",
                                         'models' => $models,
                                         'model_detailed' => $model_detailed
                                        )
                  );

?>