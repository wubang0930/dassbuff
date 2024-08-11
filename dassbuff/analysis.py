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
    chunk_size = 1000
    # 打开文件准备读取
    with open('dassbuff/data/base_name_copy_anallysis_add.txt', 'r', encoding='utf-8') as file:
        df_chunk = pd.DataFrame()
        for i, line in enumerate(file):
            data = json.loads(line)
            df_chunk = df_chunk._append(data, ignore_index=True)
            # 确保在第一次迭代时不执行写入操作
            if (i + 1) % chunk_size == 0:
                with pd.ExcelWriter('output.xlsx', mode='w', engine='openpyxl', if_sheet_exists='replace') as writer:
                    df_chunk.to_excel(writer, index=False, header=not writer.book.sheetnames)
                df_chunk = pd.DataFrame()  # 重置df_chunk为空
        # 处理最后一部分数据
        if not df_chunk.empty:
            with pd.ExcelWriter('output.xlsx', mode='w', engine='openpyxl', if_sheet_exists='replace') as writer:
                df_chunk.to_excel(writer, index=False, header=False)

if __name__ == '__main__':
    # case_name_analysis()
    # filter_all_name()
    export_json_to_excel()




