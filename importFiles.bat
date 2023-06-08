@echo off
::recursively detect the existing imported files and run script on them 
D:\ghidra_10.3_PUBLIC\support\analyzeHeadless D:\testproject BatchProcess -scriptPath D:\ghidra_10.3_PUBLIC\Ghidra\Features\BridgeRelated\ghidra_scripts -preScript ExportFunction.py -process -recursive
