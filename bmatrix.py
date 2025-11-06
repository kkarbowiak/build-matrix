import argparse
from dataclasses import dataclass
from pathlib import Path
import subprocess


@dataclass
class Options:
    compilers: list[str]
    build_types: list[str]
    source_dir: str
    build_dir: str
    target: str
    quiet: bool
    post_build_cmds: list[str]


def main():
    parser = get_args_parser()
    options = parse_args(parser)

    build_matrix(options)


def build_matrix(options):
    for compiler in options.compilers:
        for build_type in options.build_types:
            process(compiler, build_type, options)


def process(compiler, build_type, options):
    build_dir = create_dir(options.build_dir, compiler, build_type)
    print(f'Building with {compiler} in {build_type} mode in {build_dir} ...')
    run_cmake_configure(compiler, build_type, options.source_dir, build_dir, options.quiet)
    run_cmake_build(build_dir, options.target, options.quiet)
    run_post_build_commands(build_dir, options.post_build_cmds)


def run_cmake_configure(compiler, build_type, source_dir, build_dir, quiet):
    cmake_cfg_cmd = f'cmake -S {source_dir} -B {build_dir} ' \
        f'-DCMAKE_C_COMPILER={get_c_compiler(compiler)} ' \
        f'-DCMAKE_CXX_COMPILER={get_cxx_compiler(compiler)} '\
        f'-DCMAKE_BUILD_TYPE={build_type.capitalize()}'
    redirect = subprocess.DEVNULL if quiet else None
    subprocess.run(cmake_cfg_cmd.split(), check=True, stdout=redirect)


def run_cmake_build(build_dir, target, quiet):
    cmake_build_cmd = f'cmake --build {build_dir} -j 8'
    if target:
        cmake_build_cmd += f' --target {target}'
    redirect = subprocess.DEVNULL if quiet else None
    subprocess.run(cmake_build_cmd.split(), check=True, stdout=redirect)


def run_post_build_commands(build_dir, post_build_cmds):
    for cmd in post_build_cmds:
        subprocess.run(cmd.split(), cwd=build_dir, check=True)


def get_c_compiler(compiler):
    if compiler.startswith('gcc'):
        return compiler
    elif compiler.startswith('g++'):
        return compiler.replace('g++', 'gcc')
    elif compiler.startswith('clang'):
        return compiler
    elif compiler.startswith('clang++'):
        return compiler.replace('clang++', 'clang')


def get_cxx_compiler(compiler):
    if compiler.startswith('gcc'):
        return compiler.replace('gcc', 'g++')
    elif compiler.startswith('g++'):
        return compiler
    elif compiler.startswith('clang'):
        return compiler.replace('clang', 'clang++')
    elif compiler.startswith('clang++'):
        return compiler


def create_dir(build_base_dir, compiler, build_type):
    build_dir = Path(build_base_dir) / f'build-{compiler}-{build_type.lower()}'
    build_dir.mkdir(parents=True, exist_ok=True)
    return build_dir


def get_args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--compiler', nargs='+', help='list of compilers to use')
    parser.add_argument('--type', nargs='+', help='list of build types')
    parser.add_argument('--source-dir', help='source directory', default='.')
    parser.add_argument('--build-dir', help='build directory', default='build')
    parser.add_argument('--target', help='build target')
    parser.add_argument('--quiet', action='store_true', help='suppress configure and build output')
    parser.add_argument('--post-build-cmd', nargs='+', help='list of commands to run after build', default=[])
    return parser


def parse_args(parser):
    args = parser.parse_args()
    return Options(
        compilers=args.compiler,
        build_types=args.type,
        source_dir=args.source_dir,
        build_dir=args.build_dir,
        target=args.target,
        quiet=args.quiet,
        post_build_cmds=args.post_build_cmd
    )


if __name__ == '__main__':
    main()
