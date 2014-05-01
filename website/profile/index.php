<?php
require_once '../svg.php';
include '../init.php';

echo $twig->render('profile.twig', array('heading' => 'Profile',
                                       'file' => "profile",
                                       'logged_in' => is_logged_in(),
                                       'display_name' => $_SESSION['display_name'],
                                       'user_id' => get_uid(),
                                       'email' => get_email(),
                                       'gravatar' => "http://www.gravatar.com/avatar/".md5(get_email()),
                                       )
                  );

?>