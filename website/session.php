<?php

function is_logged_in() {
    global $mysqli;

    $email = $_SESSION['email'];
    $upass = $_SESSION['password'];

    if (!($stmt = $mysqli->prepare("SELECT `id`, `display_name` FROM `wm_users` ".
                                   "WHERE `email` = ? AND `password` = ?"))) {
        echo "Prepare for salt selection failed: (" . $mysqli->errno . ") " . $mysqli->error;
        return false;
    }

    if (!$stmt->bind_param("ss", $email, $upass)) {
        echo "Binding parameters failed: (" . $stmt->errno . ") " . $stmt->error;
        return false;
    }

    if (!$stmt->execute()) {
        echo "Execute failed: (" . $stmt->errno . ") " . $stmt->error;
        $stmt->close();
        return false;
    } else {
        /* Bind results */
        $stmt -> bind_result($id, $display_name);

        /* Fetch the value */
        $stmt -> fetch();

        if ($id > 0) {
            $_SESSION['uid'] = $id;
            $_SESSION['display_name'] = $display_name;
            $_SESSION['upass'] = $upass;
            $_SESSION['is_logged_in'] = true;
            return true;
        } else {
            $_SESSION['is_logged_in'] = false;
            $_SESSION['uid'] = NULL;
            $_SESSION['display_name'] = NULL;
            $_SESSION['upass'] = NULL;
        }
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