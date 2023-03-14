<?php
    $host = 'your-database-endpoint.rds.amazonaws.com';
    $username = 'your-username';
    $password = 'your-password';
    $dbname = 'your-database-name';

    // 创建数据库连接
    $conn = new mysqli($host, $username, $password, $dbname);

    // 检查数据库连接是否成功
    if ($conn->connect_error) {
        die("连接失败: " . $conn->connect_error);
    }
    echo "连接成功";
?>
