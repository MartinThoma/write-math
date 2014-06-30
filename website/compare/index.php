<?php
require_once '../svg.php';
require_once '../init.php';
require_once '../preprocessing.php';
require_once '../classification.php';

$epsilon = 0;
$dtw_distance = 0;
$pathA = null;
$pathB = null;

if (!is_logged_in()) {
    header("Location: ../login");
}

if (!isset($_GET['A']) || !isset($_GET['B'])) {
    $msg[] = array("class" => "alert-warning",
                   "text" => "Please provide 'A' and 'B' with a raw_data_id. ".
                             'e.g. <a href="?A=300&B=306">like this</a> or '.
                             '<a href="?A=300&B=290">like that</a>.');
} else {
    $sql = "SELECT `id`, `data` FROM `wm_raw_draw_data` ".
           "WHERE `id` = :ida OR `id` = :idb";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':ida', $_GET['A'], PDO::PARAM_INT);
    $stmt->bindParam(':idb', $_GET['B'], PDO::PARAM_INT);
    $stmt->execute();
    $data = $stmt->fetchAll(PDO::FETCH_ASSOC);

    $epsilon = isset($_POST['epsilon']) ? $_POST['epsilon'] : 0;
    $A = $data[0]['data'];
    $B = $data[1]['data'];
    $As = scale_and_shift(pointLineList($A));
    $Bs = scale_and_shift(pointLineList($B));
    $dtw_distance = apply_greedy_matching_dtw_linewise($As, $Bs);

    $pathA = get_path($A, $epsilon);
    $pathB = get_path($B, $epsilon);
}



echo $twig->render('compare.twig', array('heading' => 'Compare',
                                         'file'=> 'compare',
                                         'logged_in' => is_logged_in(),
                                         'display_name' => $_SESSION['display_name'],
                                         'msg' => $msg,
                                         'pathA' => $pathA,
                                         'pathB' => $pathB,
                                         'epsilon' => $epsilon,
                                         'dtw_distance' => $dtw_distance
                                       )
                  );

?>