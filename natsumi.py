# "Natsume" is a module management system to run functions in order according to dependency.
# The name "Natsumi" is from the flash video "なつみ STEP!".

import os
import importlib

def gen_stepfunc_list_dict(search_path, module_prefix):
    """Discovers, sorts, and organizes step functions from modules.

    This function scans a directory for modules with a given prefix, identifies
    functions that follow the `_step_` naming convention, and sorts them based
    on their declared dependencies. The functions are then grouped by their
    step ID into a dictionary.

    Args:
        search_path (str): The path to the directory to search for modules.
        module_prefix (str): The prefix used to identify feature modules.

    Returns:
        dict: A dictionary where keys are step IDs and values are lists of
              sorted step functions.
    """
    my_dir = os.path.dirname(search_path)
    feature_module_list = os.listdir(my_dir)
    feature_module_list = filter(lambda x: x.startswith(module_prefix), feature_module_list)
    feature_module_list = filter(lambda x: x.endswith('.py'), feature_module_list)
    feature_module_list = map(lambda x: x[:-3], feature_module_list)
    feature_module_list = map(lambda i: importlib.import_module(i), feature_module_list)
    feature_module_list = list(feature_module_list)

    stepid_to_stepkey_set_dict = {}
    stepkey_to_stepfunc_dict = {}
    stepkey_dependency_0_to_1_set_dict = {}
    stepkey_dependency_1_to_0_set_dict = {}

    for module in feature_module_list:
        for func_name in dir(module):
            if func_name.startswith('_step_'):
                stepfunc = getattr(module, func_name)
                step_key = get_step_key(stepfunc)
                step_id = func_name.split('_')[2]
                stepkey_to_stepfunc_dict[step_key] = stepfunc
                if step_id not in stepid_to_stepkey_set_dict:
                    stepid_to_stepkey_set_dict[step_id] = set()
                stepid_to_stepkey_set_dict[step_id].add(step_key)
                if step_key not in stepkey_dependency_0_to_1_set_dict:
                    stepkey_dependency_0_to_1_set_dict[step_key] = set()
                if step_key not in stepkey_dependency_1_to_0_set_dict:
                    stepkey_dependency_1_to_0_set_dict[step_key] = set()
        if hasattr(module, '_STEP_DEPENDENCY_LIST'):
            for func_dependency in getattr(module, '_STEP_DEPENDENCY_LIST'):
                for i in range(len(func_dependency)-1):
                    func0_key = get_step_key(func_dependency[i])
                    func1_key = get_step_key(func_dependency[i+1])
                    if func0_key not in stepkey_dependency_0_to_1_set_dict:
                        stepkey_dependency_0_to_1_set_dict[func0_key] = set()
                    stepkey_dependency_0_to_1_set_dict[func0_key].add(func1_key)
                    if func1_key not in stepkey_dependency_1_to_0_set_dict:
                        stepkey_dependency_1_to_0_set_dict[func1_key] = set()
                    stepkey_dependency_1_to_0_set_dict[func1_key].add(func0_key)

    ret_stepfunc_list_dict = {}
    for stepid, stepkey_set in stepid_to_stepkey_set_dict.items():
        ready_stepkey_set = set(stepkey_set)
        ready_stepkey_set = filter(lambda stepkey: len(stepkey_dependency_1_to_0_set_dict[stepkey]) == 0, ready_stepkey_set)
        ready_stepkey_set = set(ready_stepkey_set)

        remain_stepkey_set = set(stepkey_set)

        stepfunc_list = []

        while len(ready_stepkey_set) > 0:
            stepkey = ready_stepkey_set.pop()
            remain_stepkey_set.remove(stepkey)
            stepfunc_list.append(stepkey_to_stepfunc_dict[stepkey])

            for stepkey1 in stepkey_dependency_0_to_1_set_dict[stepkey]:
                stepkey_dependency_1_to_0_set_dict[stepkey1].remove(stepkey)
                if len(stepkey_dependency_1_to_0_set_dict[stepkey1]) == 0:
                    ready_stepkey_set.add(stepkey1)

        if (len(remain_stepkey_set) > 0):
            print(f'ERROR: Some functions are not run: stepid={stepid}')
            for stepkey in remain_stepkey_set:
                print(stepkey)
            assert(False)

        ret_stepfunc_list_dict[stepid] = stepfunc_list

    return ret_stepfunc_list_dict

def get_step_key(func):
    """Generates a unique key for a step function.

    This key is used to identify and manage dependencies between step
    functions. If the input is already a string, it is returned as-is.

    Args:
        func (function or str): The function to generate a key for, or a
                                string that is already a key.

    Returns:
        str: A unique string identifier for the function.
    """
    if(isinstance(func, str)):
        return func
    return f'{func.__module__}.{func.__name__}'

