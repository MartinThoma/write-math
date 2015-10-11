<?php
include '../init.php';

$min_unicode = 31;
$max_unicode = 61;

if (isset($_GET['min']) && isset($_GET['max'])) {
    $min_unicode_g = intval($_GET['min']);
    $max_unicode_g = intval($_GET['max']);
    $min_unicode = max($min_unicode_g, 0);
    $max_unicode = max($max_unicode_g, $min_unicode_g+1);
    if ($max_unicode - $min_unicode > 2000) {
        $max_unicode = $min_unicode + 2000;
    }


    $sql = "SELECT `wm_formula`.id, best_rendering, formula_name, unicode_dec, font, ".
           "font_style, formula_in_latex  ".
           "FROM  `wm_formula` ";
    $sql .= "WHERE (:min_unicode <= `unicode_dec` AND `unicode_dec` <= :max_unicode) ";
    $sql .= "ORDER BY `unicode_dec`, `formula_name` ASC";
    $stmt = $pdo->prepare($sql);
    $stmt->execute(array(':min_unicode' => $min_unicode,
                         ':max_unicode' => $max_unicode));
    $searchresults = $stmt->fetchAll();

    $res = array();
    for ($unicode=$min_unicode; $unicode <= $max_unicode; $unicode++) {
        $res[$unicode] = array();
    }

    # Fill array with searched values
    foreach ($searchresults as $key => $value) {
        $value['base16'] = base_convert($value['unicode_dec'], 10, 16);
        $res[$value['unicode_dec']][] = $value;
    }

    $searchresults = $res;

    # Read the unicode.json
    $string = file_get_contents("unicode.json");
    $json_a = json_decode($string, true);

    # Go through unicode website, if no result was found
    for ($unicode=$min_unicode; $unicode <= $max_unicode; $unicode++) {
        if (count($searchresults[$unicode]) == 0) {
            $base16 = base_convert($unicode, 10, 16);
            $searchresults[$unicode][] = array('unicode_dec' => $unicode,
                                               'font' => 'STIXGeneral',
                                               'font_style' => 'normal',
                                               'formula_name' => $json_a[$unicode],
                                               'base16' => $base16);
        }
    }
}


echo $twig->render('unicode.twig', array('heading' => 'Unicode',
                                         'logged_in' => is_logged_in(),
                                         'display_name' => $_SESSION['display_name'],
                                         'file'=> "search",
                                         'searchresults' => $searchresults,
                                         'min_unicode' => $min_unicode,
                                         'max_unicode' => $max_unicode
                                        )
                  );

?>