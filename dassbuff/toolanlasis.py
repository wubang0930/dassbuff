import json

# 原始字符串（需手动补全外层结构）
original_str = '''
oldAccount:{"nickName":"mofumofu2364","userNameModifyCount":0,"updateTime":1654407452548,"global":false,"registerType":"1","userName":"jky_n586fy77t3dx","type":1,"uid":"982895936344686592","createBy":"982895936344686592","isDeleted":false,"createTime":1654407452548,"updateBy":"982895936344686592","profileId":167538,"birthdayModifyCount":0,"id":5581060020985,"belongBrandChannel":1,"email":"mofumofu2364@gmail.com","status":4},
oldProfileAccount:{"gender":0,"contactEmail":"mofumofu2364@gmail.com","nickName":"mofumofu2364","userNameModifyCount":0,"ipAddress":"172.16.12.247","updateTime":1654407452548,"global":false,"uid":"982895936344686592","createBy":"982895936344686592","isDeleted":false,"createTime":1654407452548,"updateBy":"982895936344686592","existPassword":false,"id":167538},
accountThirdList:[],cancelTime:1719889765557
'''




# 解析逻辑
def parse_custom_json(s):
    # 手动补全外层结构
    s = s.strip().replace('},', '}},')
    # 分割顶层键值对
    parts = s.strip().split('},')
    result = {}

    # 遍历，并获取当前的位置
    for i, part in enumerate(parts):
        if i <=1:
            # 去除可能存在的多余逗号
            part = part.rstrip(',')
            # 分割键和值（仅分割一次）
            key, value_str = part.split(':', 1)
            key = key.strip()
            # 解析值部分（需确保值是合法JSON）
            value_str = value_str.strip()
            # 确保最后一个对象的右括号存在
            value = json.loads(value_str)
            result[key] = value
        else:
            # 截取cancelTime:后面的内容
            value_str = part.strip().split('cancelTime:')[1]
            result['cancelTime'] = int(value_str)

    return result


# 转换并打印结果
all_data = []

with open('E:\\projectInfo\\华宝新能\\user-service\\20250305-注销账户同步user\\xxx2.txt', 'r', encoding='utf-8') as f:
    #一行一行的读出来
    for line in f:
        parsed_data = parse_custom_json(line)
        all_data.append(parsed_data)

all_filter_data = []

if all_data is not None:
    for data in all_data:
        
        cancle_user={}
        cancle_user['jackeryId'] = data['oldAccount']['userName']
        cancle_user['registerTime'] = int(data['oldAccount']['createTime'] )      
        cancle_user['cancelTime'] = int(data['cancelTime'] )      
        cancle_user['uid'] = data['oldAccount']['uid']  
        cancle_user['email'] = data['oldAccount']['email']  
        cancle_user['remark'] = "jackery-client cancle"
        all_filter_data.append(cancle_user)

print(all_filter_data)
            
            
