import queue
import pygame as py
import random
from queue import Queue
import time
#Starting pygame module
py.init()
#global variables
WIDTH=650
HEIGHT=750
background_col="grey"
rows=8
columns=8
bombs=8
nr_font=py.font.SysFont('trebuchetms',20)
green=67, 115, 30
nrs_col={1:"black",2:green,3:"blue",4:"purple", 5:"pink", 6:"orange",7:"red",8:"pink"}
covered_col=85, 87, 84
size=WIDTH/rows
flag_color=209, 145, 36
bomb_color=173, 42, 42
window=py.display.set_mode((WIDTH,HEIGHT))
py.display.set_caption("Be the best MINESWEEPER!")
game_running=True
statement_font=py.font.SysFont('trebuchetms',30)
timer_font=py.font.SysFont("trebuchetms",15)
dupa=3


def neighbour_positions(row,column,rows, columns):
    neigh=[]
    if row>0:
        neigh.append((row-1,column))
    if row <rows -1:
        neigh.append((row + 1,column))
    if column >0:
        neigh.append((row,column-1))
    if column <columns -1:
        neigh.append((row,column+1))
    if row > 0 and column >0:
        neigh.append((row-1,column-1))
    if row<rows -1 and column<columns -1:
        neigh.append((row+1,column+1))
    if row >0 and column<columns-1:
        neigh.append((row-1,column+1))
    if row<rows -1 and column >0:
        neigh.append((row+1,column-1))
    return neigh


def mine_grid(rows,columns,bombs,):
    place=[[0 for _ in range (columns)] for _ in range(rows)]
    mines_coordinates=set()
    global dupa

    while len(mines_coordinates)<bombs:
        row=random.randrange(0,rows)
        column=random.randrange(0,columns)
        position=row,column

        if position in mines_coordinates:
            continue

        mines_coordinates.add(position)
        place[row][column]=-1


    for mine in mines_coordinates:
        neigh= neighbour_positions(*mine,rows,columns)
        for ro,co in neigh:
            if place[ro][co]!=-1:
                place[ro][co]+=1
    print(mines_coordinates)
    dupa=mines_coordinates
    print(dupa)


    return place
    return dupa



def preparing_window(window,place,covered_place,actual_time):
    window.fill(background_col)
    timer_text=timer_font.render(f"Time passed:{round(actual_time)}",1,"black")
    window.blit(timer_text,(10,HEIGHT-timer_text.get_height()))

    for i,row in enumerate(place):
        y=size*i
        for j, value in enumerate(row):
            x=size*j
            covered_field=covered_place[i][j]==0
            flag=covered_place[i][j]==-2
            here_is_bomb=value==-1
            if flag:
                py.draw.rect(window, flag_color, (x, y, size, size))
                py.draw.rect(window, "black", (x, y, size, size), 2)
                continue
            if covered_field:
                py.draw.rect(window,covered_col,(x,y,size,size))
                py.draw.rect(window, "black", (x, y, size, size), 2)
                continue
            else:
                py.draw.rect(window,"grey",(x,y,size,size))
                py.draw.rect(window, "black", (x, y, size, size),2)
                if here_is_bomb:
                    py.draw.rect(window, covered_col, (x, y, size, size))
                    py.draw.rect(window, "black", (x, y, size, size), 2)


            if value>0:
                text=nr_font.render(str(value),True,nrs_col[value])
                window.blit(text, (x + (size / 2 - text.get_width() / 2), y + (size / 2 - text.get_height() / 2)))
    py.display.update()

def get_clicked_position(mouse_position):
    mx,my=mouse_position
    row=int(my//size)
    column=int(mx//size)
    return row,column

def uncover_post_click(row,column,place,covered_place):
    q=Queue()
    q.put((row,column))
    clicked=set()
    while not q.empty():
        current=q.get()
        neights=neighbour_positions(*current,rows,columns)
        for r,c in neights:
            if (r,c) in clicked:
                continue

            value=place[r][c]
            covered_place[r][c]=1
            if value==0 and covered_place[row][column]!=-2:
                q.put((r,c))
            if covered_place[r][c]!=-2:
                covered_place[r][c]=1

            clicked.add((r,c))

def player_lose(window,text):
    text=statement_font.render(text,1,bomb_color)
    window.blit(text,(WIDTH/2-text.get_width()/2,HEIGHT/2-text.get_height()/2))
    py.display.update()

def player_win(window, text_win):
    text_win=statement_font.render(text,1,bomb_color)
    window.blit(text,(WIDTH/2-text.get_width()/2,HEIGHT/2-text.get_height()/2))
    py.display.update()


def main_game():
    game_running=True
    place=mine_grid(rows,columns,bombs)
    covered_place=[[0 for _ in range(columns)]for _ in range(rows)]
    clicks=0
    lose=False
    start_timer=0
    win=False
    all_flags=set()

    flags=bombs
    print(place)



    while game_running:
        if start_timer >0:
            actual_time=time.time() - start_timer
        else:
            actual_time=0




        for event in py.event.get():
            if event.type == py.QUIT:
                game_running=False
                break
            if event.type == py.MOUSEBUTTONDOWN:
                mouse_press=py.mouse.get_pressed()
                row, column = get_clicked_position(py.mouse.get_pos())
                if row >= rows or column >= columns:
                    continue
                if mouse_press[0] and covered_place[row][column]!=-2:
                    covered_place[row][column]=1
                    if place[row][column]==-1:
                        py.draw.rect(window, bomb_color, (row, column, size, size))
                        lose=True

                        flags = bombs

                    if clicks==0 or place[row][column]==0:
                        uncover_post_click(row, column, place, covered_place)
                    if clicks==0:
                        start_timer=time.time()
                    clicks+=1
                elif mouse_press[2]:
                    if covered_place[row][column]==-2:
                        covered_place[row][column]=0
                        flag_pos.remove((row,column))
                        flags+=1
                    else:
                        covered_place[row][column]=-2
                        flags -=1

                    if covered_place[row][column]==-2:
                        flags_coordinates=(row,column)
                        print(flags_coordinates)
                        all_flags.add(flags_coordinates)
                        print(all_flags)

                        if dupa.issubset(all_flags):
                            win=True
        if win:
            preparing_window(window, place, covered_place, actual_time)
            player_lose(window, "You win!")

        if lose:
            preparing_window(window, place, covered_place,actual_time)
            player_lose(window, "BUM!!!!!!! ... Opsi, try again ...")
            py.time.delay(3000)
            place = mine_grid(rows, columns, bombs)
            covered_place = [[0 for _ in range(columns)] for _ in range(rows)]
            clicks = 0
            lose=False
        preparing_window(window,place,covered_place,actual_time)

    py.quit()



if __name__ == "__main__":
    main_game()
