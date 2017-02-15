#pragma once

#include <vector>

#include <boost/filesystem/path.hpp>

namespace Meta {
  class Compiler {
    public:
      using Path = boost::filesystem::path;
      using UnitList = std::vector<Path>;

      void addUnit(const Path& path);

      void compile();

    private:

      Path resolveUnit(const Path& path);

      UnitList m_Units;
  };
}
