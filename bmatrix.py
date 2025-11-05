import argparse
from pathlib import Path
import subprocess


def main():
    args = parse_args()

    for compiler in args.compiler:
        for type in args.type:
            build_dir = Path(f'build-{compiler}-{type.lower()}')
            build_dir.mkdir(exist_ok=True)
            cmake_cfg_cmd = f'cmake -S . -B {build_dir} ' \
                        f'-DCMAKE_C_COMPILER={get_c_compiler(compiler)} ' \
                        f'-DCMAKE_CXX_COMPILER={get_cxx_compiler(compiler)} '\
                        f'-DCMAKE_BUILD_TYPE={type.capitalize()}'
            subprocess.run(cmake_cfg_cmd.split(), check=True)
            cmake_build_cmd = f'cmake --build {build_dir} -j'
            subprocess.run(cmake_build_cmd.split(), check=True)


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


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--compiler', nargs='+', help='list of compilers to use')
    parser.add_argument('--type', nargs='+', help='list of build types')
    return parser.parse_args()


if __name__ == '__main__':
    main()
