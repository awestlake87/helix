#include <metac/compiler.hpp>

#include <meta/index.hpp>

#include <boost/filesystem.hpp>

using namespace Meta;

namespace fs = boost::filesystem;

void Compiler::addUnit(const Path& path) {
  m_Units.push_back(resolveUnit(path));
}

void Compiler::compile() {
  throw NotImplementedError("Compiler::compile has not been implemented yet");
}

Compiler::Path Compiler::resolveUnit(const Path& path) {
  if (!fs::exists(path)) {
    Path file_path = path;
    file_path += ".meta";
    
    if (!fs::exists(file_path)) {
      throw UnableToResolveFileError(path);
    }
  }

  if (fs::is_directory(path)) {
    return fs::absolute(path / "index.meta");
  }
  else {
    return fs::absolute(path);
  }
}
