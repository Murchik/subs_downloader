import json
import os
import shutil
import sys

import requests
from tqdm import tqdm
import patoolib


def load_conf(file_name: str):
    """
    Загружает конфиг файл
    :param file_name:
    :return:
    """
    try:
        with open(file_name, encoding='UTF-8') as file:
            conf = json.load(file)
            entries = [entry for entry in conf.get('entries')]
            path = conf.get('dir')
            return entries, path
    except FileNotFoundError:
        print('Введите корректное имя конфиг файла')
        exit()


def get_subs(anime_path: str, anime_name: str, url: str):
    """
    Удаляет из папки предыдущие субтитры и добавляет новые
    :param anime_path:
    :param anime_name:
    :param url:
    :return:
    """
    # TODO поиск сабов по названию аниме и извлечение ссылки на скачивание архива

    dir_path = os.path.join(anime_path, anime_name)

    try:
        for path in os.listdir(dir_path):
            file_path = os.path.join(dir_path, path)
            if os.path.isdir(file_path):
                shutil.rmtree(file_path)
            if os.path.isfile(file_path):
                if path.endswith('.ass'):
                    os.remove(file_path)
    except FileNotFoundError:
        print('Введите корректную папку с аниме в конфиг файле')
        exit()

    subs_archive = anime_name + '.rar'
    r = requests.get(url, stream=True)

    with open(subs_archive, 'wb') as f:
        for data in tqdm(r.iter_content()):
            f.write(data)

    patoolib.extract_archive(subs_archive, outdir=dir_path)
    os.remove(subs_archive)


def attach_subs(anime_path: str, anime_name: str):
    """
    Переименновывает субтитры для корректной подвязки к соответсвующим эпизодам
    :param anime_path:
    :param anime_name:
    :return:
    """
    anime_list = []
    subs_list = []
    dir_path = os.path.join(anime_path, anime_name)
    for path in os.listdir(dir_path):
        if os.path.isfile(os.path.join(dir_path, path)):
            if path.endswith('.txt'):
                anime_list.append(os.path.join(dir_path, path))
            if path.endswith('.ass'):
                subs_list.append(os.path.join(dir_path, path))

    for anime, subs in zip(anime_list, subs_list):
        new_subs_name = anime.replace('.txt', '.ass')  # заменить .txt на расширение видео
        os.rename(subs, new_subs_name)


def main():
    if len(sys.argv) == 2:
        conf_filename = sys.argv[1]
    else:
        print('Введите путь до конфиг файла')
        exit()

    entries, anime_path = load_conf(conf_filename)

    for entry in entries:
        get_subs(anime_path, entry.get('name'), entry.get('link'))
        attach_subs(anime_path, entry.get('name'))


if __name__ == '__main__':
    main()

