<?php
$db = mysqli_connect("localhost", "pi", "raspberry", "SensorHat");
if(!$db)
{
  exit("Verbindungsfehler: ".mysqli_connect_error());
}
?>