import core.progress_circle
import core.cli
import configparser
import datetime
import time
import sys
import os


def main(root_pth: str):
    # ===>----------------------
    # READ THE CONFIG
    # ===>----------------------
    assert os.path.exists(os.path.join(root_pth, 'config.ini')), 'The file config.ini does`t exists in the root folder!'
    config = configparser.ConfigParser()
    config.read(os.path.join(root_pth, 'config.ini'))

    cli = core.cli.ConsoleUI(config)
    cli.run()


if __name__ == '__main__':
    main(
        root_pth=os.getcwd()
    )


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



