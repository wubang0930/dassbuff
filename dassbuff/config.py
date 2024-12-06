
# 账号1的配置
dmarket_public_key = "341c7893bd5d1cf05150a38fcabd4008f01e9edb473e7c91ea5199ce088b0b8b"
dmarket_secret_key = "4016059fb0b3b6ba29c31cb06a224c5951312a7b0a59e964faf558ce0c1e65af341c7893bd5d1cf05150a38fcabd4008f01e9edb473e7c91ea5199ce088b0b8b"
authorization="eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJlOTNkMWQxZC0wMjk1LTRiNWItOTA2YS1hYWJmZDhkZDZjM2EiLCJleHAiOjE3MzIwODE4MjIsImlhdCI6MTcyOTQ4OTgyMiwic2lkIjoiYjJmZjBiODAtMTU4Ni00Y2FkLWI4OGYtMzIwZDIxZmFkZDFkIiwidHlwIjoiYWNjZXNzIiwiaWQiOiI0MWU0Y2RlZC1hMDcxLTRiMDUtODRjYS1lYzM2OWEzZjYyZjUiLCJwdmQiOiJyZWd1bGFyIiwicHJ0IjoiMjQxMCIsImF0dHJpYnV0ZXMiOnsic2FnYV93YWxsZXRfYWRkcmVzcyI6IjB4Qzc5ZmUzOGMzQjgzMmQ4NTZkMkYxRWZBMEZjMDBFRTMxOEE5MzY2NCIsImFjY291bnRfaWQiOiI4NmFmZDFmZi0wNWU4LTQ3MzktOTM2ZC03YjY1ZTA5ZDc4NWUiLCJ3YWxsZXRfaWQiOiJmODUxMzhiNzQ1YWI0YjJjYWM1NjdlMWYwNWY3ZWY0ZmU0MmMxNTNjMmQxODQ0MzViODY5OTc4M2QwOWM5ODE1In19.PMWgHARt63_aDp5ntYF6lkn3ffb-pG8rQTngRRhO9jP54Fm_K9NvNuKk_7JbBEckdZRy8dnSg3gqlIvFgk49eA"


# 账号2的配置
dmarket_public_key_two = "2ca4af55da5504955e59a7c276bf163e550043ef00e441e8f87711737185fe7a"
dmarket_secret_key_two = "096af639e5d36777278465a0aa3cdada54f0944dbdda231292086d4bc3072c8a2ca4af55da5504955e59a7c276bf163e550043ef00e441e8f87711737185fe7a"
authorization_two="eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiI3YzExMzVhOS0yZGMwLTRjMTktODQ1Zi1lOTE5NWNiYzE4YzUiLCJleHAiOjE3MzQxNjE2NzAsImlhdCI6MTczMTU2OTY3MCwic2lkIjoiODI1NGEwMzctYWMxMC00Yjg0LWIwZGItYmM4MThkMGM0ZTk5IiwidHlwIjoiYWNjZXNzIiwiaWQiOiJiYjNmNTkyZS03ZWEwLTQ2ZDQtODYzMS1lNTk5ODE2YzI4ZjMiLCJwdmQiOiJtcCIsInBydCI6IjI0MTEiLCJhdHRyaWJ1dGVzIjp7InNhZ2Ffd2FsbGV0X2FkZHJlc3MiOiIweDdmZGYyZDBFZWEwMTdFNjFhNzg5MjhiZDI0N0M3MmM5NDU2QTllRTUiLCJhY2NvdW50X2lkIjoiNTFiNTQyNjMtMWFkZi00MmVlLTg5Y2UtOGZkYTYzZjM0MWRiIiwid2FsbGV0X2lkIjoiN2RlZjVkZTUxMjQ1NDRmNmI5MDdjZmI1YjI0NzBlNzhhOGNjZGRjNGUwOTY0M2E2YWZiNWYxY2NmZmEwYTZkYSJ9fQ.ValhrSdpTAxPcR_J1YKdcTqS5_nLB6AI920j2DnWaliK2JRcUdgw52SH_5pmqdPwYTPZmbeQlg9UkZbtLjIDyg"



# 初始化文件夹
data_local="data_local"
data_local_excel=data_local+"/excel"
data_local_analysis=data_local+"/analysis"

#文件路径-源文件
cs_product_all_name="data/cs_product_all_name.txt"


#文件路径-查询数据
skin_86_product_all=data_local_analysis+"/skin_86_product_all.txt" # buff的源数据
# skin_86_product_all_buy=data_local_analysis+"/skin_86_product_all_buy.txt" # buff的源数据
buff_filter_file=data_local_analysis+"/skin_86_filter_file.txt" # buff的源数据
filter_data_not_buy="data/filter_data_not_buy.txt" # 过滤购买的数据


# 查询 三羊平台的数据实时分析导购
skin_86_product_all_buff=data_local_analysis+"/skin_86_product_all_buff.txt" # buff的源数据
skin_86_product_all_yp=data_local_analysis+"/skin_86_product_all_yp.txt" # buff的源数据
skin_86_product_all_igxe=data_local_analysis+"/skin_86_product_all_igxe.txt" # buff的源数据
skin_86_product_all_steam=data_local_analysis+"/skin_86_product_all_steam.txt" # buff的源数据
csgo_db_deal=data_local_analysis+"/csgo_db_deal.txt" # 实时成交数据



# 保存 三羊平台的数据到数据库 每天定时查询
skin_86_product_all_buff_mysql=data_local_analysis+"/skin_86_product_all_buff_mysql.txt" # buff的源数据
skin_86_product_all_yp_mysql=data_local_analysis+"/skin_86_product_all_yp_mysql.txt" # buff的源数据
skin_86_product_all_igxe_mysql=data_local_analysis+"/skin_86_product_all_igxe_mysql.txt" # buff的源数据
skin_86_product_all_steam_mysql=data_local_analysis+"/skin_86_product_all_steam_mysql.txt" # buff的源数据
csgo_db_deal_mysql=data_local_analysis+"/csgo_db_deal_mysql.txt" # 实时成交数据

# 下载挂刀网站的数据，分析导购
priority_archive="priority_archive.json"



# 出售购买记录
my_buy_current_file=data_local_analysis+"/my_buy_list.txt"
my_buy_current_file_two=data_local_analysis+"/my_buy_list_two.txt"




itone_authorization='tt_khhx2zwJn8LD0kwFzlOldbdtA7pD7WuX.fd6d5ef0ca123454ebc3937c89e47b7f'