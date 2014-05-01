<?php
include '../init.php';

echo $twig->render('about.twig', array('heading' => 'About',
                                       'logged_in' => is_logged_in(),
                                       'display_name' => $_SESSION['display_name'],
                                       'file'=> "about"
                                       )
                  );