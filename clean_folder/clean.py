"""Procedure for sorting files in directory
    All files and folders are renamed using the normalize function;
    File extensions do not change after renaming;
    Empty folders are deleted;
    The unpacked contents of the archive are transferred to the archives' folder
    in a sub folder named the same as the archive;
    Files whose extensions are unknown remain unchanged.
"""

import os
import re
import shutil
import sys


CYRILLIC_SYMBOLS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюяєіїґ'
TRANSLATION = ("a", "b", "v", "g", "d", "e", "e", "j", "z", "i", "j", "k", "l", "m", "n", "o", "p", "r", "s", "t", "u",
               "f", "h", "ts", "ch", "sh", "sch", "", "y", "", "e", "yu", "u", "ja", "je", "ji", "g")

TRANS = {}
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()


def normalize(name: str) -> str:
    t_name = name.translate(TRANS)
    t_name = re.sub(r'[^a-zA-Z\d_\.]', '_', t_name)
    return t_name


# key names is new folder names
extensions = {

    'images': ['jpeg', 'png', 'jpg', 'svg'],

    'video': ['avi', 'mp4', 'mov', 'mkv'],

    'documents': ['pdf', 'txt', 'doc', 'docx', 'rtf', 'tex', 'wpd', 'odt'],

    'audio': ['mp3', 'ogg', 'wav', 'amr'],

    'archives': ['zip', 'gz', 'tar'],

    'other': []  # for unknown extensions

}

if len(sys.argv) != 2:
    print("\n\033[31mNeed a name of the folder for sorting\033[0m\n")
    quit()

else:
    root_folder = sys.argv[1]


def tree_items(path):
    all_addresses = []
    for address, dirs, files in os.walk(path):
        for name in files:
            all_addresses.append(os.path.join(f'{address}\\{name}'))
    return all_addresses


def create_folders_from_list(folder_path, folder_names):
    for folder in folder_names:
        if not os.path.exists(f'{folder_path}\\{folder}'):
            os.mkdir(f'{folder_path}\\{folder}')


def sort_files(folder_path):
    file_paths = tree_items(folder_path)
    ext_list = list(extensions.items())

    for file_path in file_paths:
        extension = str(file_path.split('.')[-1])
        file_name = normalize(str(file_path.split('\\')[-1]))

        for dict_key_int in range(len(ext_list)):
            if extension in ext_list[dict_key_int][1]:
                if os.path.exists(f'{root_folder}\\{ext_list[dict_key_int][0]}\\{file_name}'):
                    file_name += '.copy'
                os.rename(
                    file_path, f'{root_folder}\\{ext_list[dict_key_int][0]}\\{file_name}')
                break
            if dict_key_int == len(ext_list) - 1:
                if os.path.exists(f'{root_folder}\\{ext_list[dict_key_int][0]}\\{file_name}'):
                    file_name += '.copy'
                os.rename(
                    file_path, f'{root_folder}\\{ext_list[dict_key_int][0]}\\{file_name}')


def remove_empty_folders(folder_path):
    dir_list = []
    for root, dirs, files in os.walk(folder_path):
        dir_list.append(root)
    for root in dir_list[::-1]:
        if not os.listdir(root):
            os.rmdir(root)


def unpack_file(folder_path):
    for archive in os.listdir(folder_path):
        archive_name = archive.split('.')[0]
        if not os.path.exists(f'{folder_path}\\{archive_name}'):
            os.mkdir(f'{folder_path}\\{archive_name}')
        shutil.unpack_archive(
            f'{folder_path}\\{archive}', f'{folder_path}\\{archive_name}')
        os.remove(f'{folder_path}\\{archive}')


def main():
    create_folders_from_list(root_folder, extensions)
    sort_files(root_folder)
    remove_empty_folders(root_folder)
    unpack_file(f'{root_folder}\\archives')


if __name__ == "__main__":
    main()
