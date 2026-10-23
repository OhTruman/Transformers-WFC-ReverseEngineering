// Batch read-only query tool for the WFC snapshot project (used while ReVa is unavailable).
// Usage (headless, -readOnly): -postScript WfcQuery.java <queries.txt> <out.txt>
// Query lines:
//   refs <addr>            references to addr (with containing function)
//   decomp <addr>          decompile function containing addr
//   strs <substring>       defined strings containing substring, plus refs to each
//   func <addr>            function name/body range/callers/callees
//   asm <addr> <count>     disassembly listing
//@category WFC

import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.*;
import ghidra.program.model.address.*;
import ghidra.program.model.listing.*;
import ghidra.program.model.symbol.*;
import ghidra.program.model.data.StringDataInstance;
import java.io.*;
import java.nio.file.*;
import java.util.*;

public class WfcQuery extends GhidraScript {
    PrintWriter out;
    DecompInterface di;

    Address A(String s) { return toAddr(Long.parseLong(s.replace("0x", ""), 16)); }

    String fname(Address a) {
        Function f = getFunctionContaining(a);
        return f == null ? "<nofunc>" : f.getName() + "@" + f.getEntryPoint();
    }

    void refs(Address a) {
        for (Reference r : getReferencesTo(a))
            out.printf("  ref %s %s from %s in %s%n", a, r.getReferenceType(), r.getFromAddress(), fname(r.getFromAddress()));
    }

    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        List<String> qs = Files.readAllLines(Paths.get(args[0]));
        out = new PrintWriter(new FileWriter(args[1]));
        di = new DecompInterface();
        di.openProgram(currentProgram);
        Listing L = currentProgram.getListing();
        for (String q : qs) {
            q = q.trim();
            if (q.isEmpty() || q.startsWith("#")) continue;
            String[] p = q.split("\\s+", 3);
            out.println("=== " + q);
            try {
                switch (p[0]) {
                case "refs": refs(A(p[1])); break;
                case "func": {
                    Function f = getFunctionContaining(A(p[1]));
                    if (f == null) { out.println("  no function"); break; }
                    out.printf("  %s entry=%s body=%s%n", f.getName(), f.getEntryPoint(), f.getBody());
                    for (Function c : f.getCallingFunctions(monitor)) out.println("  caller " + c.getName() + "@" + c.getEntryPoint());
                    for (Function c : f.getCalledFunctions(monitor)) out.println("  callee " + c.getName() + "@" + c.getEntryPoint());
                    refs(f.getEntryPoint());
                    break;
                }
                case "decomp": {
                    Function f = getFunctionContaining(A(p[1]));
                    if (f == null) { out.println("  no function"); break; }
                    DecompileResults r = di.decompileFunction(f, 120, monitor);
                    out.println(r.decompileCompleted() ? r.getDecompiledFunction().getC() : "  FAILED " + r.getErrorMessage());
                    break;
                }
                case "asm": {
                    Address a = A(p[1]);
                    int n = p.length > 2 ? Integer.parseInt(p[2]) : 40;
                    Instruction ins = L.getInstructionAt(a);
                    if (ins == null) ins = L.getInstructionAfter(a);
                    for (int i = 0; i < n && ins != null; i++, ins = ins.getNext()) {
                        StringBuilder sb = new StringBuilder();
                        for (Reference r : ins.getReferencesFrom()) sb.append(" ->").append(r.getToAddress());
                        out.printf("  %s  %s%s%n", ins.getAddress(), ins, sb);
                    }
                    break;
                }
                case "strs": {
                    String needle = q.substring(5).trim();
                    DataIterator it = L.getDefinedData(true);
                    int n = 0;
                    while (it.hasNext() && n < 400) {
                        Data d = it.next();
                        if (!d.hasStringValue()) continue;
                        Object v = d.getValue();
                        if (v == null || !v.toString().contains(needle)) continue;
                        n++;
                        out.printf("  str %s \"%s\"%n", d.getAddress(), v);
                        refs(d.getAddress());
                    }
                    break;
                }
                case "dis": {
                    // disassemble undefined bytes in memory only (project is opened -readOnly; never saved)
                    Address a = A(p[1]);
                    int n = p.length > 2 ? Integer.parseInt(p[2]) : 40;
                    new ghidra.app.cmd.disassemble.DisassembleCommand(a, null, true).applyTo(currentProgram, monitor);
                    Instruction ins = L.getInstructionAt(a);
                    for (int i = 0; i < n && ins != null; i++, ins = ins.getNext())
                        out.printf("  %s  %s%n", ins.getAddress(), ins);
                    break;
                }
                case "rawdis": {
                    // linear disassembly, one instruction at a time, no flow following (in memory only)
                    Address a = A(p[1]);
                    int n = p.length > 2 ? Integer.parseInt(p[2]) : 40;
                    for (int i = 0; i < n; i++, a = a.add(4)) {
                        Instruction ins = L.getInstructionAt(a);
                        if (ins == null) {
                            new ghidra.app.cmd.disassemble.DisassembleCommand(new AddressSet(a, a.add(3)), null, false).applyTo(currentProgram, monitor);
                            ins = L.getInstructionAt(a);
                        }
                        out.printf("  %s  %s%n", a, ins == null ? "??" : ins.toString());
                    }
                    break;
                }
                case "opscan": {
                    // instructions whose text contains a displacement / immediate, optionally filtered by mnemonic prefix
                    String needle = p[1].toLowerCase(), mn = p.length > 2 ? p[2].toLowerCase() : "";
                    int hits = 0;
                    for (Instruction ins : L.getInstructions(true)) {
                        String s = ins.toString().toLowerCase();
                        if (!s.startsWith(mn) || !s.contains(needle)) continue;
                        Function f = currentProgram.getFunctionManager().getFunctionContaining(ins.getAddress());
                        out.printf("  %s  %s  in %s%n", ins.getAddress(), ins, f == null ? "?" : f.getEntryPoint());
                        if (++hits > 400) break;
                    }
                    break;
                }
                case "funcs": {
                    // function entries in [start, end) with body size and caller count
                    Address s = A(p[1]), e = A(p[2]);
                    for (Function f : currentProgram.getFunctionManager().getFunctions(s, true)) {
                        if (f.getEntryPoint().compareTo(e) >= 0) break;
                        out.printf("  %s  size=%d  callers=%d%n", f.getEntryPoint(), f.getBody().getNumAddresses(),
                                   f.getCallingFunctions(monitor).size());
                    }
                    break;
                }
                case "decomprange": {
                    // decompile every function entry in [start, end)
                    Address s = A(p[1]), e = A(p[2]);
                    ghidra.app.decompiler.DecompInterface di = new ghidra.app.decompiler.DecompInterface();
                    di.openProgram(currentProgram);
                    for (Function f : currentProgram.getFunctionManager().getFunctions(s, true)) {
                        if (f.getEntryPoint().compareTo(e) >= 0) break;
                        ghidra.app.decompiler.DecompileResults r = di.decompileFunction(f, 60, monitor);
                        out.printf("### %s%n%s%n", f.getEntryPoint(),
                                   r.decompileCompleted() ? r.getDecompiledFunction().getC() : "(failed)");
                    }
                    di.dispose();
                    break;
                }
                case "findword": {
                    // every initialized-memory location holding the given big-endian u32 (e.g. vtable slots)
                    int v = (int) Long.parseLong(p[1].replace("0x", ""), 16);
                    byte[] pat = {(byte) (v >>> 24), (byte) (v >>> 16), (byte) (v >>> 8), (byte) v};
                    Address at = currentProgram.getMinAddress();
                    int hits = 0;
                    while (at != null && hits < 64) {
                        at = currentProgram.getMemory().findBytes(at, pat, null, true, monitor);
                        if (at == null) break;
                        out.printf("  %s%n", at);
                        hits++;
                        at = at.add(1);
                    }
                    break;
                }
                case "words": {
                    // raw big-endian u32 words (vtables, data tables)
                    Address a = A(p[1]);
                    int n = p.length > 2 ? Integer.parseInt(p[2]) : 16;
                    for (int i = 0; i < n; i++, a = a.add(4))
                        out.printf("  %s  %08x%n", a, currentProgram.getMemory().getInt(a));
                    break;
                }
                case "named": {
                    // user-named functions (prior manual labels), optional substring filter
                    String needle = p.length > 1 ? p[1].toLowerCase() : "";
                    for (Function f : currentProgram.getFunctionManager().getFunctions(true)) {
                        String n = f.getName();
                        if (n.startsWith("FUN_") || n.startsWith("Function_") || n.startsWith("thunk_") || n.startsWith("LAB_")) continue;
                        if (f.getSymbol().getSource() == SourceType.DEFAULT || f.getSymbol().getSource() == SourceType.ANALYSIS) continue;
                        if (!needle.isEmpty() && !n.toLowerCase().contains(needle)) continue;
                        out.printf("  %s %s%n", f.getEntryPoint(), n);
                    }
                    break;
                }
                case "comments": {
                    String needle = p.length > 1 ? p[1].toLowerCase() : "";
                    for (int t : new int[]{CodeUnit.PLATE_COMMENT, CodeUnit.PRE_COMMENT, CodeUnit.EOL_COMMENT, CodeUnit.POST_COMMENT}) {
                        AddressIterator it = L.getCommentAddressIterator(t, currentProgram.getMemory(), true);
                        while (it.hasNext()) {
                            Address a = it.next();
                            String c = L.getComment(t, a);
                            if (c == null || (!needle.isEmpty() && !c.toLowerCase().contains(needle))) continue;
                            out.printf("  %s [%d] %s%n", a, t, c.replace("\n", " | "));
                        }
                    }
                    break;
                }
                case "bookmarks": {
                    java.util.Iterator<ghidra.program.model.listing.Bookmark> it = currentProgram.getBookmarkManager().getBookmarksIterator();
                    while (it.hasNext()) {
                        ghidra.program.model.listing.Bookmark b = it.next();
                        if (b.getTypeString().equals("Analysis") || b.getTypeString().equals("Error") || b.getTypeString().equals("Warning")) continue;
                        out.printf("  %s %s %s %s%n", b.getAddress(), b.getTypeString(), b.getCategory(), b.getComment());
                    }
                    break;
                }
                case "labels": {
                    String needle = p.length > 1 ? p[1].toLowerCase() : "";
                    SymbolIterator it = currentProgram.getSymbolTable().getAllSymbols(true);
                    while (it.hasNext()) {
                        Symbol s = it.next();
                        if (s.getSource() != SourceType.USER_DEFINED && s.getSource() != SourceType.IMPORTED) continue;
                        if (!needle.isEmpty() && !s.getName().toLowerCase().contains(needle)) continue;
                        out.printf("  %s %s %s%n", s.getAddress(), s.getSymbolType(), s.getName(true));
                    }
                    break;
                }
                default: out.println("  unknown");
                }
            } catch (Exception e) { out.println("  ERR " + e); }
            out.flush();
        }
        out.close();
    }
}
