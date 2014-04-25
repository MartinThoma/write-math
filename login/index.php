<?php
require_once '../vendor/autoload.php';
include '../init.php';

$loader = new Twig_Loader_Filesystem('../templates');
$twig = new Twig_Environment($loader, array(
    'cache' => '../cache',
));
$msg = array();

function login($email, $upass) {
    global $msg, $mysqli;

    if (!($stmt = $mysqli->prepare("SELECT `id`, `salt` FROM `wm_users` ".
                                   "WHERE `email` = ?")) ){
        echo "Prepare login failed: (" . $mysqli->errno . ") " . $mysqli->error;
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
        $stmt -> bind_result($uid, $salt);

        /* Fetch the value */
        $stmt -> fetch();
        $stmt->close();

        if ( !((int)$uid == $uid && (int)$uid > 0) ) {
            array_push($msg, array("class" => "alert-warning",
                                   "text" => "Email '$email' not known."));
            return false;
        }

        if (!($stmt = $mysqli->prepare("SELECT `id` FROM `wm_users` ".
                                       "WHERE `id` = ? AND `password` = ?")) ){
            echo "Prepare failed: (" . $mysqli->errno . ") " . $mysqli->error;
            return false;
        }

        echo $upass."<br/>";
        echo $salt."<br/>";
        echo md5($upass.$salt);

        if (!$stmt->bind_param("is", $uid, md5($upass.$salt))) {
            echo "Binding parameters failed: (" . $stmt->errno . ") " . $stmt->error;
            return false;
        }
        
        $stmt->execute();
        $stmt -> bind_result($id);
        $stmt -> fetch();
        $stmt->close();

        if ($id == $uid) {
            $_SESSION['email'] = $email;
            $_SESSION['password'] = md5($upass.$salt);
            $_SESSION['is_logged_in'] = true;
            header('Location: ../train');
        } else {
            $_SESSION['is_logged_in'] = false;
            array_push($msg, array("class" => "alert-warning",
                                   "text" => "Logging in failed. The email ".
                                             "did not match the password."));
        }
    }
}

if (isset($_POST['email']) && isset($_POST['password'])) {
    login($_POST['email'], $_POST['password']);
}

echo $twig->render('login.twig', array('heading' => 'Login',
                                       'logged_in' => is_logged_in(),
                                       'display_name' => $_SESSION['display_name'],
                                       'file'=> "login",
                                       'msg' => $msg
                                       )
                  );
?>