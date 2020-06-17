<?php
	require_once("dbconnect.php");
	require_once("Tabellen_ermitteln.php");
?>

<?php
	$datensatz_messungen = array();
	for ($i=0; $i<$tabellenanzahl; $i++)
	{	
		$auslesen = "SELECT * FROM " .$tabellennamen[$i];
		if ($erg = $db->query($auslesen)) {
			if ($erg->num_rows) {
				$messungen_gesamt = $erg->num_rows;
				$erg->free();
			}
		if ($erg = $db->query($auslesen)) {
				while ($messung = $erg->fetch_object()) {
					$neuer_datensatz[] = $messung;
				}
			}
		}
		$erg->free();
		array_push($datensatz_messungen, $neuer_datensatz);
		$neuer_datensatz = array();
		
		
	}
?>