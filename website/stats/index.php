<?php
include '../init.php';

$sql = "SELECT `wm_formula`.`id`, `formula_in_latex`, `formula_name`, ".
       "COUNT(  `wm_formula`.`id` ) AS counter ".
       "FROM  `wm_raw_draw_data` ".
       "JOIN  `wm_formula` ON  `wm_formula`.`id` =  `accepted_formula_id` ".
       "GROUP BY  `accepted_formula_id` ".
       "ORDER BY counter DESC";
$stmt = $pdo->prepare($sql);
$stmt->execute();
$symbol_training_data_count = $stmt->fetchAll();

echo $twig->render('stats.twig', array('heading' => 'Stats',
                                       'file'=> "stats",
                                       'logged_in' => is_logged_in(),
                                       'display_name' => $_SESSION['display_name'],
                                       'msg' => $msg,
                                       'symbol_training_data_count' => $symbol_training_data_count
                                       )
                  );