#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

$DIR/meta/test.sh

echo -e "\033[0;34m---x[  SUPER FANCY TEST SUITE BEGIN  ]x---\033[0m"

function meta_test {
  local DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

  function echo_fail {
    echo -e "\033[1;31m[FAIL]\033[0m $@"
  }

  function echo_pass {
    echo -e "\033[0;32m[PASS]\033[0m $@"
  }

  local output="$1.out"
  local output_dir=`dirname $output`

  mkdir -p $output_dir
  bin/metac -o $output $1

  local compile_status=$?

  if [ $compile_status -ne 0 ]; then
    echo_fail "while compiling test $1"

    return $compile_status
  fi

  $output arg1 arg2

  local execute_status=$?

  if [ $execute_status -ne 0 ]; then
    echo_fail "$1 returned $execute_status"

    return $execute_status
  else
    echo_pass $1
  fi

  return 0
}

rm -rf $DIR/tests/compile-unit/*.out
rm -rf $DIR/tests/compile-unit/*.o
rm -rf $DIR/tests/compile-unit/*.ll

# run meta_test for *.meta recursively in ./test
export -f meta_test
find "$DIR/tests/compile-unit" -name "*.meta" | xargs -n 1 bash -c 'meta_test "$@"' _
