<?php
	require_once("dbconnect.php");
?>

<?php
	$tabelleninfo = "SHOW TABLES FROM SensorHat";
	if ($info = $db->query($tabelleninfo)) {
		if ($info->num_rows) {
			$tabellenanzahl = $info->num_rows;
			$info->free();
		}
	if ($info = $db->query($tabelleninfo)) {
			while ($db_object = $info->fetch_object()) {
				$datensatz_tabellen[] = $db_object;
			}
		}
	}
	$tabellennamen = array();
	foreach ($datensatz_tabellen as $Namen)
		{
		array_push($tabellennamen, $Namen->Tables_in_SensorHat);
		}
		// tabellenanzahl (int)
		// tabellennamen (array)
?>

