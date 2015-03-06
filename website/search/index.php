<?php
include '../init.php';

$searchterm = '';

if (isset($_GET['search'])) {
    $searchterm = $_GET['search'];

    $sql = "SELECT id, best_rendering, formula_name, unicode_dec, font, ".
           "font_style, formula_in_latex  ".
           "FROM  `wm_formula` ".
           "WHERE  `description` COLLATE UTF8_GENERAL_CI LIKE :searchstring ".
           "OR `unicodexml_description` COLLATE UTF8_GENERAL_CI LIKE :searchstring ".
           "ORDER BY `formula_name` ASC";
    $stmt = $pdo->prepare($sql);
    $stmt->execute(array(':searchstring' => '%'.$searchterm.'%'));
    $searchresults = $stmt->fetchAll();
}


echo $twig->render('search.twig', array('heading' => 'Search',
                                         'logged_in' => is_logged_in(),
                                         'display_name' => $_SESSION['display_name'],
                                         'file'=> "search",
                                         'searchterm' => $searchterm,
                                         'searchresults' => $searchresults
                                        )
                  );

?>