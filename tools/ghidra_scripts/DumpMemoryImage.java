// Dumps every initialized memory block of the current program to <outDir>/<block>.bin
// plus blocks.tsv (name, start, size) so the image can be scanned offline.
// Usage (headless): -postScript DumpMemoryImage.java <outDir>
//@category WFC

import ghidra.app.script.GhidraScript;
import ghidra.program.model.mem.MemoryBlock;
import java.io.*;

public class DumpMemoryImage extends GhidraScript {
    @Override
    public void run() throws Exception {
        String[] args = getScriptArgs();
        File out = new File(args.length > 0 ? args[0] : "image");
        out.mkdirs();
        try (PrintWriter idx = new PrintWriter(new File(out, "blocks.tsv"), "UTF-8")) {
            idx.println("name\tstart\tsize\texec");
            for (MemoryBlock b : currentProgram.getMemory().getBlocks()) {
                if (!b.isInitialized()) continue;
                byte[] buf = new byte[(int) b.getSize()];
                b.getBytes(b.getStart(), buf);
                String fn = b.getName().replaceAll("[^A-Za-z0-9_]", "_") + ".bin";
                try (FileOutputStream fo = new FileOutputStream(new File(out, fn))) { fo.write(buf); }
                idx.printf("%s\t0x%08x\t%d\t%b%n", fn, b.getStart().getOffset(), b.getSize(), b.isExecute());
            }
        }
        println("Dumped memory image to " + out);
    }
}
