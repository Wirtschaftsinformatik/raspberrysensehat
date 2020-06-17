<?php
	require_once("dbconnect.php");
	require_once("Tabellen_ermitteln.php");
	require_once("datensatz_einlesen.php");
?>

<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8" />
	<meta name="viewport" content="width=device-width, initial-scale=1.0" />
	<link rel="stylesheet" type="text/css" href="WetterstationStyle.css" media="screen" />
	<title>Karte mit den Koordinaten der Messungen</title>
</head>

<body>

<h1>Karte mit den Koordinaten der Messungen</h1>

<link	rel="stylesheet" href="https://unpkg.com/leaflet@1.5.1/dist/leaflet.css"
		integrity="sha512-xwE/Az9zrjBIphAcBb3F6JVqxf46+CDLwfLMHloNu6KEQCAWi6HcDUbeOfBIptF7tcCzusKFjFw2yuvEpDL9wQ=="
		crossorigin=""
	/>
   
<script src="https://unpkg.com/leaflet@1.5.1/dist/leaflet.js"
		integrity="sha512-GffPMF3RvMeYyc1LWMHtK8EbPv0iNZ8/oTtHPx9/cc2ILxQ+u905qIwdpULaqDkyBKgOaB57QTMg7ztg8Jm2Og=="
		crossorigin=""
	></script>
	
<div id="mapid"></div>


<script type="text/javascript">
		
			var mymap = L.map('mapid').setView([50.927054,11.5892372], 10); 
			L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}', {
			attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
			maxZoom: 18,
			id: 'mapbox.streets',
			accessToken: 'pk.eyJ1IjoidGVub3ZpYyIsImEiOiJjangzNGZsMTgwOGZtM3pxcnRiZGhjemh6In0.TSHxKh2PN5riOJdyfSJ1UQ'
			}).addTo(mymap);
		
</script>


<script type="text/javascript">
	<?php
		$zeilenanzahl=0;
		for($k=0; $k<$tabellenanzahl; $k++)
		{	
		
			$zeilenanzahl=0;
			foreach($datensatz_messungen[$k] as $zeilen)
			{
				$zeilenanzahl=$zeilenanzahl+1;
			}
			for($l=0; $l<$zeilenanzahl; $l++)
			{
				$longitud = $datensatz_messungen[$k][$l]->longitude;
				$latitud = $datensatz_messungen[$k][$l]->latitude;
				$dat = $datensatz_messungen[$k][$l]->date;
				$tim = $datensatz_messungen[$k][$l]->time;
	?>
				var longi = parseFloat("<?php echo $longitud?>");
				if (longi > -1) {
					var marker = L.marker(["<?php echo $latitud?>","<?php echo $longitud?>"]).addTo(mymap);
					marker.bindPopup("<?php echo $dat." ".$tim?>").openPopup;
				}
	<?php
			}
		}	
	?>
</script>

</body>
</html>