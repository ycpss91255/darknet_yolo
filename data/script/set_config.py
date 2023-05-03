#!/usr/bin/env python3
from os import path
from glob import iglob
from shutil import copy


def main():
    # Adjustable parameters
    train_ratio = 90

    # Do not tune parameters unless necessary
    obj_folder = "obj"
    image_format = "jpg"

    train_file = 'train.txt'
    valid_file = 'valid.txt'

    obj_data_file = "obj.data"

    classes_file = "classes.txt"
    obj_names_file = "obj.names"

    # Non-tunable parameters
    data_folder = path.abspath(path.join(path.dirname(__file__), '..'))
    obj_folder = path.join(data_folder, obj_folder)
    classes_file = path.join(obj_folder, classes_file)
    train_file = path.join(data_folder, train_file)
    valid_file = path.join(data_folder, valid_file)
    obj_data_file = path.join(data_folder, obj_data_file)
    obj_names_file = path.join(data_folder, obj_names_file)

    jpg_list = list(iglob(path.join(obj_folder, '*.', image_format)))
    jpg_num = len(jpg_list)

    train_num = int(jpg_num * train_ratio / 100)
    valid_num = jpg_num - train_num
    classes_num = 0

    # Copy classes_file to obj_names_file
    copy(classes_file, obj_names_file)

    # Write data config to obj_data_file
    with open(classes_file, 'r') as file:
        lines = file.readlines()
        non_empty_lines = [line for line in lines if len(line.strip())]
        classes_num = len(non_empty_lines)

    obj_config = f"""classes = {classes_num}
train = {train_file}
valid = {valid_file}
names = {obj_names_file}
backup = {data_folder}/weights
"""
    with open(obj_data_file, 'w') as f:
        f.write(obj_config)

    # Write train object list to train_file
    with open(train_file, 'w') as f:
        f.write('\n' .join(jpg_list[:train_num]) + '\n')

    # Write valid object list to valid_file
    if train_ratio < 100:
        with open(valid_file, 'w') as f:
            f.write('\n' .join(jpg_list[train_num + 1:]) + '\n')

    # Print parameters
    print('{:<18}{:<}'.format('obj_folder', obj_folder))
    print('{:<18}{:<}'.format('classes_file', classes_file))
    print('{:<18}{:<}'.format('image_format', image_format))
    print('---')
    print('{:<18}{:<}'.format('train_file', train_file))
    print('{:<18}{:<}'.format('valid_file', valid_file))
    print('{:<18}{:<}'.format('obj_data_file', obj_data_file))
    print('{:<18}{:<}'.format('obj_names_file', obj_names_file))
    print('---')
    print('---')
    print('{:<18}{:<}%'.format('train_ratio', train_ratio))
    print('{:<18}{:<}%'.format('valid_ratio', 100 - train_ratio))
    print('{:<18}{:<}'.format('total object num', jpg_num))
    print('{:<18}{:<}'.format('train_num', train_num))
    print('{:<18}{:<}'.format('valid_num', valid_num))


if __name__ == '__main__':
    main()
