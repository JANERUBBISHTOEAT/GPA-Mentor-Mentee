from make_png import paste_all
from os.path import dirname, join
import threading
import xlrd
# u know what's new in gamma

# Constants
QRC_DIREC = ".\\qr\\"
OUT_DIREC = ".\\out\\"
POS_DIREC = "in.png"
FILE_TYPE = ".png"
EXCRECORD = "21.xls"
SEPERATOR = '#'
VERSION   = str(hex(20200409))
_FONT_RETGULAR = ".\\fonts\\" + "Alibaba-PuHuiTi-B.ttf"



# Global Var
email_List = []
name_List = []
nick_List = []
intro_List = []

spec_List = []
dbl_major_List = []
major_List = []
minor_List = []

WeChat_ID = []
sex_List = []

def run_paste(post_path, i):
    out_path = OUT_DIREC + name_List[i].value.strip() + FILE_TYPE
    out_path = join(dirname(__file__), out_path )
    post_path= join(dirname(__file__), post_path)
    font_path= join(dirname(__file__),_FONT_RETGULAR)


    data_List = {}
    data_List['email'] = (email_List[i].value)
    data_List['name'] = ((name_List[i].value).strip())
    data_List['nick'] = (nick_List[i].value)
    data_List['intro'] = (intro_List[i].value.strip('\n').strip())

    # # For 22
    # data_List['spec'] = (spec_List[i])
    # data_List['dblm'] = (dbl_major_List[i])
    # data_List['majr'] = (major_List[i].value)
    # data_List['minr'] = (minor_List[i])

    # For 21 & 20
    data_List['spec'] = (spec_List[i].value)
    data_List['dblm'] = (dbl_major_List[i].value)
    data_List['majr'] = (major_List[i].value)
    data_List['minr'] = (minor_List[i].value)

    data_List['wechat'] = (WeChat_ID[i].value)
    data_List['sex'] = (sex_List[i].value)

    paste_all(post_path, out_path, font_path, data_List)

def open_record():
    global email_List
    global name_List
    global nick_List
    global intro_List

    global spec_List
    global dbl_major_List
    global major_List
    global minor_List

    global WeChat_ID
    global sex_List

    # print(sys.getdefaultencoding())

    print("----------------------------")
    print("Reading record from " + EXCRECORD + ":")
    
    # fp = open(join(dirname(__file__),TXTRECORD), mode = 'r', encoding = "utf-8")
    excel = xlrd.open_workbook(join(dirname(__file__),EXCRECORD), encoding_override="utf-8")
    all_sheet = excel.sheets()
    print(all_sheet)

    sheet_0 =all_sheet[0]
    

    # # # For 20
    # name_List = sheet_0.col(0)
    # email_List = sheet_0.col(4)
    # nick_List = sheet_0.col(1)
    # intro_List = sheet_0.col(10)

    # spec_List = sheet_0.col(9)
    # dbl_major_List = sheet_0.col(6)
    # major_List = sheet_0.col(7)
    # minor_List = sheet_0.col(8)

    # WeChat_ID = sheet_0.col(3)
    # sex_List = sheet_0.col(2)


    # For 21
    name_List = sheet_0.col(0)
    email_List = sheet_0.col(6)
    nick_List = sheet_0.col(1)
    intro_List = sheet_0.col(12)

    spec_List = sheet_0.col(8)
    dbl_major_List = sheet_0.col(9)
    major_List = sheet_0.col(10)
    minor_List = sheet_0.col(11)

    WeChat_ID = sheet_0.col(5)
    sex_List = sheet_0.col(2)


    # # For 22
    # name_List = sheet_0.col(0)
    # email_List = sheet_0.col(4)
    # nick_List = sheet_0.col(1)
    # intro_List = sheet_0.col(6)

    # spec_List = ["(跳过)"]*len(name_List)
    # dbl_major_List = ["(跳过)"]*len(name_List)
    # major_List = sheet_0.col(5)
    # minor_List =["(跳过)"]*len(name_List)

    # WeChat_ID = sheet_0.col(3)
    # sex_List = sheet_0.col(2)



if __name__ == '__main__':
    print("Running on ver." + VERSION[2:])
    open_record()
    post_path = join(dirname(__file__),POS_DIREC)
    Thread_List = []

    # # Make QRcode
    # for i in range(cnt):
    #     t = threading.Thread(target = run_mkqr, args = (i,))
    #     Thread_List.append(t)

    # for t in Thread_List:
    #     # print ("Starting thread" + str(t))
    #     t.start()

    # for t in Thread_List:
    #     t.join()
        
    # Thread_List.clear()

    # Paste QRcode on Post
    cnt = len(name_List)
    for i in range(1, cnt):
        t = threading.Thread(target = run_paste, args = (post_path, i))
        Thread_List.append(t)

    for t in Thread_List:
        t.start()
        # input() # for debug

    for t in Thread_List:
        t.join()