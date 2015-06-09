<?php

include dirname(__FILE__).'/user.func.php';

function is_logged_in() {
    global $pdo;

    if (!isset($_SESSION['email']) || !($_SESSION['password'])) {
        #return false;
        $_SESSION = login_as_ipuser();
    }

    $email = $_SESSION['email'];
    $upass = $_SESSION['password'];
    $account_type = $_SESSION['account_type'];

    $sql = "SELECT `id`, `display_name`, `account_type` FROM `wm_users` ".
           "WHERE (`email` = :email AND `password` = :password ".
                    "AND `account_type` != 'IP-User') OR ".
            "(`email` = :email AND `account_type` = 'IP-User')";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':email', $email, PDO::PARAM_STR);
    $stmt->bindParam(':password', $upass, PDO::PARAM_STR);
    $stmt->execute();
    $row =$stmt->fetchObject();

    if ($row->id > 0) {
        $_SESSION['uid'] = $row->id;
        $_SESSION['display_name'] = $row->display_name;
        $_SESSION['upass'] = $upass;
        $_SESSION['is_logged_in'] = true;
        $_SESSION['account_type'] = $row->account_type;
        return true;
    } else {
        $_SESSION['is_logged_in'] = false;
        $_SESSION['uid'] = NULL;
        $_SESSION['display_name'] = NULL;
        $_SESSION['upass'] = NULL;
        $_SESSION['account_type'] = NULL;
    }

    $_SESSION = login_as_ipuser();
    return true;
}

function login_as_ipuser() {
    global $pdo;
    $uid = create_ip_user();

    $sql = "SELECT `id`, `display_name`, `email`, `account_type` FROM `wm_users` ".
           "WHERE `id` = :uid";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':uid', $uid, PDO::PARAM_INT);
    $stmt->execute();
    $row =$stmt->fetchObject();

    $_SESSION['uid'] = $row->id;
    $_SESSION['display_name'] = $row->display_name;
    $_SESSION['password'] = 'sdf';  # TODO: This is a problem
    $_SESSION['is_logged_in'] = true;
    $_SESSION['account_type'] = $row->account_type;
    $_SESSION['email'] = $row->email;
    return $_SESSION;
}

function generateRandomString($length = 10) {
    $characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
    $randomString = '';
    for ($i = 0; $i < $length; $i++) {
        $randomString .= $characters[rand(0, strlen($characters) - 1)];
    }
    return $randomString;
}

function create_ip_user() {
    $display_name = generate_display_name();
    $email = $display_name."@write-math.com";
    $pw = generateRandomString();
    $ret = create_new_user($display_name, $email, $pw, 'IP-User');
    activate_user($email, $ret['confirmation_code']);
    return $ret['id'];
}

function get_uid() {
    if (!isset($_SESSION['uid'])) {
        return false;
    } else {
        return $_SESSION['uid'];
    }
}

function get_email() {
    if (!isset($_SESSION['email'])) {
        return false;
    } else {
        return $_SESSION['email'];
    }
}

function get_language() {
    global $pdo;
    $sql = "SELECT `language` FROM `wm_users` ".
           "WHERE `id` = :id";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':id', $_SESSION['uid'], PDO::PARAM_INT);
    $stmt->execute();
    $row =$stmt->fetchObject();
    return $row->language;
}

function get_handedness() {
    global $pdo;
    $sql = "SELECT `handedness` FROM `wm_users` ".
           "WHERE `id` = :id";
    $stmt = $pdo->prepare($sql);
    $stmt->bindParam(':id', $_SESSION['uid'], PDO::PARAM_INT);
    $stmt->execute();
    $row =$stmt->fetchObject();
    return $row->handedness;
}

function is_ip_user() {
    global $pdo;
    $sql = "SELECT `account_type` FROM `wm_users` WHERE `id` = :uid";
    $stmt = $pdo->prepare($sql);
    $uid = get_uid();
    $stmt->bindParam(':uid', $uid, PDO::PARAM_INT);
    $stmt->execute();
    $row =$stmt->fetchObject();
    if ($row->account_type == 'IP-User') {
        return true;
    }
    return false;
}

function is_admin() {
    global $pdo;
    $sql = "SELECT `account_type` FROM `wm_users` WHERE `id` = :uid";
    $stmt = $pdo->prepare($sql);
    $uid = get_uid();
    $stmt->bindParam(':uid', $uid, PDO::PARAM_INT);
    $stmt->execute();
    $row =$stmt->fetchObject();
    if ($row->account_type == 'Admin') {
        return true;
    }
    return false;
}

/**
 * This method merges two user accounts.
 * The caller has to make super-sure that they are really the same!
 * @param  int $ip_id      ID of an IP-User (gets deleted)
 * @param  int $regular_id ID of an NON-IP User (remains)
 * @return int             0 if everything is fine, something else otherwise
 */
function merge_accounts($ip_id, $regular_id) {
    global $pdo;
    $ip_id = intval($ip_id);
    $regular_id = intval($regular_id);

    // This approach might fail due to uniqueness constraints
    $tables = array('wm_flags', 'wm_formula_svg_missing',
                    'wm_partial_answer', 'wm_raw_draw_data', 'wm_renderings',
                    'wm_user_unknown_formula', 'wm_workers');
    foreach ($tables as $table) {
        $sql = "UPDATE `$table` ".
               "SET `user_id` =  '$regular_id' WHERE `user_id` =$ip_id;";
        $pdo->query($sql);
    }

    // Take a look at every dataset, try to change it and delete it if changing
    // wasn't successfull
    $tables = array('wm_flags', 'wm_formula_svg_missing',
                    'wm_partial_answer', 'wm_raw_draw_data', 'wm_renderings',
                    'wm_user_unknown_formula', 'wm_workers');
    foreach ($tables as $table) {
        $sql = "SELECT `id` FROM `$table` WHERE `user_id` = $ip_id;";
        $stmt = $pdo->prepare($sql);
        $stmt->execute();
        $flag_ids = $stmt->fetchAll();
        foreach ($flag_ids as $data) {
            $id = $data['id'];
            $sql = "UPDATE `$table` SET `user_id` = $ip_id WHERE id=$id;";
            $result = $pdo->query($sql);
            if ($result === false) {
                $sql = "DELETE FROM `$table` ".
                       "WHERE `id`=$id AND `user_id`=$ip_id LIMIT 1;";
                $pdo->query($sql);
            }
        }
    }

    $sql = "DELETE FROM `wm_users` WHERE `id`=$ip_id LIMIT 1;";
    $pdo->query($sql);

    return 0;
}