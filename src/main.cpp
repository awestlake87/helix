#include <iostream>

#include <argp.h>

static int parse_opt(int key, char* arg, struct argp_state* state) {
  switch (key) {

    case 'o':
      std::cout << arg << std::endl; //s_Compiler->setOutput(arg);
      break;

    case ARGP_KEY_ARG:
      //s_Compiler->setEntry(arg);
      break;
  }

  return 0;
}

int main(int argc, char** argv) {
  //llvm::InitializeAllTargetInfos();
  //llvm::InitializeAllTargets();
  //llvm::InitializeAllTargetMCs();
  //llvm::InitializeAllAsmParsers();
  //llvm::InitializeAllAsmPrinters();

  struct argp_option options[] = {
    { "output", 'o', "PATH", 0, "path to output executable [TEMPORARY]" },
    { 0 }
  };
  struct argp argp_instance = { options, parse_opt, "PATH" };

  int result = argp_parse(&argp_instance, argc, argv, 0, 0, 0);

  if (result == 0) {
    //s_Compiler->compile();
  }

  return result;
}
