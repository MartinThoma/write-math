<?php
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

function create_new_user($display_name, $email, $pw,
                         $account_type='Regular User') {
    global $pdo;

    $sql = "INSERT INTO  `wm_users` (".
           "`display_name` ,".
           "`email` ,".
           "`password`, ".
           "`confirmation_code`, ".
           "`status`, ".
           "`account_type` ".
           ") VALUES (".
           ":display_name, :email, :password, ".
           ":confirmation_code, 'deactivated', :account_type);";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':display_name', $display_name, PDO::PARAM_STR);
    $stmt->bindParam(':email', $email, PDO::PARAM_STR);
    $hash = password_hash($pw, PASSWORD_BCRYPT, array("cost" => 10));
    $stmt->bindParam(':password', $hash, PDO::PARAM_STR);
    $stmt->bindParam(':account_type', $account_type, PDO::PARAM_STR);
    $code = md5(rand());
    $stmt->bindParam(':confirmation_code', $code, PDO::PARAM_STR);
    $stmt->execute();

    return array("id" => $pdo->lastInsertId(), "confirmation_code" => $code);
}

function activate_user($email, $code) {
    global $pdo;
    $sql = "UPDATE `wm_users` ".
           "SET status = 'activated' ".
           "WHERE `email` = :email AND `confirmation_code` = :code";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':code', $code, PDO::PARAM_STR);
    $stmt->bindParam(':email', $email, PDO::PARAM_STR);
    
    $stmt->execute();
    if ($stmt->rowCount() == 1) {
        return true;
    }

    return false;
}
?>