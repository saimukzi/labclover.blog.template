import argparse
import importlib
import natsumi
import os
import types

import _common

MY_PATH = os.path.abspath(__file__)

def main():
    """Main entry point for the static site generator.

    This function parses command-line arguments, initializes the runtime
    environment, discovers and sorts the step functions using natsumi,
    and executes the 'main' step functions to generate the site.
    """
    parser = argparse.ArgumentParser(description='Generate the article')
    parser.add_argument('--config', type=str, default='config.json', help='config file')
    parser.add_argument('--verbose', action='store_true', help='enable verbose debug output')

    args = parser.parse_args()

    runtime = types.SimpleNamespace()
    runtime.args = args

    runtime.stepfunc_list_dict = natsumi.gen_stepfunc_list_dict(MY_PATH, '_feature_')
    
    if args.verbose:
        print("Debug: runtime.stepfunc_list_dict content:")
        for key, func_list in runtime.stepfunc_list_dict.items():
            print(f"  Step group '{key}':")
            for func in func_list:
                print(f"    - {func.__name__}")
        print()
    
    for func in runtime.stepfunc_list_dict['main']:
        if args.verbose:
            print(f"Running step: {func.__name__}")
        func(runtime)

if __name__ == '__main__':
    main()
