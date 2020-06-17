<?php
	require_once("dbconnect.php");
	require_once("Tabellen_ermitteln.php");
	require_once("datensatz_einlesen.php");
?>

<?php
	echo "<pre>";
	print_r($datensatz_messungen);
	echo "</pre>";
?>