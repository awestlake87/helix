#include <iostream>

#include <meta/err/index.hpp>

#include <argp.h>

using namespace Meta;

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
  auto _handleError = [](ErrorCode ec, const char* msg) -> int {
    int ec_int = static_cast<int>(ec);
    std::cerr << '[' << ec_int << "]: " << msg << std::endl;
    return ec_int;
  };

  try {
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

    if (result != 0) {
      throw InvalidCommandLineArgsError("invalid command line arguments");
    }

    return result;
  }
  catch (Exception& e) {
    return _handleError(e.getCode(), e.what());
  }
  catch (std::exception& e) {
    return _handleError(ErrorCode::UNKNOWN, e.what());
  }
  catch (...) {
    return _handleError(ErrorCode::UNKNOWN, "an unknown error occurred");
  }
}
