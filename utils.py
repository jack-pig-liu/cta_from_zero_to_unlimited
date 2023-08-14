import lineTool
from config import line_token


def line_print(msg):
    print(msg)
    try:
        lineTool.lineNotify(line_token, msg)
    except:
        print('line notify 失效')
