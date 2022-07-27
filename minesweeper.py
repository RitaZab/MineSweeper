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
rows=15
columns=15
bombs=15
nr_font=py.font.SysFont('trebuchetms',20)
green=67, 115, 30
nrs_col={1:"black",2:green,3:"blue",4:"purple", 5:"pink", 6:"orange",7:"red",8:"pink"}
covered_col=85, 87, 84
size=WIDTH/rows
flag_color=209, 145, 36
bomb_color=173, 42, 42
yes_col=152, 173, 127
no_col=158, 72, 55
window=py.display.set_mode((WIDTH,HEIGHT),py.RESIZABLE)
py.display.set_caption("Be the best MINESWEEPER!")
game_running=True
statement_font=py.font.SysFont('trebuchetms',30)
timer_font=py.font.SysFont("trebuchetms",15)
button_font=py.font.SysFont("trebuchetms",40)
dupa=3
losen=True


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

def player_lose(window,losen):
    global game_running

    game_running=False
    print(losen)
    text1=statement_font.render("You loose :(...",True,bomb_color)
    text2=statement_font.render("You win! :)",True,bomb_color)
    window.blit(text1,(WIDTH/2-text1.get_width()/2,HEIGHT/2-text1.get_height()/2))
    window.blit(text2, (WIDTH / 2 - text2.get_width() / 2, HEIGHT / 2 - text2.get_height() / 2))
    py.draw.rect(window, "grey", (90,90,470,300))
    text_play_again = button_font.render("Do you wanna play again?", True, "black")
    py.draw.rect(window,yes_col,(120,270,180,90))
    py.draw.rect(window,no_col,(350,270,180,90))
    text_yes=button_font.render("Yes :)", True, "black")
    text_no=button_font.render("No :(", True, "black")
    if losen==True:
        window.blit(text1,(WIDTH/2-text1.get_width()/2,150))
    else:
        window.blit(text2, (WIDTH/2-text1.get_width()/2,150))

    window.blit(text_play_again, ((95,200)))
    window.blit(text_yes,((160,340-text_yes.get_width()/2,)))
    window.blit(text_no, ((400, 340 - text_yes.get_width() / 2,)))
    while game_running==False:
        for event in py.event.get():
            if event.type == py.QUIT:
                game_running = False
                break
            if event.type == py.MOUSEBUTTONDOWN:
                menu_mouse_pos = py.mouse.get_pos()

                c, d = menu_mouse_pos
                print(c, d)
                if 120<c< 300 and 270<d<360:
                    print("yes")
                    game_running=True
                    break
                if 350<c<470 and 270<d<360:
                    print("no")

                    py.quit()

        py.display.update()


def play_again():
    global game_running
    text1=statement_font.render("You loose :(...",True,bomb_color)
    text2 = statement_font.render("You win! :)", True, bomb_color)
    window.blit(text,((10,10)))
    py.draw.rect(window, "grey", (90,90,470,300))
    text_play_again = button_font.render("Do you wanna play again?", True, "black")
    py.draw.rect(window,yes_col,(120,270,180,90))
    py.draw.rect(window,no_col,(350,270,180,90))
    text_yes=button_font.render("Yes :)", True, "black")
    text_no=button_font.render("No :(", True, "black")

    window.blit(text_yes,((160,340-text_yes.get_width()/2,)))
    window.blit(text_no, ((400, 340 - text_yes.get_width() / 2,)))
    while lose == True:
        game_running=False
        for event in py.event.get():
            if event.type == py.QUIT:

                break
            if event.type == py.MOUSEBUTTONDOWN:
                menu_mouse_pos = py.mouse.get_pos()

                c, d = menu_mouse_pos
                print(c, d)
                if 120<c< 300 and 270<d<360:
                    print("yes")
                if 350<c<470 and 270<d<270:
                    print("no")
    py.display.update()
def start_menu():
    global rows,columns, bombs
    game_running=False
    while game_running==False:
        window.fill(background_col)
        menu_mouse_pos=py.mouse.get_pos()
        choice_text=statement_font.render("Choose your game difficulty", True, "black")
        window.blit(choice_text,((WIDTH/2-choice_text.get_width()/2),HEIGHT/5))
        beginner_tx=statement_font.render("Beginner",True,"black")
        medium_tx = statement_font.render("Medium", True, "black")
        expert_tx = statement_font.render("Expert", True, "black")
        py.draw.rect(window,(102, 68, 39),(150,230,350,100),border_radius=15)
        py.draw.rect(window, (115, 112, 109), (150, 360, 350, 100),border_radius=15)
        py.draw.rect(window, (179, 123, 27), (150, 490, 350, 100),border_radius=15)
        window.blit(beginner_tx,(int(325-beginner_tx.get_width()/2),int(280-beginner_tx.get_height()/2)))
        window.blit(medium_tx, (int(325 - beginner_tx.get_width() / 2), int(410 - beginner_tx.get_height() / 2)))
        window.blit(expert_tx, (int(325 - beginner_tx.get_width() / 2), int(540 - beginner_tx.get_height() / 2)))
        py.display.update()
        while game_running == False:
            for event in py.event.get():
                if event.type == py.QUIT:
                    game_running=False
                    py.quit()
                if event.type == py.MOUSEBUTTONDOWN:
                    menu_mouse_pos = py.mouse.get_pos()

                    c,d = menu_mouse_pos
                    print(c,d)
                    if 150<c<500 and 230<d<330:
                        print("beginner")
                        rows = 10
                        columns = 10
                        bombs = 10
                        game_running=True
                    if 150 < c < 500 and 360 < d < 460:
                        print("medium")
                        game_running = True
                        rows = 16
                        columns = 16
                        bombs = 40
                    if 150 < c < 500 and 490 < d < 590:
                        print("expert")
                        game_running = True
                        rows = 20
                        columns = 20
                        bombs = 75
        print(rows,columns,bombs)
        return rows,columns,bombs

    py.display.update()


def main_game():
    py.display.update()
    start_menu()
    game_running=True
    place=mine_grid(rows,columns,bombs)
    covered_place=[[0 for _ in range(columns)]for _ in range(rows)]
    clicks=0
    losen=False
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
                        losen=True

                        flags = bombs

                    if clicks==0 or place[row][column]==0:
                        uncover_post_click(row, column, place, covered_place)
                    if clicks==0:
                        start_timer=time.time()
                    clicks+=1
                elif mouse_press[2]:
                    if covered_place[row][column]==-2:
                        covered_place[row][column]=0
                        all_flags.remove((row,column))
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
                            losen=False
                            print(win)
                            print(losen)



        if win:
            losen=False
            preparing_window(window, place, covered_place, actual_time)
            player_lose(window,losen)
            start_menu()
            py.time.delay(1000)
            preparing_window(window, place, covered_place, actual_time)
            place = mine_grid(rows, columns, bombs)
            covered_place = [[0 for _ in range(columns)] for _ in range(rows)]
            clicks = 0
            losen = False
            win=False

        preparing_window(window, place, covered_place, actual_time)


        if losen:

            preparing_window(window, place, covered_place,actual_time)
            player_lose(window,losen)
            start_menu()
            py.time.delay(1000)
            preparing_window(window, place, covered_place, actual_time)
            place = mine_grid(rows, columns, bombs)
            covered_place = [[0 for _ in range(columns)] for _ in range(rows)]
            clicks = 0
            losen=False

        preparing_window(window,place,covered_place,actual_time)





if __name__ == "__main__":
    main_game()
