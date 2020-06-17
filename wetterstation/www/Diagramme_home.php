<?php
	require_once("dbconnect.php");
	require_once("Tabellen_ermitteln_home.php");
	require_once("datensatz_einlesen.php");
	require_once("variablen.php");
?>

<!DOCTYPE html>
<html>
<head>
	<meta charset="utf-8" />
	<meta name="viewport" content="width=device-width, initial-scale=1.0" />
	<link rel="stylesheet" type="text/css" href="WetterstationStyle.css" media="screen" />
	<title>Diagramme der Messungen</title>
</head>

<body>

<div id = "ueberschrift"><h1><u> Diagramme der Messungen</u><h1></div>

<script
    src = "https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.4.0/Chart.bundle.min.js">
</script>

<div id="diagramme"></div>

<script>
	Variablen_umschreiben();
	var CreateDiv = document.getElementById('diagramme');
	var Fragment = document.createDocumentFragment();
	for(var i=0; i<"<?php echo $tabellenanzahl?>"; i++){
		var newDiv = document.createElement('div');
		newDiv.id = "x"+i;
		newDiv.style = "margin-left:auto;margin-right:auto;width:800px;"
		var newText = document.createElement('h2');
		newText.id = "ueberschrift" + i;
		var node = document.createTextNode("Messung vom " + datensatz_date[i][0] + " " + datensatz_time[i][0]);
		newText.appendChild(node);
		var newCanvas = document.createElement('canvas');
		newCanvas.id = "myChart" + i;
		var newCanvas2 = document.createElement('canvas');
		newCanvas2.id = "myChart_bar" + i;
		newDiv.appendChild(newText);
		newDiv.appendChild(newCanvas);
		newDiv.appendChild(newCanvas2);
		Fragment.appendChild(newDiv);
	}
CreateDiv.appendChild(Fragment);

</script>

<script>

for(var i=0; i<"<?php echo $tabellenanzahl?>";i++){
var string = "myChart" + i;
var myChartObject = document.getElementById(string);
var chart = new Chart(myChartObject,{
  type: 'line',
  data: {
    labels: datensatz_time[i],
    datasets: [{
        label: "Temperatur in Grad Celsius",
        backgroundColor: 'rgba(65,105,225,0.3)',
        borderColor: 'rgba(65,105,225,1)',
        data: datensatz_temp [i]
   },{
        label: "Luftfeuchtigkeit in %",
        backgroundColor: 'rgba(255,0,0,0.4)',
        borderColor: 'rgba(255,0,0.1,)',
        data: datensatz_hum[i],
   }]
  }
});

var myChartObject = document.getElementById("myChart_bar"+i)
//Y-Achse
var chart = new Chart(myChartObject,{
  type: 'bar',
  data: {
    labels: datensatz_time[i],
    datasets: [{
        label: "Luftdruck in hPa",
        backgroundColor: 'rgba(70,105,225,0.3)',
        borderColor: 'rgba(100,100,255,1)',
        data: datensatz_pres[i]
   }]
  },
  options: {
    scales: {
      yAxes : [{
        ticks: {
          beginAtZero: true 
        }
      }]
    }
  }
}); 



}
</script>

</body>
</html>
