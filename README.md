# Build matrix

This is a script for automating building a matrix of builds for every combination of provided compilers and build types. The purpose is to fill this matrix with a single command:

|         | gcc         | clang         |
|---------|-------------|---------------|
| debug   | gcc-debug   | clang-debug   |
| release | gcc-release | clang-release |

For example, to build some project with both gcc and clang in both debug and release modes, run:
```shell
python3 bmatrix.py --compiler clang gcc --type debug release --source-dir <src> --build-dir <bld>
```
where:
 * <src> is the source directory
 * <bld> is the target build directory

The script will run CMake to configure and then build the project, placing the output in subdirectories of <bld>, e.g.
```
 <bld>
   + build-gcc-debug
   + build-gcc-release
   + build-clang-debug
   + build-clang-release
```

You can also pass additional commands using `--post-build-cmd` to be executed in each of the output directories, for example to run some tests:
```shell
python3 bmatrix.py --compiler clang gcc --type debug release --source-dir <src> --build-dir <bld> --post-build-cmd 'valgrind ./app'
```
