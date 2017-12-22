import os
import sys
import random
import pygame

# reference = http://blog.csdn.net/xiaohui_hubei/article/details/25333775

# import: struct
# on binary file io(high score): https://www.cnblogs.com/qq78292959/archive/2013/04/07/3003607.html

# on random generating: https://www.cnblogs.com/zywscq/p/5469661.html

pygame.init()

window_pos_x = 100
window_pos_y = 50
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (window_pos_x, window_pos_y)

wind_width = 400
wind_height = 440

# TODO
score_bar_height = 40

row_num = 4
col_num = 4
grid_size = wind_width / row_num

bg_color = (0, 0, 0)
line_color = (255, 0, 255)
font = pygame.font.SysFont(None, 48)
game_over_font = pygame.font.SysFont(None, 40)
score_font = pygame.font.SysFont(None, 30)

init_matrix = [[2, 0, 0, 0], [0, 2, 0, 0], [0, 0, 2, 0], [0, 0, 0, 0]]

new_item_list = [2, 4]
weigh_list = [7, 1]
# generate new 2 or 4 blocks randomly in a certain rate

# directions
RIGHT = 1
DOWN = 2
LEFT = 3
UP = 4


def display_matrix(screen, matrix):
    for i in range(0, row_num):
        for j in range(0, col_num):
            if matrix[i][j]:
                elem_str = format(str(matrix[i][j]))
                elem_image = font.render(
                    elem_str,
                    True,
                    (255, 255, 255),
                )
                elem_rect = elem_image.get_rect()
                elem_rect.centery = i * grid_size + grid_size / 2
                elem_rect.centerx = j * grid_size + grid_size / 2
                screen.blit(elem_image, elem_rect)


# rotate matrix(4x4) clock-wisely
def rotate_matrix_clockwise(matrix):
    new_matrix = []
    for i in range(0, row_num):
        new_matrix_row = list(matrix[i])
        new_matrix.append(new_matrix_row)
    # 列表在复制时，必须使用切片等方法才可以实现传值，否则为传引用！参考《Python编程：从入门到实践》4.4.3
    # 对于二维数组，必须逐层操作，否则易引起未定义行为

    for i in range(0, row_num):
        for j in range(0, col_num):
            new_matrix[i][j] = matrix[row_num - 1 - j][i]
    return new_matrix


# rotate matrix(4x4) anti-clock-wisely
def rotate_matrix_anticlockwise(matrix):
    new_matrix = []
    for i in range(0, row_num):
        new_matrix_row = list(matrix[i])
        new_matrix.append(new_matrix_row)
    # 列表在复制时，必须使用切片等方法才可以实现传值，否则为传引用！参考《Python编程：从入门到实践》4.4.3
    # 对于二维数组，必须逐层操作，否则易引起未定义行为

    for i in range(0, row_num):
        for j in range(0, col_num):
            new_matrix[i][j] = matrix[j][col_num - 1 - i]
    return new_matrix


# def row_move_available(row):
#     if row == [0, 0, 0, 0]:
#         return False
#     for i in range(0, col_num - 1):
#         if (row[col_num - 1 - i] == 0 and row[col_num - 1 - i - 1] != 0) or\
#                 (row[col_num - 1 - i] != 0 and row[col_num - 1 - i] == row[col_num - 1 - i - 1]):
#             return True
#     return False


def move_matrix(matrix, direction):
    for i in range(1, direction):
        matrix = rotate_matrix_anticlockwise(matrix)

    # change into move RIGHT
    score = 0
    # score generated from shrinking only

    for i in range(0, row_num):
        # only available when row_num == col_num == 4
        # # more critical move behaviors

        # the 1st time bubbling zeros to the front
        # 花费了很多时间
        for j in range(0, col_num):
            for k in range(col_num - 1, j, -1):
                if matrix[i][k] == 0 and matrix[i][k - 1] != 0:
                    matrix[i][k] = matrix[i][k - 1]
                    matrix[i][k - 1] = 0

        # shrinking
        if matrix[i][0] != 0 and matrix[i][0] == matrix[i][1]:
            matrix[i][1] = matrix[i][0] << 1
            score = matrix[i][1]
            matrix[i][0] = 0
        if matrix[i][2] != 0 and matrix[i][2] == matrix[i][3]:
            matrix[i][3] = matrix[i][2] << 1
            score = matrix[i][3]
            matrix[i][2] = 0
        if matrix[i][1] != 0 and matrix[i][1] == matrix[i][2]:
            matrix[i][2] = matrix[i][1] << 1
            score = matrix[i][2]
            matrix[i][1] = 0

        # the 2nd time bubbling zeros to the front
        for j in range(0, col_num):
            for k in range(col_num - 1, j, -1):
                if matrix[i][k] == 0 and matrix[i][k - 1] != 0:
                    matrix[i][k] = matrix[i][k - 1]
                    matrix[i][k - 1] = 0

        # while row_move_available(matrix[i]):
        #     for j in range(0, col_num - 1):
        #         if matrix[i][col_num - 1 - j] == 0 and matrix[i][col_num - 1 - j - 1] != 0:
        #             # x,0
        #             matrix[i][col_num - 1 - j], matrix[i][col_num - 1 - j - 1] =\
        #                 matrix[i][col_num - 1 - j - 1], matrix[i][col_num - 1 - j]
        #         if matrix[i][col_num - 1 - j] != 0 and matrix[i][col_num - 1 - j] == matrix[i][col_num - 1 - j - 1]:
        #             # x,x
        #             matrix[i][col_num - 1 - j], matrix[i][col_num - 1 - j - 1] =\
        #                 matrix[i][col_num - 1 - j] << 1, 0

    for i in range(1, direction):
        matrix = rotate_matrix_clockwise(matrix)
    return matrix, score


def show_game_over(screen):
    elem_str = "Game Over! press R to restart"
    elem_image = game_over_font.render(
        elem_str,
        True,
        (255, 0, 0),
    )
    elem_rect = elem_image.get_rect()
    elem_rect.centerx = wind_width / 2
    elem_rect.centery = wind_height / 2
    screen.blit(elem_image, elem_rect)


def game_over(matrix):
    for direction in [RIGHT, DOWN, LEFT, UP]:
        new_matrix = []
        for i in range(0, row_num):
            new_matrix_row = list(matrix[i])
            new_matrix.append(new_matrix_row)
            # 列表在复制时，必须使用切片等方法才可以实现传值，否则为传引用！参考《Python编程：从入门到实践》4.4.3
            # 对于二维数组，必须逐层操作，否则易引起未定义行为

        new_matrix, score = move_matrix(new_matrix, direction)
        # 如果把 matrix 作为形参，会出现未知错误

        for i in range(0, row_num):
            for j in range(0, col_num):
                if matrix[i][j] != new_matrix[i][j]:
                    return False
    return True


def show_score(screen, score):
    elem_str = "Score: " + format(str(score))
    elem_image = score_font.render(
        elem_str,
        True,
        (255, 255, 0),
    )
    elem_rect = elem_image.get_rect()
    elem_rect.left = 0
    elem_rect.bottom = wind_height
    screen.blit(elem_image, elem_rect)


def show_high_score(screen, high_score):
    elem_str = "High score: " + format(str(high_score))
    elem_image = score_font.render(
        elem_str,
        True,
        (255, 255, 0),
    )
    elem_rect = elem_image.get_rect()
    elem_rect.right = wind_width
    elem_rect.bottom = wind_height
    screen.blit(elem_image, elem_rect)


def update_screen(screen, matrix, score, high_score):

    screen.fill(bg_color)

    if game_over(matrix):
        show_game_over(screen)

    for i in range(int(grid_size), wind_width, int(grid_size)):
        pygame.draw.line(screen, line_color, (i, 0), (i, wind_height - score_bar_height), 1)
    for j in range(int(grid_size), wind_height, int(grid_size)):
        pygame.draw.line(screen, line_color, (0, j), (wind_width, j), 1)

    display_matrix(screen, matrix)

    show_score(screen, score)
    show_high_score(screen, high_score)

    pygame.display.flip()


# def trial(lst):
#     new_lst = list(lst)
#     # 列表在复制时，必须使用切片等方法才可以实现传值，否则为传引用！参考《Python编程：从入门到实践》4.4.3
#     for i in range(0, 4):
#         new_lst[i] = lst[4 - 1 - i]
#     return new_lst


# test
def print_matrix(matrix):
    print(' ', end='')
    for i in range(0, row_num):
        for j in range(0, col_num):
            print(matrix[i][j], end=' ')
        print('\n', end=' ')
    print('\n')


def generate_new_block(matrix):
    rdm = random.randint(0, sum(weigh_list) - 1)
    # https://www.cnblogs.com/zywscq/p/5469661.html
    index = 0
    for i, val in enumerate(new_item_list):
        rdm -= val
        if rdm < 0:
            index = i
            break
    new_item = new_item_list[index]

    empty_blocks = []
    for i in range(0, row_num):
        for j in range(0, col_num):
            if matrix[i][j] == 0:
                empty_blocks.append([i, j])

    if len(empty_blocks) > 0:
        k = random.randint(0, len(empty_blocks) - 1)
        # randint(a, b): return a <= rand <=b
        i_new = empty_blocks[k][0]
        j_new = empty_blocks[k][1]
        if matrix[i_new][j_new] == 0:
            matrix[i_new][j_new] = new_item

    return matrix


def normal_exit(high_score):
    with open('high_score.data', 'w') as high_score_file:
        high_score_file.write(str(high_score))
    sys.exit()


def run_game():
    pygame.display.set_caption("2048")
    screen = pygame.display.set_mode((wind_width, wind_height))

    matrix = init_matrix[:]

    # test

    # lst = [0, 3, 4, 5]
    # print(trial(lst))

    # print_matrix(matrix)

    # print_matrix(rotate_matrix_clockwise(matrix))
    # print_matrix(rotate_matrix_anticlockwise(matrix))

    # matrix = move_matrix(matrix, DOWN)
    # print_matrix(matrix)
    # for i in range(1, 6):
    #     matrix = move_matrix(matrix, LEFT)
    #     print_matrix(matrix)
    # matrix = move_matrix(matrix, UP)
    # print_matrix(matrix)

    # for i in range(1, 19):
    #     matrix = generate_new_block(matrix)
    #     print_matrix(matrix)

    # /test

    score = 0
    add_score = 0

    with open('high_score.data', 'r') as high_score_file:
        high_score = int(high_score_file.read())

    while True:
        update_screen(screen, matrix, score, high_score)
        if game_over(matrix):
            update_screen(screen, matrix, score, high_score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                normal_exit(high_score)
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_RIGHT:
                    matrix, add_score = move_matrix(matrix, RIGHT)
                elif event.key == pygame.K_LEFT:
                    matrix, add_score = move_matrix(matrix, LEFT)
                elif event.key == pygame.K_UP:
                    matrix, add_score = move_matrix(matrix, UP)
                elif event.key == pygame.K_DOWN:
                    matrix, add_score = move_matrix(matrix, DOWN)

                elif event.key == pygame.K_r:
                    matrix = init_matrix[:]
                    score = 0
                    with open('high_score.data', 'w') as high_score_file:
                        high_score_file.write(str(high_score))
                    break
                elif event.key == pygame.K_q:
                    normal_exit(high_score)

                score += add_score
                if score > high_score:
                    high_score = score
                matrix = generate_new_block(matrix)


run_game()
