#!/bin/sh
# Run WfcQuery.java read-only against the RE-Workspace Ghidra snapshot.
# usage: tools/wfcq.sh queries.txt out.txt
R="F:/Transformers Rebuild/RE-Workspace"
"F:/Transformers Rebuild/ghidra_12.1.4_PUBLIC/support/analyzeHeadless.bat" "$R/work/ghidra-snapshot" WFC-Rebuild \
  -process default.xex -readOnly -noanalysis -scriptPath "$R/tools/ghidra_scripts" \
  -postScript WfcQuery.java "$(cygpath -w "$1")" "$(cygpath -w "$2")" > "$2.log" 2>&1
tail -3 "$2.log"
