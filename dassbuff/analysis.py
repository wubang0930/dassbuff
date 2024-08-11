import json
import pandas as pd



# 通过获取的数据，解析出来箱子的中英文名称的json数据
def case_name_analysis():
    print("case_name_analysis")
    with open('dassbuff/data/case.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    weapons=data['weapons']
    case_analysis="dassbuff/data/case_analysis.json"

    all_weapons='{'

    with open(case_analysis, 'w', encoding='utf-8') as file:
        for weapon in weapons:
            all_weapons=all_weapons+'"'+weapon['title_ch']+'":"'+weapon['title_en']+'",'
        all_weapons=all_weapons[:-1]
        all_weapons=all_weapons+"}"
        file.write(all_weapons)




# 获取所有的中文和英文名称的饰品名称
def filter_all_name():
    print("filter_all_name")
    with open('dassbuff/data/base.json', 'r', encoding='utf-8') as base:
        with open('dassbuff/data/base_name.txt', 'w', encoding='utf-8') as base_name:
            num = 0
            for line in base:
                num += 1
                line_date=json.loads(line)
                if line_date["appid"]== 730 :
                    print(line_date["appid"])
                    all_names=line_date['cn_name']+':'+line_date['en_name']
                    base_name.write(all_names+'\n')

        


# 一行一行的读取json数组，并写入到excel中
def export_json_to_excel():
    all_data=[]
    # 打开文件准备读取
    with open('dassbuff/data/base_name_copy_anallysis.txt', 'r', encoding='utf-8') as file:
       for line in file:
           json_data=json.loads(line)
           for single in json_data:
               all_data.append(single)


    # 将JSON数据转换为pandas DataFrame
    df = pd.DataFrame(all_data)
    # 写入Excel文件
    # 注意：如果你需要写入.xlsx文件，需要指定引擎为openpyxl
    df.to_excel("output.xlsx", index=False, engine='openpyxl')



if __name__ == '__main__':
    # case_name_analysis()
    # filter_all_name()
    export_json_to_excel()




