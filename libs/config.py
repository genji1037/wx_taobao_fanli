import yaml

try:
    f = open(r'./config.yaml')
except Exception as e:
    f = open(r'../config.yaml')
conf = yaml.load(f)

if __name__ == '__main__':
    print(conf)
