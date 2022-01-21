#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    This is an example of a bot for the 3rd project.
    ...a pretty bad bot to be honest -_-
"""

from logging import DEBUG, debug, getLogger, FileHandler

# We use the logger.debugger to print messages to stderr
# You cannot use print as you usually do, the vm would intercept it
# You can hovever do the following:
#
# import sys
# print("HEHEY", file=sys.stderr)

getLogger().setLevel(DEBUG)

# create logger with 'spam_application'
logger = getLogger('spam_application')
logger.setLevel(DEBUG)
# create file handler which logs even logger.logger.debug messages
fh = FileHandler('spam2.log')
fh.setLevel(DEBUG)
logger.addHandler(fh)


def parse_field_info():
    """
    Parse the info about the field.

    However, the function doesn't do anything with it. Since the height of the field is
    hard-coded later, this bot won't work with maps of different height.

    The input may look like this:

    Plateau 15 17:
    """
    info = input()
    info = [val.strip(':') for val in info.split()]
    height, width = info[1:]
    return int(height), int(width)


def parse_field(size: tuple):
    """
    Parse the field.

    First of all, this function is also responsible for determining the next
    move. Actually, this function should rather only parse the field, and return
    it to another function, where the logic for choosing the move will be.

    Also, the algorithm for choosing the right move is wrong. This function
    finds the first position of _our_ character, and outputs it. However, it
    doesn't guarantee that the figure will be connected to only one cell of our
    territory. It can not be connected at all (for example, when the figure has
    empty cells), or it can be connected with multiple cells of our territory.
    That's definitely what you should address.

    Also, it might be useful to distinguish between lowecase (the most recent piece)
    and uppercase letters to determine where the enemy is moving etc.

    The input may look like this:

        01234567890123456
    000 .................
    001 .................
    002 .................
    003 .................
    004 .................
    005 .................
    006 .................
    007 ..O..............
    008 ..OOO............
    009 .................
    010 .................
    011 .................
    012 ..............X..
    013 .................
    014 .................

    :param player int: Represents whether we're the first or second player
    """
    height, width = size
    caption = input()
    rows = [caption]
    for i in range(height):
        row = input()
        rows.append(row)
    return rows


def parse_figure():
    """
    Parse the figure.

    The function parses the height of the figure (maybe the width would be
    useful as well), and then reads it.
    It would be nice to save it and return for further usage.

    The input may look like this:

    Piece 2 2:
    **
    ..
    """
    info = input()
    height = int(info.split()[1])
    rows = []
    for _ in range(height):
        row = input()
        rows.append(row)
    return rows


def step(player: int):
    """
    Perform one step of the game.

    :param player int: Represents whether we're the first or second player
    """
    size = parse_field_info()
    field = parse_field(size)
    figure = parse_figure()
    # logger.debug(f"Hello {size}, field {field} , figure {figure} ")
    correct_attempts = []
    figure_1 = figure[1]  # index of the figure!!!
    points = filter_extreme_points(field, find_all_player_points(field, player))
    stars = get_figure_points(figure)

    for point in points:
        for star in stars:
            result = is_correct_step_for_figure(field, figure, point, star, player)
            if result is not None:
                correct_attempts.append((point[0] - star[0], point[1] - star[1]))
                print(result)
                print()

    return correct_attempts


def play(player: int):
    """
    Main game loop.

    :param player int: Represents whether we're the first or second player
    """
    while True:
        move = step(player)
        print(*move)


def parse_info_about_player():
    """
    This function parses the info about the player

    It can look like this:

    $$$ exec p2 : [./player1.py]
    """
    info = input()
    player = 1 if "p1 :" in info else 2
    return player


def convert_str_field_into_list(field: str) -> list:
    return [[val for val in row] for row in field.lower().split("\n")]


def find_all_player_points(field: str, player: int) -> list:
    player = "x" if player == 1 else "o"
    field = convert_str_field_into_list(field)
    points = []
    for i in range(len(field)):
        for j in range(len(field[0])):
            if field[i][j] == player:
                points.append((i, j))

    return points


def filter_extreme_points(field: str, points: list) -> list:
    field = convert_str_field_into_list(field)
    available_points = []

    for x, y in points:
        neighbors = []
        for i, j in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
            try:
                if i >= 0 and j >= 0:
                    neighbors.append(field[i][j])
            except IndexError:
                pass

        if neighbors.count(".") > 0:
            available_points.append((x, y))

    return available_points


def get_figure_points(figure: str) -> list:
    figure = convert_str_field_into_list(figure)
    points = []

    for i in range(len(figure)):
        for j in range(len(figure[0])):
            if figure[i][j] == "*":
                points.append((i, j))

    return points


def is_correct_step_for_figure(field: str, figure: str, field_point: tuple, fig_point: tuple, player: int):
    new_field = convert_str_field_into_list(field)
    figure = convert_str_field_into_list(figure)
    player = "x" if player == 1 else "o"

    start_x, start_y = field_point[0] - fig_point[0], field_point[1] - fig_point[1]
    if start_x < 0 or start_y < 0:
        return None

    try:
        for i1, i2 in zip(range(start_x, start_x + len(figure)), range(len(figure))):
            for j1, j2 in zip(range(start_y, start_y + len(figure[0])), range(len(figure[0]))):
                new_field[i1][j1] = figure[i2][j2].replace("*", player)

        new_field = convert_list_field_into_str(new_field)
        opponent = "o" if player == "x" else "x"

        if (field.count(opponent) != new_field.count(opponent) or
                new_field.count(player) != field.count(player) + convert_list_field_into_str(figure).count("*") - 1):
            return None

    except IndexError:
        return None

    return new_field


def convert_list_field_into_str(field: list) -> str:
    return "\n".join(["".join(row) for row in field])


def main():
    player = parse_info_about_player()
    try:
        play(player)
    except EOFError:
        pass


if __name__ == "__main__":
    main()
