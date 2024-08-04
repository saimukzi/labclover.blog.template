import jinja2
import json
import os
from urllib.parse import urljoin

import _common
import _feature_base

_FUNC_DEPENDENCY_LIST = []

def _func_init_env(runtime):
    runtime.jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(runtime.config_data['templates_path']))
    runtime.jinja_env.filters['json_encode'] = jinja_filter_json_encode
    runtime.jinja_env.filters['url'] = jinja_filter_url

    runtime.main_template = runtime.jinja_env.get_template('_main.html')

_FUNC_DEPENDENCY_LIST.append((_feature_base._func_load_config, _func_init_env))
_FUNC_DEPENDENCY_LIST.append((_func_init_env, _feature_base._func_output_ready))

def _func_output(runtime):
    template_file_list = _common.find_file(runtime.config_data['templates_path'])
    for template_file in template_file_list:
        if os.path.basename(template_file)[:1] == '_':
            return
        rel_path = os.path.relpath(template_file, runtime.config_data['templates_path'])
        output_file = os.path.join(runtime.config_data['output_path'], rel_path)
        template = runtime.jinja_env.get_template(rel_path)
        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        render_data = {}
        for k,v in runtime.config_data.items():
            render_data[f'config_{k}'] = v
        with open(output_file, 'wt', encoding='utf-8') as f:
            f.write(template.render(render_data))

_FUNC_DEPENDENCY_LIST.append((_feature_base._func_output_ready, _func_output))

# jinja_env functions

def jinja_filter_json_encode(obj):
    return json.dumps(obj)

@jinja2.pass_context
def jinja_filter_url(context, input_relpath, ttype='articles'):
    assert(ttype in ['articles', 'templates'])
    runtime = context['runtime']
    if ttype == 'articles':
        blog_file_path = context['blog_meta_data']['_path']
        article_file_folder_path = os.path.dirname(blog_file_path)
        input_abspath = os.path.join(article_file_folder_path, input_relpath)
        assert(os.path.commonprefix([input_abspath, runtime.config_data['input_path']]) == runtime.config_data['input_path'])
        input_relpath = os.path.relpath(input_abspath, runtime.config_data['input_path'])
        output_url = runtime.article_res_fn_to_url[input_relpath]
        return output_url
    elif ttype == 'templates':
        output_url = urljoin(runtime.config_data['base_url'], input_relpath)
        return output_url
    assert(False)