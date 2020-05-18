import json, sys

def create_dataset():
    with open('./local.json') as json_file:
        data = json.load(json_file)

    locations = {}

    for item in data:
        districts = {}
        for item2 in item['districts']:
            # print(item2)
            wards=[o['name'] for o in item2['wards']]
            # Tất cả các xã của 1 huyện
            districts[item2['name']]=wards
        locations[item['name']] = districts
    with open('dataset.json', 'w', encoding='utf8') as fp:
        json.dump(locations, fp, ensure_ascii=False)
    print("OK!")

def test():
    with open('dataset.json', 'r') as fp:
        new_data = json.load(fp)
    print(new_data['Quảng Nam']['Tiên Phước'])
    print(new_data.keys())
if __name__ == "__main__":

    
    
    test()


    


    
    
    