import os
import tqdm
import random
import numpy as np
from batch_generator import generate_batch

VARIANCE_TOTAL_RANGE = {
    "none": [0, 0],
    "viewpoint": [-90, 90],
    "translation": [-0.75, 0.75],
    "rotation": [-90, 90],
    "scaling": [0.625, 1.375]
}

VARIANCE_TEST_RANGE = {
    "none": [0, 0],
    "viewpoint": [-60, 60],
    "translation": [-0.3, 0.3],
    "rotation": [-60, 60],
    "scaling": [0.85, 1.15]
}

ROOT_DIR = os.path.abspath(os.curdir)
route = os.path.join(ROOT_DIR, "ModelNet10")
save_address = os.path.join(ROOT_DIR, "stimulus")

def render_selectivity_var_set(var_type, dir_list):
    save_route = os.path.join(save_address, "selectivity_var")
    for subdir in tqdm.tqdm(dir_list):
        if os.path.isdir(os.path.join(route, subdir)):
            # single file handler
            file_list = os.listdir(os.path.join(route, subdir))
            file_list.sort()
            file_count = 0
            for file in file_list:
                if os.path.isfile(os.path.join(route, subdir, file)) and file_count < 200+60 and file[0]!='.':
                    file_name = os.path.join(route, subdir, file)
                    if file_count >= 0 and file_count < 200:
                        variance = random.random() * (VARIANCE_TEST_RANGE[var_type][1] - VARIANCE_TEST_RANGE[var_type][0])\
                                   + VARIANCE_TEST_RANGE[var_type][0]
                        generate_batch(file_name, save_route, subdir, var_type, var_number=1, max_var=variance, min_var=variance,
                                       divide_folder=False, render_scrambled_set=True)
                file_count += 1

def render_invariance_test_set(var_type, dir_list, task):
    if task==1:
        start=0
        end=100
    else:
        start=100
        end=200
    save_route = os.path.join(save_address, "invariance_test")
    for subdir in tqdm.tqdm(dir_list):
        if os.path.isdir(os.path.join(route, subdir)):
            # single file handler
            file_list = os.listdir(os.path.join(route, subdir))
            file_list.sort()
            file_count = 0
            for file in file_list:
                if os.path.isfile(os.path.join(route, subdir, file)) and file_count < 200+60 and file[0]!='.':
                    file_name = os.path.join(route, subdir, file)
                    if file_count >= start and file_count < end:
                        generate_batch(file_name, save_route, subdir, var_type, var_number=13,
                                       max_var=VARIANCE_TOTAL_RANGE[var_type][1], min_var=VARIANCE_TOTAL_RANGE[var_type][0],
                                       divide_folder=True, render_scrambled_set=False)
                    file_count += 1

def render_invariance_unit_set(var_type, dir_list):
    save_route = os.path.join(save_address, "invariance_unit")
    for subdir in tqdm.tqdm(dir_list):
        if os.path.isdir(os.path.join(route, subdir)):
            # single file handler
            file_list = os.listdir(os.path.join(route, subdir))
            file_list.sort()
            file_count = 0
            for file in file_list:
                if os.path.isfile(os.path.join(route, subdir, file)) and file_count < 200+60 and file[0]!='.':
                    file_name = os.path.join(route, subdir, file)
                    if file_count >= 200 and file_count < 250:
                        generate_batch(file_name, save_route, subdir, var_type, var_number=5,
                                       max_var=VARIANCE_TEST_RANGE[var_type][1], min_var=VARIANCE_TEST_RANGE[var_type][0],
                                       divide_folder=True, render_scrambled_set=False)
                    file_count += 1

def render_SVM_var_set(var_type, dir_list):
    sub_variance = np.linspace(0,VARIANCE_TOTAL_RANGE[var_type][1],18+1)

    for SVM_variance in sub_variance:
        save_route = os.path.join(save_address, "SVM_var", var_type, str(SVM_variance*2))
        for subdir in tqdm.tqdm(dir_list):
            if os.path.isdir(os.path.join(route, subdir)):
                # single file handler
                file_list = os.listdir(os.path.join(route, subdir))
                file_list.sort()
                file_count = 0
                for file in file_list:
                    if os.path.isfile(os.path.join(route, subdir, file)) and file_count < 200 + 60 and file[0] != '.':
                        file_name = os.path.join(route, subdir, file)
                        if file_count >= 200 and file_count < 260:
                            variance = random.random() * 2 * SVM_variance - SVM_variance
                            generate_batch(file_name, save_route, subdir, var_type, var_number=1, max_var=variance,
                                           min_var=variance,
                                           divide_folder=False, render_scrambled_set=True, set_subfolder=False)
                        file_count += 1

def main():
    var_type = "viewpoint"
    #dir_list = os.listdir(route)
    #dir_list = ["bed", "chair", "desk", "dresser", "night_stand", "monitor", "sofa", "table", "toilet"]
    dir_list = ["sofa", "table", "toilet"]
    render_invariance_unit_set(var_type, dir_list)

if __name__ == "__main__":
	main()