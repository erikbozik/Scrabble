import tkinter as tk
import threading
from PIL import Image, ImageTk
import random
import os

words = set()

class Program:
    canvas = None
    root = None

    def __init__(self):
        # tkinter parameters
        self.size = 1000
        self.root = tk.Tk()
        self.root.geometry(f'{self.size}x{self.size}')
        self.root.iconphoto(False, tk.PhotoImage(file='logo1.png'))
        self.root.title('Scrabble')
        self.root.config(cursor='cross')
        self.root.resizable(False, False)
        self.canvas = tk.Canvas(self.root, height=self.size, width=self.size, bg='black')
        self.canvas.pack()

        self.stop_loading = False
        loading_thread = threading.Thread(target=self.load_words)
        loading_thread.start()
        self.loading_screen()
        loading_thread.join()
        self.object = None
        self.cursor_bind = False
        self.players = []
        self.mm_menu()

    def load_words(self):
        with open('database.txt', 'r', encoding='UTF-8') as file:
            for i in file:
                word = i.strip()
                if len(word) != 1:
                    words.add(i.strip())
            # self.words = set(file.read().split())
            self.stop_loading = True

    def loading_screen(self):
        try:
            a = 0
            self.canvas.create_text((self.size / 2), (self.size * 0.1), text='Hra sa načítava', fill='white',
                                    font=('Helvetica', '20', 'bold'))
            while not self.stop_loading:
                for i in range(8):
                    x, y = (self.size / 2), (self.size / 2)
                    img = ImageTk.PhotoImage(Image.open(f'loading/loading{i}.png'))
                    self.canvas.create_image(x, y, image=img)
                    self.canvas.update()
                    self.canvas.after(50)
                a += 1
        except:
            pass

    def field(self):
        self.field = Field(self.canvas, self.size)
        self.field.grid()
        self.field.header()
        self.bagnon = Bricks(self.canvas, self.size)
        # self.bagnon.draw(int(self.size * (43 / 48)), int(self.size * (1 / 6)))

        # x, y, stepx, stepy = int(self.field.end + (self.size * (1 / 60))), self.field.start_y,\
        #     self.size * (5 / 24), self.field.step * 15
        # self.info_rec = self.canvas.create_rectangle(x, y, self.size * 0.95, y + stepy, fill = '#E3CFAA')

        # self.size * (104 / 120), self.size * 0.6875, self.size * (113 / 120), self.size * (89 / 120)
        self.done_but = self.canvas.create_rectangle(self.size * 0.775, self.size * 0.6875, self.size * 0.85,
                                                     self.size * (89 / 120),
                                                     fill='dark green')
        # self.size * 0.9, self.size * (8575 / 12000)
        self.done_text = self.canvas.create_text(self.size * 0.8125, self.size * (8575 / 12000),
                                                 text='Začať\n  hru',
                                                 font=('Helvetica', f'{int(self.size * 0.01)}', 'bold'),
                                                 fill='white')
        self.canvas.bind('<ButtonPress>', self.click_trigger)
        self.canvas.bind('<Motion>', self.motion_grab)

    def mm_menu(self):
        self.canvas.delete('all')
        self.canvas.update()
        self.canvas.config(bg='#E3CFAA')

        logo = Image.open('menu_logo.png')
        logo = logo.resize((int(self.size * 0.55), int(self.size * 0.35)))
        self.logo = ImageTk.PhotoImage(logo)
        self.canvas.create_image(self.size // 2, self.size // 6, image=self.logo)

        sign = Image.open('sign.jpg')
        sign = sign.resize((int(self.size * 0.32), int(self.size * 0.238)))
        self.sign = ImageTk.PhotoImage(sign)
        self.si_coor = [(self.size / 2, self.size - 3 * (self.size / 5)),
                        (self.size / 2, self.size - 2 * (self.size / 5)), (self.size / 2, self.size - (self.size / 5))]
        r1, r2 = self.sign.width() / 2, self.sign.height() / 2
        self.coors = [
            (self.si_coor[0][0] - r1, self.si_coor[0][0] + r1, self.si_coor[0][1] - r2, self.si_coor[0][1] + r2),
            (self.si_coor[1][0] - r1, self.si_coor[1][0] + r1, self.si_coor[1][1] - r2, self.si_coor[1][1] + r2),
            (self.si_coor[2][0] - r1, self.si_coor[2][0] + r1, self.si_coor[2][1] - r2, self.si_coor[2][1] + r2)]
        self.canvas.create_image(self.si_coor[0], image=self.sign)
        self.canvas.create_text(self.si_coor[0], text='Hra pre\njedného\n hráča', fill='dark green',
                                font=('Helvetica', f'{int(self.size * 0.03)}', 'bold'), anchor='center', tag='A')
        self.canvas.create_image(self.si_coor[1], image=self.sign)
        self.canvas.create_text(self.si_coor[1], text='  Hra pre\nviacerých\n  hráčov', fill='dark green',
                                font=('Helvetica', f'{int(self.size * 0.03)}', 'bold'), anchor='center', tag='B')
        self.canvas.create_image(self.si_coor[2], image=self.sign)
        self.canvas.create_text(self.si_coor[2], text='Koniec', fill='dark green',
                                font=('Helvetica', f'{int(self.size * 0.03)}', 'bold'), anchor='center', tag='C')

        self.canvas.bind('<Motion>', self.mm_color_change)
        self.canvas.bind('<ButtonPress>', self.mm_trigger)

    def menu_reset(self):
        self.canvas.delete('all')
        self.canvas.unbind('<ButtonPress>')
        self.canvas.unbind('<Motion>')
        self.root.config(cursor='cross')

    def mm_color_change(self, event):
        x, y = event.x, event.y
        tags = ['A', 'B', 'C']
        if self.coors[0][0] < x < self.coors[0][1] and self.coors[0][2] < y < self.coors[0][3]:
            self.canvas.itemconfig('A', fill='white')
            tags.remove('A')
            self.root.config(cursor='circle')
        elif self.coors[1][0] < x < self.coors[1][1] and self.coors[1][2] < y < self.coors[1][3]:
            tags.remove('B')
            self.root.config(cursor='circle')
            self.canvas.itemconfig('B', fill='white')
        elif self.coors[2][0] < x < self.coors[2][1] and self.coors[2][2] < y < self.coors[2][3]:
            tags.remove('C')
            self.canvas.itemconfig('C', fill='white')
            self.root.config(cursor='circle')
        else:
            self.root.config(cursor='cross')
        for i in tags:
            self.canvas.itemconfig(i, fill='dark green')

    def mm_trigger(self, event):
        x, y = event.x, event.y
        if self.coors[0][0] < x < self.coors[0][1] and self.coors[0][2] < y < self.coors[0][3]:
            self.single()
        elif self.coors[1][0] < x < self.coors[1][1] and self.coors[1][2] < y < self.coors[1][3]:
            self.multiple()
        elif self.coors[2][0] < x < self.coors[2][1] and self.coors[2][2] < y < self.coors[2][3]:
            self.end()

    def single(self):
        self.menu_reset()
        self.field()
        self.count_players = 1
        # self.game(1)
        # self.main = Player(self.canvas, self.size, 1)
        #
        #
        # self.main.hand = self.bagnon.draw_hand()
        # self.main.draw_hand()

    def multiple(self):
        self.canvas.unbind('<ButtonPress>')
        self.root.config(cursor='cross')

        self.canvas.itemconfig('A', text='Dvaja', fill='dark green')
        self.canvas.itemconfig('B', text='Traja', fill='dark green')
        self.canvas.itemconfig('C', text='Štyria', fill='dark green')

        self.num_players = [False for i in range(3)]
        self.canvas.bind('<ButtonPress>', self.mul_trigger)

    def mul_trigger(self, event):
        x, y = event.x, event.y
        if self.coors[0][0] < x < self.coors[0][1] and self.coors[0][2] < y < self.coors[0][3]:
            self.num_players[0] = True
        elif self.coors[1][0] < x < self.coors[1][1] and self.coors[1][2] < y < self.coors[1][3]:
            self.num_players[1] = True
        elif self.coors[2][0] < x < self.coors[2][1] and self.coors[2][2] < y < self.coors[2][3]:
            self.num_players[2] = True

        if True in self.num_players:
            # self.players = []
            self.field()
            # for i in range(self.num_players.index(True) + 2):
            #     self.players.append(Player(self.canvas, self.size, i + 1))
            #     self.players[-1].hand = self.bagnon.draw_hand()
            self.count_players = self.num_players.index(True) + 2
            # self.game(self.num_players.index(True) + 2)
            self.num_players = [False for i in range(3)]

    def end(self):
        self.stop_loading = False
        self.root.after(2000, self.countdown_end)
        self.end_screen()

    def countdown_end(self):
        self.stop_loading = True
        self.root.destroy()

    def end_screen(self):
        self.menu_reset()
        self.canvas.config(bg='black')
        self.canvas.create_text(self.size // 2, self.size - 3 * (self.size // 4), text='HRA SKONČILA', fill='white',
                                font=('Helvetica', f'{int(self.size * 0.03)}', 'bold'))
        self.canvas.create_text(self.size // 2, self.size - (self.size // 2), text='Okno sa zatvára', fill='white',
                                font=('Helvetica', f'{int(self.size * 0.02)}', 'bold'))
        try:
            a = 0
            while not self.stop_loading:
                for i in range(8):
                    if self.stop_loading:
                        break
                    x, y = self.size / 2, self.size - (self.size / 4)
                    img = ImageTk.PhotoImage(Image.open(f'loading/loading{i}.png'))
                    self.canvas.create_image(x, y, image=img)
                    self.canvas.update()
                    self.canvas.after(50)

                a += 1
        except AttributeError:
            pass

    def motion_grab(self, event):
        x, y = event.x, event.y
        if not self.cursor_bind:
            self.root.config(cursor='cross')
        else:
            self.root.config(cursor='dot')

        if self.object != None:
            # self.root.config(cursor='dot')
            self.object.delete_drawn()
            self.object.draw(x - (self.object.scale / 2), y - 2 * (self.object.scale / 2))
        try:
            coor = self.canvas.bbox(self.check_word)
            if coor[0] < x < coor[2] and coor[1] < y < coor[3]:
                self.canvas.itemconfig(self.check_wtext, fill='black')
            else:
                self.canvas.itemconfig(self.check_wtext, fill='white')
        except AttributeError:
            pass
        coor = self.canvas.bbox(self.done_but)
        if coor[0] < x < coor[2] and coor[1] < y < coor[3]:
            self.canvas.itemconfig(self.done_text, fill='black')
        else:
            self.canvas.itemconfig(self.done_text, fill='white')



    def click_trigger(self, event):
        x, y = event.x, event.y
        if self.canvas.itemcget(self.done_text, 'text') == ' Ukončiť\n kolo':
            self.pos_end = True
            self.gen_summary()
        else:
            self.pos_end = False

        if self.cursor_bind and not self.pos_end:
            for i in self.field.boxes:
                for j in i:
                    cx, cy, step = j.x, j.y, j.scale
                    if self.object != None:
                        if cx < x < cx + step and cy < y < cy + step:
                            if j.who == 'empty':
                                self.object.delete_drawn()
                                j.letter_in(self.object)
                                self.cursor_bind = False
                                self.object = None
                                break

            if self.player.x1 < x < self.player.x2 and self.player.y1 < y < self.player.y2:
                self.object.delete_drawn()
                self.player.in_hand(self.object)
                self.player.draw_hand()
                self.cursor_bind = False
                self.object = None
        else:
            try:
                coor = self.canvas.bbox(self.check_word)
                if not self.pos_end:
                    if coor[0] < x < coor[2] and coor[1] < y < coor[3]:
                        field_check = self.field.checking()
                        if type(field_check) != str:
                            self.player.points += field_check
                            self.player.points_added = True
                            self.canvas.itemconfig(self.done_text, text=' Ukončiť\n kolo')
                            self.canvas.itemconfig(self.info_text,
                                                   text=f'    Získal si {field_check} bodov,\n    môžeš ukončiť kolo')
                            self.strikes = 0
                        else:
                            if field_check == 'not connected':
                                self.canvas.itemconfig(self.info_text, text='Slovíčka si nenadpojil!')
                            elif field_check == 'nonsense':
                                self.canvas.itemconfig(self.info_text, text='Slovíčko nedáva zmysel!')
                            elif field_check == 'no word':
                                self.canvas.itemconfig(self.info_text, text='Nepoložil si žiadne slovo!')
                            elif field_check == 'middle_line':
                                self.canvas.itemconfig(self.info_text, text='Je prvé kolo, slovo musí\nísť do stredu!')
            except AttributeError:
                pass

            coor = self.canvas.bbox(self.done_but)
            if coor[0] < x < coor[2] and coor[1] < y < coor[3]:
                if self.canvas.itemcget(self.done_text, 'text') == 'Začať\n  hru':
                    self.ended_play = False
                    self.canvas.itemconfig(self.done_text, text='  Prehoď\n písmená')
                    self.check_word = self.canvas.create_rectangle(self.size * (104 / 120), self.size * 0.6875,
                                                                   self.size * (113 / 120), self.size * (89 / 120),
                                                                   fill='dark green')
                    # self.size * 0.775, self.size * 0.6875, self.size * 0.85, self.size * (89 / 120)
                    self.check_wtext = self.canvas.create_text(self.size * 0.9, self.size * (8575 / 12000),
                                                               text='  Skontroluj\n       slovo', fill='white',
                                                               font=('Helvetica', f'{int(self.size * 0.01)}', 'bold'))
                    self.summary_coor = self.size * 0.775, self.size * 0.05, self.size * (113 / 120), self.size * (
                            34 / 120)
                    self.summary_text_coor = self.summary_coor[0] + ((self.summary_coor[2] - self.summary_coor[0]) / 2), \
                                             self.summary_coor[1] + ((self.summary_coor[3] - self.summary_coor[1]) / 2)

                    self.summary_rec = self.canvas.create_rectangle(*self.summary_coor, fill='#E3CFAA')
                    self.summary_text = self.canvas.create_text(*self.summary_text_coor, text='',
                                                                font=('Helvetica', f'{int(self.size * 0.01)}', 'bold'))

                    self.infoS_coor = self.size * 0.775, self.size * 0.5625, \
                                      self.size * (113 / 120), self.size * (79 / 120)
                    self.info_table = self.canvas.create_rectangle(*self.infoS_coor, fill='#E3CFAA')

                    self.infoT_coor = self.size * 0.775 + ((self.size * (113 / 120) - self.size * 0.775) / 2), \
                                      self.size * 0.5625 + ((self.size * (79 / 120) - self.size * 0.5625) / 2)
                    self.info_text = self.canvas.create_text(*self.infoT_coor, text='Začni hru !\n        :)',
                                                             font=('Helvetica', f'{int(self.size * 0.01)}', 'bold'),
                                                             fill='black')
                    # self.size * 0.8125, self.size * (8575 / 12000)
                    self.strikes = 0
                    self.game(self.count_players)
                elif self.canvas.itemcget(self.done_text, 'text') == '  Prehoď\n písmená':
                    if self.shuffle():
                        self.canvas.itemconfig(self.done_text, text=' Ukončiť\n kolo')
                else:
                    self.end_round()
                    self.canvas.itemconfig(self.done_text, text='  Prehoď\n písmená')
            elif not self.pos_end:
                try:
                    for j in self.player.hand:
                        cx, cy, step = j.x, j.y, j.scale
                        if cx < x < cx + step and cy < y < cy + step:
                            self.object = j
                            self.player.out_hand(j)
                            self.cursor_bind = True
                            break

                    for i in self.field.boxes:
                        for j in i:
                            cx, cy, step = j.x, j.y, j.scale
                            if cx < x < cx + step and cy < y < cy + step and j.who != 'empty' and j.locked == False:
                                self.object = j.letter
                                j.letter_out()
                                self.cursor_bind = True
                                break
                except AttributeError:
                    pass

    def game(self, player_count=None):

        if self.players == []:
            for i in range(player_count):
                self.players.append(Player(self.canvas, self.size, i + 1))
                self.players[-1].hand = self.bagnon.load_hand()
                self.p_index = 0
        self.gen_summary()

        self.player = self.players[self.p_index]
        self.canvas.itemconfig(self.info_text, text=f'Hráč č.: {str(self.player)} si na rade')
        self.player.draw_hand()

    def end_round(self):
        # ak sa uz neda pokracovat
        if self.strikes == 3:
            self.canvas.unbind('<ButtonPress>')
            self.canvas.unbind('<Motion>')
            self.end_message = 'Prehodili sa písmená\n3-krát.'
            self.end_game()

        if self.bagnon.not_enough():
            self.canvas.unbind('<ButtonPress>')
            self.canvas.unbind('<Motion>')
            self.end_message = 'Minuli sa kocky vo vrecku.'
            self.end_game()

        # resetovanie ruky
        if self.player.points_added:
            hand = self.player.hand[:]
            hand.extend(self.bagnon.load_hand(7 - len(hand)))
            self.player.hand = hand
            self.player.empty_space.clear()
        self.player.points_added = False
        self.player.delete_hand()
        # prehodenie hraca
        if self.p_index == len(self.players) - 1:
            self.p_index = 0
        else:
            self.p_index += 1
        # zamknutie policok
        self.field.lock_grid()
        self.game()

    def shuffle(self):
        if len(self.player.hand) == 7:
            self.player.delete_hand()
            self.bagnon.back_bag(self.player.hand)
            self.player.hand = self.bagnon.load_hand()
            self.player.draw_hand()
            self.canvas.itemconfig(self.info_text, text='Prehodil si písmená,\nmôžeš ukončiť kolo  ')
            self.strikes += 1
            return True
        else:
            self.canvas.itemconfig(self.info_text, text='Uprac písmená do ruky!')
            return False

    # def gen_summary(self):
    #     pass
    #     # output = ''
    #     # for i in self.players:
    #     #     output += f'Hráč č.: {i} má {i.points} bodov\n'
    #     # self.canvas.itemconfig(self.summary_text, text = output)

    def end_game(self):
        self.ended_play = True
        self.endgame = tk.Tk()
        self.endgame.geometry('250x200')
        self.endgame.title('Scrabble')
        # self.endgame.iconphoto(False, self.icon_photo)
        # self.endgame.iconphoto(False, tk.PhotoImage(file = 'logo2.png'))
        self.endgame.config(bg='#E3CFAA')
        self.end_but = tk.Button(self.endgame,
                                 text='Skončiť a pozrieť výpis', command=self.terminate)
        self.end_but.place(x=50, y=100)

        self.end_label = tk.Label(self.endgame, text=self.end_message)
        self.end_label.place(x=50, y=50)
        self.gen_summary()

    def terminate(self):
        os.startfile('vypis.txt')
        self.endgame.destroy()
        self.end()

    def winner(self):
        points = []
        for i in self.players:
            points.append(i.points)
        maximum = max(points)
        winner = []
        for i in self.players:
            if maximum == i.points:
                winner.append(i)

        return winner

    def gen_summary(self):
        output = ''
        for i in self.players:
            output += f'Hráč č.: {i} má {i.points} bodov\n'

        winner = self.winner()
        if len(winner) > 1:
            output += '\nNajvyšší počet bodov\nmajú:\n'
            for i in winner:
                output += f'Hráč č.: {i} ({i.points})\n'
        else:
            output += f'\nNajvyšší počet bodov\nmá:\nHráč č.: {winner[0]} ({winner[0].points})'
        try:
            if self.end_message:
                pass
        except AttributeError:
            if self.strikes != 0:
                output += f'\nPočet prehodení kociek\npo sebe: {self.strikes}'

        if self.ended_play:
            output += f'\nHra sa skončila, pretože:\n{self.end_message}'
            with open('vypis.txt', 'w', encoding='UTF-8') as file:
                file.write(output)
        else:
            self.canvas.itemconfig(self.summary_text, text=output)


class Field:
    word3x = {(0, 0), (0, 7), (0, 14), (7, 0), (7, 14), (14, 0),
              (14, 7), (14, 14)}
    word2x = {(4, 4), (4, 10), (13, 1), (10, 4), (1, 1), (11, 3),
              (13, 13), (10, 10), (1, 13), (3, 3), (2, 12), (12, 2),
              (2, 2), (12, 12), (11, 11), (3, 11)}
    letter3x = {(5, 5), (9, 13), (1, 5), (9, 9), (1, 1), (5, 1),
                (5, 13), (13, 13), (9, 5), (13, 9), (5, 9), (9, 1),
                (13, 5), (1, 9)}
    letter2x = {(0, 3), (0, 11), (2, 6), (2, 8), (3, 0), (3, 7),
                (3, 14), (6, 2), (6, 6), (6, 8), (6, 12), (7, 3),
                (7, 11), (8, 2), (8, 6), (8, 8), (8, 12), (11, 0),
                (11, 7), (11, 14), (12, 6), (12, 8), (14, 3), (14, 11)}

    def __init__(self, canvas, size):
        """Inicializacia hracieho pola"""
        self.boxes = None
        self.canvas = canvas
        self.size = size

        self.board_points = 0

        self.first_move = True

    def grid(self):
        """Vygenerovanie 15x15 prazdnych policok"""
        self.canvas.delete('all')
        self.canvas.config(bg='white')
        self.boxes = []
        self.start_x, self.start_y = int(self.size * 0.05), int(self.size * 0.05)
        self.end = int(self.size * 0.75)
        self.step = (self.end - self.start_x) / 15
        x, y = self.start_x, self.start_y
        for i in range(15):
            local = []
            for j in range(15):
                local.append(Box(self.canvas, self.size, x, y, self.step))
                coor = (i, j)
                # local[j].special(f'{(i, j)}')
                if coor in self.word3x:
                    local[j].special('word3x')
                elif coor in self.word2x:
                    local[j].special('word2x')
                elif coor in self.letter3x:
                    local[j].special('letter3x')
                elif coor in self.letter2x:
                    local[j].special('letter2x')
                elif coor == (7, 7):
                    local[j].special('middle')
                x += self.step
            self.boxes.append(local)
            y += self.step
            x = self.start_x

    def header(self):
        """Vygenerovanie legendy/hlavicky okolo policok"""
        for number, coor in zip(range(65, 80), self.boxes[0]):
            x, y = coor.x + (coor.scale / 2), coor.y - 15
            self.canvas.create_text(x, y, text=chr(number), font='Helvetica')

        for number, coor in zip(range(1, 16), self.boxes):
            x, y = coor[0].x - 15, coor[number - 1].y + (coor[number - 1].scale / 2)
            self.canvas.create_text(x, y, text=f'{number}', font='Helvetica')

    def lock_grid(self):
        # to_lock = []
        # former = []
        for i in self.boxes:
            for j in i:
                if j.letter != None:
                    # to_lock.append(j)
                    # former.append((j.x, j.y))
                    j.locked = True
        # if to_lock != []:
        #     do = True
        # else:
        #     do = False
        # while do:
        #     for box, former_c in zip(to_lock, former):
        #         if former_c[1] + (box.letter.scale / 2) < box.letter.y:
        #             box.letter.delete_drawn()
        #             box.letter.draw(box.letter.x, box.letter.y - 1)
        #
        #         else:
        #             do = False
        #             box.letter.delete_drawn()
        #             box.letter.draw(box.letter.x, former_c[1])
        #
        #         self.canvas.update()
        #         self.canvas.after(20)

    def checking(self):
        word = ''
        points = 0
        board_points = 0
        mul_word = 1
        minimum = False
        one_lock = False
        if self.first_move:
            for order, i in enumerate(self.boxes):
                for j in i:
                    if order != 7 and j.who != 'empty':
                        return 'middle_line'

        for order_r, i in enumerate(self.boxes):
            for order_s, j in enumerate(i):
                num = 0
                if j.who != 'empty':
                    try:
                        if i[order_s + 1].who == 'empty':
                            num += 1
                    except IndexError:
                        num += 1

                    try:
                        if i[order_s - 1].who == 'empty':
                            num += 1
                    except IndexError:
                        num += 1

                    try:
                        if self.boxes[order_r - 1][order_s].who == 'empty':
                            num += 1
                    except IndexError:
                        num += 1

                    try:
                        if self.boxes[order_r + 1][order_s].who == 'empty':
                            num += 1
                    except IndexError:
                        num += 1

                    if num == 4:
                        return 'not connected'


        for i in self.boxes:
            for j in i:
                if j.who != 'empty':
                    word += j.who
                    points += j.value * j.mul_letter
                    if j.locked == True:
                        one_lock = True
                    if j.word != 1:
                        mul_word *= j.word
                elif word != '' and len(word) != 1:
                    if word not in words:
                        # print(f'{word} nedava zmysel')
                        return 'nonsense'
                    else:
                        if one_lock or self.first_move:
                            # print(f'{word} je zmysluplne slovo')
                            minimum = True
                            board_points += points * mul_word
                        else:
                            # print(f'{word} si nenadpojil')
                            return 'not connected'
                    one_lock = False
                    mul_word = 1
                    word = ''
                    points = 0
                else:
                    one_lock = False
                    mul_word = 1
                    word = ''
                    points = 0

        one_lock = False
        for i in range(len(self.boxes)):
            for j in self.boxes:
                if j[i].who != 'empty':
                    word += j[i].who
                    points += j[i].value * j[i].mul_letter
                    if j[i].locked == True:
                        one_lock = True
                    if j[i].word != 1:
                        mul_word *= j[i].word
                elif word != '' and len(word) != 1:
                    if word not in words:
                        # print(f'{word} nedava zmysel')
                        return 'nonsense'
                    else:
                        if one_lock or self.first_move:
                            # print(f'{word} je zmysluplne slovo')
                            minimum = True
                            board_points += points * mul_word
                        else:
                            # print(f'{word} si nenadpojil')
                            return 'not connected'
                    one_lock = False
                    mul_word = 1
                    word = ''
                    points = 0
                else:
                    one_lock = False
                    mul_word = 1
                    word = ''
                    points = 0

        if not minimum or board_points == self.board_points:
            return 'no word'
        player_points = board_points - self.board_points
        self.board_points = board_points
        self.first_move = False
        return player_points


class Box:
    def __init__(self, canvas, w_size, x, y, scale, color='#E3CFAA'):
        self.canvas = canvas
        self.size = w_size
        self.x, self.y, self.scale = x, y, scale
        self.color = color
        self.representation()
        self._who = 'empty'
        self.letter = None
        self.value = 0
        self.word = 1
        self.mul_letter = 1
        self._locked = False

    @property
    def locked(self):
        return self._locked

    @locked.setter
    def locked(self, other):
        self._locked = other

    @property
    def who(self):
        return self._who

    @who.setter
    def who(self, other):
        self._who = other

    def representation(self):
        self.tag = self.canvas.create_rectangle(self.x, self.y, self.x + self.scale, self.y + self.scale,
                                                fill=self.color, outline='black')
        return self.tag

    def letter_in(self, letter):
        letter.draw(self.x, self.y)
        self.letter = letter
        self.who = letter.letter
        self.value = letter.value

    def letter_out(self):
        self.letter = None
        self.who = 'empty'
        self.value = 0

    def special(self, special):
        x, y = self.x + (self.scale / 2), self.y + (self.scale / 2)
        text_size = 1 / 120
        middle = True
        if special == 'word3x':
            color = 'red'
            text = '   3x\nslovo'
            text_size = 0.01
            self.word = 3
        elif special == 'word2x':
            color = 'pink'
            text = '   2x\nslovo'
            text_size = 0.01
            self.word = 2
        elif special == 'letter3x':
            color = 'deep sky blue'
            text = '     3x\npismeno'
            self.mul_letter = 3
        elif special == 'letter2x':
            color = 'light blue'
            text = '     2x\npismeno'
            self.mul_letter = 2
        elif special == 'middle':
            color = 'pink'
            text = 'STRED'
            middle = False
        # else:
        #     self.canvas.create_text(x, y, text=special)
        if self.size < 1200:
            text = text[:text.find('x') + 7]
            if 'slovo' not in text:
                text += '.'

        if middle:
            self.canvas.create_text(x, y, text=text, fill='white', anchor='center',
                                    font=('Helvetica', f'{int(self.size * text_size)}', 'bold'))
        else:
            star = Image.open('middle_star.jpg')
            star = self.del_bg(star)
            star = star.resize((int(self.scale), int(self.scale)))
            self.star = ImageTk.PhotoImage(star)
            self.canvas.create_image(x, y, image=self.star)
        self.canvas.itemconfig(self.tag, fill=color)

    def __repr__(self):
        return self.who

    def del_bg(self, image):
        img = image
        img = img.convert("RGBA")
        datas = img.getdata()
        newData = []
        for item in datas:
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)
        img.putdata(newData)
        return img


class Bricks:
    occurence = dict()
    bag = set()

    def __init__(self, canvas, scale):
        self.canvas = canvas
        self.size = scale
        self.load_occurences()

        for letter, occurence in self.occurence.items():
            for i in range(occurence):
                self.bag.add(Letters(self.canvas, self.size, letter))

    # def remove(self, other):
    #     for order, i in enumerate(self.bag):
    #         if i.letter == other:
    #             del self.bag[order]
    #             break

    def not_enough(self):
        if len(self.bag) < 7:
            return True
        else:
            return False

    def load_hand(self, num=7):
        hand = []
        self.bag = list(self.bag)
        for i in range(num):
            index = random.randint(0, len(self.bag) - 1)
            hand.append(self.bag[index])
            del self.bag[index]
        self.bag = set(self.bag)
        return hand

    def load_occurences(self):
        with open('occurences.txt', 'r', encoding='UTF-8') as file:
            for i in file:
                load = i.split()
                self.occurence[load[0]] = int(load[1])

    def back_bag(self, tiles):
        for i in tiles:
            self.bag.add(i)



class Letters:
    points = None

    def __init__(self, canvas, scale, letter):
        self.canvas = canvas
        self.size = scale
        start_x, start_y = int(scale * 0.05), int(scale * 0.05)
        end = int(scale * 0.75)
        step = (end - start_x) / 15
        self.scale = step
        self.letter = letter
        self._hpos = None
        if self.points == None:
            self.load_points()

        self.value = self.points[self.letter]

    @property
    def hpos(self):
        return self._hpos

    @hpos.setter
    def hpos(self, other):
        self._hpos = other

    def __repr__(self):
        return self.letter

    def load_points(self):
        self.points = dict()
        with open('points.txt', 'r', encoding='UTF-8') as file:
            for i in file:
                load = i.split()
                self.points[load[0]] = int(load[1])

    def draw(self, x, y):
        self.x, self.y = x, y
        self.tag_rec = self.canvas.create_rectangle(x, y, x + self.scale, y + self.scale, fill='dark green')
        self.tag_text = self.canvas.create_text(x + (self.scale / 2), y + (self.scale / 2), fill='white',
                                                text=f'{self.letter.upper()}',
                                                font=('Helvetica', f'{int(self.size * (1 / 48))}', 'bold'))
        self.tag_points = self.canvas.create_text(x + 4 * (self.scale / 5), y + 4 * (self.scale / 5),
                                                  text=f'{self.value}',
                                                  font=('Helvetica', f'{int(self.size * 0.0075)}', 'bold'),
                                                  fill='white')

    def delete_drawn(self):
        self.canvas.delete(self.tag_rec)
        self.canvas.delete(self.tag_text)
        self.canvas.delete(self.tag_points)


class Player:
    def __init__(self, canvas, size, index):
        self.canvas = canvas
        self.size = size

        self.index = index
        self._points = 0

        self._hand = []
        self.empty_space = []
        self._points_added = False

    @property
    def points_added(self):
        return self._points_added

    @points_added.setter
    def points_added(self, other):
        self._points_added = other

    @property
    def hand(self):
        return self._hand

    @hand.setter
    def hand(self, hand):
        self._hand = hand

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, other):
        self._points = other

    def draw_hand(self):
        # nakreslenia noveho
        self.x1, self.y1, self.x2, self.y2 = int(self.size * 0.05), int(self.size * (19 / 24)), int(
            self.size * 0.75), int(self.size * (11 / 12))
        self.hlayout = self.canvas.create_rectangle(self.x1, self.y1, self.x2, self.y2, fill='#E3CFAA')
        x, y = self.x1 + self.size * (1 / 24), self.y1 + self.size * (1 / 60)
        for order, i in enumerate(self.hand):
            if order in self.empty_space and len(self.hand) != 7:
                x += self.size * (1 / 12)
            i.hpos = x, y
            i.draw(*i.hpos)
            scale = i.scale
            x += self.size * (1 / 12)

        self.y2 = self.y1 + self.size * (1 / 30) + scale
        self.x2 = self.x1 + self.size * (1 / 12) + 7 * scale + 6 * (self.size * (1 / 12) - scale)
        self.canvas.coords(self.hlayout, self.x1, self.y1, self.x2, self.y2)

    def delete_hand(self):
        try:
            self.canvas.delete(self.hlayout)
            for i in self.hand:
                i.delete_drawn()
        except:
            pass

    def out_hand(self, tile):
        self.empty_space.append(self._hand.index(tile))
        self._hand.remove(tile)

    def in_hand(self, tile):
        self._hand.insert(self.empty_space[-1], tile)
        self.empty_space.pop()

    def __repr__(self):
        return f'Player: {self.index}'

    def __str__(self):
        return str(self.index)


Program()

tk.mainloop()
