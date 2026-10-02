# ReVa / Ghidra Claude lane

Project root: F:\Transformers Rebuild\RE-Workspace. Start a fresh conversation here; subsequently use claude.cmd --continue from this directory. Never resume a legacy conversation from F:\Transformers Rebuild for this lane.

- Write project files only under F:\Transformers Rebuild\RE-Workspace, including analysis notes, scripts, logs, and exports.
- Read F:\Transformers Rebuild\Game Dump in place, read-only. Never modify, rename, move, delete, or copy the dump wholesale.
- Read existing Ghidra projects, Rebuild documentation, AssetTools manifests, and ExtractedAssets in place as needed. Do not modify a Ghidra project outside RE-Workspace; any writable analysis project must live under RE-Workspace.
- Do not write to AssetTools, ExtractedAssets, or any Rebuild lane. Do not duplicate the large Game Dump or ExtractedAssets folders or create links that bypass write boundaries.
- Do not delete or alter old Claude sessions. Do not launch, resume, stop, or coordinate other lanes or their background agents.
- Use only the intended ReVa/Ghidra connection. Do not restart shared servers, change their configuration, or run concurrent mutating analysis against a project used by another lane.
