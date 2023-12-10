import math
import random
gradient = {
    lambda x:    0 < x <= 0.25: '#',
    lambda x: 0.25 < x <= 0.50: 'o',
    lambda x: 0.50 < x <= 2: '.',
}

ratio = 2.3
step  = 0.05
prec  = 5


class CircleProgressBar(object):
    def __init__(self, min_value: int, max_value: int) -> None:
        assert isinstance(min_value, int), 'min_value must be an integer'
        assert isinstance(max_value, int), 'max_value must be an integer'
        assert min_value <= max_value, 'min_value must be less_eq than max_value'

        self.min_value        = min_value
        self.max_value        = max_value
        self.current_progress = min_value

    def get_simple_progress(self) -> float:
        return self.current_progress/self.max_value

    def get_display(self, desc: str, radius=10, thickness=2) -> str:
        # Draw a circle
        circle = [
            [
                ' '
                for _ in range(round(ratio*2*radius)+1)
            ]
            for _ in range(2*radius+1)
        ]

        for t in self.line(self.min_value, self.current_progress, step):
            t = round(2*math.pi*(t-self.min_value)/(self.max_value-self.min_value), prec)

            for dr in range(thickness):
                x = (radius - dr) * math.cos(t)
                y = (radius - dr) * math.sin(t)
                dst = self.euclidean_distance(x, y, round(x), round(y))
                char = '#'
                for key in gradient:
                    if key(dst):
                        char = gradient[key]
                        break
                circle[round(y)+radius][round(ratio*(x+radius))] = char

        # # Put the text inside the circle
        # desc = desc.strip()
        # lines = desc.split('\n')
        # n = len(lines)
        # c = 0
        # for circle_line_ind in range(round(radius-n/2), round(radius + n/2) + n % 2):
        #     line = lines[c].strip()
        #     n_l  = len(line)
        #     w = 0
        #     for i in range(round(ratio*radius)-n_l//2, round(ratio*radius)+n_l//2):
        #         circle[circle_line_ind][i] = line[w]
        #         w += 1
        #     c += 1

        # Put the text inside the circle
        lines: list[str] = desc.split('\n')
        len_lines: int = len(lines)
        for cur_line in range(len_lines):
            line = lines[cur_line].strip()
            len_line = len(line)
            for cur_char in range(len_line):
                circle[
                    radius - len_lines // 2 + cur_line
                    ][
                    round(ratio*radius) - len_line // 2 + cur_char
                    ] = lines[cur_line].strip()[cur_char]
        return '\n'.join(''.join(line) for line in circle)

    @staticmethod
    def euclidean_distance(x: float, y: float, x1: float, y1: float) -> float:
        return math.sqrt((x-x1)**2 + (y-y1)**2)

    def update(self, i=1) -> None:
        self.current_progress = min(self.current_progress+i, self.max_value)

    def reset(self):
        self.current_progress = self.min_value

    def __repr__(self) -> str:
        return f"CircleProgressBar[{self.min_value}|{self.current_progress}|{self.max_value}]:{self.get_simple_progress():.5f}"

    @classmethod
    def line(cls, min_: float, max_: float, step: float):
        assert step != 0, 'step must be non-zero value'
        if step < 0:
            return cls.line(max_, min_, -step)
        while min_ <= max_:
            yield min_
            min_ += step
