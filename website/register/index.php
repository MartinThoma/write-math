<?php
require_once '../vendor/autoload.php';
include '../init.php';

$loader = new Twig_Loader_Filesystem('../templates');
$twig = new Twig_Environment($loader, array(
    'cache' => '../cache',
));
$msg = array();

function does_user_exist($display_name) {
    global $mysqli;

    if (!($stmt = $mysqli->prepare("SELECT `id` FROM `wm_users` ".
                                   "WHERE `display_name` = (?)"))) {
        echo "Prepare failed: (" . $mysqli->errno . ") " . $mysqli->error;
        return false;
    }

    if (!$stmt->bind_param("s", $display_name)) {
        echo "Binding parameters failed: (" . $stmt->errno . ") " . $stmt->error;
        return false;
    }

    if (!$stmt->execute()) {
        echo "Execute failed: (" . $stmt->errno . ") " . $stmt->error;
        return false;
    } else {
      /* Bind results */
      $stmt -> bind_result($result);

      /* Fetch the value */
      $stmt -> fetch();

      return !($result == 0);
    }
}

function does_email_exist($email) {
    global $mysqli;

    if (!($stmt = $mysqli->prepare("SELECT `id` FROM `wm_users` ".
                                   "WHERE `email` = (?)"))) {
        echo "Prepare failed: (" . $mysqli->errno . ") " . $mysqli->error;
        return false;
    }

    if (!$stmt->bind_param("s", $email)) {
        echo "Binding parameters failed: (" . $stmt->errno . ") " . $stmt->error;
        return false;
    }

    if (!$stmt->execute()) {
        echo "Execute failed: (" . $stmt->errno . ") " . $stmt->error;
        return false;
    } else {
      /* Bind results */
      $stmt -> bind_result($result);

      /* Fetch the value */
      $stmt -> fetch();

      return !($result == 0);
    }
}

function rand_string( $length ) {
    $chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
    $size = strlen( $chars );
    for( $i = 0; $i < $length; $i++ ) {
        $str .= $chars[ rand( 0, $size - 1 ) ];
    }
    return $str;
}

function create_new_user($display_name, $email, $pw, $salt) {
    global $mysqli;

    if (!($stmt = $mysqli->prepare("INSERT INTO  `wm_users` (".
                                   "`display_name` ,".
                                   "`email` ,".
                                   "`password` ,".
                                   "`salt`".
                                   ") VALUES (?, ?, ?, ?);"
                                   )
          )
       ) {
        echo "Prepare failed: (" . $mysqli->errno . ") " . $mysqli->error;
    }

    if (!$stmt->bind_param("ssss", $display_name, $email, md5($pw.$salt), $salt)) {
        echo "Binding parameters failed: (" . $stmt->errno . ") " . $stmt->error;
        return 0;
    }

    if (!$stmt->execute()) {
        echo "Execute failed: (" . $stmt->errno . ") " . $stmt->error;
        return 0;
    }
    return $mysqli->insert_id;
}

if (isset($_POST['display_name']) && isset($_POST['email']) && isset($_POST['password'])) {
    $display_name = $_POST['display_name'];
    $pw    = $_POST['password'];
    $email = $_POST['email'];

    if (does_user_exist($display_name)) {
        array_push($msg, array("class" => "alert-warning",
                               "text" => "There is already a user with ".
                                         "display name '".$display_name."'."));
    } elseif (does_email_exist($email)) {
        array_push($msg, array("class" => "alert-warning",
                               "text" => "There is already a user with ".
                                         "email '".$email."'."));
    } else {
        $salt = rand_string(8);
        $user_id = create_new_user($display_name, $email, $pw, $salt);
        $_SESSION['uid'] = $user_id;
        array_push($msg, array("class" => "alert-success",
                               "text" => "Your account has been created."));
    }
}

echo $twig->render('register.twig', array('heading' => 'Register',
                                          'logged_in' => is_logged_in(),
                                          'display_name' => $_SESSION['display_name'],
                                          'file'=> "register",
                                          'msg' => $msg
                                       )
                  );
?>