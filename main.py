import yaml


class Entry(yaml.YAMLObject):
    yaml_tag = "!entry"
    yaml_loader = yaml.SafeLoader

    def __init__(self, name, link) -> None:
        self.name = name
        self.link = link


def load_from_yaml(file_name: str) -> list[Entry]:
    with open(file_name, 'r', encoding='UTF-8') as file:
        entrys = yaml.safe_load(file)
        return entrys


def dump_to_yaml(entrys: list[Entry], file_name: str) -> None:
    with open(file_name, 'w', encoding='UTF-8') as file:
        file.write(yaml.dump(entrys))


if __name__ == '__main__':
    animes = load_from_yaml('./subs_out.yaml')
    print(type(animes))
    for entry in animes:
        print(entry.name)
