<?php
$db = "martinbu_konjugaattori";//Your database name
$dbu = "martinbu_user";//Your database username
$dbp = "8oV0OlOEIQS7l2L1ta";//Your database users' password
$host = "localhost";//MySQL server - usually localhost

$dblink = mysqli_connect($host,$dbu,$dbp,$db);

if(isset($_GET['name']) && isset($_GET['pool00']) && isset($_GET['pool01']) && isset($_GET['pool02']) && isset($_GET['pool03'])){
$name = mysqli_real_escape_string($dblink,$_GET['name']);
$pool00 = mysqli_real_escape_string($dblink,$_GET['pool00']);
$pool01 = mysqli_real_escape_string($dblink,$_GET['pool01']);
$pool02 = mysqli_real_escape_string($dblink,$_GET['pool02']);
$pool03 = mysqli_real_escape_string($dblink,$_GET['pool03']);

$sql = mysqli_query($dblink, "REPLACE INTO `$db`.`scores` (`name`,`pool00`,`pool01`,`pool02`,`pool03`) VALUES ('$name','$pool00','$pool01','$pool02','$pool03');");

if($sql){
echo 'Success'; 
}else{
echo 'Error';
}
}else{
echo "Add ?name=str&pool00=str&pool01=str&pool02=str&pool03=str to the tags.";
}

mysqli_close($dblink);
?>