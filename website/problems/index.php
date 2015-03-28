<?php
include '../init.php';
include '../svg.php';

if (!is_logged_in()) {
    header("Location: ../login");
}

if (isset($_GET['wild_point_count'])) {
    $r = array();
    $r['min_wild_points']      = intval($_GET['wild_point_count']);
    $r['missing_line']         = intval(isset($_GET['missing_line']) &&
                                        $_GET['missing_line'] == '1');
    $r['has_hook']             = intval(isset($_GET['has_hook']) &&
                                        $_GET['has_hook'] == '1');
    $r['has_too_long_line']    = intval(isset($_GET['has_too_long_line']) &&
                                        $_GET['has_too_long_line'] == '1');
    $r['has_interrupted_line'] = intval(isset($_GET['has_interrupted_line']) &&
                                        $_GET['has_interrupted_line'] == '1');
    $r['other_problem']        = intval(isset($_GET['other_problem']) &&
                                        $_GET['other_problem'] == '1');
    $r['is_image']             = intval(isset($_GET['is_image']) &&
                                        $_GET['is_image'] == '1');
    $where = "WHERE wild_point_count >= ".$r['min_wild_points']." ".
             "AND missing_line >= ".$r['missing_line']." ".
             "AND has_hook >= ".$r['has_hook']." ".
             "AND has_too_long_line >= ".$r['has_too_long_line']." ".
             "AND has_interrupted_line >= ".$r['has_interrupted_line']." ".
             "AND other_problem >= ".$r['other_problem']." ".
             "AND is_image >= ".$r['is_image']." ";
} else {
    $r = array();
    $r['min_wild_points'] = 0;
    $r['missing_line'] = 0;
    $r['has_hook'] = 0;
    $r['has_too_long_line'] = 0;
    $r['has_interrupted_line'] = 0;
    $r['other_problem'] = 0;
    $r['is_image'] = 0;
}

$pagination_url = "&wild_point_count=".$r['min_wild_points'].
                  "&missing_line=".$r['missing_line'].
                  "&has_hook=".$r['has_hook'].
                  "&has_too_long_line=".$r['has_too_long_line'].
                  "&has_interrupted_line=".$r['has_interrupted_line'].
                  "&other_problem=".$r['other_problem'].
                  "&is_image=".$r['is_image'];

// Get total number of elements for pagination
$sql = "SELECT COUNT(`id`) as counter FROM `wm_raw_draw_data` $where";
$stmt = $pdo->prepare($sql);
$stmt->execute();
$row = $stmt->fetchObject();
$total = $row->counter;

// Get all raw data of this user
$currentPage = isset($_GET['page']) ? intval($_GET['page']) : 1;
$sql = "SELECT `id`, `data` as `image`, `creation_date` ".
       "FROM `wm_raw_draw_data` ".
       $where.
       "ORDER BY `creation_date` DESC ".
       "LIMIT ".(($currentPage-1)*14).", 14";
$stmt = $pdo->prepare($sql);
$stmt->execute();
$userimages = $stmt->fetchAll();

$tab = "all";


echo $twig->render('problems.twig', array('heading' => "Problematic raw data ($total results)",
                                          'logged_in' => is_logged_in(),
                                          'display_name' => $_SESSION['display_name'],
                                          'file'=> "problems",
                                          'userimages' => $userimages,
                                          'total' => $total,
                                          'pages' => ceil(($total)/14),
                                          'currentPage' => $currentPage,
                                          'restrictions' => $r,
                                          'pagination_url' => $pagination_url
                                        )
                  );

?>