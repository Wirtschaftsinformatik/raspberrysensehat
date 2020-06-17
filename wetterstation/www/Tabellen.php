<?php
	require_once("dbconnect.php");
	require_once("Tabellen_ermitteln.php");
	require_once("datensatz_einlesen.php");
?>

<!DOCTYPE html>

<html lang="de">
	<head>
		<meta charset="utf-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1.0" />
		<link rel="stylesheet" type="text/css" href="WetterstationStyle.css" media="screen" />
		<title>Tabellen der Messungen</title>
	</head>
	<body>


<div data-role="page" id="headline" data-theme="b">
	<div data-role="main" class="ui-content">
		<h1><u>Tabellen der Messungen</u></h1>
	</div>
</div>

<?php
	for($j=0; $j<$tabellenanzahl; $j++) { ?>
		<?php echo "<h2>Messung vom " .$datensatz_messungen[$j][0]->date . " "  .$datensatz_messungen[$j][0]->time . "</h2>"; ?>
		<div data-role="main" class="ui-content" style="overflow-x:auto;"> 
		
		<table id="Messung" data-role="table" class="ui-responsive" data-mode="columntoggle" data-column-btn-text="Spalten"  >
			<thead>
			<tr>
				<th>Datum</th>
				<th>Zeit</th>
				<th>Temperatur</th>
				<th>Luftdruck</th>
				<th>Luftfeuchtigkeit</th>
				<th>Längengrad</th>
				<th>Breitengrad</th>
			</tr>
			</thead>
		<tbody>
<?php
		foreach ($datensatz_messungen[$j] as $inhalt_messungen) {
?>
			<tr>
				<td>
					<?php echo $inhalt_messungen->date; ?>
				</td>
				<td>
					<?php echo $inhalt_messungen->time; ?>
				</td>
				<td>
					<?php echo $inhalt_messungen->temperature; ?>
				</td>
				<td>
					<?php echo $inhalt_messungen->pressure; ?>
				</td>   
				<td>
					<?php echo $inhalt_messungen->humidity; ?>
				</td> 
				<td>
					<?php echo $inhalt_messungen->longitude; ?>
				</td> 
				<td>
					<?php echo $inhalt_messungen->latitude; ?>
				</td> 
			</tr>
		<?php
		}
		?>
      </tbody>
    </table>
		</div>
<?php
	}
?>
</body>
</html>