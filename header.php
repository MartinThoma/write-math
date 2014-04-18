<?php
echo "<header>";
if (is_logged_in()) {
    echo "Hallo " . $_SESSION['uname'];
} else {
    echo '<a href="login.php">Login</a>';
}
echo "</header>";
?>