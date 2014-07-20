<?php
include '../init.php';

$password_changed = false;

function randomPassword() {
    $alphabet = "ABCDEFGHJKLMNPQRSTUWXYZ23456789";
    $pass = array();
    $alphaLength = strlen($alphabet) - 1;
    for ($i = 0; $i < 8; $i++) {
        $n = rand(0, $alphaLength);
        $pass[] = $alphabet[$n];
    }
    return implode($pass);
}

if (isset($_GET['email']) && !isset($_GET['code'])) {
    $sql = "UPDATE `wm_users` ".
           "SET `confirmation_code` = :code ".
           "WHERE `email` = :email AND status = 'activated';";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':email', $_GET['email'], PDO::PARAM_STR);
    $code = md5(rand());
    $stmt->bindParam(':code', $code, PDO::PARAM_STR);
    $stmt->execute();
    if ($stmt->rowCount() == 1) {
        $message = "Hello ".$display_name."\n\n".
                   "A password reset has been requested for http://write-math.com. ".
                   "Please click on the following link if you want to reset ".
                   "your password:\n".
                   "http://write-math.com/forgot/?email=".$_GET['email']."&code=$code\n\n".
                   "If you did not request a new password you should ignore".
                   "this email.\n\n".
                   "Best regards,\n".
                   "Martin Thoma";
        $headers = 'From: Martin Thoma <info@martin-thoma.de>' . PHP_EOL .
                   'Reply-To: Martin Thoma <info@martin-thoma.de>' . PHP_EOL .
                   'X-Mailer: PHP/' . phpversion();
        mail($_GET['email'],
             "[Write-Math] Password reset",
             $message,
             $headers
        );
        $msg[] = array("class" => "alert-success",
                       "text" => "An email has been sent to '".$_GET['email'].
                                 "' with a confirmation ".
                                 "code to reset your password.");
    } else {
        $msg[] = array("class" => "alert-warning",
                       "text" => "The user '".$_GET['email'].
                                 "' is not in the database.");
    }
} elseif (isset($_GET['email']) && isset($_GET['code'])) {
    $new_password = randomPassword();
    $hash = password_hash($new_password, PASSWORD_BCRYPT, array("cost" => 10));
    $sql = "UPDATE `wm_users` ".
           "SET `password` = :password, confirmation_code = '' ".
           "WHERE `email` = :email AND `confirmation_code` = :code;";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':email', $_GET['email'], PDO::PARAM_STR);
    $stmt->bindParam(':code', $_GET['code'], PDO::PARAM_STR);
    $stmt->bindParam(':password', $hash, PDO::PARAM_STR);
    $stmt->execute();
    if ($stmt->rowCount() == 1) {
        $message = "Hello\n\n".
                   "Your new password for http://write-math.com ".
                   "is: '".$new_password."' (without the apostrophes)\n\n".
                   "Best regards,\n".
                   "Martin Thoma";
        $headers = 'From: Martin Thoma <info@martin-thoma.de>' . PHP_EOL .
                   'Reply-To: Martin Thoma <info@martin-thoma.de>' . PHP_EOL .
                   'X-Mailer: PHP/' . phpversion();
        mail($_GET['email'], "[Write-Math] New password", $message,
             $headers);
        $msg[] = array("class" => "alert-success",
                       "text" => "Congratulations. Your password was reseted. ".
                                 "An Email with your new password was sent ".
                                 "to you. You can change that in your profile.");
        $password_changed = true;
        print_r($message);
    } else {
        $msg[] = array("class" => "alert-danger",
                       "text" => "Your password could not be resetted. ".
                                 "Please contact info@martin-thoma.de.");
    }
}


echo $twig->render('forgot.twig', array('heading' => 'Reset password',
                                        'logged_in' => is_logged_in(),
                                        'file'=> "forgot",
                                        'msg' => $msg,
                                        'password_changed' => $password_changed
                                       )
                  );
?>