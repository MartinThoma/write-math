<?php
require("config.php");
$dsn = "mysql:host=$server;dbname=$dbname";

try { 
    $pdo = new PDO($dsn, $username, $password, array(PDO::MYSQL_ATTR_INIT_COMMAND => "SET NAMES 'utf8'"));
    $pdo ->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) { 
    echo 'Connection failed: ' . $e->getMessage(); 
}