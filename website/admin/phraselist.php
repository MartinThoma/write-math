<?php
include '../init.php';
$sql = "SELECT `formula_in_latex` FROM `wm_formula` ".
       "WHERE `formula_type` != 'formula' AND `formula_type` != '' ORDER BY `id`";

$stmt = $pdo->prepare($sql);
$stmt->bindParam(':uid', $uid, PDO::PARAM_INT);
$stmt->execute();
$formulas = $stmt->fetchAll();
$cachedir = '../cache-data/';
$datafile = 'phraselist.js';
$formula_list = array();


function endsWith($haystack, $needle) {
    // search forward starting from end minus needle length characters
    return $needle === "" || (($temp = strlen($haystack) - strlen($needle)) >= 0 && strpos($haystack, $needle, $temp) !== FALSE);
}


foreach ($formulas as $key => $formula) {
    $formula = $formula['formula_in_latex'];
    if (strlen($formula) <= 2 || endsWith($formula, "\\")) {
        continue;
    }
    $formula_list[] = $formula;
}
$fp = fopen($cachedir.$datafile, 'w');
fwrite($fp, json_encode($formula_list));
fclose($fp);

header('Location: ../admin');
?>