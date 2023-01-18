from email.mime.application import MIMEApplication
import smtplib
from os.path import dirname, join
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
# from email.utils import formataddr
from email.header import Header

# Constants
VERSION = str(hex(20200514))
ATTACH_ERR = "Attachment Failed"
LOGIN__ERR = "Login Failed" # Take place in main
IMAGE__ERR = "Image Failed"
ALL_GOOD   = "All Good"
UNKNOWN_ERR= "Unknown Error"
SEND_ERR   = "Sending Failed"
QUIT_ERR   = "Quitting Failed" # Take place in main
_ENCODING = "utf-8"
SEPERATOR = "#"
MSG_ERR = "Message Error"

# Global
_signature = ""
_position  = ""




def mail(email_info, server, mentee_dict, mentor_dict, wxid_dict):
    my_sender= 'hello@utscgpa.org'
    my_pass  = '********'
    my_user =email_info[0] # Address of Recipient
    _Subject=email_info[1]
    _From=   email_info[2] # Nickname of Sender
    _To  =   email_info[3] # Nickname of Recipient
    # _Attr=   attach_list
    _Image = "logo.png"
    
    
    try:
        if _To in mentee_dict:
            attach_dir_list = mentee_dict[_To]
            mail_msg ="\
亲爱的" + _To + "同学, <br><br>你好，<br>非常感谢你报名本次 Mentor-Mentee Program，欢迎即将来到 UTSC 的你！\
<br><br>根据各项匹配得出的结果，你的 Mentor 数量为" + str(len(mentee_dict[_To])) + "名。<br>\
你的 Mentor 中至少有一位与你会是相同专业。<br>\
以下为你的 Mentor 分配结果：<br><b>"
            for mentor in mentee_dict[_To]:
                mail_msg += mentor.strip() + ": " + wxid_dict[mentor.strip()] + "<br>"
            mail_msg += "</b><br>请你尽快主动添加他/她们为好友。因为有可能存在时差问题，若Mentor未及时通过你的好友申请，请不要太过着急～<br>\
<br>为确保 Mentor-Mentee Program 顺利进行，GPA希望所有 Mentee 可以遵守社交礼仪～礼貌友好地交流哦！<br><br>\
我们也非常欢迎你对 Mentor 的行为进行监督。若发现 Mentor 存在骚扰或商业行为，你有权利联系本次活动负责人 \
XXX（微信号：wxid）进行举报，一经不正当行为被确认后会为你更换 Mentor。<br><br>\
如有其他问题可联系XXX或GPA小助手（微信号：wxid）<br>非常感谢你的耐心等待，祝你们相处愉快！\
<div><br><br>祝好，<br><br>\
<font color='#38761d'><b>" + _signature + "</b></font><br>" + _position + "<br>\
<img src='cid:image1' width='200' height='52' style='border:0px'><br> \
<font color='#38761d'>\
<span style='font-size:8pt;font-family:Arial;\
background-color:transparent;font-weight:700;\
vertical-align:baseline;white-space:pre-wrap'>\
Website: <a href='https://uoftgpa.ca' target='_blank'\
style='font-weight:300;'>uoftgpa.ca</a> | Bilibili: <a \
href='https://space.bilibili.com/403536025' target='_blank'>\
UofTGPA</a></span></font>\
</div>\
"
        elif _To in mentor_dict:
            attach_dir_list = mentor_dict[_To]
            mail_msg ="\
亲爱的" + _To + "同学, <br><br>你好，<br>非常感谢你报名本次 Mentor-Mentee Program，和GPA一起陪伴新入学的同学们成长。<br>\
<br>根据各项匹配得出的结果，你的 Mentee 数量为" + str(len(mentor_dict[_To])) + "名。\
<br>以下为你的 Mentee 分配结果：<br><b>"
            for mentee in mentor_dict[_To]:
                mail_msg += mentee.strip() + ": " + wxid_dict[mentee.strip()] + "<br>"
            mail_msg += "</b>更多Mentee个人信息可在附件中查看。<br>\
<br>他/她们会主动添加你为好友，请你及时通过他/她们的好友申请。但因为有可能存在的时差问题，请不要太过着急～<br><br>\
根据往届活动经验，GPA总结出了以下几点，希望能为你和你的 Mentee 带来更好的活动体验：<br><br>\
1. 初生牛犊实际上还是怕虎的。新入学的 Mentee 们多少会因为刚经历从高中生到大学生身\
份的转换而不适应。尽管有很多疑惑，可能怕你们觉得烦，也不敢自如地提问。此时，\
需要你们展示出自己的耐心与热情，让即将来到异国他乡的他们获得“安全感”。<br><br>\
2. 有部分 Mentee 在备注中提到自己较为内向与慢热，希望学姐学长不要介意。只要他报名了\
这个活动，就证明他有想要主动与人交流的心。此时，需要 Mentor 们主动引导一下气氛，向他们抛出“话引子”。\
GPA为各位 Mentor 整理了一份 <b>Question List</b>，内含新生普遍感兴趣的学习及生活方面的问题，供大家参考<b>（请至附件中查看）</b>。<br><br>\
3. 授之以鱼不如授之以渔。有些思维活跃的同学可能会提出你们不知道答案的问题。相比\
起让 Mentor 成为一个无所不能的哆啦A梦，我们更希望你们能教会他们如何充分利用学校\
官网，Quercus，Acorn等平台，学会自己找寻问题的答案（例如：选课，转专业要求）。<br><br>\
4. 以上皆为GPA的小建议，实际如何与你的 Mentee 相处是大家自由的选择。不论你是想收获一\
个一起吃喝玩乐分享经历的好朋友，还是只想做他/她们初入大学的引路人，我们都向温暖、热情、\
愿意奉献的你们表示诚挚的感谢。<br><br><br>\
如有其他问题可联系本次活动负责人XXX（微信号：wxid）或GPA小助手（微信号：wxid）<br>\
非常感谢你的耐心等待，祝你们相处愉快！\
<div><br><br>祝好，<br><br>\
<font color='#38761d'><b>" + _signature + "</b></font><br>" + _position + "<br>\
<img src='cid:image1' width='200' height='52' style='border:0px'><br> \
<font color='#38761d'>\
<span style='font-size:8pt;font-family:Arial;\
background-color:transparent;font-weight:700;\
vertical-align:baseline;white-space:pre-wrap'>\
Website: <a href='https://uoftgpa.ca' target='_blank'\
style='font-weight:300;'>uoftgpa.ca</a> | Bilibili: <a \
href='https://space.bilibili.com/403536025' target='_blank'>\
UofTGPA</a></span></font>\
</div>\
"
        else:
            print("Exception Occurred: " + _To + " CANNOT be found in either mentor or mentee list.")
            return MSG_ERR

        #创建一个带附件的实例
        msg = MIMEMultipart()
        msg['From'] = Header(_From, 'utf-8')  # 括号里的对应发件人邮箱昵称
        msg['To'] = Header(_To, 'utf-8')              # 括号里的对应收件人邮箱昵称
        msg['Subject'] = Header(_Subject, 'utf-8')            # 邮件的主题，也可以说是标题
        msg.attach(MIMEText(mail_msg, 'html', 'utf-8'))

        if _To in mentor_dict:  
            filename = "question_list.pdf"              
            att0 = MIMEApplication(open(join(dirname(__file__), filename), 'rb').read())
            att0.add_header("Content-Disposition", 'attachment', filename = ('utf-8', '', filename))
            msg.attach(att0)

        # In case of multiple Attachments
        for _Att_Name in attach_dir_list:
            _Att_Name = _Att_Name.strip()
            _File_Type = '.png'
            # 构造附件n，传送当前目录下的 "" 文件
            try:
                filename = _Att_Name + _File_Type
                att1 = MIMEApplication(open(join(dirname(__file__), "res" + "\\" + filename), 'rb').read())
                att1.add_header("Content-Disposition", 'attachment', filename = ('utf-8', '', filename))
                msg.attach(att1)
            except Exception: 
                print(ATTACH_ERR + ": " + _Att_Name + _File_Type)
                return ATTACH_ERR


        # 指定图片为当前目录
        try:
            fp = open(join(dirname(__file__), _Image), 'rb')
            msgImage = MIMEImage(fp.read())
            fp.close()
            # 定义图片 ID，在 HTML 文本中引用
            msgImage.add_header('Content-ID', '<image1>')
            msg.attach(msgImage)
        except Exception:
            print(IMAGE__ERR)
            return IMAGE__ERR

        # Send
        try:
            # server=smtplib.SMTP_SSL("smtp.gmail.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
            # server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码

            pass
            # shut down for test
            # server.sendmail(my_sender,[my_user,],msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件

            # server.quit()  # 关闭连接
        except Exception:
            return SEND_ERR

    except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
        return UNKNOWN_ERR
    return ALL_GOOD

def test_mail(mentee_dict, mentor_dict, wxid_dict):
    global _signature
    global _position

    print ("These information will \
be used for sending formal emails if\
you claim that the test mail is correct.\n\
PLEASE CHECK TWICE\n")

    my_sender= 'hello@utscgpa.org'
    my_pass  = '********'

    try:
        server=smtplib.SMTP_SSL("smtp.gmail.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
    except Exception:
        input(LOGIN__ERR)
        return LOGIN__ERR

    _From = "GPA"
    # _To   = "管理员"
    _To   = "XXX"
    _Subject="Mentor-Mentee 分配结果通知"
    my_user ="monitor_email@monitor.com"
    
    email_info = []
    email_info.append(my_user)
    email_info.append(_Subject)
    email_info.append(_From)
    email_info.append(_To)

    _signature = "XXX | XXX"
    _position  = "HR Director | Marketing Director"
    
    print("\n----------------------------")
    print("Sending mail to: {} [{}]".format(_To, my_user))
    print(mail(email_info, server, mentee_dict, mentor_dict, wxid_dict))
    return email_info, server


if __name__ == "__main__":
    print("Running on ver." + VERSION[2:])
    from main import make_dict, make_email_list, make_wxid_list

    (mentee_dict, mentor_dict) = make_dict()
    (cnt, email_dict, sent_List, mail_List, name_List) = make_email_list()
    wxid_dict = make_wxid_list()

    email_info, server = test_mail(mentee_dict, mentor_dict, wxid_dict)
    server.quit()  # 关闭连接