
def read_text(text):

    raw_list = list(text)
    new_list = []
    temp_str = ''

    for i in range(0, len(raw_list), 1):
        if ((raw_list[i] == ' ')
            or(raw_list[i] == '.')or(raw_list[i] == ',')
            or(raw_list[i] == '?')or(raw_list[i] == '!')):
            new_list.append(raw_list[i])
        elif (raw_list[i].isdigit()):
            new_list.append(raw_list[i])
        else:
            temp_str = temp_str + raw_list[i]
            if (len(temp_str) == 3):
                new_list.append(temp_str)
                temp_str = ""

    return new_list

