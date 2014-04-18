<?php
include_once 'init.php';
include_once 'session.php';

?><footer><?php
if (is_logged_in()) {
    ?><a href="register.php">Register</a> - 
      <a href="login.php">Login</a><?php
} else {
    ?><a href="train.php">Train</a><?php
}
?></footer>