rem This script parses xmls files and produces a params.json file in the selected folders. 
rem
rem to make it work, open the explorer, highlight projects you want to analyze with
rem IsoQuant, right click on any of them and select SendTo/_projectize
python D:\ms_soft\lab_scripts\projectizer2\projectizer2\xmls2jsons.py %* -v
@echo off
pause
