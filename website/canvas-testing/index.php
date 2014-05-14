<?php
include '../init.php';



echo $twig->render('canvas-testing.twig', array('heading' => 'Canvas Testing',
                                       'logged_in' => is_logged_in(),
                                       'display_name' => $_SESSION['display_name'],
                                       'file'=> "canvas-testing",
                                       'msg' => $msg
                                       )
                  );

?>