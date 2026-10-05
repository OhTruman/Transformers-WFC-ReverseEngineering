// Read-only: list instructions whose mnemonic starts with a prefix and that use a given displacement,
// inside functions that also use ALL of a set of other displacements.
// Usage (headless -readOnly): -postScript WfcStoreScan.java <out.txt> <mnemonicPrefix> <hexdisp> [hexdisp,...]
//@category WFC
import ghidra.app.script.GhidraScript;
import ghidra.program.model.listing.*;
import ghidra.program.model.scalar.Scalar;
import java.io.*;
import java.util.*;

public class WfcStoreScan extends GhidraScript {
    static boolean uses(Instruction ins, long v) {
        for (int i = 0; i < ins.getNumOperands(); i++)
            for (Object o : ins.getOpObjects(i))
                if (o instanceof Scalar && (((Scalar) o).getUnsignedValue() & 0xffffffffL) == v) return true;
        return false;
    }
    @Override
    public void run() throws Exception {
        String[] a = getScriptArgs();
        PrintWriter out = new PrintWriter(new FileWriter(a[0]));
        String mn = a[1].toLowerCase();
        long disp = Long.parseLong(a[2].replace("0x", ""), 16);
        Set<Long> also = new HashSet<>();
        if (a.length > 3) for (String s : a[3].split(",")) also.add(Long.parseLong(s.replace("0x", ""), 16));
        Listing L = currentProgram.getListing();
        int n = 0;
        for (Function f : L.getFunctions(true)) {
            List<Instruction> hits = new ArrayList<>(); Set<Long> seen = new HashSet<>();
            for (Instruction ins : L.getInstructions(f.getBody(), true)) {
                if (ins.getMnemonicString().toLowerCase().startsWith(mn) && uses(ins, disp)) hits.add(ins);
                for (long v : also) if (uses(ins, v)) seen.add(v);
            }
            if (!hits.isEmpty() && seen.size() == also.size()) {
                for (Instruction ins : hits) out.printf("%s %s @%s: %s%n", f.getEntryPoint(), f.getName(), ins.getAddress(), ins);
                n++;
            }
        }
        out.println("functions " + n);
        out.close();
    }
}
