# The name "Natsumi" is from the flash video "なつみ STEP!".

import os
import importlib

def gen_stepfunc_list_dict(search_path, module_prefix):
    my_dir = os.path.dirname(search_path)
    feature_py_list = os.listdir(my_dir)
    feature_py_list = filter(lambda x: x.startswith(module_prefix), feature_py_list)
    feature_py_list = filter(lambda x: x.endswith('.py'), feature_py_list)
    feature_py_list = map(lambda x: x[:-3], feature_py_list)
    feature_py_list = list(feature_py_list)
    module_id_to_module_dict = {}
    for feature_py in feature_py_list:
        module_id_to_module_dict[feature_py[len(module_prefix):]] = importlib.import_module(feature_py)

    stepid_to_stepkey_set_dict = {}
    stepkey_to_stepfunc_dict = {}
    # stepid_to_stepkey_to_stepfunc_dict_dict = {}
    stepkey_dependency_0_to_1_set_dict = {}
    stepkey_dependency_1_to_0_set_dict = {}

    for module in module_id_to_module_dict.values():
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
    if(isinstance(func, str)):
        return func
    return f'{func.__module__}.{func.__name__}'
