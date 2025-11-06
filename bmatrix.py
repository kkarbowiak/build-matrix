import argparse
from pathlib import Path
import subprocess


def main():
    args = parse_args()

    build_matrix(args.compiler, args.type, args.source_dir, args.build_dir, args.target, args.post_build_cmd)


def build_matrix(compilers, build_types, source_dir, build_base_dir, target, post_build_cmds):
    for compiler in compilers:
        for build_type in build_types:
            build_dir = create_dir(build_base_dir, compiler, build_type)
            run_cmake_configure(compiler, build_type, source_dir, build_dir)
            run_cmake_build(build_dir, target)
            run_post_build_commands(build_dir, post_build_cmds)


def run_cmake_configure(compiler, build_type, source_dir, build_dir):
    cmake_cfg_cmd = f'cmake -S {source_dir} -B {build_dir} ' \
        f'-DCMAKE_C_COMPILER={get_c_compiler(compiler)} ' \
        f'-DCMAKE_CXX_COMPILER={get_cxx_compiler(compiler)} '\
        f'-DCMAKE_BUILD_TYPE={build_type.capitalize()}'
    subprocess.run(cmake_cfg_cmd.split(), check=True)


def run_cmake_build(build_dir, target):
    cmake_build_cmd = f'cmake --build {build_dir} -j 8'
    if target:
        cmake_build_cmd += f' --target {target}'
    subprocess.run(cmake_build_cmd.split(), check=True)


def run_post_build_commands(build_dir, post_build_cmds):
    for cmd in post_build_cmds:
        subprocess.run(cmd.split(), cwd=build_dir, check=True)


def get_c_compiler(compiler):
    match compiler:
        case 'gcc' | 'g++':
            return 'gcc'
        case 'clang' | 'clang++':
            return 'clang'


def get_cxx_compiler(compiler):
    match compiler:
        case 'gcc' | 'g++':
            return 'g++'
        case 'clang' | 'clang++':
            return 'clang++'


def create_dir(build_base_dir, compiler, build_type):
    build_dir = Path(build_base_dir) / f'build-{compiler}-{build_type.lower()}'
    build_dir.mkdir(parents=True, exist_ok=True)
    return build_dir


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--compiler', nargs='+', help='list of compilers to use')
    parser.add_argument('--type', nargs='+', help='list of build types')
    parser.add_argument('--source-dir', help='source directory', default='.')
    parser.add_argument('--build-dir', help='build directory', default='build')
    parser.add_argument('--target', help='build target')
    parser.add_argument('--post-build-cmd', nargs='+', help='list of commands to run after build', default=[])
    return parser.parse_args()


if __name__ == '__main__':
    main()
