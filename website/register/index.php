<?php
include '../init.php';

function does_user_exist($display_name) {
    global $pdo;

    $sql = "SELECT `id` FROM `wm_users` WHERE `display_name` = :display_name";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':display_name', $display_name, PDO::PARAM_STR);
    $stmt->execute();
    $row = $stmt->fetchObject();
    return !($row->id == 0);
}

function does_email_exist($email) {
    global $pdo;

    $sql = "SELECT `id` FROM `wm_users` WHERE `email` = :email";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':email', $email, PDO::PARAM_STR);
    $stmt->execute();
    $row = $stmt->fetchObject();
    return !($row->id == 0);
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
    global $pdo;

    $sql = "INSERT INTO  `wm_users` (".
           "`display_name` ,".
           "`email` ,".
           "`password` ,".
           "`salt`".
           ") VALUES (:display_name, :email, :password, :salt);";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':display_name', $display_name, PDO::PARAM_STR);
    $stmt->bindParam(':email', $email, PDO::PARAM_STR);
    $stmt->bindParam(':password', $pw, PDO::PARAM_STR);
    $stmt->bindParam(':salt', $salt, PDO::PARAM_STR);
    $stmt->execute();

    return $pdo->lastInsertId();
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