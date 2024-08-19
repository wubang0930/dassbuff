import json
import pandas as pd
from datetime import datetime
import time


data_path="E:/pythonFile/python/python_data/dassbuff/data"


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
    with open(data_path+'/analysis/1_cs_buff_uu_c5_base.json', 'r', encoding='utf-8') as base:
        with open('data/cs_product_all_name.txt', 'w', encoding='utf-8') as all_name:
            with open('data/cs_product_cn_name.txt', 'w', encoding='utf-8') as cn_name:
                num = 0
                for line in base:
                    num += 1
                    line_date=json.loads(line)

                    
                    buff_buy_price= line_date['buff_buy']['price']
                    buff_sale_price= line_date['buff_sell']['price']
                    buff_sale_count= line_date['buff_sell']['count'] if line_date['buff_sell']['count'] is not None else 0

                    c5_buy_price= line_date['c5_buy']['price']
                    c5_sale_price= line_date['c5_sell']['price']
                    c5_sale_count= line_date['c5_sell']['count'] if line_date['c5_sell']['count'] is not None else 0

                    igxe_buy_price= line_date['igxe_buy']['price']
                    igxe_sale_price= line_date['igxe_sell']['price']
                    igxe_sale_count= line_date['igxe_sell']['count'] if line_date['igxe_sell']['count'] is not None else 0


                    uuyp_buy_price= line_date['uuyp_buy']['price']
                    uuyp_sale_price= line_date['uuyp_sell']['price']
                    uuyp_sale_count= line_date['uuyp_sell']['count'] if line_date['uuyp_sell']['count'] is not None else 0


                    steam_buy_price= line_date['steam_order']['buy_price']  
                    steam_sale_price= line_date['steam_order']['sell_price']  
                    steam_buy_count= line_date['steam_order']['buy_order_count']  if line_date['steam_order']['buy_order_count'] is not None else 99999
                    steam_sale_count= line_date['steam_order']['sell_order_count']  if line_date['steam_order']['sell_order_count'] is not None else 99999


                    buy_prices=[buff_buy_price,c5_buy_price,igxe_buy_price,uuyp_buy_price]
                    sale_prices=[buff_sale_price,c5_sale_price,igxe_sale_price,uuyp_sale_price]
                    sale_account=[buff_sale_count,c5_sale_count,igxe_sale_count,uuyp_sale_count]


                    buy_prices_none=[price for price in buy_prices if price is not None]
                    sale_prices_none=[price for price in sale_prices if price is not None]
                    sale_account_none=[price for price in sale_account if price is not None]

                    min_buy_price=min(buy_prices_none) if buy_prices_none else 0
                    min_sale_price=min(sale_prices_none) if sale_prices_none else 0
                    
                    max_buy_price=max(buy_prices_none) if buy_prices_none else 0
                    max_sale_price=max(sale_prices_none) if sale_prices_none else 0



                    max_sale_account=max(sale_account_none) if sale_account_none else 0
                    # 优先以buff的出售数量为准
                    if buff_sale_count >0:
                        max_sale_account=buff_sale_count
                    
                    # 只获取cs的饰品数据名称
                    if line_date["appid"]== 730 and "印花" not in line_date['cn_name'] and "涂鸦" not in line_date['cn_name'] and "纪念品" not in line_date['cn_name'] and min_sale_price>1 and max_sale_account>500 :
                        print(line_date["appid"])
                        all_names=line_date['cn_name']+'----'+line_date['en_name']+'----'+str(min_sale_price)+'----'+str(max_sale_account)+'----'+str(buff_sale_count)

                        all_name.write(all_names+'\n')
                        cn_name.write(line_date['cn_name']+'\n')

        


# 一行一行的读取json数组，并写入到excel中
def export_json_to_excel():
    filename="dmakert_all_"+"".join(datetime.now().strftime("%Y%m%d%H%M%S"))+".xlsx"
    all_data=[]
    # 打开文件准备读取
    with open('dassbuff/data/3_cs_dmarket_price_all.txt', 'r', encoding='utf-8') as file:
       for line in file:
           json_data=json.loads(line.replace("\\b",""))
           for single in json_data:
               all_data.append(single)


    # 将JSON数据转换为pandas DataFrame
    df = pd.DataFrame(all_data)
    # 写入Excel文件
    # 注意：如果你需要写入.xlsx文件，需要指定引擎为openpyxl
    df.to_excel(filename, index=False, engine='openpyxl')



# 获取所有的中文和英文名称的饰品名称
def filter_test():
    filename="filter_test_"+"".join(datetime.now().strftime("%Y%m%d%H%M%S"))+".xlsx"
    print("filter_test")
    with open('dassbuff/data/filter_test.json', 'r', encoding='utf-8') as base:
        all_datas=json.load(base)
        # 只获取cs的饰品数据名称
        objects=all_datas['objects']

        num_list=[]
        for obj in objects:
            if obj['extra']['floatValue'] <0.24:
                price={}
                price['num_1']= round(float(obj['price']['USD'])/100*7.18,2)
                price['num_2']= round(float(obj['extra']['floatValue']),4)
                num_list.append(price)


        # 按age字段降序排序字典列表
        sorted_list = sorted(num_list, key=lambda x: x['num_1'], reverse=True)

        # 将JSON数据转换为pandas DataFrame
        df = pd.DataFrame(sorted_list)
        # 写入Excel文件
        # 注意：如果你需要写入.xlsx文件，需要指定引擎为openpyxl
        df.to_excel(filename, index=False, engine='openpyxl')




# 获取所有的中文饰品名称
def filter_name_cs():
    with open("dassbuff/data/analysis/1_cs_buff_uu_c5_base.json", "r", encoding='utf-8') as cs_buff_uu_c5_base:
        with open("dassbuff/data/analysis/0_origin_names.json", "w", encoding='utf-8') as origin_names_file:
            for base_info_line in cs_buff_uu_c5_base:
                base_info_json=json.loads(base_info_line)
                price=base_info_json['uuyp_sell']['price'] if base_info_json['uuyp_sell']['price'] else 99999
                sale_num=base_info_json['uuyp_sell']['count'] if base_info_json['uuyp_sell']['count'] else 0

                if base_info_json["appid"]== 730 and "印花" not in base_info_json['cn_name'] and "涂鸦" not in base_info_json['cn_name'] and price>1 and price<800 and sale_num>400:
                    origin_names_file.write(base_info_json['cn_name']+'\n')  
            


if __name__ == '__main__':
    # case_name_analysis()
    filter_all_name()
    # filter_name_cs()




