from django.contrib import messages

# Displays error messages in forms
def form_errors(request, errors):
    for msg in errors:
        for message in errors[msg]:
            messages.error(request, f"{message}")


def accounting_num(number):
    if number >= 0:
        str_num = str(number)
        sign = ""
    else:
        str_num = str(number)[1:]
        sign = "-"

    if len(str_num) > 6:
        if len(str_num) > 9:
            acct_num = str_num[:len(str_num)-9] + "," + \
                      str_num[len(str_num)-9:len(str_num)-6] + "," + \
                      str_num[len(str_num)-6:]
            return sign + acct_num
        else:
            acct_num = str_num[:len(str_num)-6] + "," + str_num[len(str_num)-6:]
            return sign + acct_num

    return sign + str_num
