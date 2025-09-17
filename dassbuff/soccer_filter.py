import json
from turtle import end_fill
import pandas as pd
import datetime




file_path = r'F:\myFiles\数据分析\数据分析最佳\20250917-分析.txt'

def load_json_data(file_path):
    """
    加载json文件，支持整体为数组（即整个文件是[{},{}]）或每行一个json对象的格式，自动跳过格式错误的行。
    针对整体为数组的情况，做了兼容处理。
    """
    data = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
            if content.startswith('[') and content.endswith(']'):
                try:
                    data = json.loads(content)
                except Exception as e:
                    print(f"整体数组格式解析失败: {e}")
                    data = []
            else:
                f.seek(0)
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        obj = json.loads(line)
                        data.append(obj)
                    except Exception as e:
                        print(f"跳过格式错误的行: {line}，错误: {e}")
    except Exception as e:
        print(f"文件读取失败: {e}")
        data = []
    return data

def build_result_dict(data_list):
    """
    构建字典，key为"初始数量,当前时间,当前数量"，value为[当前预期结束数量, 结束数量]的集合
    """
    result_dict = {}
    for item in data_list:
        if not isinstance(item, dict):
            continue
        key = f"{item.get('初始数量','')},{item.get('当前时间','')},{item.get('当前数量','')}"
        value = (item.get('当前预期结束数量',''), item.get('结束数量',''), item.get('id',''))
        if key not in result_dict:
            result_dict[key] = set()
        result_dict[key].add(value)
    return result_dict

def win_result(result_dict):
    """
    汇总统计，返回summary_set列表
    """
    win_set = []
    for k, v in result_dict.items():
        total_count = 0
        ping_zero = 0
        win_half = 0
        lose_half = 0
        win_all = 0
        lose_all = 0
        for value in v:
            try:
                cur_end = float(value[0])
                end = float(value[1])
                diff = end - cur_end 
                total_count += 1
                # 1e-8表示1乘以10的负8次方，即0.00000001，用于判断两个浮点数是否足够接近（近似相等）
                if abs(diff - 0) < 1e-8:
                    ping_zero += 1
                elif diff == 0.25:
                    win_half += 1
                elif diff == -0.25:
                    lose_half += 1
                if diff >= 0.5:
                    win_all += 1
                if diff <= -0.5:
                    lose_all += 1
            except Exception as e:
                print(f"数据解析错误: {value}, 错误: {e}")

        if total_count >= 50:
            denominator = win_all + win_half*0.5 + lose_all + lose_half*0.5
            if denominator > 0 and (win_all + win_half*0.5)/denominator >= 0.55:
                # print("符合条件:",k,cur_end,end,ping_zero,win_half,lose_half,win_all,lose_all,denominator)
                init_num, cur_time, cur_num = k.split(",")
                win_rate = (win_all + win_half*0.5)/denominator * 100
                win_obj = {
                    "初始数量": init_num,
                    "当前时间": cur_time,
                    "当前数量": cur_num,
                    "总数量": total_count,
                    "平": ping_zero,
                    "胜一半": win_half,
                    "负一半": lose_half,
                    "胜": win_all,
                    "负": lose_all,
                    "胜率": f"{win_rate:.1f}%",
                    "实际数据": list(v)
                }
                win_set.append(win_obj)
    return win_set


def small_result(result_dict):
    """
    汇总统计，返回summary_set列表
    """
    small_set = []
    for k, v in result_dict.items():
        total_count = 0
        ping_zero = 0
        win_half = 0
        lose_half = 0
        win_all = 0
        lose_all = 0
        for value in v:
            try:
                cur_end = float(value[0])
                end = float(value[1])
                diff = end - cur_end 
                total_count += 1
                # 1e-8表示1乘以10的负8次方，即0.00000001，用于判断两个浮点数是否足够接近（近似相等）
                if abs(diff - 0) < 1e-8:
                    ping_zero += 1
                elif diff == 0.25:
                    lose_half += 1
                elif diff == -0.25:
                    win_half += 1
                if diff >= 0.5:
                   lose_all += 1
                if diff <= -0.5:
                    win_all += 1
            except Exception as e:
                print(f"数据解析错误: {value}, 错误: {e}")

        if total_count >= 50:
            denominator = win_all + win_half*0.5 + lose_all + lose_half*0.5
            if denominator > 0 and (win_all + win_half*0.5)/denominator >= 0.55:
                # print("符合条件:",k,cur_end,end,ping_zero,win_half,lose_half,win_all,lose_all,denominator)
                init_num, cur_time, cur_num = k.split(",")
                win_rate = (win_all + win_half*0.5)/denominator * 100
                smarll_obj = {
                    "初始数量": init_num,
                    "当前时间": cur_time,
                    "当前数量": cur_num,
                    "总数量": total_count,
                    "平": ping_zero,
                    "胜一半": win_half,
                    "负一半": lose_half,
                    "胜": win_all,
                    "负": lose_all,
                    "胜率": f"{win_rate:.1f}%",
                    "实际数据": list(v)
                }
                small_set.append(smarll_obj)
    return small_set


def export_to_excel(summary_set,file_name, output_dir=r"F:\myFiles\数据分析\数据分析最佳"):
    """
    将summary_set按照初始数量升序，当前时间升序排序后导出到指定目录的Excel文件，文件名加上时间戳
    """
    df = pd.DataFrame(summary_set)
    if df.empty:
        print("没有可导出的数据")
        return
    df["初始数量"] = pd.to_numeric(df["初始数量"], errors="coerce")
    df["当前时间"] = pd.to_numeric(df["当前时间"], errors="coerce")
    df["当前数量"] = pd.to_numeric(df["当前数量"], errors="coerce")
    df = df.sort_values(by=["初始数量", "当前时间", "当前数量"], ascending=[True, True, True])
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    excel_filename = fr"{output_dir}\{file_name}{timestamp}.xlsx"
    df.to_excel(excel_filename, index=False)
    print(f"已将summary_set导出到 {excel_filename}")
    

# 查询sql，将数据导出为excel文件，并转换为json.txt，然后运行本脚本分析
# SELECT
# 	st.soccer_id AS 'id',
# 	st.m_type_value AS '初始数量',
# 	an.c_time AS '当前时间',
# 	an.m_type_value AS '当前预期结束数量',
# 	an.goal_home + an.goal_guest AS '当前数量',
# 	en.m_type_value AS '结束数量' 
# FROM
# 	soccer_analysis_start_new st
# 	LEFT JOIN soccer_analysis an ON st.soccer_id = an.soccer_id
# 	LEFT JOIN soccer_analysis_end_new en ON st.soccer_id = en.soccer_id 
# WHERE
# 	en.soccer_id IS NOT NULL 
# 	and en.m_type_value IS NOT NULL 
# 	AND st.m_type_value >= 2 
# 	AND st.m_type_value <= 3.5
# 	and ((an.c_time>=50 and  an.c_time<=85 ) or (an.c_time>=1 and  an.c_time<=40) )
def main():
    data_list = load_json_data(file_path)
    result_dict = build_result_dict(data_list)
    win_set = win_result(result_dict)
    export_to_excel(win_set,"大初数量时间结果分析_")

    small_set = small_result(result_dict)
    export_to_excel(small_set,"小初数量时间结果分析_")

if __name__ == "__main__":
    main()