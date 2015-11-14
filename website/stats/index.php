<?php
include '../init.php';

// tags
$sql = "SELECT `id`, `tag_name`, `is_package` ".
       "FROM `wm_tags` ";
$stmt = $pdo->prepare($sql);
$stmt->execute();
$tags = $stmt->fetchAll();
$tag_data = array();
foreach ($tags as $value) {
    $tag_data[$value['id']] = array('tag_name' => $value['tag_name'],
                                    'is_package' => $value['is_package']);
}

$sql = "SELECT `tag_id`, `symbol_id` ".
       "FROM `wm_tags2symbols` ";
$stmt = $pdo->prepare($sql);
$stmt->execute();
$tags2symbol_fetched = $stmt->fetchAll();
$symbol2tags = array();
foreach ($tags2symbol_fetched as $value) {
    $symbol2tags[$value['symbol_id']][] = $value['tag_id'];
}


$sql = "SELECT `wm_formula`.`id`, `formula_in_latex`, `formula_name`, ".
       "`best_rendering`, `variant_of`, ".
       "COUNT(`wm_formula`.`id`) AS `counter` ".
       "FROM `wm_raw_draw_data` ".
       "JOIN `wm_formula` ON `wm_formula`.`id` = `accepted_formula_id` ".
       "WHERE (`formula_type` = 'single symbol' OR ".
       "`formula_type` = 'drawing' OR `formula_type` = 'nesting symbol') ".
       "GROUP BY  `accepted_formula_id` ".
       "ORDER BY counter DESC";
$stmt = $pdo->prepare($sql);
$stmt->execute();
$symbol_training_data_count = $stmt->fetchAll();

$sql = "SELECT `wm_formula`.`id`, COUNT(`symbol_id`) as `paper_count` ".
       "FROM `wm_formula` ".
       "JOIN `wm_formula_in_paper` ON `wm_formula`.`id` = `symbol_id` ".
       "WHERE (`formula_type` = 'single symbol' OR ".
       "`formula_type` = 'drawing' OR `formula_type` = 'nesting symbol') ".
       "GROUP BY  `symbol_id` ";
$stmt = $pdo->prepare($sql);
$stmt->execute();
$paper_count = $stmt->fetchAll();
$formulaid2count = array();
foreach ($paper_count as $key => $value) {
    $formulaid2count[$value['id']] = $value['paper_count'];
}

$sum = 0;
$total_references = 0;
$important_count = 0;
$important_count_raw = 0;
$tmp = array();
foreach ($symbol_training_data_count as $key=>$s) {
    $sum += $s['counter'];
    if (array_key_exists($s['id'], $formulaid2count)) {
        $symbol_training_data_count[$key]['used_by_counter'] = $formulaid2count[$s['id']];
    } else {
        $symbol_training_data_count[$key]['used_by_counter'] = 0;
    }
    $total_references += $symbol_training_data_count[$key]['used_by_counter'];
}

echo $twig->render('stats.twig', array('heading' => 'Stats',
                                       'file'=> "stats",
                                       'logged_in' => is_logged_in(),
                                       'user_id' => get_uid(),
                                       'display_name' => $_SESSION['display_name'],
                                       'msg' => $msg,
                                       'symbol_training_data_count' => $symbol_training_data_count,
                                       'sum' => $sum,
                                       'total_references' => $total_references,
                                       'symbol2tags' => $symbol2tags,
                                       'tag_data' => $tag_data
                                       )
                  );