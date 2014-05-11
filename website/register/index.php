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

function validate_display_name($name) {
    return preg_match('/^[A-Za-z]{1}[A-Za-z0-9_ ]{1,}[A-Za-z0-9]{1}$/',$name);
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

if (isset($_POST['display_name']) && isset($_POST['email']) && isset($_POST['password'])) {
    $display_name = $_POST['display_name'];
    $pw    = $_POST['password'];
    $email = $_POST['email'];

    if (!validate_display_name($display_name)) {
        $msg[] = array("class" => "alert-warning",
               "text" => "Your username didn't validate. It has to have at ".
                         "least 3 symbols, where the first and the last is ".
                         "a character. You may only use A-Z, a-z, 0-9, _, ".
                         "spaces and -.");
    } elseif (does_user_exist($display_name)) {
        $msg[] = array("class" => "alert-warning",
                       "text" => "There is already a user with ".
                                 "display name '".$display_name."'.");
    } elseif (does_email_exist($email)) {
        $msg[] = array("class" => "alert-warning",
                       "text" => "There is already a user with ".
                                 "email '".$email."'.");
    } else {
        $return = create_new_user($display_name, $email, $pw);
        $user_id = $return["id"];
        $code = $return["confirmation_code"];

        $message = "Hello ".$display_name."\n\n".
                   "You can activate your account for http://write-math.com ".
                   "with the following link:\n".
                   "http://write-math.com/register/?id=$user_id&code=$code\n\n".
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

if (isset($_GET['id']) && isset($_GET['code'])) {
    $sql = "UPDATE `wm_users` ".
           "SET status = 'activated' ".
           "WHERE `id` = :id AND `confirmation_code` = :code";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':id', $_GET['id'], PDO::PARAM_INT);
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
                                          'msg' => $msg
                                       )
                  );
?>