<?php
session_start();
require("config.php");
$mysqli = new mysqli($server, $username, $password, $dbname);

if (isset($_POST['uname']) && isset($_POST['upass'])) {
    $uname = $_POST['uname'];
    $upass = $_POST['upass'];

    ;

    if (!($stmt = $mysqli->prepare("SELECT `id`, `salt` FROM `users` WHERE `display_name` = ?")) ){
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
        $stmt -> bind_result($uid, $salt);

        /* Fetch the value */
        $stmt -> fetch();
        $stmt->close();

        if (!($stmt = $mysqli->prepare("SELECT `id` FROM `users` WHERE `id` = ? AND `password` = ?")) ){
            echo "Prepare failed: (" . $mysqli->errno . ") " . $mysqli->error;
            return false;
        }
        if (!$stmt->bind_param("is", $uid, md5($upass.$salt))) {
            echo "Binding parameters failed: (" . $stmt->errno . ") " . $stmt->error;
            return false;
        }
        
        $stmt->execute();
        $stmt -> bind_result($id);
        $stmt -> fetch();
        $stmt->close();

        if ($id == $uid) {
            $_SESSION['uname'] = $uname;
            $_SESSION['upass'] = $upass;
            $_SESSION['is_logged_in'] = true;
            header('Location: train.php');
        } else {
            $_SESSION['is_logged_in'] = false;
        }
    }
}

?>
<html>
<head>
    <title>Login</title>
</head>
<body>
    <h1>Login</h1>
    <form action="login.php" method="post">
        <label for="uname">Username</label>
        <input type="text" id="uname" name="uname" />

        <label for="upass">Password</label>
        <input type="password" id="upass" name="upass" />
        <input type="submit"/>
    </form>
</body>
</html>