<?php
require_once '../vendor/autoload.php';
include '../init.php';

$loader = new Twig_Loader_Filesystem('../templates');
$twig = new Twig_Environment($loader, array(
    'cache' => '../cache',
));

echo $twig->render('about.twig', array('heading' => 'About',
                                       'logged_in' => is_logged_in(),
                                       'username' => $_SESSION['uname'],
                                       'file'=> "about"
                                       )
                  );