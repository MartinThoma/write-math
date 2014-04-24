<?php

function is_logged_in() {
    global $mysqli;

    if ($_SESSION['is_logged_in']) {
        $uname = $_SESSION['uname'];
        $upass = $_SESSION['upass'];

        if (!($stmt = $mysqli->prepare("SELECT `id`, `salt` FROM `wm_users` WHERE `display_name` = ?"))) {
            echo "Prepare for salt selection failed: (" . $mysqli->errno . ") " . $mysqli->error;
            return false;
        }

        if (!$stmt->bind_param("s", $uname)) {
            echo "Binding parameters failed: (" . $stmt->errno . ") " . $stmt->error;
            return false;
        }

        if (!$stmt->execute()) {
            echo "Execute failed: (" . $stmt->errno . ") " . $stmt->error;
            $stmt->close();
            return false;
        } else {
            $stmt->close();
            /* Bind results */
            $stmt -> bind_result($id, $salt);

            /* Fetch the value */
            $stmt -> fetch();

            if (!($stmt = $mysqli->prepare("SELECT `id` FROM `wm_users` WHERE `id` = ? AND `password` = ?")) ){
                echo "Prepare for user id selection failed: (" . $mysqli->errno . ") " . $mysqli->error;
                return false;
            }

            if (!$stmt->bind_param("is", $id, md5($upass.$salt))) {
                echo "Binding parameters failed: (" . $stmt->errno . ") " . $stmt->error;
                return false;
            }
            
            $stmt->execute();
            $stmt -> bind_result($uid);
            $stmt -> fetch();

            if ($id == $uid) {
                $_SESSION['uid'] = $uid;
                $_SESSION['uname'] = $uname;
                $_SESSION['upass'] = $upass;
                $_SESSION['is_logged_in'] = true;
                return true;
            } else {
                $_SESSION['is_logged_in'] = false;
            }
        }
    }

    return false;
}


function get_uid() {
    is_logged_in();
    return $_SESSION['uid'];
}