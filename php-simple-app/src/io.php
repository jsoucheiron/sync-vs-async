<?php
$response = file_get_contents("http://nginx/" . $_GET['delay']);

echo "Request finished!";
?>
