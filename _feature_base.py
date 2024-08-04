import _common
import json
import shutil

_FUNC_DEPENDENCY_LIST = []

def _func_load_config(runtime):
    config_path = runtime.args.config
    with open(config_path, 'r') as f:
        runtime.config_data = json.load(f)
    for k,v in runtime.config_data.items():
        if k.endswith('_path'):
            runtime.config_data[k] = _common.to_native_path(v)

def _func_clear_output_path(runtime):
    shutil.rmtree(runtime.config_data['output_path'], ignore_errors=True)

_FUNC_DEPENDENCY_LIST.append((_func_load_config, _func_clear_output_path))