// Read-only: disassemble + create a function at an address IN MEMORY ONLY (project opened -readOnly; never saved),
// then decompile it. For code Ghidra never turned into a function.
// Usage (headless -readOnly): -postScript WfcDecompAt.java <out.txt> <hexaddr> [<hexaddr> ...]
//@category WFC
import ghidra.app.script.GhidraScript;
import ghidra.app.decompiler.*;
import ghidra.app.cmd.disassemble.DisassembleCommand;
import ghidra.app.cmd.function.CreateFunctionCmd;
import ghidra.program.model.address.*;
import ghidra.program.model.listing.*;
import java.io.*;

public class WfcDecompAt extends GhidraScript {
    @Override
    public void run() throws Exception {
        String[] a = getScriptArgs();
        PrintWriter out = new PrintWriter(new FileWriter(a[0]));
        // in memory only (-readOnly, never saved): many PPC callees are wrongly flagged no-return
        int cleared = 0;
        FunctionIterator all = currentProgram.getFunctionManager().getFunctions(true);
        while (all.hasNext()) { Function g = all.next(); if (g.hasNoReturn()) { g.setNoReturn(false); cleared++; } }
        out.println("  cleared noreturn on " + cleared + " functions (in memory)");
        DecompInterface di = new DecompInterface();
        di.openProgram(currentProgram);
        for (int i = 1; i < a.length; i++) {
            // optional explicit body: <hexaddr>:<hexsize>
            if (a[i].contains(":")) {
                String[] p = a[i].split(":");
                Address st = toAddr(Long.parseLong(p[0], 16));
                long sz = Long.parseLong(p[1], 16);
                AddressSet body = new AddressSet(st, st.add(sz - 1));
                new DisassembleCommand(body, null, true).applyTo(currentProgram, monitor);
                InstructionIterator bit = currentProgram.getListing().getInstructions(body, true);
                while (bit.hasNext()) {
                    Instruction ins = bit.next();
                    for (Address t : ins.getFlows()) {
                        Function cf = getFunctionAt(t);
                        if (cf == null) cf = getFunctionContaining(t);
                        if (cf != null && cf.hasNoReturn()) { out.println("  clearing noreturn " + cf.getName()); cf.setNoReturn(false); }
                    }
                }
                Function old = getFunctionContaining(st);
                if (old != null && old.getEntryPoint().equals(st)) removeFunction(old);
                new CreateFunctionCmd("fill_" + p[0], st, body, ghidra.program.model.symbol.SourceType.USER_DEFINED)
                    .applyTo(currentProgram, monitor);
                Function f2 = getFunctionAt(st);
                out.println("=== decompat " + a[i] + "  body " + (f2 == null ? "none" : f2.getBody().toString()));
                if (f2 == null) continue;
                DecompileResults r2 = di.decompileFunction(f2, 600, monitor);
                out.println(r2.decompileCompleted() ? r2.getDecompiledFunction().getC() : "  FAILED " + r2.getErrorMessage());
                continue;
            }
            Address ad = toAddr(Long.parseLong(a[i], 16));
            out.println("=== decompat " + a[i]);
            Function f = getFunctionAt(ad);
            if (f == null) {
                new DisassembleCommand(ad, null, true).applyTo(currentProgram, monitor);
                // in-memory only: callees wrongly flagged no-return truncate the body; clear the flag
                // on every call target within the next 0x4000 bytes, then (re)disassemble and create.
                for (int pass = 0; pass < 3; pass++) {
                    InstructionIterator it = currentProgram.getListing().getInstructions(ad, true);
                    while (it.hasNext()) {
                        Instruction ins = it.next();
                        if (ins.getAddress().subtract(ad) > 0x4000) break;
                        if (ins.getFlowOverride() != ghidra.program.model.listing.FlowOverride.NONE) {
                            out.println("  clearing flow override at " + ins.getAddress());
                            ins.setFlowOverride(ghidra.program.model.listing.FlowOverride.NONE);
                        }
                        for (Address t : ins.getFlows()) {
                            Function cf = getFunctionAt(t);
                            if (cf != null && cf.hasNoReturn()) { out.println("  clearing noreturn " + cf.getName()); cf.setNoReturn(false); }
                        }
                        if (ins.getMnemonicString().startsWith("bl") && ins.getFallThrough() == null)
                            out.println("  call without fallthrough at " + ins.getAddress());
                        if (ins.getFallThrough() != null && getInstructionAt(ins.getFallThrough()) == null)
                            new DisassembleCommand(ins.getFallThrough(), null, true).applyTo(currentProgram, monitor);
                    }
                }
                new CreateFunctionCmd(ad).applyTo(currentProgram, monitor);
                f = getFunctionAt(ad);
            }
            if (f == null) { out.println("  could not create function"); continue; }
            out.println("  body " + f.getBody());
            DecompileResults r = di.decompileFunction(f, 300, monitor);
            out.println(r.decompileCompleted() ? r.getDecompiledFunction().getC() : "  FAILED " + r.getErrorMessage());
        }
        out.close();
    }
}
