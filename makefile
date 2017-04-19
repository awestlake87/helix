
all:
	make build

create-build-dir:
	mkdir -p build/

build: build-ninja

rebuild: rebuild-ninja


generate-make: create-build-dir
	cd build/; \
	cmake -DCMAKE_BUILD_TYPE=Debug -G"Unix Makefiles" ..

build-make: generate-make
	cd build/; \
	make -j4

rebuild-make:
	make clean
	make build-make


generate-ninja: create-build-dir
	cd build/; \
	cmake -DCMAKE_BUILD_TYPE=Debug -G"Ninja" ..

build-ninja: generate-ninja
	cd build/; \
	ninja

rebuild-ninja:
	make clean
	make build-ninja


clean:
	rm -rf build
