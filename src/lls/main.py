import pathlib as pt
import os
import argparse

NO_DIR = "Specified directory does not exist"
NOT_DIR = "{} is not a name of directory"

def arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        description = "List all files in target directory",
        disable_help = True)
    
    p.add_argument('-l',
        help = "more info",
        action = 'store_true',
        dest = 'expanded_info')
    p.add_argument('--si',
        help = "SI units",
        action = 'store_true',
        dest = 'use_si')
    
    hidden_files = p.add_mutually_exclusive_group()
    hidden_files.add_argument('-a', '--all',
        help = "print files with name starting with '.'",
        dest = 'all',
        action = 'store_true')
    hidden_files.add_argument('-A', '--almost-all',
        help = "print all files besides '.' and '..'",
        dest = 'almost_all',
        action = 'store_true')
    
    sort_order = p.add_mutually_exclusive_group()
    sort_order.add_argument('-S',
        help = "sort by size",
        action = 'store',
        dest = 'order')
    #p.add_argument('-S', action='store_true', help="sort by size")
    #p.add_argument('-t', action='store_true', help="sort by time of last modification")
    #p.add_argument('-X', action='store_true', help="sort by extention")
    return p

def validate_and_exit_on_error(path_str: str):
    path = pt.Path(path_str)
    
    if not path.exists():
        print(NO_DIR)
        os.exit(1)
    
    if not path.is_dir():
        print(NOT_DIR.format(path_str))
        os.exit(1)
    
    return path

def list_contents(path: pt.Path):
    for entry in os.scandir(path):
        print(entry.name)
    
    return

if __name__ == "__main__":
    args = arg_parser().parse_args()
    path = validate_and_exit_on_error(args.target)
    list_contents(path)
