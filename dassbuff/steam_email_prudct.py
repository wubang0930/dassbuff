import random
import string
import os

# 随机生成邮箱和密码的函数
def generate_email_password(email_backs):

    all_emails=[]
    # 各生成50个账号
    for back in email_backs:
        for _ in range(50):
            # 生成5位小写字母
            letters = ''.join(random.choices(string.ascii_lowercase, k=5))
            # 生成2位数字
            digits = ''.join(random.choices(string.digits, k=2))
            # 拼接并输出结果
            email_chars = letters + digits

            # 生成5位小写字母
            letters_password = ''.join(random.choices(string.ascii_lowercase, k=5))
            # 生成2位数字
            digits_password = ''.join(random.choices(string.digits, k=2))

            # 拼接并输出结果
            password_chars = letters_password +digits_password
            
            email = email_chars +"@"  + back
            password = password_chars
            return_info=f"{email}----{password}"
            all_emails.append(return_info)

    return  all_emails

# 解析成邮箱创建
def create_email_cvs(email_password):
    email_and_password = email_password.split('----')

    email_pre=email_and_password[0].split('@')[0]
    email_back=email_and_password[0].split('@')[1]
    password=email_and_password[1]
    
    return email_pre+","+password+","+email_back

# 生成2000个邮箱和密码，并存储到一个文件中
def generate_and_store(email_password_count=10):

    #所有的邮箱
    all_emails=[]
    for i in range(email_password_count):
        # 100个邮箱和账号
        sigle_file_emails=generate_email_password(['bseml08.cn','mycol.vip'])

        single_filename = "dassbuff/data/email/email"+f"_{i + 1}.txt"
        with open(single_filename, 'w') as new_file:
            for single_email in sigle_file_emails:
                new_file.write(single_email + '\n')

        all_emails.extend(sigle_file_emails)

        print(all_emails)

    all_email_file = "dassbuff/data/email/email_all_"+f"_{i + 1}.txt"
    all_email_crv_file = "dassbuff/data/email/email_all_cvs_"+f"_{i + 1}.txt"
    
    with open(all_email_file, 'w') as new_file_all:
        with open(all_email_crv_file, 'w') as crv_file:
            for file_email in all_emails:
                new_file_all.write(file_email + '\n')
                crv_file.write(create_email_cvs(file_email) + '\n')



# 调用主函数
all_emails=generate_and_store(20)


