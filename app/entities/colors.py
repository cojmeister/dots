from typing import Tuple, Union

BaseColorTheme = {'text': (214, 187, 192),
                  'BG': (101, 66, 54),
                  1: (108, 207, 246),
                  2: (214, 255, 121),
                  3: (255, 16, 83),
                  4: (247, 231, 51),
                  5: (71, 0, 99)}

SecondaryColorTheme = {'text': "#84a98c",
                       'BG': "#d6d6d6",
                       1: "#d00000",
                       2: "#ffba08",
                       3: "#3f88c5",
                       4: "#032b43",
                       5: "#136f63"}

colorType = Union[Tuple[int, int, int], str]
