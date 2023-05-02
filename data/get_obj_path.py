#!/usr/bin/env python3
import os
import glob


def main():
    # adjustable parameters
    train_ratio = 90

    # Do not tune parameters unless necessary
    train_file = 'train.txt'
    valid_file = 'valid.txt'
    obj_folder = os.path.abspath('./obj')

    # Non-tunable parameters
    jpg_list = list(glob.iglob(os.path.join(obj_folder, '*.jpg')))
    jpg_num = len(jpg_list)

    train_num = int(jpg_num * train_ratio / 100)
    valid_num = jpg_num - train_num

    # write train object list to train_file
    with open(train_file, 'w') as f:
        f.write('\n' .join(jpg_list[:train_num]) + '\n')

    # write valid object list to valid_file
    if train_ratio < 100:
        with open(valid_file, 'w') as f:
            f.write('\n' .join(jpg_list[train_num + 1:]) + '\n')

    # print parameters
    print('{:<18}{:<}'.format('obj_folder', obj_folder))
    print('{:<18}{:<}'.format('train_file', train_file))
    print('{:<18}{:<}'.format('valid_file', valid_file))
    print('---')
    print('{:<18}{:<}'.format('train_ratio', train_ratio))
    print('{:<18}{:<}'.format('valid_ratio', 100 - train_ratio))
    print('{:<18}{:<}'.format('total object num', jpg_num))
    print('{:<18}{:<}'.format('train_num', train_num))
    print('{:<18}{:<}'.format('valid_num', valid_num))


if __name__ == '__main__':
    main()
