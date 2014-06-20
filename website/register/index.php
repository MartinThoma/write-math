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

function generate_display_name() {
    $prefix = "user_";
    $i = rand();
    return $prefix.$i;
}

function create_new_user($display_name, $email, $pw) {
    global $pdo;

    $sql = "INSERT INTO  `wm_users` (".
           "`display_name` ,".
           "`email` ,".
           "`password`, ".
           "`confirmation_code`, ".
           "`status` ".
           ") VALUES (".
           ":display_name, :email, :password, ".
           ":confirmation_code, 'deactivated');";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':display_name', $display_name, PDO::PARAM_STR);
    $stmt->bindParam(':email', $email, PDO::PARAM_STR);
    $hash = password_hash($pw, PASSWORD_BCRYPT, array("cost" => 10));
    $stmt->bindParam(':password', $hash, PDO::PARAM_STR);
    $code = md5(rand());
    $stmt->bindParam(':confirmation_code', $code, PDO::PARAM_STR);
    $stmt->execute();

    return array("id" => $pdo->lastInsertId(), "confirmation_code" => $code);
}


if (isset($_POST['accept_terms']) && $_POST['accept_terms'] == 'on') {
    $accept_terms = true;
} else {
    $accept_terms = false;
}

/* Start registration */
if (isset($_POST['email']) && isset($_POST['password'])) {
    $pw    = $_POST['password'];
    $email = $_POST['email'];
    do {
        $display_name = generate_display_name();
    } while (does_user_exist($display_name));
    $_SESSION['display_name'] = $display_name;

    if (does_email_exist($email)) {
        $msg[] = array("class" => "alert-warning",
                       "text" => "There is already a user with ".
                                 "email '".$email."'.");
    } elseif(!$accept_terms) {
        $msg[] = array("class" => "alert-warning",
                       "text" => "You have to accept the terms.");
    } else {
        $return = create_new_user($display_name, $email, $pw);
        $user_id = $return["id"];
        $code = $return["confirmation_code"];

        $message = "Hello ".$display_name."\n\n".
                   "You can activate your account for http://write-math.com ".
                   "with the following link:\n".
                   "http://write-math.com/register/?email=$email&code=$code\n\n".
                   "Please note that I will use and publish everything ".
                   "you enter except your email address and your password. ".
                   "As I share everything (for free) entering data cannot be ".
                   "removed.\n\n".
                   "Best regards,\n".
                   "Martin Thoma";
       $headers = 'From: Martin Thoma <info@martin-thoma.de>' . PHP_EOL .
                  'Reply-To: Martin Thoma <info@martin-thoma.de>' . PHP_EOL .
                  'X-Mailer: PHP/' . phpversion();
        mail($email, "[Write-Math] Confirm account creation", $message,
             $headers);
        $msg[] = array("class" => "alert-success",
                       "text" => "Your account has been created. An ".
                                 "activation Email was sent to the given ".
                                 "address.");
    }
}

/* confirm email */
if (isset($_GET['email']) && isset($_GET['code'])) {
    $sql = "UPDATE `wm_users` ".
           "SET status = 'activated' ".
           "WHERE `email` = :email AND `confirmation_code` = :code";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':email', $_GET['email'], PDO::PARAM_STR);
    $stmt->bindParam(':code', $_GET['code'], PDO::PARAM_STR);
    $stmt->execute();
    if ($stmt->rowCount() == 1) {
        $msg[] = array("class" => "alert-success",
                       "text" => "Congratulations. Your account was activated.");
    }
}

echo $twig->render('register.twig', array('heading' => 'Register',
                                          'logged_in' => is_logged_in(),
                                          'display_name' => $_SESSION['display_name'],
                                          'file'=> "register",
                                          'msg' => $msg,
                                          'accepted_terms' => $accepted_terms,
                                          'email' => $email,
                                          'password_plain' => $_POST['password']
                                       )
                  );
?>