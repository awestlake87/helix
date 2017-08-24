
import llvmlite.binding as llvm

def init_metac():
    llvm.initialize()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()

    llvm.load_library_permanently("/usr/lib/x86_64-linux-gnu/libstdc++.so.6")
