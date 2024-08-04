import json
import os
import re
import shutil
from urllib.parse import urljoin

import _common
import _feature_base
import _feature_resource
import _global

_FUNC_DEPENDENCY_LIST = []

def _func_scan(runtime):
    copy_re_list = runtime.config_data['copy_re_list']
    copy_re_list = list(map(re.compile, copy_re_list))

    runtime.copy_list = []
    input_path = runtime.config_data['input_path']
    input_file_absnpath_list = _common.find_file(input_path)
    input_folder_absppath = _common.native_path_to_posix(input_path)

    runtime.copy_absnpath_list = []
    for input_file_absnpath in input_file_absnpath_list:
        input_file_absppath = _common.native_path_to_posix(input_file_absnpath)
        input_file_relppath = os.path.relpath(input_file_absppath, input_folder_absppath)
        if not any(map(lambda x: x.fullmatch(input_file_relppath), copy_re_list)):
            continue
        runtime.copy_absnpath_list.append(input_file_absnpath)


_FUNC_DEPENDENCY_LIST.append((_feature_base._func_load_config, _func_scan))

def _func_filter(runtime):
    copy_absnpath_set = set(runtime.copy_absnpath_list)
    runtime.input_resource_file_list = list(filter(lambda x: x not in copy_absnpath_set, runtime.input_resource_file_list))

_FUNC_DEPENDENCY_LIST.append((_feature_base._func_load_config, _func_filter))
_FUNC_DEPENDENCY_LIST.append((_func_scan,_func_filter))
_FUNC_DEPENDENCY_LIST.append((_feature_resource._func_gen_file_list, _func_filter))
_FUNC_DEPENDENCY_LIST.append((_func_filter, _feature_resource._func_input_resource_file_list_ready))

def _func_copy(runtime):
    for copy_absnpath in runtime.copy_absnpath_list:
        copy_relnpath = os.path.relpath(copy_absnpath, runtime.config_data['input_path'])
        copy_output_npath = os.path.join(runtime.config_data['output_path'], copy_relnpath)
        os.makedirs(os.path.dirname(copy_output_npath), exist_ok=True)
        shutil.copy2(copy_absnpath, copy_output_npath)

_FUNC_DEPENDENCY_LIST.append((_feature_base._func_output_ready, _func_copy))