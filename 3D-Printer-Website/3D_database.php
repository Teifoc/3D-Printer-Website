<?php
    $host = 'database-1.c8eew8ixqxd2.eu-north-1.rds.amazonaws.com';
    $username = 'Wxz';
    $password = 'Zhenzz021127.';
    $dbname = 'website_3Dprint';

    // 创建数据库连接
    $conn = new mysqli($host, $username, $password, $dbname);

    // 检查数据库连接是否成功
    if ($conn->connect_error) {
        die("连接失败: " . $conn->connect_error);
    }
    echo "连接成功";
?>
