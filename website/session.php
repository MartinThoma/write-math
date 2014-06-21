<?php

function is_logged_in() {
    global $pdo;

    if (!isset($_SESSION['email']) || !($_SESSION['password'])) {
        return false;
    }

    $email = $_SESSION['email'];
    $upass = $_SESSION['password'];

    $sql = "SELECT `id`, `display_name` FROM `wm_users` ".
           "WHERE `email` = :email AND `password` = :password";
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
        return true;
    } else {
        $_SESSION['is_logged_in'] = false;
        $_SESSION['uid'] = NULL;
        $_SESSION['display_name'] = NULL;
        $_SESSION['upass'] = NULL;
    }

    return false;
}


function get_uid() {
    is_logged_in();
    return $_SESSION['uid'];
}

function get_email() {
    is_logged_in();
    return $_SESSION['email'];
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

function is_admin() {
    global $pdo;
    $sql = "SELECT `account_type` FROM `wm_users` WHERE `id` = :uid";
    $stmt = $pdo->prepare($sql);
    $uid = get_uid();
    $stmt->bindParam(':uid', $uid, PDO::PARAM_INT);
    $stmt->execute();
    $row =$stmt->fetchObject();
    return $row->account_type;
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
    $ip_id = int($ip_id);
    $regular_id = int($regular_id);
    $tables = array('wm_flags', 'wm_formula_svg_missing',
                    'wm_raw_data2formula', 'wm_raw_draw_data', 'wm_renderings',
                    'wm_user_unknown_formula', 'wm_votes', 'wm_workers');
    foreach ($tables as $table) {
        $sql = "UPDATE `$table` ".
               "SET `user_id` =  '$regular_id' WHERE `user_id` =$ip_id;";
        $pdo->query($sql);
    }
    return 0;
}