import json, sys
from collections import Counter
import re
from itertools import islice

from symspellpy import SymSpell, Verbosity

def correct_address(data, input):

    sym_spell = SymSpell()
    sym_spell.create_address_list_from_data(data)

    suggestions = sym_spell.lookup(input, Verbosity.ALL,
                                max_edit_distance=6)
    # display suggestion term, term frequency, and edit distance
    
    return suggestions


def find_address(input_str):
    input_str = input_str.replace('\n', ',')
    input_str = input_str.replace(';', ',')
    input_arr=[(o.strip().lstrip()) for o in input_str.split(',')]


    with open('.\\utils\\dataset\\dataset.json', 'r',encoding='utf-8') as fp:
        data = json.load(fp)
    provinces=data.keys()
    results = correct_address(provinces, input_arr[-1])
    for item in results:
        print(item)
    if (len(results)==0):
        return "Không so khớp được tỉnh/thành phố"
    key1 = results[0].term
    
    results2 = correct_address(data[key1].keys(), input_arr[-2])
    if (len(results2)==0):
       return "Không so khớp được quận/huyện"
    key2 = results2[0].term


  

    results3 = correct_address(data[key1][key2], input_arr[-3])
    if (len(results3)==0):
       return "Không so khớp được xã/phường {},{}".format(results2[0].term,results[0].term)
    # print(results3[0].term)

    final_result = '{}, {}, {}'.format(results3[0].term,results2[0].term,results[0].term)

    return final_result


def demo(path):
    from os import walk
    files = []
    for (dirpath, dirnames, filenames) in walk(path):
        files.extend(filenames)
        break
    lines = ''
    for index, f in enumerate(files):
        with open(path+'\\'+f,'r',encoding='utf-8') as sampleJson:
            sampledata = json.load(sampleJson)
            txt = sampledata['Nơi thường trú']
            lines += '\n' + str(index) + "\nĐầu vào: {}".format(txt) + "\nĐầu ra: {}".format(find_address(txt))
    f = open('hello.txt', "w", encoding="utf-8")
    f.write(lines)
    f.close()

if __name__ == "__main__":
    # print("Hello world")
    demo('.\\utils\\DataSample')