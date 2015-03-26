<?php
require_once dirname(__FILE__).'/vendor/autoload.php';
session_start();
require("config.php");
$dsn = "mysql:host=$server;dbname=$dbname";

try {
    $pdo = new PDO($dsn, $username, $password, array(PDO::MYSQL_ATTR_INIT_COMMAND => "SET NAMES 'utf8'"));
    $pdo ->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch (PDOException $e) {
    echo 'Connection failed: ' . $e->getMessage();
}

include 'session.php';

$loader = new Twig_Loader_Filesystem(dirname(__FILE__).'/templates');
$twig = new Twig_Environment($loader, array(
    'cache' => dirname(__FILE__).'/cache',
));
$twig->addGlobal('logged_in', is_logged_in());
$twig->addGlobal('display_name', $_SESSION['display_name']);
$twig->addGlobal('account_type', $_SESSION['account_type']);
$msg = array();