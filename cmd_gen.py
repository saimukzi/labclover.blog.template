import argparse
import importlib
import natsumi
import os
import types

import _common

MY_PATH = os.path.abspath(__file__)

def main():
    parser = argparse.ArgumentParser(description='Generate the article')
    parser.add_argument('--config', type=str, default='config.json', help='config file')

    args = parser.parse_args()

    runtime = types.SimpleNamespace()
    runtime.args = args

    runtime.stepfunc_list_dict = natsumi.gen_stepfunc_list_dict(MY_PATH, '_feature_')
    for func in runtime.stepfunc_list_dict['main']:
        func(runtime)

if __name__ == '__main__':
    main()
