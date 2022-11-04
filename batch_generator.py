from render import *
from background_generator import *
from image_processing import *

import os
import random
from PIL import Image

CLASS_MAIN_VIEWPOINT = {
    "bed": 0.0,
    "chair": 0.0,
    "desk": 90.0,
    "dresser": 90.0,
    "monitor": 90.0,
    "toilet": 0.0,
    "bathtub": 0.0,
    "night_stand": 90.0,
    "sofa": 90.0,
    "table": 90.0
}

PIXEL_DIST = {
    "mean": 255./2,
    "std": 255./5
}

ROOT_DIR = os.path.abspath(os.curdir)

def render_non_variance_set(filename, save_route, subdir, phi, delta, render_scrambled_set):
    # pick background image randomly
    background_file_path = os.path.join(ROOT_DIR, "background")
    file_list = os.listdir(background_file_path)
    for file in file_list:
        if not os.path.isfile(os.path.join(background_file_path, file)) or file[0] == '.':
            file_list.remove(file)
    main_viewpoint = CLASS_MAIN_VIEWPOINT[subdir]

    # Render selectivity set: (1) original image
    createFolder(os.path.join(save_route, "non_variance",  subdir))
    image = image_normalizing(offRender(filename, phi, delta, main_viewpoint), PIXEL_DIST["mean"], PIXEL_DIST["std"])
    background_file = os.path.join(background_file_path, random.choice(file_list))
    background = image_normalizing(np.asarray(Image.open(background_file).convert("L").resize(SHAPE)), PIXEL_DIST["mean"], PIXEL_DIST["std"])
    merged = mergeBgFg(image, image_normalizing(phaseScrambledBg(background, PIXEL_DIST["mean"], PIXEL_DIST["std"]), PIXEL_DIST["mean"], PIXEL_DIST["std"], True))
    merged = image_normalizing(merged, PIXEL_DIST["mean"], PIXEL_DIST["std"], True)
    Image.fromarray(merged).convert("L").save(os.path.join(save_route, "non_variance", subdir, "{0}.png".format(filename.split('/')[-1].split('.')[0])))

    # Render selectivity set: (2) scrambled image
    if render_scrambled_set:
        createFolder(os.path.join(save_route, "non_variance", subdir + "_scrambled"))
        background_file = os.path.join(background_file_path, random.choice(file_list))
        background = image_normalizing(np.asarray(Image.open(background_file).convert("L").resize(SHAPE)), PIXEL_DIST["mean"], PIXEL_DIST["std"])
        merged = mergeBgFg(scramble_image_generator(image), image_normalizing(phaseScrambledBg(background, PIXEL_DIST["mean"], PIXEL_DIST["std"]), PIXEL_DIST["mean"], PIXEL_DIST["std"], True))
        merged = image_normalizing(merged, PIXEL_DIST["mean"], PIXEL_DIST["std"], True)
        Image.fromarray(merged).convert("L").save(os.path.join(save_route, "non_variance", subdir + "_scrambled", "{0}.png".format(filename.split('/')[-1].split('.')[0])))

def render_viewpoint_set(filename, save_route, subdir, view_number, max_angle, min_angle, divide_folder, render_scrambled_set, set_subfolder):

    phi_list = np.linspace(min_angle, max_angle, view_number)

    # pick background image randomly
    background_file_path = os.path.join(ROOT_DIR, "background")

    file_list = os.listdir(background_file_path)
    for file in file_list:
        if not os.path.isfile(os.path.join(background_file_path, file)) or file[0] == '.':
            file_list.remove(file)

    main_viewpoint = CLASS_MAIN_VIEWPOINT[subdir]

    # Render viewpoint set
    for j in range(len(phi_list)):
        phi = phi_list[len(phi_list) - j - 1]

        normal_folder_path = save_route
        scrambled_folder_path = save_route
        if set_subfolder:
            normal_folder_path = os.path.join(normal_folder_path, "viewpoint")
            scrambled_folder_path = os.path.join(scrambled_folder_path, "viewpoint")
        normal_folder_path = os.path.join(normal_folder_path, subdir)
        scrambled_folder_path = os.path.join(scrambled_folder_path, subdir + "_scrambled")
        if divide_folder:
            normal_folder_path = os.path.join(normal_folder_path, str(phi))
            scrambled_folder_path = os.path.join(scrambled_folder_path, str(phi))

        # Render normal Image
        image = image_normalizing(offRender(filename, phi, 0, main_viewpoint), PIXEL_DIST["mean"], PIXEL_DIST["std"]/2)
        background_file = os.path.join(background_file_path, random.choice(file_list))
        background = image_normalizing(np.asarray(Image.open(background_file).convert("L").resize(SHAPE)), PIXEL_DIST["mean"], PIXEL_DIST["std"])
        merged = mergeBgFg(image, phaseScrambledBg(background, PIXEL_DIST["mean"], PIXEL_DIST["std"]))
        merged = image_normalizing(merged, PIXEL_DIST["mean"], PIXEL_DIST["std"], norm_all=True)
        createFolder(normal_folder_path)
        Image.fromarray(merged).convert("L").save(os.path.join(normal_folder_path ,
                                 '{0}_{1}.png'.format(filename.split('/')[-1].split('.')[0], phi)))

        # Render scrambled Image
        if render_scrambled_set:
            background_file = os.path.join(background_file_path, random.choice(file_list))
            background = image_normalizing(np.asarray(Image.open(background_file).convert("L").resize(SHAPE)), PIXEL_DIST["mean"], PIXEL_DIST["std"])
            merged = mergeBgFg(scramble_image_generator(image), phaseScrambledBg(background, PIXEL_DIST["mean"], PIXEL_DIST["std"]))
            merged = image_normalizing(merged, PIXEL_DIST["mean"], PIXEL_DIST["std"], norm_all=True)
            createFolder(scrambled_folder_path)
            Image.fromarray(merged).convert("L").save(os.path.join(scrambled_folder_path, '{0}_{1}.png'.format(filename.split('/')[-1].split('.')[0], phi)))

def render_linear_transform_set(filename, save_route, subdir, var_type, var_number, max_var, min_var, divide_folder, render_scrambled_set, set_subfolder):

    var_list = np.linspace(min_var, max_var, var_number)

    # pick background image randomly
    background_file_path = os.path.join(ROOT_DIR, "background")
    file_list = os.listdir(background_file_path)
    for file in file_list:
        if not os.path.isfile(os.path.join(background_file_path, file)) or file[0] == '.':
            file_list.remove(file)

    main_viewpoint = CLASS_MAIN_VIEWPOINT[subdir]

    image = image_normalizing(offRender(filename, 0, 0, main_viewpoint), PIXEL_DIST["mean"], PIXEL_DIST["std"])
    background_file = os.path.join(background_file_path, random.choice(file_list))

    for var in var_list:
        normal_folder_path = save_route
        scrambled_folder_path = save_route
        if set_subfolder:
            normal_folder_path = os.path.join(normal_folder_path, var_type)
            scrambled_folder_path = os.path.join(scrambled_folder_path, var_type)
        normal_folder_path = os.path.join(normal_folder_path, subdir)
        scrambled_folder_path = os.path.join(scrambled_folder_path, subdir + "_scrambled")
        if divide_folder:
            normal_folder_path = os.path.join(normal_folder_path, str(var))
            scrambled_folder_path = os.path.join(scrambled_folder_path, str(var))

        # linear transformed Image
        if var_type == "translation":
            transformed_image = image_translation(image, var)
        elif var_type == "rotation":
            transformed_image = image_rotation(image, var)
        elif var_type == "scaling":
            transformed_image = image_scaling(image, var)

        # Normal image set
        background = image_normalizing(np.asarray(Image.open(background_file).convert("L").resize(SHAPE)), PIXEL_DIST["mean"], PIXEL_DIST["std"])
        merged = mergeBgFg(transformed_image, image_normalizing(phaseScrambledBg(background, PIXEL_DIST["mean"], PIXEL_DIST["std"]), PIXEL_DIST["mean"], PIXEL_DIST["std"], True))
        merged = image_normalizing(merged, PIXEL_DIST["mean"], PIXEL_DIST["std"], True)
        createFolder(normal_folder_path)
        Image.fromarray(merged).convert("L").save(os.path.join(normal_folder_path, '{0}_{1}.png'.format(filename.split('/')[-1].split('.')[0], var)))

        # Scrambled image set
        if render_scrambled_set:
            background = image_normalizing(np.asarray(Image.open(background_file).convert("L").resize(SHAPE)), PIXEL_DIST["mean"], PIXEL_DIST["std"])
            merged = mergeBgFg(scramble_image_generator(transformed_image), image_normalizing(phaseScrambledBg(background, PIXEL_DIST["mean"], PIXEL_DIST["std"]), PIXEL_DIST["mean"], PIXEL_DIST["std"], True))
            merged = image_normalizing(merged, PIXEL_DIST["mean"], PIXEL_DIST["std"], True)
            createFolder(scrambled_folder_path)
            Image.fromarray(merged).convert("L").save(os.path.join(scrambled_folder_path, '{0}_{1}.png'.format(filename.split('/')[-1].split('.')[0], var)))

def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)

def generate_batch(filename, save_route, subdir, var_type, var_number=0, max_var=0, min_var=0, divide_folder = True, render_scrambled_set = True, set_subfolder = True):
    if var_type == "None":
        phi = 0
        delta = 0
        render_non_variance_set(filename, save_route, subdir, phi, delta, render_scrambled_set, set_subfolder)
    elif var_type == "viewpoint":
        render_viewpoint_set(filename, save_route, subdir, var_number, max_var, min_var, divide_folder, render_scrambled_set, set_subfolder)
    else:
        render_linear_transform_set(filename, save_route, subdir, var_type, var_number, max_var, min_var, divide_folder, render_scrambled_set, set_subfolder)