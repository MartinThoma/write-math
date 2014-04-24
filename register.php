<?php
include 'init.php';

function does_user_exist($uname) {
    global $mysqli;

    if (!($stmt = $mysqli->prepare("SELECT `id` FROM `users` WHERE `display_name` = (?)"))) {
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
      $stmt -> bind_result($result);

      /* Fetch the value */
      $stmt -> fetch();

      return !($result == 0);
    }
}

function rand_string( $length ) {
    $chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";  
    $size = strlen( $chars );
    for( $i = 0; $i < $length; $i++ ) {
        $str .= $chars[ rand( 0, $size - 1 ) ];
    }
    return $str;
}

function create_new_user($uname, $email, $pw, $salt) {
    global $mysqli;

    if (!($stmt = $mysqli->prepare("INSERT INTO  `write-math`.`users` (".
                                   "`display_name` ,".
                                   "`email` ,".
                                   "`password` ,".
                                   "`salt`".
                                   ") VALUES (?, ?, ?, ?);"
                                   )
          )
       ) {
        echo "Prepare failed: (" . $mysqli->errno . ") " . $mysqli->error;
    }

    if (!$stmt->bind_param("ssss", $uname, $email, md5($pw.$salt), $salt)) {
        echo "Binding parameters failed: (" . $stmt->errno . ") " . $stmt->error;
        return 0;
    }

    if (!$stmt->execute()) {
        echo "Execute failed: (" . $stmt->errno . ") " . $stmt->error;
        return 0;
    }
    return $mysqli->insert_id;
}

if (isset($_POST['username']) && isset($_POST['email']) && isset($_POST['password'])) {
    $uname = $_POST['username'];
    $pw = $_POST['password'];
    $email = $_POST['email'];

    if (!does_user_exist($uname)) {
        $salt = rand_string(8);
        $user_id = create_new_user($uname, $email, $pw, $salt);
        $_SESSION['uid'] = $user_id;
    } else {
        echo "There is already a user with username '".$uname."'.";
    }
}

?>

<html>
<head>
    <title>Register</title>
</head>
<body>
    <?php include 'header.php'; ?>
    <h1>Register</h1>
    <form action="register.php" method="post">
        <label for="username">Username</label>
        <input type="text" name="username" id="username"
               pattern=".{4,20}" required title="4 to 20 characters"/>

        <label for="password">Password</label>
        <input type="password" name="password" id="password" 
               pattern=".{5,}" required title="5 characters minimum"/>

        <label for="email">Email</label>
        <input type="email" name="email" id="email" />

        <input type="submit" />
    </form>

    <?php include 'footer.php'; ?>
</body>
</html>