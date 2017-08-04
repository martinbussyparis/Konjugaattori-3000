<?php
header('Access-Control-Allow-Origin: *');

$host="localhost"; // Host name 
$username="martinbu_user"; // Mysql username 
$password="8oV0OlOEIQS7l2L1ta"; // Mysql password 
$db_name="martinbu_konjugaattori"; // Database name 
$tbl_name="scores"; // Table name

// Connect to server and select database.
$link = mysqli_connect("$host", "$username", "$password", "$db_name");

// Retrieve data from database 
$sql="SELECT * FROM scores ORDER BY name DESC LIMIT 100";
$result=mysqli_query($link,$sql);

// Start looping rows in mysql database.
while($rows=mysqli_fetch_array($result)){
echo $rows['name'] . "_" . $rows['pool00'] . "|" . $rows['pool01'] . "|" . $rows['pool02'] . "|" . $rows['pool03'] . "_";

// close while loop 
}

// close MySQL connection 
mysqli_close($link);
?>