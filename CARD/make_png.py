from PIL import Image, ImageDraw, ImageFont 
from os.path import dirname, join


# Constants
POS_DIREC = "in.png"
FILE_TYPE = ".png"
_FONT_RETGULAR = ".\\fonts\\" + "Alibaba-PuHuiTi-B.ttf"
_FONT_BODY = ".\\fonts\\" + "Alibaba-PuHuiTi-Regular.ttf"
safe_margin = 110


def paste_all(post_path, out_path, font_path, data_Dict):
    try:
        print(data_Dict["name"])
        # print("Loading: " + post_path)
        oriImg = Image.open(post_path)

        draw = ImageDraw.Draw(oriImg)
        # print("Loading: " + font_path)
        width, height = oriImg.size

        # # For 22
        # _name = data_Dict["name"]
        # if data_Dict["sex"] == "男":
        #     _name += "学弟"
        # elif data_Dict["sex"] == "女":
        #     _name += "学妹"

        # For 21 & 20
        _name = data_Dict["name"]
        if data_Dict["sex"] == "男":
            _name += "学长"
        elif data_Dict["sex"] == "女":
            _name += "学姐"

    
        _font = ImageFont.truetype(font_path,60)
        w, h = _font.getsize(_name)
        draw.text((270, 85), _name, fill = (107, 142, 65), font=_font)

        # # nick
        # if data_Dict["nick"] != ("(空)"):
        #     _font = ImageFont.truetype(join(dirname(__file__),_FONT_RETGULAR),20)
        #     w, h = _font.getsize(data_Dict["nick"])
        #     draw.text((272, 165), data_Dict["nick"], fill = (0, 0, 0), font=_font)

        # # "Mentor"
        # _font = ImageFont.truetype(font_path,50)
        # w, h = _font.getsize("Mentor")
        # draw.text(((width-w)/2 + 202, 575), "Mentor", fill = (0, 0, 0), font=_font)

        
        # program
        _font = ImageFont.truetype(font_path, 25)
        program = "Program: "
        if data_Dict["spec"] != "(跳过)":
            program += "Specialist " + data_Dict["spec"]
        if data_Dict["dblm"] != "(跳过)":
            program += "Double Major " + data_Dict["dblm"]
        if data_Dict["majr"] != "(跳过)":
            program += "Major " + data_Dict["majr"]
        if data_Dict["minr"] != "(跳过)":
            program += " + Minor " +data_Dict["minr"]
        w, h = _font.getsize(program)
        # auto newline
        if w + 272 > width - safe_margin:
            new_str = ""
            p = 0
            q = 0
            w = 0
            cnt = 0
            while (q < len(program)):
                while (w + 272 <= width - safe_margin and q < len(program)):
                    qq = q
                    while (program[qq:qq+1].isalpha()):
                        qq += 1
                    w, h = _font.getsize(program[p:qq])
                    if w + 272 > width - safe_margin:
                        break
                    else:
                        q = qq + 1
                    w, h = _font.getsize(program[p:q])
                new_str += program[p:q] + '\n'
                cnt += 1
                p = q
                w = 0
            if cnt > 2: # >= 3 
                draw.text((272, 255), new_str.strip('\n'), fill = (0, 0, 0), font=_font)
            elif cnt > 1: # 2
                draw.text((272, 282), new_str.strip('\n'), fill = (0, 0, 0), font=_font)
            else: # 1-2
                draw.text((272, 310), new_str.strip('\n'), fill = (0, 0, 0), font=_font)
        else:
            draw.text((272, 310), program.strip('\n'), fill = (0, 0, 0), font=_font)

        # intro
        _font = ImageFont.truetype(join(dirname(__file__), _FONT_BODY), 25)
        intro = data_Dict["intro"]
        w, h = _font.getsize(intro)
        # auto newline
        if w + 272 > width - safe_margin: # > 1 line
            new_str = ""
            p = 0
            q = 0
            w = 0
            while (q < len(intro)):
                while (w + 272 <= width - safe_margin and q < len(intro)):
                    qq = q
                    while (intro[qq:qq+1].encode('utf-8').isalpha()):
                        qq += 1
                    w, h = _font.getsize(intro[p:qq])
                    if w + 272 > width - safe_margin:
                        break
                    else:
                        q = qq + 1
                    w, h = _font.getsize(intro[p:q])
                new_str += intro[p:q] + '\n'
                p = q
                w = 0
            draw.text((272, 360), new_str.strip('\n'), fill = (0, 0, 0), font=_font)
        else:
            _font = ImageFont.truetype(join(dirname(__file__), _FONT_BODY), 30)
            new_str = ""
            p = 0
            q = 0
            w = 0
            while (q < len(intro)):
                while (w + 272 <= width - safe_margin and q < len(intro)):
                    qq = q
                    while (intro[qq:qq+1].encode('utf-8').isalpha()):
                        qq += 1
                    w, h = _font.getsize(intro[p:qq])
                    if w + 272 > width - safe_margin:
                        break
                    else:
                        q = qq + 1
                    w, h = _font.getsize(intro[p:q])
                new_str += intro[p:q] + '\n'
                p = q
                w = 0
            draw.text((270, 370), new_str.strip('\n'), fill = (0, 0, 0), font=_font)

        # wechat
        _font = ImageFont.truetype(font_path,25)
        w, h = _font.getsize("WeChat ID: " + data_Dict["wechat"])
        draw.text((272, 160), "WeChat ID: " + data_Dict["wechat"], fill = (0, 0, 0), font=_font)

        # oriImg.show()
        oriImg.save(out_path)

    except IOError:
        print("Process failed\n")
        newImg = Image.new('RGBA',(320,240),'blue')
        newImg.save(out_path)


# for single use
if __name__ == '__main__':
    tmp_name = "sample"
    # makea_qr(tmp_code, tmp_name)
    # qr_path  = join(dirname(__file__), QRC_DIREC + tmp_name + FILE_TYPE)
    post_path= join(dirname(__file__), POS_DIREC)
    font_path= join(dirname(__file__),_FONT_RETGULAR)

    tmp_dict = {}
    tmp_dict['email'] = "???"
    tmp_dict['name'] = "sample_name"
    tmp_dict['nick'] = "Nickname"
    tmp_dict['intro'] = "Hi there, this is a sample introduction."
    tmp_dict['spec'] = "(跳过)"
    tmp_dict['dblm'] = "Mathematics | Statistics"
    tmp_dict['majr'] = "(跳过)"
    tmp_dict['minr'] = "(跳过)"

    tmp_dict['wechat'] = "sample_wxid"
    tmp_dict['sex'] = "N/A"

    out_path = join(dirname(__file__) + '\\' + tmp_dict['name'] + FILE_TYPE)
    paste_all(post_path, out_path, font_path, tmp_dict)