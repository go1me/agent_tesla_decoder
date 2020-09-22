import re
import pandas as pd
ff = open("mail.txt",'r',encoding="utf-8")
mail_txt = ff.read()
ff.close()
#print(mail_txt)
url_user_password_df = pd.DataFrame(columns=["Target_id","URL","Username","Password","Application"])
target_info_df = pd.DataFrame(columns=["Target_id","Time","User Name","Computer Name","OSFullName","CPU","RAM"])
mail_txt_list = mail_txt.split("--------------->>>")
Target_id =0
for mail_info in mail_txt_list:
    mail_zhengwen = re.findall(r"Time: ([\s\S]*?)$",mail_info)
    if len(mail_zhengwen)>0:
        mail_zhengwen = mail_zhengwen[0].replace('\n','').replace("<h=r>","<hr>").replace("<b=r>","<br>").replace("U=RL","URL").replace("<br=>","<br>").replace("<=br>","<br>").replace("=0D=0A","").replace("=0D=0A=","").replace("<br>=Password:","<br>Password:")
        print(mail_zhengwen)
        mail_time = re.findall(r"^([\s\S]*?)<br>",mail_zhengwen)[0]
        target_info_dict = {"Target_id":Target_id,"Time":pd.to_datetime(mail_time)}
        pc_info = re.findall(r"<br>([\s\S]*?)<br><hr>",mail_zhengwen)[0].split("<br>")
        for pc in pc_info:
            pc_list = pc.replace("=","").split(": ")
            target_info_dict[pc_list[0]]=pc_list[1]

        target_info_df = target_info_df.append(target_info_dict,ignore_index=True)

        user_pass_info_all_list = re.findall(r"<br><hr>([\s\S]*?)$",mail_zhengwen)[0].split("<hr>")
        print(user_pass_info_all_list)
        
        for user_pass_info in user_pass_info_all_list:
            if len(user_pass_info) != 0:
                user_pass_info_dict = {"Target_id":Target_id}
                for info_i in user_pass_info.split("<br>"):
                    if "URL" in info_i:
                        user_pass_info_dict["URL"] = re.findall(r":([\s\S]*?)$",info_i)[0]
                    if "Username" in info_i:
                        user_pass_info_dict["Username"] = re.findall(r":([\s\S]*?)$",info_i)[0]
                    if "Password" in info_i:
                        user_pass_info_dict["Password"] = re.findall(r":([\s\S]*?)$",info_i)[0]
                    if "Application" in info_i:
                        user_pass_info_dict["Application"] = re.findall(r":([\s\S]*?)$",info_i)[0]
                url_user_password_df = url_user_password_df.append(user_pass_info_dict,ignore_index=True)
                
        Target_id +=1
print(target_info_df.head())
print(url_user_password_df.head())
target_info_df.to_excel("target_info_df.xlsx")
url_user_password_df.to_excel("url_user_password_df.xlsx")

