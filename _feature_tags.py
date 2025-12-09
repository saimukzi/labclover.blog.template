import _common
import _feature_articles
import _feature_base
import _global
import json
import os

_STEP_DEPENDENCY_LIST = []

def _step_main_gen_tag_id_to_data_dict(runtime):
    """Generates a dictionary mapping tag IDs to tag data.

    This function iterates through the article metadata list and builds a
    dictionary where each key is a tag ID and the value is a dictionary
    containing the tag ID and a list of associated article IDs.

    Args:
        runtime: The runtime environment object.
    """
    runtime.tag_id_to_data_dict = {}
    for article_meta in runtime.article_meta_list:
        for tag in article_meta['tags']:
            if tag not in runtime.tag_id_to_data_dict:
                runtime.tag_id_to_data_dict[tag] = {
                    'tag_id': tag,
                    'article_id_list': [],
                }
            runtime.tag_id_to_data_dict[tag]['article_id_list'].append(article_meta['id'])

def _step_main_tag_id_to_data_dict_ready(runtime):
    """A placeholder step indicating that the tag data dictionary is ready.

    Args:
        runtime: The runtime environment object.
    """
    pass

_STEP_DEPENDENCY_LIST.append((_feature_articles._step_main_article_meta_list_ready, _step_main_gen_tag_id_to_data_dict, _step_main_tag_id_to_data_dict_ready))

def _step_main_meta_tag_data_list(runtime):
    """Generates a list of tag data for the blog metadata.

    This function processes the article metadata to create a sorted list of
    tags, including the count of articles for each tag and a URL to the
    tag's data file.

    Args:
        runtime: The runtime environment object.
    """
    tag_data_list = runtime.article_meta_list
    tag_data_list = map(lambda x: x['tags'], tag_data_list)
    tag_data_list = sum(tag_data_list, [])
    value_to_count_dict = {}
    for tag in tag_data_list:
        value_to_count_dict[tag] = value_to_count_dict.get(tag, 0) + 1
    tag_data_list = set(tag_data_list)
    tag_data_list = map(lambda x: {'tag_id': x, 'count': value_to_count_dict[x]}, tag_data_list)
    tag_data_list = sorted(tag_data_list, key=lambda x: (-x['count'], x['tag_id']))
    tag_data_list = list(tag_data_list)
    for tag_data in tag_data_list:
        tag_data['data_url'] = _common.urljoin(_global.db_url('tag.'+tag_data['tag_id'], runtime),'tag_data.json')
    runtime.blog_meta_dict['tag_data_list'] = tag_data_list

_STEP_DEPENDENCY_LIST.append((_feature_base._step_main_init_done, _step_main_meta_tag_data_list))
_STEP_DEPENDENCY_LIST.append((_feature_articles._step_main_article_meta_list_ready, _step_main_meta_tag_data_list))
_STEP_DEPENDENCY_LIST.append((_step_main_meta_tag_data_list, _feature_base._step_main_output_ready))

def _step_main_output(runtime):
    """Outputs the tag data to JSON files.

    This function iterates through the tag data dictionary and writes each
    tag's data to a separate JSON file in the output directory.

    Args:
        runtime: The runtime environment object.
    """
    for tag_data in runtime.tag_id_to_data_dict.values():
        tag_id = tag_data['tag_id']
        tag_output_path = _global.db_path(f'tag.{tag_id}', runtime)
        os.makedirs(tag_output_path, exist_ok=True)
        tag_output_path = os.path.join(tag_output_path, 'tag_data.json')
        with open(tag_output_path, 'w') as f:
            json.dump(tag_data, f, indent=2, sort_keys=True)

_STEP_DEPENDENCY_LIST.append((_step_main_tag_id_to_data_dict_ready, _step_main_output))
_STEP_DEPENDENCY_LIST.append((_feature_base._step_main_output_ready, _step_main_output))
