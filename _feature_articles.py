import copy
import json
import os
import types
from urllib.parse import urljoin

import _common
import _feature_base
import _feature_resource
import _global

_STEP_DEPENDENCY_LIST = []

def _step_main_gen_article_file_list(runtime):
    """Generates a list of article files from the input directory.

    Args:
        runtime: The runtime environment object.
    """
    article_dir = runtime.config_data['input_path']
    article_file_list = _common.find_file(article_dir)
    article_file_list = list(filter(lambda x: x.endswith('.article.txt'), article_file_list))
    runtime.article_file_list = article_file_list

def _step_main_article_file_list_ready(runtime):
    """A placeholder step indicating that the article file list is ready.

    Args:
        runtime: The runtime environment object.
    """
    pass

_STEP_DEPENDENCY_LIST.append((_feature_base._step_main_load_config, _step_main_gen_article_file_list))
_STEP_DEPENDENCY_LIST.append((_step_main_gen_article_file_list, _step_main_article_file_list_ready))
_STEP_DEPENDENCY_LIST.append((_step_main_article_file_list_ready, _feature_base._step_main_output_ready))

def _step_main_gen_article_meta_list(runtime):
    """Generates a list of article metadata from the article files.

    Args:
        runtime: The runtime environment object.
    """
    runtime.article_meta_list = []
    for article_path in runtime.article_file_list:
        article_meta = get_article_data(article_path)['meta']
        if not article_meta['enable']:
            continue
        runtime.article_meta_list.append(article_meta)

def _step_main_article_meta_list_ready(runtime):
    """A placeholder step indicating that the article metadata list is ready.

    Args:
        runtime: The runtime environment object.
    """
    pass

_STEP_DEPENDENCY_LIST.append((_step_main_gen_article_file_list, _step_main_gen_article_meta_list))
_STEP_DEPENDENCY_LIST.append((_step_main_gen_article_meta_list, _step_main_article_meta_list_ready))
_STEP_DEPENDENCY_LIST.append((_step_main_article_meta_list_ready, _feature_base._step_main_output_ready))

def _step_main_output_article(runtime):
    """Outputs each article by executing the 'outputarticle' step functions.

    Args:
        runtime: The runtime environment object.
    """
    for article_meta in runtime.article_meta_list:
        # article_data = get_article_data(article_meta['_path'])
        # article_meta = article_data['meta']
        article_runtime = types.SimpleNamespace()
        article_runtime.article_meta = article_meta

        for func in runtime.stepfunc_list_dict['outputarticle']:
            func(article_runtime, runtime)

        # db_path = _global.db_path('article.'+article_meta['id'], runtime)
        # os.makedirs(db_path, exist_ok=True)

        # output meta
        # meta_output_path = os.path.join(db_path, 'meta.json')
        # with open(meta_output_path, 'w') as f:
        #     json.dump(article_meta, f, indent=2, sort_keys=True)

        # # process article_content
        # article_content = article_data['content']
        # render_data = {
        #     'res_base_absnpath': os.path.dirname(article_meta['_path']),
        #     'article_meta_data': article_meta,
        #     'config': runtime.config_data,
        #     'runtime': runtime,
        # }
        # article_content = runtime.jinja_env.from_string(article_content)
        # article_content = article_content.render(render_data)
        # render_data['article_content'] = article_content

        # # output content txt
        # content_txt_output_path = os.path.join(db_path, 'content.txt')
        # with open(content_txt_output_path, 'wt', encoding='utf-8') as f:
        #     f.write(article_content)
        
        # # output html
        # render_data['res_base_absnpath'] = runtime.config_data['input_path']
        # article_id = article_meta['id']
        # article_html_output_path = os.path.join(runtime.config_data['output_path'], 'articles', f'{article_id}.html')
        # os.makedirs(os.path.dirname(article_html_output_path), exist_ok=True)
        # with open(article_html_output_path, 'wt', encoding='utf-8') as f:
        #     f.write(runtime.main_template.render(render_data))

_STEP_DEPENDENCY_LIST.append((_feature_base._step_main_output_ready, _step_main_output_article))

def _step_main_resource_suffix_blacklist(runtime):
    """Adds the '.article.txt' suffix to the resource blacklist.

    Args:
        runtime: The runtime environment object.
    """
    runtime.resource_suffix_blackset.add('.article.txt')

_STEP_DEPENDENCY_LIST.append((_feature_resource._step_main_resource_suffix_blacklist_init, _step_main_resource_suffix_blacklist))
_STEP_DEPENDENCY_LIST.append((_step_main_resource_suffix_blacklist, _feature_resource._step_main_resource_suffix_blacklist_ready))

# _step_outputarticle

def _step_outputarticle_article_data(article_runtime, main_runtime):
    """Loads the article data for the current article.

    Args:
        article_runtime: The runtime environment for the specific article.
        main_runtime: The main runtime environment object.
    """
    article_runtime.article_data = get_article_data(article_runtime.article_meta['_path'])

def _step_outputarticle_db_path(article_runtime, main_runtime):
    """Determines and creates the database path for the article.

    Args:
        article_runtime: The runtime environment for the specific article.
        main_runtime: The main runtime environment object.
    """
    db_path = _global.db_path('article.'+article_runtime.article_meta['id'], main_runtime)
    article_runtime.db_path = db_path
    os.makedirs(db_path, exist_ok=True)

def _step_outputarticle_output_meta(article_runtime, main_runtime):
    """Outputs the article metadata to a JSON file.

    Args:
        article_runtime: The runtime environment for the specific article.
        main_runtime: The main runtime environment object.
    """
    meta_output_path = os.path.join(article_runtime.db_path, 'meta.json')
    article_runtime.meta_output_path = meta_output_path
    with open(meta_output_path, 'w') as f:
        json.dump(article_runtime.article_meta, f, indent=2, sort_keys=True)

_STEP_DEPENDENCY_LIST.append((_step_outputarticle_db_path, _step_outputarticle_output_meta))

def _step_outputarticle_article_content(article_runtime, main_runtime):
    """Renders the article content using Jinja2.

    Args:
        article_runtime: The runtime environment for the specific article.
        main_runtime: The main runtime environment object.
    """
    render_data = {
        'res_base_absnpath': os.path.dirname(article_runtime.article_meta['_path']),
        'article_runtime': article_runtime,
        'main_runtime': main_runtime,
    }

    article_content = article_runtime.article_data['content']
    article_content = main_runtime.jinja_env.from_string(article_content)
    article_content = article_content.render(render_data)
    article_runtime.article_content = article_content

# _STEP_DEPENDENCY_LIST.append((_step_outputarticle_render_data, _step_outputarticle_article_content))
_STEP_DEPENDENCY_LIST.append((_step_outputarticle_article_data, _step_outputarticle_article_content))

def _step_outputarticle_output_content_txt(article_runtime, main_runtime):
    """Outputs the rendered article content to a text file.

    Args:
        article_runtime: The runtime environment for the specific article.
        main_runtime: The main runtime environment object.
    """
    content_txt_output_path = os.path.join(article_runtime.db_path, 'content.txt')
    article_runtime.content_txt_output_path = content_txt_output_path
    with open(content_txt_output_path, 'wt', encoding='utf-8') as f:
        f.write(article_runtime.article_content)

_STEP_DEPENDENCY_LIST.append((_step_outputarticle_article_content, _step_outputarticle_output_content_txt))

def _step_outputarticle_output_content_html(article_runtime, main_runtime):
    """Outputs the final article as an HTML file.

    Args:
        article_runtime: The runtime environment for the specific article.
        main_runtime: The main runtime environment object.
    """
    render_data = {
        'res_base_absnpath': main_runtime.config_data['input_path'],
        'article_runtime': article_runtime,
        'main_runtime': main_runtime,
    }

    article_id = article_runtime.article_meta['id']
    article_html_output_path = os.path.join(main_runtime.config_data['output_path'], 'articles', f'{article_id}.html')
    article_runtime.article_html_output_path = article_html_output_path
    os.makedirs(os.path.dirname(article_html_output_path), exist_ok=True)
    with open(article_html_output_path, 'wt', encoding='utf-8') as f:
        f.write(main_runtime.main_template.render(render_data))

_STEP_DEPENDENCY_LIST.append((_step_outputarticle_article_content, _step_outputarticle_output_content_html))

# Helper functions

ARTICLE_META_DEFAULT = {
    'enable': True,
    'is_sample': False,
    'tags': [],
}
def get_article_data(article_path):
    """Reads and parses an article file.

    This function reads an article file, which is expected to have three
    sections: metadata (in JSON format), and content, each delimited by
    '===' lines.

    Args:
        article_path (str): The path to the article file.

    Returns:
        dict: A dictionary containing the article's 'meta' and 'content'.
    """
    article = _common.read_file(article_path)
    article_meta_start_line_num = article.index('=== META START ===')
    article_meta_end_line_num = article.index('=== META END ===')
    article_meta_lines = article[article_meta_start_line_num+1:article_meta_end_line_num]
    article_meta = '\n'.join(article_meta_lines)
    article_meta = json.loads(article_meta)
    article_meta = {**ARTICLE_META_DEFAULT, **article_meta}
    article_meta['_path'] = article_path

    article_start_line_num = article.index('=== CONTENT START ===')
    article_end_line_num = article.index('=== CONTENT END ===')
    article_lines = article[article_start_line_num+1:article_end_line_num]
    article_content = '\n'.join(article_lines)
    
    return {
        'meta': article_meta,
        'content': article_content,
    }
