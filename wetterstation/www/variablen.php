<?php
	require_once("dbconnect.php");
	require_once("Tabellen_ermitteln.php");
	require_once("datensatz_einlesen.php");
?>

<link href="Startseite.css" type="text/css" rel="stylesheet">

<script type="text/javascript">
	
var datensatz_temp = new Array("<?php echo $tabellenanzahl?>"-1);
var datensatz_hum = new Array("<?php echo $tabellenanzahl?>"-1);
var datensatz_pres = new Array("<?php echo $tabellenanzahl?>"-1); 
var datensatz_time = new Array("<?php echo $tabellenanzahl?>"-1);
var datensatz_date = new Array("<?php echo $tabellenanzahl?>"-1);          	

function Variablen_umschreiben () {
	<?php
		$zeilenanzahl=0;
		for($k=0; $k<$tabellenanzahl; $k++)
		{	
		
			$zeilenanzahl=0;
			foreach($datensatz_messungen[$k] as $zeilen)
			{
				$zeilenanzahl=$zeilenanzahl+1;
			}
	?>
			datensatz_temp["<?php echo $k?>"] = new Array("<?php echo $zeilenanzahl?>"-1);
			datensatz_hum["<?php echo $k?>"] = new Array("<?php echo $zeilenanzahl?>"-1);
			datensatz_pres["<?php echo $k?>"] = new Array("<?php echo $zeilenanzahl?>"-1);
			datensatz_time["<?php echo $k?>"] = new Array("<?php echo $zeilenanzahl?>"-1);
			datensatz_date["<?php echo $k?>"] = new Array("<?php echo $zeilenanzahl?>"-1);
	<?php
			for($l=0; $l<$zeilenanzahl; $l++)
			{ 
	?>
			datensatz_temp["<?php echo $k?>"]["<?php echo $l?>"] = "<?php echo $datensatz_messungen[$k][$l]->temperature;?>";
			datensatz_hum["<?php echo $k?>"]["<?php echo $l?>"] = "<?php echo $datensatz_messungen[$k][$l]->humidity;?>";
			datensatz_pres["<?php echo $k?>"]["<?php echo $l?>"] = "<?php echo $datensatz_messungen[$k][$l]->pressure;?>";
			datensatz_time["<?php echo $k?>"]["<?php echo $l?>"] = "<?php echo $datensatz_messungen[$k][$l]->time;?>";
			datensatz_date["<?php echo $k?>"]["<?php echo $l?>"] = "<?php echo $datensatz_messungen[$k][$l]->date;?>";
	<?php
			}
		}	
	?>

}

</script>
