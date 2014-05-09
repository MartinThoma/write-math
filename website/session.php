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