from os.path import join, dirname

# CONSTANTS
SEPERATOR = "#"
_ENCODING = "utf-8"

# GLOBAL
mentee_dict = {}
mentor_dict = {}
email_dict = {}

def make_dict():
    global mentee_dict
    global mentor_dict

    f_name = open(join(dirname(__file__),"name_list.txt"), mode = 'r', encoding = _ENCODING)

    text = f_name.read()
    for line in text.split('\n'):
        if "	" in line:
            name_split = line.split("	") # One tab
            mentee_dict[name_split[0]] = name_split[1].split(SEPERATOR)
            for mentor in name_split[1].split(SEPERATOR):
                if mentor not in mentor_dict:
                    mentor_dict[mentor] = [name_split[0]]
                else:
                    mentor_dict[mentor].append(name_split[0])
        else:
            print("Unexpected Format!")


def make_email_list():
    global email_dict
    f_email= open(join(dirname(__file__),"all_mail.txt"), mode = 'r', encoding = _ENCODING)
    
    text = f_email.read()
    for line in text.split('\n'):
        if SEPERATOR in line:
            email_dict[line.split(SEPERATOR)[2]] = line.split(SEPERATOR)[1]
        else:
            print("Unexpected Format!")

if __name__ == '__main__':
    make_dict()
    make_email_list()
    input()
    f_out = open(join(dirname(__file__),"out.txt"), mode = 'w', encoding = _ENCODING)