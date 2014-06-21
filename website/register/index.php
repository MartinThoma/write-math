<?php
include '../init.php';
include '../user.func.php';



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
    $return = activate_user($_GET['email'], $_GET['code']);
    if ($return) {
        $msg[] = array("class" => "alert-success",
               "text" => "Congratulations. Your account was activated.");
    } else {
        $msg[] = array("class" => "alert-warning",
               "text" => "This account could not be activated.");
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