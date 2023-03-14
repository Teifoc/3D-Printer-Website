<?php
// 数据库连接参数
$dbhost = "database-1.c8eew8ixqxd2.eu-north-1.rds.amazonaws.com";
$dbport = 3306;
$dbname = "webside_3Dprint";
$dbuser = "Wxz";
$dbpass = "Zhenz021127.";

// 创建连接
$conn = new mysqli($dbhost, $dbuser, $dbpass, $dbname, $dbport);

// 检查连接是否成功
if ($conn->connect_error) {
    die("连接失败: " . $conn->connect_error);
}

// 执行查询语句
$sql = "SELECT * FROM your-table-name-here";
$result = $conn->query($sql);

// 检查查询结果
if ($result->num_rows > 0) {
    // 输出数据
    while($row = $result->fetch_assoc()) {
        echo "ID: " . $row["id"]. " - Name: " . $row["name"]. "<br>";
    }
} else {
    echo "没有结果";
}

// 关闭连接
$conn->close();
?>
