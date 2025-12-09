import jinja2
import os
import shutil
from urllib.parse import urljoin

import _common
import _feature_base
# import _feature_templates
import _global

_STEP_DEPENDENCY_LIST = []

def _step_main_resource_suffix_blackset_init(runtime):
    """Initializes the resource suffix blacklist.

    Args:
        runtime: The runtime environment object.
    """
    runtime.resource_suffix_blackset = set()

def _step_main_resource_suffix_blackset_ready(runtime):
    """A placeholder step indicating that the resource suffix blacklist is ready.

    Args:
        runtime: The runtime environment object.
    """
    pass

_STEP_DEPENDENCY_LIST.append((_step_main_resource_suffix_blackset_init, _step_main_resource_suffix_blackset_ready))

def _step_main_gen_file_list(runtime):
    """Generates the list of input resource files.

    This function scans the input directory, filters out any files with
    blacklisted suffixes, and stores the resulting list in the runtime
    environment.

    Args:
        runtime: The runtime environment object.
    """
    input_path = runtime.config_data['input_path']
    input_resource_file_list = _common.find_file(input_path)
    input_resource_file_list = filter(lambda x: not is_black(x, runtime), input_resource_file_list)
    input_resource_file_list = list(input_resource_file_list)
    runtime.input_resource_file_list = input_resource_file_list

def _step_main_input_resource_file_list_ready(runtime):
    """A placeholder step indicating that the input resource file list is ready.

    Args:
        runtime: The runtime environment object.
    """
    pass

_STEP_DEPENDENCY_LIST.append((_feature_base._step_main_load_config,_step_main_gen_file_list))
_STEP_DEPENDENCY_LIST.append((_step_main_resource_suffix_blackset_ready,_step_main_gen_file_list))
_STEP_DEPENDENCY_LIST.append((_step_main_gen_file_list,_step_main_input_resource_file_list_ready))

def _step_main_scan_res(runtime):
    """Scans the resource files and prepares them for output.

    This function calculates the MD5 hash of each resource file, determines
    the output path, and creates a mapping from the input file path to the
    final output URL.

    Args:
        runtime: The runtime environment object.
    """
    runtime.article_res_fn_to_url = {}
    runtime.article_res_output_list = []
    for res_path in runtime.input_resource_file_list:
        dot_idx = res_path.rfind('.')
        if dot_idx == -1:
            file_suffix = ''
        else:
            file_suffix = res_path[dot_idx:]
        file_md5 = _common.md5_file(res_path)
        key = 'article_res.'+file_md5+file_suffix
        output_folder_path = _global.db_path(key, runtime)
        output_path = os.path.join(output_folder_path, 'bin'+file_suffix)
        runtime.article_res_output_list.append((res_path, output_path))
        output_rel_path = os.path.relpath(output_path, runtime.config_data['output_path'])
        output_rel_url = _common.to_rel_url(output_rel_path)
        output_url = urljoin(runtime.config_data['base_url'], output_rel_url)
        input_rel_path = os.path.relpath(res_path, runtime.config_data['input_path'])
        runtime.article_res_fn_to_url[input_rel_path] = output_url

def _step_main_article_res_fn_to_url_ready(runtime):
    """A placeholder step indicating that the resource URL mapping is ready.

    Args:
        runtime: The runtime environment object.
    """
    pass

def _step_main_article_res_output_list_ready(runtime):
    """A placeholder step indicating that the resource output list is ready.

    Args:
        runtime: The runtime environment object.
    """
    pass

_STEP_DEPENDENCY_LIST.append((_feature_base._step_main_load_config, _step_main_scan_res))
_STEP_DEPENDENCY_LIST.append((_step_main_input_resource_file_list_ready, _step_main_scan_res))
_STEP_DEPENDENCY_LIST.append((_step_main_scan_res, _step_main_article_res_fn_to_url_ready))
_STEP_DEPENDENCY_LIST.append((_step_main_scan_res, _step_main_article_res_output_list_ready))
_STEP_DEPENDENCY_LIST.append((_step_main_article_res_fn_to_url_ready, _feature_base._step_main_output_ready))
_STEP_DEPENDENCY_LIST.append((_step_main_article_res_output_list_ready, _feature_base._step_main_output_ready))

def _step_main_output_res(runtime):
    """Outputs the resource files to the appropriate directory.

    This function iterates through the list of resource files and copies them
    to their calculated output paths.

    Args:
        runtime: The runtime environment object.
    """
    for res_path, output_path in runtime.article_res_output_list:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        if os.path.exists(output_path):
            assert(_common.is_file_equal(res_path, output_path))
        else:
            shutil.copy(res_path, output_path)

_STEP_DEPENDENCY_LIST.append((_feature_base._step_main_output_ready, _step_main_output_res))

def _step_main_jinja_env(runtime):
    """Adds the 'res' filter to the Jinja2 environment.

    Args:
        runtime: The runtime environment object.
    """
    runtime.jinja_env.filters['res'] = jinja_filter_res

@jinja2.pass_context
def jinja_filter_res(context, input_path):
    """A Jinja2 filter for resolving resource URLs.

    This filter takes a relative resource path, resolves it to its final
    output URL, and returns the URL.

    Args:
        context: The Jinja2 context.
        input_path (str): The relative path to the resource.

    Returns:
        str: The final URL for the resource.
    """
    runtime = context['main_runtime']
    res_base_absnpath = context['res_base_absnpath']
    input_absnpath = os.path.join(res_base_absnpath, input_path)
    assert(os.path.commonprefix([input_absnpath, runtime.config_data['input_path']]) == runtime.config_data['input_path'])
    input_relpath = os.path.relpath(input_absnpath, runtime.config_data['input_path'])
    output_url = runtime.article_res_fn_to_url[input_relpath]
    return output_url

_STEP_DEPENDENCY_LIST.append((
    '_feature_templates._step_main_jinja_env_init',
    _step_main_jinja_env,
    '_feature_templates._step_main_jinja_env_ready',
))

# Helper functions

def is_black(path, runtime):
    """Checks if a file path has a blacklisted suffix.

    Args:
        path (str): The file path to check.
        runtime: The runtime environment object.

    Returns:
        bool: True if the path has a blacklisted suffix, False otherwise.
    """
    for suffix in runtime.resource_suffix_blackset:
        if path.endswith(suffix):
            return True
    return False
