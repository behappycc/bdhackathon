import sys
sys.path.append("../")
from web_util import load_json, write_json

def main():
    data = load_json('new_term.json')
    new_data = {}
    for k, v in data.items():
        #print(k, v)
        #input()
        if v['popularity'] != 0 and v['coord'][0] != 0:
            new_data[k] = data[k]
    write_json(new_data, 'new_term.json')

if __name__ == '__main__':
    main()
