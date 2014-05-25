<?php
$testing = false;
$server = 'productive';

if ($server == 'testing') {
    $server = "localhost";
    $username = "root";
    $password = "yourPassword";
    $dbname = 'write-math';   // Database NAME
} elseif ($server == 'productive') {
    $server = "example.com";
    $username = "example_user";
    $password = "asfasdf";
    $dbname = 'example_db';   // Database NAME
} elseif ($server == 'student') {
    $server = "mysql.student.kit.edu";
    $username = "u-kuerzel";
    $password = "asdfasdf";
    $dbname = 'u-kuerzel_writemath';   // Database NAME
    // mysql --host=mysql.student.kit.edu --user=uaeto --password 
    // mysql --ssl-ca=/usr/common/machine/etc/X.509/all.crt --ssl-verify-server-cert --host=mysql.student.kit.edu --user=u-kuerzel --password
}
?>