<?php

function is_logged_in() {
    global $mysqli;

    if ($_SESSION['is_logged_in']) {
        $uname = $_SESSION['uname'];
        $upass = $_SESSION['upass'];

        if (!($stmt = $mysqli->prepare("SELECT `id`, `salt` FROM `users` WHERE `display_name` = ?"))) {
            echo "Prepare failed: (" . $mysqli->errno . ") " . $mysqli->error;
            return false;
        }

        if (!$stmt->bind_param("s", $uname)) {
            echo "Binding parameters failed: (" . $stmt->errno . ") " . $stmt->error;
            return false;
        }

        if (!$stmt->execute()) {
            echo "Execute failed: (" . $stmt->errno . ") " . $stmt->error;
            return false;
        } else {
            /* Bind results */
            $stmt -> bind_result($id, $salt);

            /* Fetch the value */
            $stmt -> fetch();
            $stmt->close();

            if (!($stmt = $mysqli->prepare("SELECT `id` FROM `users` WHERE `id` = ? AND `password` = ?")) ){
                echo "Prepare failed: (" . $mysqli->errno . ") " . $mysqli->error;
                return false;
            }

            if (!$stmt->bind_param("is", $id, md5($upass.$salt))) {
                echo "Binding parameters failed: (" . $stmt->errno . ") " . $stmt->error;
                return false;
            }
            
            $stmt->execute();
            $stmt -> bind_result($uid);
            $stmt -> fetch();
            $stmt->close();

            if ($id == $uid) {
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
