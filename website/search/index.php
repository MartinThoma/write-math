<?php
include '../init.php';

$searchterm = '';

function parse_search($text) {
    $words = array();
    $tags = array();
    $current_chunk = "";
    $tag_began = false;
    foreach (str_split($text) as $char) {
        if ($tag_began) {
            if ($char == ']') {
                $tags[] = $current_chunk;
                $current_chunk = '';
                $tag_began = false;
            } elseif ($char == '[' || $char == ' ') {
                continue;
            } else {
                $current_chunk .= $char;
            }
        } else {
            if ($char == '[') {
                if (strlen($current_chunk) > 0) {
                    $words[] = $current_chunk;
                }
                $current_chunk = '';
                $tag_began = true;
            } elseif ($char == ' ') {
                $words[] = $current_chunk;
                $current_chunk = '';
            } else {
                $current_chunk .= $char;
            }
        }
    }

    if ($current_chunk != '') {
        if ($tag_began) {
            $tags[] = trim($current_chunk);
        } else {
            $words[] = trim($current_chunk);
        }
    }

    return array('words' => $words, 'tags' => $tags, 'original' => $text);
}


function uniord($u) {
    $k = mb_convert_encoding($u, 'UCS-2LE', 'UTF-8');
    $k1 = ord(substr($k, 0, 1));
    $k2 = ord(substr($k, 1, 1));
    return $k2 * 256 + $k1;
}


if (isset($_GET['search'])) {
    $searchterm = trim($_GET['search']);

    if (strlen($searchterm) > 0) {
        $parsed_search = parse_search($searchterm);

        // Get a list of all tags
        $sql = "SELECT `id`, `tag_name` FROM  `wm_tags` ";
        $stmt = $pdo->prepare($sql);
        $stmt->execute();
        $tag_list_complete = $stmt->fetchAll();
        $tags_to_id = array();
        foreach ($tag_list_complete as $tag) {
            $tags_to_id[$tag['tag_name']] = $tag['id'];
        }

        // Get relevant tag ids
        $nonexisting_tag = false;
        $tag_ids = array();
        foreach ($parsed_search['tags'] as $tag_name) {
            if (array_key_exists($tag_name, $tags_to_id)) {
                $tag_ids[] = $tags_to_id[$tag_name];
            } else {
                $nonexisting_tag = true;
                $nonexisting_tag_name = $tag_name;
            }
        }

        if($nonexisting_tag) {
            $searchresults = array();
            $msg[] = array("class" => "alert-warning",
                           "text" => "The tag '".$nonexisting_tag_name."' does not exist.");
        } else {
            $sql = "SELECT `wm_formula`.id, best_rendering, formula_name, unicode_dec, font, ".
                   "font_style, formula_in_latex  ".
                   "FROM  `wm_formula` ";
            $sql .= "WHERE (`description` COLLATE UTF8_GENERAL_CI LIKE :searchstring ".
                    "OR `unicodexml_description` COLLATE UTF8_GENERAL_CI LIKE :searchstring) ";
            $sql .= "OR `unicode_dec` = :uni_dec ";
            $sql .= "ORDER BY `unicode_dec`, `formula_name` ASC";
            $stmt = $pdo->prepare($sql);
            $searchstring_words = trim(implode(" ", $parsed_search['words']));
            $stmt->execute(array(':searchstring' => '%'.$searchstring_words.'%',
                                 ':uni_dec' => uniord($searchterm)));
            $searchresults = $stmt->fetchAll();

            $current_valid_ids = array();
            foreach ($searchresults as $result) {
                $current_valid_ids[] = $result['id'];
            }

            // get tags
            if (count($tag_ids) > 0) {
                foreach ($tag_ids as $tag_id) {
                    $sql = "SELECT `wm_formula`.`id` ".
                           "FROM `wm_formula` ".
                           "JOIN `wm_tags2symbols` ON ".
                           "(`wm_tags2symbols`.`symbol_id` = `wm_formula`.`id`) ".
                           "WHERE tag_id = :tag_id ";
                           "ORDER BY `formula_name` ASC";
                    $stmt = $pdo->prepare($sql);
                    $stmt->bindParam(':tag_id', $tag_id, PDO::PARAM_INT);
                    $stmt->execute();
                    $tag_results = $stmt->fetchAll();
                    $valid_ids = array();
                    foreach ($tag_results as $result) {
                        if (in_array($result['id'], $current_valid_ids)) {
                            $valid_ids[] = $result['id'];
                        }
                    }
                    $next_valid_ids = array();
                    foreach ($current_valid_ids as $id) {
                        if (in_array($id, $valid_ids)) {
                            $next_valid_ids[] = $id;
                        }
                    }
                    $current_valid_ids = $next_valid_ids;
                }

                // Filter the results
                $results = array();
                foreach ($searchresults as $result) {
                    if (in_array($result['id'], $current_valid_ids)) {
                        $results[] = $result;
                    }
                }
                $searchresults = $results;
            }
        }
    }
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