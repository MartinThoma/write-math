<?php
include '../init.php';

function login($email, $upass) {
    global $msg, $pdo;

    $sql = "SELECT `id`, `salt` FROM `wm_users` WHERE `email` = :email";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':email', $email, PDO::PARAM_STR);
    $stmt->execute();

    $row = $stmt->fetchObject();
    $uid = $row->id;
    $salt = $row->salt;

    if ( !((int)$uid == $uid && (int)$uid > 0) ) {
        array_push($msg, array("class" => "alert-warning",
                               "text" => "Email '$email' not known."));
        return false;
    }

    $sql = "SELECT `id` FROM `wm_users` WHERE `id` = :id AND `password` = :pw";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':id', $uid, PDO::PARAM_INT);
    $stmt->bindParam(':pw', md5($upass.$salt), PDO::PARAM_STR);
    $stmt->execute();
    $row = $stmt->fetchObject();
    $id = $row->id;

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

if (isset($_POST['email']) && isset($_POST['password'])) {
    login($_POST['email'], $_POST['password']);
}

echo $twig->render('login.twig', array('heading' => 'Login',
                                       'logged_in' => is_logged_in(),
                                       'display_name' => $_SESSION['display_name'],
                                       'file'=> "login",
                                       'msg' => $msg,
                                       'email' => $_SESSION['email']
                                       )
                  );
?>