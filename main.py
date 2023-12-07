import core.progress_circle
import datetime


def main():
    a = core.progress_circle.CircleProgressBar(0, 10)
    desc = f"""
{datetime.datetime.now().date()}
{datetime.datetime.now().time()}
Current Cycle: [10/10]
[]
"""

    print(a.get_display(desc, 12, thickness=5))


if __name__ == '__main__':
    main()



#    print("""
#                             ┓ •  ┓    ┏┓        ┓
#                             ┃ ┓┏┓┣┓╋  ┃┃┏┓┏┳┓┏┓┏┫┏┓┏┓┏┓
#                             ┗┛┗┗┫┛┗┗  ┣┛┗┛┛┗┗┗┛┗┻┗┛┛ ┗┛
#                                 ┛
#                             Work time      :   25 minutes (0 - 90)
#                             Rest time      :   5  minutes (0 - 90)
#                             Long Rest time :   15 minutes (0 - 90)
#                             Period         :   3    times (0 - 5)
#
# """)