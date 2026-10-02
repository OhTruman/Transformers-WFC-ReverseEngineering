# Run WfcQuery.java read-only against the RE-Workspace Ghidra snapshot.
# usage: powershell -File tools\wfcq.ps1 <queries.txt> <out.txt>
param($q, $o)
$R = 'F:\Transformers Rebuild\RE-Workspace'
& 'F:\Transformers Rebuild\ghidra_12.1.4_PUBLIC\support\analyzeHeadless.bat' "$R\work\ghidra-snapshot" WFC-Rebuild -process default.xex -readOnly -noanalysis -scriptPath "$R\tools\ghidra_scripts" -postScript WfcQuery.java $q $o *> "$o.log"
