<?php
$db = "martinbu_konjugaattori";//Your database name
$dbu = "martinbu_user";//Your database username
$dbp = "8oV0OlOEIQS7l2L1ta";//Your database users' password
$host = "localhost";//MySQL server - usually localhost

$dblink = mysqli_connect($host,$dbu,$dbp,$db);

if(isset($_GET['name']) && isset($_GET['password'])){
$name = mysqli_real_escape_string($dblink,$_GET['name']);
$password = mysqli_real_escape_string($dblink,$_GET['password']);

$sql = mysqli_query($dblink, "REPLACE INTO `$db`.`passwords` (`name`,`password`) VALUES ('$name','$password');");

if($sql){
echo 'Success'; 
}else{
echo 'Error';
}
}else{
echo "Add ?name=NAME_HERE&password=1337 to the tags.";
}

mysqli_close($dblink);
?>