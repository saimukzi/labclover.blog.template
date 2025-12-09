import _feature_articles

_STEP_DEPENDENCY_LIST = []

def _step_main_filter(runtime):
    """Filters out sample articles from the article list.

    This function checks if all articles are samples. If they are not, it
    removes any articles marked as 'is_sample' from the 'article_meta_list'
    in the runtime environment.

    Args:
        runtime: The runtime environment object.
    """
    is_all_sample = True
    for runtime.article in runtime.article_meta_list:
        if runtime.article['is_sample']: continue
        is_all_sample = False
        break
    if is_all_sample: return

    new_article_meta_list = []
    for runtime.article in runtime.article_meta_list:
        if runtime.article['is_sample']: continue
        new_article_meta_list.append(runtime.article)

    runtime.article_meta_list = new_article_meta_list

_STEP_DEPENDENCY_LIST.append((_feature_articles._step_main_gen_article_meta_list, _step_main_filter, _feature_articles._step_main_article_meta_list_ready))
