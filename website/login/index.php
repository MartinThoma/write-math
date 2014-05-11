<?php
include '../init.php';

function login($email, $upass) {
    global $msg, $pdo;

    $sql = "SELECT `id`, `status`, `password` ".
           "FROM `wm_users` WHERE `email` = :email";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':email', $email, PDO::PARAM_STR);
    $stmt->execute();

    $user = $stmt->fetchObject();
    $uid = $user->id;
    $status = $user->status;

    if (!((int)$uid == $uid && (int)$uid > 0)) {
        $msg[] = array("class" => "alert-warning",
                       "text" => "Email '$email' not known.");
        return false;
    }

    if ($user->id > 0 && password_verify($_POST['password'], $user->password)) {
        $_SESSION['email'] = $email;
        $_SESSION['password'] = $user->password;
        $_SESSION['is_logged_in'] = true;
        header('Location: ../train');
    } else {
        $_SESSION['is_logged_in'] = false;
        $msg[] = array("class" => "alert-warning",
                       "text" => "Logging in failed. The email ".
                                 "did not match the password.");
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