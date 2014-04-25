<?php
session_start();
require("config.php");
$mysqli = new mysqli($server, $username, $password, $dbname);

/* check connection */
if ($mysqli->connect_errno) {
    echo "Failed to connect to MySQL: (" . $mysqli->connect_errno . ") " . $mysqli->connect_error;
}
include 'session.php';
