// Read-only: list functions whose instructions use ALL of a set of memory displacements (PPC d(rA) operands),
// optionally also requiring an immediate constant somewhere in the function.
// Usage (headless -readOnly): -postScript WfcDispScan.java <out.txt> <hexdisp,hexdisp,...> [hexconst,...]
//@category WFC
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.*;
import ghidra.program.model.scalar.Scalar;
import java.io.*;
import java.util.*;

public class WfcDispScan extends GhidraScript {
    @Override
    public void run() throws Exception {
        String[] a = getScriptArgs();
        PrintWriter out = new PrintWriter(new FileWriter(a[0]));
        Set<Long> want = new HashSet<>();
        for (String s : a[1].split(",")) want.add(Long.parseLong(s.replace("0x", ""), 16));
        Set<Long> consts = new HashSet<>();
        if (a.length > 2) for (String s : a[2].split(",")) consts.add(Long.parseLong(s.replace("0x", ""), 16));
        Listing L = currentProgram.getListing();
        int n = 0;
        for (Function f : L.getFunctions(true)) {
            Set<Long> seen = new HashSet<>(); Set<Long> cseen = new HashSet<>();
            for (Instruction ins : L.getInstructions(f.getBody(), true)) {
                for (int i = 0; i < ins.getNumOperands(); i++) {
                    for (Object o : ins.getOpObjects(i)) {
                        if (o instanceof Scalar) {
                            long v = ((Scalar) o).getUnsignedValue() & 0xffffffffL;
                            if (want.contains(v)) seen.add(v);
                            if (consts.contains(v)) cseen.add(v);
                        }
                    }
                }
            }
            if (seen.size() == want.size() && cseen.size() == consts.size()) {
                out.printf("%s %s size=%d%n", f.getEntryPoint(), f.getName(), f.getBody().getNumAddresses());
                n++;
            }
        }
        out.println("matches " + n);
        out.close();
    }
}
