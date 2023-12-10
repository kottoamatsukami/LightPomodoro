import time

import core.progress_circle
import configparser
import os
import datetime


class ConsoleUI(object):
    def __init__(self, config: configparser.ConfigParser) -> None:
        # todo asserts
        self.width       : int = int(config['bounds']['width'])
        self.height      : int = int(config['bounds']['height'])
        self.config      : configparser.ConfigParser = config

    def run(self) -> None:
        # create a console
        self.clear_console()
        console: list[list[str]] = [[' ' for _ in range(self.width)] for _ in range(self.height)]

        # print an assertion
        text: str = """
        Please, resize your pbar to fit rectangle!
        Press <ENTER> to continue
        """
        lines    : list[str] = text.split('\n')
        len_lines: int       = len(lines)
        for cur_line in range(len_lines):
            line = lines[cur_line].strip()
            len_line = len(line)
            for cur_char in range(min(len_line, self.width-2)):
                console[
                    self.height//2 - len_lines//2 + cur_line
                    ][
                    self.width//2 - len_line//2 + cur_char
                ] = lines[cur_line].strip()[cur_char]
        self.draw_bounds(console)
        self.draw_console(console)
        input('>>>')
        # get settings
        settings = {}

        # - work time
        self.clear_console()
        print(settings)
        settings['work time'] = self.get_input(
            predicat    = lambda x: x.isdigit() and int(x) > 0,
            request_msg = 'Specify the work time in minutes: '
        )

        # - simple rest time
        self.clear_console()
        print(settings)
        settings['simple rest time'] = self.get_input(
            predicat=lambda x: x.isdigit() and int(x) > 0,
            request_msg='Specify the simple rest time in minutes: '
        )

        # - long rest time
        self.clear_console()
        print(settings)
        settings['long rest time'] = self.get_input(
            predicat=lambda x: x.isdigit() and int(x) > 0,
            request_msg='Specify the long rest time in minutes: '
        )

        # - title
        self.clear_console()
        print(settings)
        settings['title'] = self.get_input(
            predicat=lambda x: True,
            request_msg='Specify the title of the work: '
        )

        # - cycle
        self.clear_console()
        print(settings)
        settings['cycle'] = self.get_input(
            predicat=lambda x: x.isdigit() and int(x) > 0,
            request_msg='Specify the num of cycles: '
        )

        # - epochs
        self.clear_console()
        print(settings)
        settings['epochs'] = self.get_input(
            predicat=lambda x: x.isdigit() and int(x) > 0,
            request_msg='Specify the number of epochs of the work: '
        )

        # Create a circle pbar
        total_time = 60 * (
                int(settings['cycle'])
                +
                int(settings['simple rest time'])*(int(settings['cycle']) - 1)
                +
                int(settings['long rest time'])
        )

        pbar = core.progress_circle.CircleProgressBar(
            min_value = 0,
            max_value = total_time
        )

        for epoch in range(int(settings['epochs'])):
            pbar.reset()
            for cycle in range(int(settings['cycle'])):
                self.wait_it(pbar,
                             f"""
                                    {settings['title']}
                                    {datetime.datetime.now().date()}
                                    {datetime.datetime.now().time()}
                                    Current Cycle: [{cycle+1}/{settings['cycle']}]
                                    Current Epoch: [{epoch+1}/{settings['epochs']}]
                                    """,
                             60*int(settings['work time']))

                if cycle+1 != int(settings['cycle']):
                    self.wait_it(pbar,
                                 f"""
                                        {settings['title']}
                                        Simple Rest Time!
                                        [chill and relax]
                                        """,
                                 60*int(settings['simple rest time']))

            # Get the long rest
            self.wait_it(pbar,
                     f"""
                            {settings['title']}
                            Long Rest Time!
                            [megachill]
                            """,
                         60 * int(settings['long rest time']))

        print('See you soon!')

    def wait_it(self, pbar, desc, long_time):
        start = time.time()
        while time.time() - start <= long_time:
            wait = time.time()
            self.clear_console()
            print(pbar.get_display(desc, int(self.height // 2 - 2), thickness=5))
            while time.time() - wait < 1:
                pass
            pbar.update()

    @classmethod
    def get_input(cls, predicat, request_msg: str):
        while True:
            a = input(request_msg)
            if predicat(a):
                return a

    @staticmethod
    def clear_console() -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

    def draw_bounds(self, console: list[list[str]]) -> None:
        # - UD ╚ ╔ ╩ ╦ ╠ ═ ╬ ╟ ║ ╣ ╗ ╝
        for i in range(1, self.width - 1):
            console[0][i] = '═'
            console[self.height - 1][i] = '═'
        # - LR
        for i in range(1, self.height - 1):
            console[i][0] = '║'
            console[i][self.width - 1] = '║'
        # Corners
        console[0][0] = '╔'
        console[0][self.width - 1] = '╗'
        console[self.height - 1][self.width - 1] = '╝'
        console[self.height - 1][0] = '╚'

    @staticmethod
    def draw_console(console: list[list[str]]) -> None:
        print('\n'.join(''.join(line) for line in console))

    @staticmethod
    def merge_two_consoles(main_console: list[list[str]], sub_console: list[list[str]]):
        main_height : int = len(main_console)
        main_width  : int = len(main_console[0])

        sub_height  : int = len(sub_console)
        sub_width   : int = len(sub_console[0])

        assert main_height == sub_height and main_width == sub_width, 'Please check the dimensions of the two consoles.'

        for x in range(main_height):
            for y in range(main_width):
                if main_console[x][y] != ' ':
                    main_console[x][y] = sub_console[x][y]
