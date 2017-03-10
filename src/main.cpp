#include <iostream>
#include <memory>

#include <meta/ir/context.hpp>
#include <meta/err/exception.hpp>
#include <meta/err/command-line-errors.hpp>

#include <argp.h>

using namespace Meta;

static std::unique_ptr<Ir::Context> s_Compiler;

static int parse_opt(int key, char* arg, struct argp_state* state) {
  switch (key) {

    case 'o':
      s_Compiler->setOutput(arg);
      break;

    case ARGP_KEY_ARG:
      s_Compiler->addUnit(arg);
      break;
  }

  return 0;
}

int main(int argc, char** argv) {
  auto _handleError = [](ErrorCode ec, const char* msg) -> int {
    int ec_int = static_cast<int>(ec);

    switch (ec) {
      case Meta::ErrorCode::NOT_IMPLEMENTED:
        std::cerr << "todo: " << msg << std::endl;
        break;

      case Meta::ErrorCode::COMPILER_BUG:
        std::cerr << "compiler bug: " << msg << std::endl;
        break;

      default:
        std::cerr << "error[" << ec_int << "]: " << msg << std::endl;
    }
    return ec_int;
  };

  try {
    initMetaApi();

    s_Compiler = std::make_unique<Ir::Context>();

    struct argp_option options[] = {
      { "output", 'o', "PATH", 0, "path to output executable [TEMPORARY]" },
      { 0 }
    };
    struct argp argp_instance = { options, parse_opt, "PATH" };

    int result = argp_parse(&argp_instance, argc, argv, 0, 0, 0);

    if (result != 0) {
      throw InvalidCommandLineArgsError("invalid command line arguments");
    }

    s_Compiler->compile();

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
