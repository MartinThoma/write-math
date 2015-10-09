<?php
include '../init.php';

echo $twig->render('symbol-identification.twig', array('heading' => 'Symbol Identification',
                                       'file'=> "about",
                                       'logged_in' => is_logged_in(),
                                       'display_name' => $_SESSION['display_name'],
                                       'msg' => $msg,
                                       )
                  );