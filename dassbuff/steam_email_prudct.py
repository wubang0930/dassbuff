import random
import string
import os

# 随机生成邮箱和密码的函数
def generate_email_password():
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
    password_chars = letters_password + digits_password
    
    email = email_chars + '@bseml08.cn'
    password = password_chars
    
    return f"{email}----{password}"

# 解析成邮箱创建
def create_email_cvs(email_password):
    email_and_password = email_password.split('----')

    email_pre=email_and_password[0].split('@')[0]
    email_back=email_and_password[0].split('@')[1]
    password=email_and_password[1]
    
    return email_pre+","+password+","+email_back

# 生成2000个邮箱和密码，并存储到一个文件中
def generate_and_store(email_password_count=2000, line_count_per_file=100):
    email_create= "dassbuff/data/email/user.csv"
    filename = "dassbuff/data/email/emails_passwords.txt"
    with open(filename, 'w') as file:
        with open(email_create, 'w') as email_create_file:
            for _ in range(email_password_count):
                email_password=generate_email_password() 
                
                file.write(email_password + '\n')
                email_create_file.write(create_email_cvs(email_password=email_password) + '\n')

    
    

    # 拆分文件
    split_files(filename, line_count_per_file)

# 将大文件拆分为小文件
def split_files(filename, line_count_per_file):
    with open(filename, 'r') as file:
        lines = file.readlines()
    
    # 计算文件数量
    file_count = len(lines) // line_count_per_file
    
    # 创建子文件
    for i in range(file_count):
        start = i * line_count_per_file
        end = (i + 1) * line_count_per_file
        new_filename = "dassbuff/data/email/"+f"email_{i + 1}.txt"
        
        with open(new_filename, 'w') as new_file:
            new_file.writelines(lines[start:end])

# 调用主函数
generate_and_store()

