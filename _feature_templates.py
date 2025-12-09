import jinja2
import json
import os
from urllib.parse import urljoin

import _common
import _feature_base
import _feature_resource

_STEP_DEPENDENCY_LIST = []

def _step_main_jinja_env_init(runtime):
    """Initializes the Jinja2 environment.

    This function creates a Jinja2 environment, sets up the file system
    loader, and adds custom filters for JSON encoding and absolute URL
    generation.

    Args:
        runtime: The runtime environment object.
    """
    runtime.jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(runtime.config_data['input_path']))
    runtime.jinja_env.filters['json_encode'] = jinja_filter_json_encode
    runtime.jinja_env.filters['abs'] = jinja_filter_abs

def _step_main_jinja_env_ready(runtime):
    """A placeholder step indicating that the Jinja2 environment is ready.

    Args:
        runtime: The runtime environment object.
    """
    pass

_STEP_DEPENDENCY_LIST.append((_feature_base._step_main_load_config, _step_main_jinja_env_init))
_STEP_DEPENDENCY_LIST.append((_step_main_jinja_env_init, _step_main_jinja_env_ready))
_STEP_DEPENDENCY_LIST.append((_step_main_jinja_env_ready, _feature_base._step_main_output_ready))

def _step_main_init_main_template(runtime):
    """Initializes the main template for the site.

    Args:
        runtime: The runtime environment object.
    """
    runtime.main_template = runtime.jinja_env.get_template('_main.html.template')

_STEP_DEPENDENCY_LIST.append((
    _step_main_jinja_env_ready,
    _step_main_init_main_template,
    _feature_base._step_main_output_ready,
))

# def _step_main_output(runtime):
#     template_file_list = _common.find_file(runtime.config_data['templates_path'])
#     for template_file in template_file_list:
#         if os.path.basename(template_file)[:1] == '_':
#             return
#         rel_path = os.path.relpath(template_file, runtime.config_data['templates_path'])
#         output_file = os.path.join(runtime.config_data['output_path'], rel_path)
#         template = runtime.jinja_env.get_template(rel_path)
#         os.makedirs(os.path.dirname(output_file), exist_ok=True)
#         render_data = {}
#         for k,v in runtime.config_data.items():
#             render_data[f'config_{k}'] = v
#         with open(output_file, 'wt', encoding='utf-8') as f:
#             f.write(template.render(render_data))

# _STEP_DEPENDENCY_LIST.append((_feature_base._step_main_output_ready, _step_main_output))

def _step_main_resource_suffix_blacklist(runtime):
    """Adds the '.template' suffix to the resource blacklist.

    Args:
        runtime: The runtime environment object.
    """
    runtime.resource_suffix_blackset.add('.template')

_STEP_DEPENDENCY_LIST.append((_feature_resource._step_main_resource_suffix_blacklist_init, _step_main_resource_suffix_blacklist))
_STEP_DEPENDENCY_LIST.append((_step_main_resource_suffix_blacklist, _feature_resource._step_main_resource_suffix_blacklist_ready))

# jinja_env functions

def jinja_filter_json_encode(obj):
    """A Jinja2 filter for encoding an object to a JSON string.

    Args:
        obj: The object to encode.

    Returns:
        str: The JSON-encoded string representation of the object.
    """
    return json.dumps(obj)

@jinja2.pass_context
def jinja_filter_abs(context, input_uri):
    """A Jinja2 filter for creating absolute URLs.

    This filter resolves a given URI, which can be either a root-relative
    path (starting with '/') or a path relative to the current resource,
    into a full absolute URL based on the site's base URL.

    Args:
        context: The Jinja2 context.
        input_uri (str): The URI to resolve.

    Returns:
        str: The absolute URL.
    """
    runtime = context['main_runtime']
    if input_uri.startswith('/'):
        output_url = urljoin(runtime.config_data['base_url'], input_uri[1:])
        return output_url
    else:
        res_base_absnpath = context['res_base_absnpath']
        res_base_absppath = _common.native_path_to_posix(res_base_absnpath)
        config_input_absnpath = runtime.config_data['input_path']
        config_input_absppath = _common.native_path_to_posix(config_input_absnpath)
        assert(os.path.commonprefix([res_base_absnpath, config_input_absnpath]) == config_input_absnpath)
        res_base_relppath = os.path.relpath(res_base_absppath, config_input_absppath)
        # print(runtime.config_data['base_url'],res_base_relppath, input_uri)
        output_url = urljoin(runtime.config_data['base_url'],res_base_relppath)
        output_url += '/'
        output_url = urljoin(output_url, input_uri)
        # print(output_url)
        return output_url
