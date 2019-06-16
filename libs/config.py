import yaml


f = open(r'./config.yaml')
conf = yaml.load(f)


if __name__ == '__main__':
    print(conf)
