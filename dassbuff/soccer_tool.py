


def get_m_odds_list():
    m_odds=[]
    m_odds.append(round(1.5,2))

    start_num=round(1.7,2)
    for i in range(1,40):
        start_num+=0.01
        m_odds.append(round(start_num,2))

    return m_odds

# 生产查询概率的sql语句
def get_m_odds_sql():
    all_sql=""

    m_odds=get_m_odds_list()
    print("开始生产查询概率的sql语句")
    for odd in m_odds:
        all_sql=all_sql+"""select """+str(odd)+""" as currrent_m_odds,z.odds_amount,sum(cou),sum(odds_amount_cou),GROUP_CONCAT(result_flag),GROUP_CONCAT(cou),SUM(cou) AS all_odds_amount_result,SUM(odds_amount_result_cou) AS all_result,round(SUM(odds_amount_result_cou)/sum(odds_amount_cou),3) AS all_result_rate,GROUP_CONCAT(odds_amount_result_cou) from (\
select odds_amount as odds_amount,result_flag,sum(odds_amount_result) as odds_amount_result_cou,SUM(odds_amount) as odds_amount_cou,count(1) as cou from soccer_bet_history where bet_time>'2024-12-10 18:00:00' and odds_amount in (20,30) and m_odds>="""+str(odd)+""" GROUP BY odds_amount,result_flag \
)z GROUP BY z.odds_amount"""
        if odd!=m_odds[-1]:
            all_sql=all_sql+""" UNION ALL """
    print("查询概率的sql语句生产完成")
    print(all_sql)

if __name__ == '__main__':
    get_m_odds_sql()