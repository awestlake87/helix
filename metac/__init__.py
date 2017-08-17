
import llvmlite.binding as llvm

def init_metac():
    llvm.initialize()
    llvm.initialize_native_target()
    llvm.initialize_native_asmprinter()
