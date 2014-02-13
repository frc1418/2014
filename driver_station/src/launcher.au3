;
; Utility AutoIt script to launch the dashboard
;
; -> The FRC Driver Station will only launch predetermined executable files,
;    so to get around this we compile this AutoIt script to an exe, and we
; 	 put it in the right spot (c:\Program Files\FRC Dashboard\dashboard.exe),
;    then this dashboard program gets launched whenever the driver station
;    is launched. 
;

$python = "C:\Python27\python.exe"
;$python = "C:\Python27\pythonw.exe"
$dir = "C:\1418\2014\driver_station\src"
$options = "--robot-ip 10.14.18.2 --front-camera-ip 10.14.18.11 --back-camera-ip 10.14.18.12 --competition --log-images"

Run($python & " " & $dir & "\main.py " & $options, $dir)
