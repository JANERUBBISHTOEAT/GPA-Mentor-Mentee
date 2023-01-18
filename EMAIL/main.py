#!/usr/bin/python
# -*- coding: UTF-8 -*-

from numpy import append
from mail import mail, test_mail
from mail import VERSION as mail_VERSION
from os.path import join, dirname
import smtplib

# Constants
VERSION = str(hex(20200514))
_ENCODING = "utf-8"
SENT_MARK = "SENT"

my_sender= 'hello@utscgpa.org'
my_pass  = '********'
SEPERATOR = "#"

# Constants
LOGIN__ERR = "Login Failed"
ALL_GOOD   = "All Good"
QUIT_ERR   = "Quitting Failed"

# Global
cnt = 0
name_List = []
mail_List = []
sent_List = []
mentee_dict = {}
mentor_dict = {}
email_dict = {}
wxid_dict  = {}
server = smtplib.SMTP_SSL("smtp.gmail.com", 465)

def make_dict():
    f_name = open(join(dirname(__file__),"name_list.txt"), mode = 'r', encoding = _ENCODING)

    text = f_name.read()
    for line in text.split('\n'):
        if "	" in line.strip():
            name_split = line.split("	") # One tab
            # mentee_dict[name_split[0].strip()] = name_split[1].split(SEPERATOR)
            mentor_list = []
            for mentor in name_split[1].split(SEPERATOR):
                mentor = mentor.strip()
                mentor_list.append(mentor)
                if mentor not in mentor_dict:
                    mentor_dict[mentor] = [name_split[0]]
                else:
                    mentor_dict[mentor].append(name_split[0])
            mentee_dict[name_split[0].strip()] = mentor_list
        else:
            f_log = open(join(dirname(__file__), ".\\" + "log.txt"), 'a+')
            f_log.write(line + '\n')
            f_log.close()
            print("Unexpected Format!")
    return (mentee_dict, mentor_dict)

def make_email_list():
    f_email= open(join(dirname(__file__),"res.txt"), mode = 'r', encoding = _ENCODING)
    cnt = 0
    text = f_email.read()
    for line in text.split('\n'):
        if SEPERATOR in line:
            email_dict[line.split(SEPERATOR)[2].strip()] = line.split(SEPERATOR)[1].strip()
            sent_List.append(line.split(SEPERATOR)[0])
            mail_List.append(line.split(SEPERATOR)[1])
            name_List.append(line.split(SEPERATOR)[2].rstrip('\n'))
            if (sent_List[cnt]):
                print("|-√- " + mail_List[cnt] + '|' + name_List[cnt])
            else:
                print("|--- " + mail_List[cnt] + '|' + name_List[cnt])
            cnt += 1
        else:
            
            print("Unexpected Format!")
    f_email.close()
    print(str(len(name_List)) + " email read sucesfully.")
    print("-----------------------\n")
    return (cnt, email_dict, sent_List, mail_List, name_List)

def make_wxid_list():
    f_wxid= open(join(dirname(__file__),"all_wxid.txt"), mode = 'r', encoding = _ENCODING)
    
    text = f_wxid.read()
    for line in text.split('\n'):
        if SEPERATOR in line:
            wxid_dict[line.split(SEPERATOR)[2].strip()] = line.split(SEPERATOR)[1].strip()
        else:
            print("Unexpected Format!")
    f_wxid.close()
    print(str(len(wxid_dict)) + " wxid read sucesfully.")
    print("-----------------------\n")
    return wxid_dict

def mass_mail(email_info):
    """
    # Data Info:
    # my_sender= 'hello@utscgpa.org'
    # my_pass  = '********'
    # my_user =email_info[0] # Address of Recipient
    # _Subject=email_info[1]
    # _From=   email_info[2] # Nickname of Sender
    # _To  =   email_info[3] # Nickname of Recipient
    """
    succ_cnt = 0
    fail_cnt = 0
    igno_cnt = 0

    f_log = open(join(dirname(__file__), ".\\" + "log.txt"), 'a+')

    try:
        # server=smtplib.SMTP_SSL("smtp.gmail.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
    except Exception:
        input(LOGIN__ERR)
        return (0, 0, 0)

    for i in range(cnt):
        if sent_List[i] == SENT_MARK:
            print(name_List[i] + " is marked as sent. Ignored.")
            igno_cnt += 1
            continue
        email_info[0] = mail_List[i]
        email_info[3] = name_List[i]
        status = mail(email_info, server, mentee_dict, mentor_dict, wxid_dict)
        print(status)

        if (status == ALL_GOOD):
            fp = open(join(dirname(__file__),"res.txt"), mode = 'w', encoding = _ENCODING) # rerwite res.
            sent_List[i] = SENT_MARK
            i = 0
            for i in range(cnt-1):
                fp.write(sent_List[i] + SEPERATOR + mail_List[i] + SEPERATOR + name_List[i] + '\n')
                # print("Writing information: {}, {}".format(cnt, scanned[i] + '#' + name_List[i]))
            i += 1
            fp.write(sent_List[i] + SEPERATOR + mail_List[i] + SEPERATOR + name_List[i]) # Avoid ending \n
            fp.close()
            succ_cnt += 1
        else:
            print(status + " in: " + mail_List[i] + '|' + name_List[i])
            f_log.write(status + " in: " + mail_List[i] + '|' + name_List[i] + '\n')
            fail_cnt += 1

    f_log.close()
    try:
        server.quit()  # 关闭连接
    except Exception:
        input(QUIT_ERR)
        return (igno_cnt, succ_cnt, fail_cnt)
    return (igno_cnt, succ_cnt, fail_cnt)



if __name__ == "__main__":
    print("Running on ver." + VERSION[2:])

    if mail_VERSION != VERSION:
        print("Version does not match!\nModule \"mail\" is running on ver.{}".format(mail_VERSION[2:]))
        exit ("Version Failure")

    (mentee_dict, mentor_dict) = make_dict()
    (cnt, email_dict, sent_List, mail_List, name_List) = make_email_list()
    wxid_dict = make_wxid_list()

    email_info, tmp_server = test_mail(mentee_dict, mentor_dict, wxid_dict)
    tmp_server.quit()

    manual_check = input("Did the test mail go well? Type your [email] to confirm, and continue to send mass emails.\n").strip()
    if (manual_check != email_info[0] and manual_check != "key"): # Mater key
        print("Check all the info and try again.")
        input()
        exit()

    result = mass_mail(email_info)

    # Activity Monitoring
    email_info[0]  = 'monitor_email@monitor.com'
    email_info[1]  = email_info[1] + \
                    "|Total: " + str(cnt) + \
                    "|Ignored: " + str(result[0]) + \
                    "|Succeeded: " + str(result[1]) + \
                    "|Failed: " + str(result[2]) + "|"
    email_info[3]  = '管理员'
    mail(email_info, server, mentee_dict, mentor_dict, wxid_dict) # No prompt

    # Activity Monitoring Forward
    email_info[0]  = 'hello@utscgpa.org'
    mail(email_info, server, mentee_dict, mentor_dict, wxid_dict) # No prompt

    f_log = open(join(dirname(__file__), ".\\" + "log.txt"), 'a+')
    f_log.write("-----------------------------------\n")
    f_log.write("    Total: {}\n    Ignored:{}\n    Succeeded: {}\n    Failed: {}\n"\
        .format(cnt, result[0], result[1], result[2]))
    f_log.write("-----------------------------------\n")
    f_log.close()

    print("-----------------------------------")
    print("    Total: {}\n    Ignored:{}\n    Succeeded: {}\n    Failed: {}"\
        .format(cnt, result[0], result[1], result[2]))
    input("-----------------------------------")