import yaml
import os

import tqdm
import requests


def countFiles(path: str, name: str, ext: str) -> int:
    count = 0
    for fileName in os.listdir(path):
        # Если директория, то пропустить
        if not os.path.isfile(path + '\\' + fileName):
            continue
        if fileName.find(name) != -1 and fileName.endswith(ext):
            count += 1
    return count


def downloadFromURL(url: str, outputName: str):
    r = requests.get(url, stream=True)
    with open(outputName, 'wb') as handle:
        for data in tqdm(r.iter_content()):
            handle.write(data)


class Entry(yaml.YAMLObject):
    yaml_tag = "!entry"
    yaml_loader = yaml.SafeLoader

    def __init__(self, name, link) -> None:
        self.name = name
        self.link = link


class EntrysManager:
    def __init__(self) -> None:
        self.entrys = []

    def loadYAML(self, fileName: str) -> None:
        with open(fileName, 'r') as file:
            self.entrys = yaml.safe_load(file)

    def dumpToYAML(self, fileName: str = 'subs_out.yaml') -> None:
        with open(fileName, 'w') as file:
            file.write(yaml.dump(self.entrys))

    def addEntry(self, entry: Entry) -> None:
        self.entrys.append(entry)

    def getEntrys(self) -> list[Entry]:
        return self.entrys

    def downloadSubs(self):
        # цикл: для каждого элемента списка
        for entry in self.entrys:
            # Найти папку
            path = animesDir + '\\' + entry.name
            if not os.path.isdir(path):
                print('Дириктория для \'' + entry.name + '\' не найдена!')
                continue

            # В папке посчитать кол-во скаченных серий
            downloadedSeries = countFiles(path, entry.name, '.mkv')

            # Посчитать кол-во скаченных файлов субтитров
            downloadedSubs = countFiles(path, entry.name, '.ass')

            print(entry.name, ' Cкачено серий: ', downloadedSeries,
                  ', скачено сабов: ', downloadedSubs)

            # Если субтитров меньше чем серий добавить элемент списка в список на обновление
            if downloadedSeries < downloadedSubs:
                print('Все субтитры скачены: ' + entry.name)
            else:
                print('Есть нескаченные субтитры: ' + entry.name)

            # : конец цикла


if __name__ == '__main__':
    animesDir = 'D:\Libraries\Videos\Anime'

    manager = EntrysManager()

    # Загрузить список название_аниме+ссылка_на_сабы
    manager.loadYAML(animesDir + '\subs.yaml')

    # Для каждого элемента в списке скачать сабы
    manager.downloadSubs()

    url = 'http://fansubs.ru/base.php?srt=13172'
    fileName = 'Tensei shitara Ken Deshita.zip'

    # downloadFromURL(url, fileName)

    # цикл: для каждого эл. списка на обновление

    # Скачать архив с сабами в папку с соответствующим аниме
    # Разархивировать в эту же папку
    # Скопировать .ass файлы в папку с сериями
    # !!!Переименовать каждый .ass файл в имя файла соответствующей серии

    # : конец цикла
