from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk
import pygame
import base64
import time
import os
import random
from mutagen.mp3 import MP3

janela = Tk()
janela.title('MP3 Player')

largura = 375
altura = 340

largura_screen = janela.winfo_screenwidth()
altura_screen = janela.winfo_screenheight()
posx = largura_screen/2 - largura/2
posy = altura_screen/2 - altura/2
janela.geometry('%dx%d+%d+%d' % (largura, altura, posx, posy))

janela.resizable(False, False)

pygame.mixer.init()


def add_song():
    song = filedialog.askopenfilename(initialdir='Downloads/', title='Escolha uma música', filetypes=(('mp3 Files', '*.mp3'), ))
    display.insert(END, song)

    #Song Status Bar
    song_wave.config(image=adding_music_img)
    song_status.config(text='Música adicionada')


def add_songs():
    songs = filedialog.askopenfilenames(initialdir='Downloads/', title='Escolha várias músicas', filetypes=(('mp3 Files', '*.mp3'), ))

    for song in songs:
        display.insert(END, song)

    #Song Status Bar
    song_wave.config(image=adding_music_img)
    song_status.config(text='Músicas adicionadas')


def open_directory():
    caminho = filedialog.askdirectory()
    arquivos = []
    os.chdir(caminho)
    for file in os.listdir():
        arquivos.append(caminho + '/' + file)
    for file in arquivos:
        display.insert(END, file)


def play_time():
    if stopped:
        return

    current_time = pygame.mixer.music.get_pos() / 1000
    converted_current_time = time.strftime('%M:%S', time.gmtime(current_time))

    song = display.get(ACTIVE)

    song_mut = MP3(song)

    global song_length
    song_length = song_mut.info.length
    converted_song_length = time.strftime('%M:%S', time.gmtime(song_length))

    current_time += 1

    if int(music_slider.get()) == int(song_length):
        status_bar.config(text=f'{converted_song_length} / {converted_song_length}')

    elif paused:
        pass

    elif int(music_slider.get()) == int(current_time):
        slider_position = int(song_length)
        music_slider.config(to=slider_position, value=current_time)

    else:
        slider_position = int(song_length)
        music_slider.config(to=slider_position, value=int(music_slider.get()))

        converted_current_time = time.strftime('%M:%S', time.gmtime(int(music_slider.get())))

        status_bar.config(text=f'{converted_current_time} / {converted_song_length}')

        next_time = int(music_slider.get()) + 1
        music_slider.config(value=next_time)

    if repeat:
        if int(music_slider.get()) == int(song_length):
            music_slider.config(value=0)
    elif menu_song:
        if int(music_slider.get()) == int(song_length):
            conteudo = display.get(0, END)
            quant = len(conteudo)
            mus = display.curselection()

            if mus[0]+1 == quant:
                pass
            else:
                next_song()
            
            if re_music:
                if mus[0] == quant-1:
                    status_bar.config(text='')
                    music_slider.config(value=0)

                    display.selection_clear(0, END)
                    display.activate(0)
                    display.selection_set(0, last=None)

                    next_one = display.curselection()
                    song = display.get(next_one)
                    pygame.mixer.music.load(song)
                    pygame.mixer.music.play(loops=0)
            
            if rand:
                tocar = random.sample(range(0,quant),1)
                status_bar.config(text='')
                music_slider.config(value=0)

                display.selection_clear(0, END)
                display.activate(tocar)
                display.selection_set(tocar, last=None)

                next_one = display.curselection()
                song = display.get(next_one)
                pygame.mixer.music.load(song)
                pygame.mixer.music.play(loops=0)

    elif menu_exit_song:
        if int(music_slider.get()) == int(song_length):
            janela.quit()
    
    status_bar.after(1000, play_time)


global playing
playing = False 

def play(is_playing):
    global stopped
    stopped = False

    global repeat
    repeat = False

    global playing
    playing = is_playing

    if playing:
        pass
    else:
        song = display.get(ANCHOR)

        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)

        #Song Status Bar
        song_wave.config(image=sound_wave_img)
        song_status.config(text='Reproduzindo')
        
        play_time()

        playing = True


global stopped
stopped = False

def stop():
    status_bar.config(text='')
    music_slider.config(value=0)
    pygame.mixer.music.unload()

    pygame.mixer.music.stop()
    display.selection_clear(ACTIVE)

    pause_button.config(image=pause_bt_img)

    #Song Status Bar
    song_wave.config(image=stopped_img)
    song_status.config(text='Parado')
    
    global stopped
    stopped = True

    global playing
    playing = False


global paused
paused = False

def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        #Unpause
        pygame.mixer.music.unpause()
        pause_button.config(image=pause_bt_img)
        paused = False

        #Song Status Bar
        song_wave.config(image=sound_wave_img)
        song_status.config(text='Reproduzindo')

    else:
        #Pause
        pygame.mixer.music.pause()
        pause_button.config(image=unpause_bt_img)
        paused = True

        #Song Status Bar
        song_wave.config(image=paused_img)
        song_status.config(text='Pausado')
    
 
def next_song():
    status_bar.config(text='')
    music_slider.config(value=0)

    conteudo = display.get(0, END)
    quant = len(conteudo)

    next_one = display.curselection()
    next_one = next_one[0]+1

    if next_one == quant:
        status_bar.config(text='')
        music_slider.config(value=0)

        display.selection_clear(0, END)
        display.activate(0)
        display.selection_set(0, last=None)

        next_one = display.curselection()
        song = display.get(next_one)
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)

    else:
        song = display.get(next_one)
        print(f'Song: {song}')
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        display.selection_clear(0, END)
        display.activate(next_one)
        display.selection_set(next_one, last=None)

    global repeat
    repeat = False

def previous_song():
    status_bar.config(text='')
    music_slider.config(value=0)

    conteudo = display.get(0, END)
    quant = len(conteudo)

    next_one = display.curselection()
    next_one = next_one[0]-1
    
    if next_one == -1:
        status_bar.config(text='')
        music_slider.config(value=0)

        display.selection_clear(0, END)
        display.activate(quant-1)
        display.selection_set(quant-1, last=None)

        next_one = display.curselection()
        song = display.get(next_one)
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
    
    else:
        song = display.get(next_one)
        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=0)
        display.selection_clear(0, END)
        display.activate(next_one)
        display.selection_set(next_one, last=None)

    global repeat
    repeat = False


def remove_song():
    stop()
    display.delete(ANCHOR)
    pygame.mixer.music.stop()

    #Song Status Bar
    song_wave.config(image=deleting_music_img)
    song_status.config(text='Música deletada')

def remove_all_songs():
    stop()
    display.delete(0, END)
    pygame.mixer.music.stop()

    #Song Status Bar
    song_wave.config(image=deleting_music_img)
    song_status.config(text='Músicas deletadas')


def slide(x):
    song = display.get(ACTIVE)

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(music_slider.get()))


def volume(x):
    pygame.mixer.music.set_volume(volume_slider.get())
    current_volume = pygame.mixer.music.get_volume()

    current_volume = current_volume * 100

    if int(current_volume) < 1:
        volume_button.config(image=vol0)
    elif int(current_volume) > 0 and int(current_volume) < 50:
        volume_button.config(image=vol1)
    elif int(current_volume) > 0 and int(current_volume) >= 50:
        volume_button.config(image=vol2)


global muted
muted = False

def mute(is_muted):
    global muted
    muted = is_muted

    if muted:
        pygame.mixer.music.set_volume(volume_slider.get())

        current_volume = pygame.mixer.music.get_volume()

        current_volume = current_volume * 100

        if int(current_volume) < 1:
            volume_button.config(image=vol0)
        elif int(current_volume) > 0 and int(current_volume) < 50:
            volume_button.config(image=vol1)
        elif int(current_volume) > 0 and int(current_volume) >= 50:
            volume_button.config(image=vol2)

        muted = False

    else:
        volume_button.config(image=vol0)
        pygame.mixer.music.set_volume(0)
        muted = True


global repeat
repeat = False

def repeat_1_music(is_repeat):
    global stopped
    stopped = False

    global repeat
    repeat = is_repeat

    if repeat:
        stop()
        repeat = False

    else:
        repeat = True
        song = display.get(ANCHOR)

        pygame.mixer.music.load(song)
        pygame.mixer.music.play(loops=-1)

        #Song Status Bar
        song_wave.config(image=sound_wave_img)
        song_status.config(text='Reproduzindo')

        play_time()


global re_music
re_music = False

def repeat_music(is_repeating):
    global re_music
    re_music = is_repeating

    if re_music:
        stop()
        re_music = False
    else:
        re_music = True
        menu_next_song()


def music_none():
    global menu_song
    menu_song = False

    global menu_exit_song
    menu_exit_song = False


global menu_song
menu_song = False

def menu_next_song():
    global menu_song
    menu_song = True

    global menu_exit_song
    menu_exit_song = False


global menu_exit_song
menu_exit_song = False

def exit_song():
    global menu_exit_song
    menu_exit_song = True

    global menu_song
    menu_song = False


global rand
rand = False

def randon(is_rand):
    global rand
    rand = is_rand

    global menu_song

    if rand:
        menu_song = False
        rand = False
    else:
        rand = True
        menu_song = True


def instrucao():
    top = Toplevel()
    top.title('Instruções')

    tx = Label(top, text='''Atenção
Este programa só abre e reproduz arquivos como formato .mp3
Quaisquer outros formatos não seram abertos, e podem gerar um erro no programa''')
    tx.pack()

    instrucao_frame = Frame(top)
    instrucao_frame.pack()

    bt = Button(top, text='OK, entendi', command=top.destroy)
    bt.pack()

    img_label01 = Label(instrucao_frame, image=add_bt_img, bd=1, relief=GROOVE)
    img_label01.grid(row=0, column=0, padx=5, pady=5)

    text_label01 = Label(instrucao_frame, text='''Aperte este botão para adicionar 1 música por vez
Há uma opção no menu caso queira abrir mais de uma música, ou um diretório''', bd=1, relief=SOLID, width=100, justify = LEFT, anchor=W)
    text_label01.grid(row=0, column=1, padx=5, pady=5, sticky=W)

    img_label02 = Label(instrucao_frame, image=del_bt_img, bd=1, relief=GROOVE)
    img_label02.grid(row=1, column=0, padx=5, pady=5)

    text_label02 = Label(instrucao_frame, text='''Aperte este botão para remover a música selecionada
Há uma opção no menu para caso queira remover todas as músicas''', bd=1, relief=SOLID, width=100, justify = LEFT, anchor=W)
    text_label02.grid(row=1, column=1, padx=5, pady=5, sticky=W)

    img_label03 = Label(instrucao_frame, image=play_bt_img, bd=1, relief=GROOVE)
    img_label03.grid(row=2, column=0, padx=5, pady=5)

    text_label03 = Label(instrucao_frame, text='''Adicionado a música, selecione qual você quer escutar e aperte este botão para começar a tocar
OBS:
Por padrão, quando a música acaba o player não ira fazer nada
Isso pode ser alterado no menu reproduzir, no qual tem as opões: 
• Não fazer nada (padrão)
• Reproduzir a proxima música
• Fechar o programa
Caso selecione algum deles, vai continuar executando a opção até que troque de novo ou feche o programa''', bd=1, relief=SOLID, width=100, justify = LEFT, anchor=W)
    text_label03.grid(row=2, column=1, padx=5, pady=5, sticky=W)

    img_label04 = Label(instrucao_frame, image=pause_bt_img, bd=1, relief=GROOVE)
    img_label04.grid(row=3, column=0, padx=5, pady=5)

    text_label04 = Label(instrucao_frame, text='''Aperte este botão para pausar, e aperte ele de novo para despausar''', bd=1, relief=SOLID, width=100, justify = LEFT, anchor=W)
    text_label04.grid(row=3, column=1, padx=5, pady=5, sticky=W)

    img_label05 = Label(instrucao_frame, image=stop_bt_img, bd=1, relief=GROOVE)
    img_label05.grid(row=4, column=0, padx=5, pady=5)

    text_label05 = Label(instrucao_frame, text='''Aperte este botão para parar a reprodução da música''', bd=1, relief=SOLID, width=100, justify = LEFT, anchor=W)
    text_label05.grid(row=4, column=1, padx=5, pady=5, sticky=W)

    img_label06 = Label(instrucao_frame, image=prox_bt_img, bd=1, relief=GROOVE)
    img_label06.grid(row=5, column=0, padx=5, pady=5)

    text_label06 = Label(instrucao_frame, text='''Aperte este botão para tocar a proxima música''', bd=1, relief=SOLID, width=100, justify = LEFT, anchor=W)
    text_label06.grid(row=5, column=1, padx=5, pady=5, sticky=W)

    img_label07 = Label(instrucao_frame, image=ante_bt_img, bd=1, relief=GROOVE)
    img_label07.grid(row=6, column=0, padx=5, pady=5)

    text_label07 = Label(instrucao_frame, text='''Aperte este botão para tocar a música anterior''', bd=1, relief=SOLID, width=100, justify = LEFT, anchor=W)
    text_label07.grid(row=6, column=1, padx=5, pady=5, sticky=W)

    img_label08 = Label(instrucao_frame, image=rep_bt_img, bd=1, relief=GROOVE)
    img_label08.grid(row=7, column=0, padx=5, pady=5)

    text_label08 = Label(instrucao_frame, text='''Depois que apertar o botão Play, aperte este botão para tocar a lista de músicas infinitamente
Aperte de novo para parar a reprodução, assim podendo escolher outra música para tocar
Essa opção é uma alternativa pra quem quer criar uma lista de reprodução que fique tocando infinitamente
Lembre-se, crie a lista adicionando as músicas com a ordem que vc queira que sejam reproduzida
Depois de adicionar todas as músicas desejadas, selecione uma música, aperte Play, depois aperte o botão Repeat e aproveite''', bd=1, relief=SOLID, width=100, justify = LEFT, anchor=W)
    text_label08.grid(row=7, column=1, padx=5, pady=5, sticky=W)

    img_label09 = Label(instrucao_frame, image=rep1_bt_img, bd=1, relief=GROOVE)
    img_label09.grid(row=8, column=0, padx=5, pady=5)

    text_label09 = Label(instrucao_frame, text='''Aperte o este botão para tocar uma única música infinitamente
Aperte de novo para parar a reprodução, assim podendo escolher outra música para tocar''', bd=1, relief=SOLID, width=100, justify = LEFT, anchor=W)
    text_label09.grid(row=8, column=1, padx=5, pady=5, sticky=W)

    img_label010 = Label(instrucao_frame, image=rand_bt_img, bd=1, relief=GROOVE)
    img_label010.grid(row=9, column=0, padx=5, pady=5)

    text_label10 = Label(instrucao_frame, text='''Aperte este botão para tocar as músicas aleatoriamente
OBS:
Ele costuma repetir a mesma música se for uma lista pequena, então tente usá-lo depois de adicionar no minino 10 músicas''', bd=1, relief=SOLID, width=100, justify = LEFT, anchor=W)
    text_label10.grid(row=9, column=1, padx=5, pady=5, sticky=W)


#Display music
display = Listbox(janela, bg='black', fg='green', width=62, height=12, selectbackground='green', selectforeground='black')
display.pack()

#Music Slider
music_slider = ttk.Scale(janela, from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=350)
music_slider.pack(pady=5)


#Adicionando imagens codificadas em base64 para que possa rodar em um executável 

pause_img = 'iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH5QEGFw4YBtBW0AAAA6FJREFUSMe1l89rG0cUxz9vZlcmhERqm+K6RmAWcoqb4lt7CP4hCRdCmoN9qntt01vvuZQU2v4FPaQ+Oyf3UEIoRpYS95KbSW2fAlZMQzAJJMgNJkTamdeDVvIPyZacyl8Y2Nl9bz4z82Zm30g+PyH0qEwmzeLiH9rp2+zsdalWd3ptiqCbgYhQLN5XgCgasWEYZpxz7wNnE5Nda+2r1dW/q5XKlgMoFCZFVY9v96gRe+8plVZURLDWDnnvp1S1AFwGBoEziekb4DmwJiJFa005jt22qpLLjYsx5mQjLpf/0oGBVEZE5pxz3wCjgO1g+h7wMTCmql/HsdsQkfmBgdRCrVavHjUwG0UjBz5YaygW76sx5lIcu1+B74EhoHPXD8oAHwFfOOdHjTHrm5tPXly8GLVNfVtjS0tlFZHPvPd3gGs9Ajt14Jr3/o4x8vnSUlk7GbRiurz8QI0xl1T1dhLL/6tPvNfbxpjR5eUH6r1vB5dKK5pKhRnv/S99gu6D+59TqTBTKq20Rm6gsWVEhHo9ngOu9hHa1NV6PZ5rcgBorjpr7RDwCNAuxSXlqPpR5VEQ2KEmc3+Mp2hsmeP0VkRuici3wDawLSI3ROQW8LaL76hzfqo11ZlMmigascnhYLs4O6AYhsHvwGvgdRgGi0Ax+XacrKoWomjEptPnG2/CMPwAWO1hunZF5EoQBBeAx8DjIAguiMgVYLcH/9WE1Vhcydk7+K4r5wQaTFit7XSWvbP3NHUmYb3TqdQXNcG7NP4yp603CasBtta+ovFrO209T1iY2dnrks0OV4G1Hp1jYyQmWanJc9yj71o2O1ydmflSTLW6Q6Wy5USkp70IFOr1eBY4B5yr1+MZoKczQESKlcqW29n5dy8RSDKHDeDTY5wHVPWH5NkAqOpv++vHaCNh7BkXCpMSx25bROYB36UBcwhyuN5JXkTm49htFwqTsr/XqCphGCwA93qM10l0LwyDhSbnwPTkcuNSq9WrxpibwHofoWvGmJu1Wr2ay4230qwW2BhDPj8h3vsNY+RGn+Brxsh33vuNfH7iQMbZFpvp6SnxXh8aY74C7tI95p3kgbvGmDnv9eH0dK4t02zLMlWVKBqRzc0nL1Kp8E/v9RkwDHxI90XkgHUR+SmVCn+MY/dPPj/RMbnvKaEPAjvkXH8Teul2dzp8hXn69FnHK0w2O3yiK0zXu5OqtvKydPq8r1S2XgIvD8/O2NhlaYatGxTgP2MBt+f97vb3AAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDIxLTAxLTA2VDIzOjE0OjI0KzAwOjAwvWwfOQAAACV0RVh0ZGF0ZTptb2RpZnkAMjAyMS0wMS0wNlQyMzoxNDoyNCswMDowMMwxp4UAAAAASUVORK5CYII='

unpause_img = 'iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH5QEGFw4ZcddmRgAABC5JREFUSMe9l89rXFUUxz/n3vcm1GBm/EVNQyQMdGXako3oQpJmZohQatWmIMaNaIk7wWVxo+KPf0ChBATRdmGLIqVImEzauCm6SGvaTQuZhpa2tNAyCcRi5t17XMybSZp5k2Rq8MCDx73nnu8959zzvedKPj8kbFEymTSnT/+qSXOjo4ekUlncqimCzRREhGLxnAJks302DMOMc+5poDNWWbbWPpid/atSLi84gEJhv6jqxnZbeey9p1SaURHBWtvtvR9W1QKwF9gJ7IhVHwJ3gTkRKVprpqPI3VFVcrlBMca05/H09O/a0ZHKiMiYc+4o0A/YBNWngF3AgKq+G0XuiohMdHSkTqysVCutHLPZbN8jE9YaisVzaox5MYrcN8BHQDeQvPVHxQDPA6855/uNMZfn56/f27072xT6JmOTk9MqIi97708CB7cImLSBg977k8bIK5OT05qk0Mjp1NR5Nca8qKrH41z+V9njvR43xvRPTZ1X730zcKk0o6lUmPHef7VNoGvA/ZepVJgplWYanhuolYyIUK1GY8CBbQSty4FqNRqr4wBQP3XW2m7gEqBtfi7+FPDxv0/QuxQEtruOuTbHw9RKZr0oMAlcTZi7LSLjIvIpEAF/iMjbwI8Juv3O+eFGqDOZNNlsn43JIalORUROGWMOAt8By2vmlsIwOA0UYy9vqOopEZlNsGNVtZDN9tl0uqs2EobhM8Bsq3CKyAcAXV1PpkTkLeDPeO5qEATPisirwD/AT/FOP25hazbGqh2umHt3bnZCxsffq6rqz9baN0Tka2pUueVLBtgZYzXKqZNV7m0pFy/OkcsNinPudjbb94kx5mhn5xOLbYDviLEei5UACAJbD99jSR14mdots6Hs27eHUmlGg8DuunZt/nPv/cTy8t/pNjbwMMaqAVtrH1DL14YyMfF9KCJvRpH7RVWPUbsQ2vH6boyFGR09JL29PRVgboMFaozZvbS09K2q/gC8FI97YySiVsOs2YRvYWeut7encvjw62IqlUXK5QUnIkVqrNMEqqpHvPdngPdZ7TwAuqrV6DBQiKP3gogcUdWBBDtORIrl8oJbXFxapcyYzi7xf1JmobBfosjdEZGJDcLUSgyrh1Ti//Xl5UVkIorcnUJhv9QXoaqoKmEYnADOtgm8FTkbhsGJOk4DGCCXG5SVlWrFGHMMuLyNoHPGmGMrK9VKLjfYiEQD2BhDPj8k3vsrxsj4NoHPGSMfeu+v5PNDj3ScTcw1MjIs3usFY8w7wBnazznxmjPGmDHv9cLISK6JUpu6TFUlm+2T+fnr91Kp8Dfv9RbQAzzH5hTrgMsi8kUqFX4WRe5GPj+U2NxvqaEPAtvt3PY29LLZ22n9E+bmzVuJT5je3p62njCbvp1UtUEy6XSXL5cX7gP310dnYGCv1NO2GSjAv4O3/3gBFuG+AAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDIxLTAxLTA2VDIzOjE0OjI1KzAwOjAwGxsUjQAAACV0RVh0ZGF0ZTptb2RpZnkAMjAyMS0wMS0wNlQyMzoxNDoyNSswMDowMGpGrDEAAAAASUVORK5CYII='

play_img = 'iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH5QEGFw4YBtBW0AAAA5RJREFUSMfFl01oG1cQgL+Zp5UcApbSUlrXCIzAUIgb8Kntpf6RFBdCakp8inot/bmUXnMstD0WCj0En51TDg1pKMaWEveSm0ltH0rBTmhwjQMJKjSkkXbf9KCVGluKJbkKHdjL7sz7dmbemzcjhcK00KNkMmmuXr1mnb4tLMxLtfpnr0uR6KYgIqys3DSAXG7MBUGQiaLoJeBkrPLYOfdoff2X6s7OvQigWJwRMzt63ed57L2nXF4zEcE5N+K9nzWzInAGeBU4Eas+AfaBDRFZcU4rYRjtmRn5/JSoan8eVyo/WyqVzIhIKYqij4AJwHVQPQW8Dkya2YdhGG2JyGIqlVyq1erV5znmcrmxAx+cU1ZWbpqqng7D6Hvgc2AE6PzrB0WB14D3oshPqOrm9vbdB+PjubbQty22vFwxEXnbe38FON8jsNMPnPfeX1GVd5aXK9ZJoZXT1dVbpqqnzexynMv/Km96b5dVdWJ19ZZ579vB5fKaJZNBxnv/zYCgz8D918lkkCmX11qeKzSOjIhQr4cl4NwAoU05V6+HpSYHgOauc86NAHcAe0HPnUTCjTSZz+Z4lsaROUr+Bq4Be8fweiKK/Gwr1JlMmlxuzMXFwXUxjkTkW1X5APgRCPsAOzMr5nJjLp0ebrwJguBlYL2HcD0WkXcBUqnksIh8CvzWR7jXY1bstuo4sNsPuFkQVPUNYBH4qwf73ZjVOk4n+bf29iTF4oycPTsr3vtfT53KfCYiF4GtLmYnYtaxqtLg5P8IdQLAOffIe79P45bpSYaGUsMiUvLefwGM92i2H7PQhYV5yWZHq8BGD4YGiKq89fRpbcnMvusDCrCRzY5WL1x4X1qVS0RKNM7lUaF6AvwA/NFDWA8/Ycw4WLmc0wrdd+UQME/jfu5XtmIGEO/qYnFGwjDaE5FFwB9j0W7iRWQxDKO9YnFGWmAzw8wIgsQScOMFgG8EQWKpyWmBAfL5KanV6lVVvQRsDhC6oaqXarV6NZ+farVZLbCqUihMi/d+S1U+HhB8Q1U+8d5vFQrTBzrOtso1Nzcr3tttVb0IXOd4OffAdVUteW+35+bybZ1mW5dpZuRyY7K9ffdBMhn85L3tAqPAK3QvsRGwKSJfJZPBl2EY/V4oTHds7ntq6BMJNxJFg23opdvsdHiEuX9/t+MIk82O9jXCdJ2dzKxV3dLpYb+zc+8h8PBwdCYnz0gzbd2gAP8ASfHhISItikwAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjEtMDEtMDZUMjM6MTQ6MjQrMDA6MDC9bB85AAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIxLTAxLTA2VDIzOjE0OjI0KzAwOjAwzDGnhQAAAABJRU5ErkJggg=='

stop_img = 'iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH5QEGFw4bn9kHagAAA4tJREFUSMe1l09oW0cQh7/Z1ZMJgUgtFNcNAfEgp7guvrUQ8B9JuBDSHuJTnWtpL2nvORba3gM9BF9ycejBlxBCMZIcuwRyC6ntq19EjTEJOCiHEJDe7vSgJyW2niQnlX+wpzdvvt2dndlZKZVmhRMqn8+xunpP074tLn4rjcark7oiM8xARKhUHipAGBZsEAR559zHwNnE5LW19uWTJ/80oqjuAMrlOVHVwX77rdh7T622qSKCtXbCez+vqmVgChgHziSmb4DnwJaIVKw163HsDlSVYnFGjDHvt+L19b91bCybF5El59z3wCRgU0w/Aj4DplX1ehy7HRFZHhvLrjSbrUa/hdkwLBz5YK2hUnmoxphLcez+AH4GJoD0qR+VAT4FvnbOTxpjtnd3n724eDHs2foeZ2tr6yoiX3rv7wJXTwhMm8BV7/1dY+SrtbV1TTPoxrRa3VBjzCVVvZ3E8v/qc+/1tjFmslrdUO99L7hW29RsNsh7738fEfQduP8tmw3ytdpmd+UG2ikjIrRa8RJwZYTQjq60WvFShwNA59RZayeAp4D2GR5wQ4Yf8P/TTMZOdJjddPLez9NOmTSpiNwCHpGeUiTgy6r6E5CWQpPO+XlgBSCTz+cIw4KNonp5gFMFHqnq6qD9TLbxRh+wVdVyGBb+zOXO+czq6j0NgiDP8ANl3w3NcVWrGzpg4h1N7e3t56OofmgAkto7zulrPGF10+ksb2vvaepMwvqgqjQSdcCvad8yp603CasNtta+pH21nbaeJ6x25xCGBQvcoX/yOxFZHOY1sXED/NwJw4K9du0byTQar4iiuhORiqpeJz0lBLic5OnAAkJ6DpNMvhJFdReGhbeVK+kcdoAv0sBJRboxbNEDwDsJA0hiXC7PSRy7AxFZpl1v+zk1Q0Y/qBeR5Th2B+XynHTBqoqqEgSZFeDBsFh+gB4EQWalw+mCAYrFGWk2Ww1jzE1ge4TQLWPMzWaz1SgWZ7o70gUbYyiVZsV7v2OM/DAi+JYx8qP3fqdUmj3ScfZUroWFefFeHxtjvgPu0z/mg+SB+8aYJe/18cJCsSf2PV2mqhKGBdndffYimw3+8l73gfPAJwwvsQ7YFpFfs9nglzh2/5ZKs6nN/Yka+kzGTjg32oZehr2djj9h9vb2U58wFy6cf68nzNC3k6p2L/9c7pyPovohcHh8d6anp6QTtmFQgP8A1BGvZcobHKoAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjEtMDEtMDZUMjM6MTQ6MjcrMDA6MDCMhAWkAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIxLTAxLTA2VDIzOjE0OjI3KzAwOjAw/dm9GAAAAABJRU5ErkJggg=='

next_img = 'iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH5QEGFw4bn9kHagAAA+tJREFUSMe1l89rXHUQwD8z3327lNJktaiJtbA8CGIbC71ZL0mzGyKUWLE5SNceioriQS/FQy+KoP4FCqUUemkvFrSWoiHZtPESQQkxzUEPSas1VIuV2B8Iu+99x8O+XZvsbndbtwPv8OYN38935jvfeTNSKAwLHUo228uZM2et2beJif2ytvZ3p0uRamcgIkxNXTCAMMy5IAiycRw/CmxOTO445/6an/9xbWXlSgwwOrpXzOze67by2HtPqTRrIoJzrt97P2Jmo8Au4AlgU2L6D/AHsCgiU87pTBTF18yMfH5IVPX+PJ6Z+dYymXRWRIpxHL8BDAKuiekjwJPAbjN7NYriJRE5nsmkT5XLlbVWjrkwzK374JwyNXXBVHVnFMWfAu8C/UDzra8XBfqAF+LYD6rqpeXly9cHBsKG0DcsNjk5YyLynPf+NDDeIbDZBsa996dVZc/k5Iw1M6if6fT0RVPVnWZ2LDnL/yvPem/HVHVwevqiee8bwaXSrKXTQdZ7/0mXoHfB/cfpdJAtlWbrnitUr4yIUKlERWBfF6E12VepRMUaB4Ba1jnn+oEFwB7Ss5BKuf4a8+4zHqF6ZTaKAZPAzxv0N4AvgVsdej0Yx36kHupstpcwzLmkODS7pyIin6vqOHACuJPob6vqeyJSBL7rAOzMbDQMc663t6eqCYJgKzDfKkwi8jpAT8+WtIi8DHwP/OKcywGkUq5PRD4Afm8T7vmElbitOgCstgMfOfJOLR+eEpG3UynXV1vj0KFXRET2AGeBSou1VhNWvWRu5r/a21IWFhbJ54ekVJr9Dfhsx45ntK/vcYnjmJs3b2Fmc5lMplgulw+a2ftUS+ndsilhPVBVAqDx72MtX1pKN0J9+HBRVOV54KtOQv2gyfXD+uRK3X9yTUzslzDMOeDkPcCvJTs9AdxO9FdUdUBExoG5NsDaczIMc+7AgRelXrmS+xg1MfbAN8BPG/R/Al8ANzuERgljfeVyTmeApSYpIMAY8PQG/VbgJWBLh/m4lDCqeQXVHimK4msicjzxsNviReR4FMXXRkf3Sh1sZpgZQZA6BZx/CODzQZA6VePUwQD5/JCUy5U1VT0KXOoidFFVj5bLlbV8fqjeZtXBqkqhMCze+yVVebNL8EVVect7v1QoDK/rOBsq19jYiHhvc6p6EDjHg525B86patF7mxsbyzd0mg1dppkRhjlZXr58PZ0OvvbeVoFtwGO0L7ExcElEPkqngw+jKP61UBhu2tx31NCnUq4/jrvb0Eu72WnjCHP16mrTEWb79m33NcK0nZ3MrF7dent7/MrKlRtU25510dm9e5fUjq0dFOBf85D8NuATBiwAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjEtMDEtMDZUMjM6MTQ6MjcrMDA6MDCMhAWkAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIxLTAxLTA2VDIzOjE0OjI3KzAwOjAw/dm9GAAAAABJRU5ErkJggg=='

prev_img = 'iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH5QEGFw4ZcddmRgAAA+5JREFUSMe1l89rXFUUgL9z7nsTSmkyWsTEWBgeBBeNhezMKmlmhgglVmwWYmw3KoqCbloXXUlB/Qu6KBHpJtlY0FqKhiTTxk0EIa2TWegiabSE1GBlUlOsmffudZE3Y5KZZCY6PfA25513v3t+3PPOlUymX2hQksk2rly56mq9Gx4+KcXiWqNL4dUzEBEmJ284gCBIGd/3k1EUPQkcjE0eGmP+mJv7sbi4uBQBZLPHxTm397q7eWytZXp6xokIxpgOa+2Acy4LHAOeBg7Epn8BvwF5EZk0RnNhGK0450in+0RV9+dxLveda2lJJEVkJIqit4BuwNQwfQJ4Buhxzr0ehlFBREZbWhJjGxul4m6OmSBIbXthjDI5ecOp6tEwjC4CHwAdQO2tbxcF2oEXo8h2q+r8wsKd1a6uoCr0VYtNTOSciLxgrR0HhhoE1trAkLV2XFV6JyZyrpZBJadTUzedqh51zl2Kc/l/5Xlr3SVV7Z6auumstdXg6ekZl0j4SWvtp02CboHbTxIJPzk9PVPxXGHzyIgIpVI4ApxoIrQsJ0qlcKTMAaBcdcaYDuA24B7Tc9vzTEeZuTXHA2wemUbkT+Ar4P4O/c/ARAzaKd1RZAcqoU4m2wiClImbg6G+fC8iI6r6IbAe6x6K8LmqDonIF0Cts2ucc9kgSJm2ttZNje/7h4G5OqG6JyIfeZ7XHqcmBfwC/CAir7S2HkoAiMibe6wxF7Nit1W7gOVdjEvA1yLSe+bMqxVPPM9rF5H3jDGdAOfOvS8NgJdjVqVlHuTf3rtVlkXkQktLYvzRo7/X19YeSDrdJ8YY7t1bXc3nCxejKCKd7pNbt/KN1MaBmFW3KwlArR+NNPwz3UMaCPVVVek9fXprqE27iLxrjHkW4OzZ/YUa2G9xmeYU1/DwSQmClAEu01gjmBWRoXjnS7FuHfhMVbtE5I09vr0cBClz6tRLUulcIjIChA3CHwBfAr/v0P8EfAvYGt+EMWN75zJGc0ChwbI4BLwMHN6hfw4YpHYDKcSMzbqCzRkpDKMVERmNd9tssSIyGobRSjZ7XCpg5xzOOXzfGwOuPwbwdd/3xsqcChggne6TjY1SUVXPA/NNhOZV9fzGRqmYTvdVUlABqyqZTL9Yawuq8naT4HlVecdaW8hk+rdNnFWda3BwQKx1s6r6GnCN/5ZzC1xT1RFr3ezgYLqq2KqmTOccQZCShYU7q4mE/421bhnoBJ6ifouNgHkR+TiR8C+EYfRrJtNfc7hvaKD3PNMRRc0d6KXe3WnnFebu3eWaV5gjRzr3dYWpe3dyzlW6W1tbq11cXLrPjpHHWktPzzEpp60eFOAfQoT3JtVQzHcAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjEtMDEtMDZUMjM6MTQ6MjUrMDA6MDAbGxSNAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIxLTAxLTA2VDIzOjE0OjI1KzAwOjAwakasMQAAAABJRU5ErkJggg=='

add_img = 'iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH5QEHESQ6AOrAywAAA9NJREFUSMetlzFsU2cQx393n5+jKFLitmppGkVKX4QYSKnY2okQOwoSogxkQE3Xqt26w1aVVureAXUGMbBUCFWRkwBd2CIaPBITlUYtlkAOVYQU+9118LMJ2Eme2/ylT7bfd9/9v7t7d76TUmlayIhCYYSbN3/xXnvz8+elXt/KqorcQQIiQrl8xwHieCJEUVRIkuRtYCgV2Q4hPF9d/b1erW4kALOzp8Xd99e7l8VmxvLyPRcRQgijZjbj7rPACeAIMJiKvgSeAmsiUg5BV5rN5C93p1g8Jaran8UrK7/5wEC+ICILSZJ8CUwBoYfoW8AHwEl3/6LZTCoi8vPAQP7azk6jvpdhIY4nXtsIQSmX77iqHm82k5+Ab4BRoPfVX4cC7wNnksSmVPXh+vrj2tGjcZfru5QtLq64iHxiZteBcxkJe13gnJldV5VPFxdXvJdAJ6ZLS3ddVY+7+9U0lv8XH5n5VVWdWlq662bWTby8fM/z+ahgZj8cEukucvs+n48Ky8v3OpYrtFJGRGg0mgvA2UMkbeNso9FcaPMA0H7rQgijwAPAM6wtEbksIpeBrYxnHuRyYbTNuTvGM7RSJgteqsoNVblBK4+zYCpJbKbj6kJhhDieCGlxCBmV4E5wzy4PBHefjeOJMDIy3HoSRdE7wGpGlzlQU9VjqnoMqPVxbjXlalWutPYe2ee2L3a5VIGaCM30d60drfRzEBjeQ8+RlOtZu2QO8ar2dkFEflSVG6lrRYTm0NDQnwDb29vn3ckBLkJi5hfd/bs9VA2mXP+pKh0eVPUosMk+6QP8na4aUAlBJ0PQSaCSPmvv75demylXK8YhhOdm9pTWv0wvDL8Zt9S9AO8B72a08WnKhc7Pn5fx8bE6sNaHk2yXFdbHubXx8bH6hQufidbrW1SrG4mIlIEkqwYREpHs8kAiIuVqdSPZ2nrxqhFIO4cK8HEGJYNmfrH9PSNxJeVo8cXxhExOfiiPHlX/EZEAnAEOagAHgJl0DWQgNRG5YmYrs7OnBdJ0cnfcnSjKXQNu9+G+rLgdRblrbZ4OMUCxeEp2dhp1Vb0EPDxE0jVVvbSz06gXi6c6nuwQqyql0rSYWUVVvjok8jVV+drMKqXS9GsdZ1flmpubETO/r6qfA7foL13aMOCWqi6Y+f25uWLXO9PVZbo7cTwh6+uPa/l89KuZbwJjtIrEQSU2AR6KyJV8Pvq22Uz+KJWmezb3mRr6XC6MJsnhNvRy0Oz05gjz5MlmzxFmfHysrxHmwNnJ3Tt92cjIsFWrG8+AZ2965+TJE9IO20GkAP8CCfXdMKmeyd0AAAAldEVYdGRhdGU6Y3JlYXRlADIwMjEtMDEtMDdUMTc6MzY6NTgrMDA6MDA+IMt0AAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIxLTAxLTA3VDE3OjM2OjU4KzAwOjAwT31zyAAAAABJRU5ErkJggg=='

del_img = 'iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH5QEHESQ7d+3wXQAAA7hJREFUSMetl89rG1cQgL95q11TCpHaUlI7MYgFn+Km9a092bEk3NqkOcSnupBDKG1OvecYaPsXFBJMIT04p1xKSIqR5cS95GZS21crxj8iGoiRC6Ug7b7pQStFtnYlOdHAIrFvZr43M++9nSf5/JTQp2Qyae7f/13jxubnr0i1etSvK1K9FESEYvGxAvh+1nFdNxOG4fvAu5HKv47jHK6v/1Utl3dCgELhkqhqd79JEVtrKZXWVERwHGfYWjutqgXgInAWeCdS/Q/4G9gQkaLjmNUgCCuqSi43KcaY00W8uvqnDg15GRFZCMPwW2AccGJU3wNGgAlV/SYIwi0RWRwa8pZqtXo1KTDH97PHBhzHUCw+VmPMhSAIfwF+AIaB+KkfFwN8BHwRhnbcGLO5vf385diY35H6DmfLy6sqIp9Za+8Bl/sExk3gsrX2njHy+fLyqsYptGq6svJEjTEXVPVOVMu3lY+t1TvGmPGVlSdqre0El0pr6nluxlr784CgbXD7k+e5mVJprRW5gcaWERHq9WABmBsgtClz9Xqw0OQA0Fx1juMMA88ATXgOgEqX8UqkkzT+LJVyhpvM9hpP09gycfJCRK6JyHVgL2Z8T0Sui8g14EWCj/EwtNOtVGcyaXw/60SHg5NgZABPVR+JyA1g/wT0hqo+AjySd4GjqgXfzzrp9JnGG9d1PwDWu6RJgV0RmQOIfveB/bZ3s8BuDx/rESsKx5ixHvVpPnttoIKIFE4BVeAgYrXAnwKHfRhqFGWhaRv93+/T9jBivdGpNDg5Rap3B5rqN1hcs2+9uObnr4jvZx3gbheDSuQ4DtC+4L6ksY+T/Nz1/axz9epXYqrVI8rlnVBEikCYUA0L1ERkVlVvA6NtY+dV9XYEr0W6cRKKSLFc3gmPjv553QhEncMW8EmM0Yiq/sbr7+1JOa+qv0YTH0kAb0WMxrqCRo8UBGFFRBa7zHgkAdqUs12gVkQWgyCsFAqXpAVWVVQV100tAQ8ZvDx03dRSk9MCA+Ryk1Kr1avGmJvA5gChG8aYm7VavZrLTbbarBbYGEM+PyXW2i1j5LsBwTeMke+ttVv5/NSxjrPj5JqZmRZr9akx5mvgAck17yYWeGCMWbBWn87M5Do6zY4uU1Xx/axsbz9/6XnuH9bqAXAO+JDeR2wIbIrIj57n3gqCcDefn4pt7vtq6FMpZzgMB9vQS6+708krzN7eQewVZnT03KmuMD3vTqra6svS6TO2XN55Bbw6mZ2JiYvSLFsvKMD/v3kRHsEU+ggAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjEtMDEtMDdUMTc6MzY6NTkrMDA6MDCYV8DAAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIxLTAxLTA3VDE3OjM2OjU5KzAwOjAw6Qp4fAAAAABJRU5ErkJggg=='

rep_img = 'iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH5QEHESQ7d+3wXQAABI5JREFUSMetl01onEUYx3/PzO6mbSDZKiVN02DY2nhorOYitSBJk11iKaVUAoLpQUFR8CB4EKk3wQ+8ePJQ9OAlpYdC0VLSuJu09VLxEGmag4Zmu22+TKFhqybV7M48HvbdNNl902xp/zCw7z7PzH+emedrJJnsFmpEPN7I2bM/aJisv/+Y5PP3al2KyGYKIkI6fUkBEok2G41G4865p4D6QGXJWrs4NnYtn83mHEAqdUhU9eHrbmSx956RkSsqIlhrm733PaqaAvYDTcDWQPU+sACMi0jaWjNaLLp5VaW3t0uMMY9m8ejoz1pXF4uLyIBz7h2gA7AhqtuBXUCnqp4oFt2EiHxbVxcbXFkp5DcyzCYSbesE1hrS6UtqjNlXLLpvgA+AZiB86+thgJ3Aq875DmPM9ampm3f27k1UHX3VYsPDoyoiB7z3p4GjNRKGbeCo9/60MfLy8PCohims3mkmc1mNMftU9VRwl4+L573XU8aYjkzmsnrvq4lHRq5oLBaNe++/eEKka8j957FYND4ycmXVcgOlkBERCoXiAHDkMUiywB8h/x8pFIoDZR4IwimTuazW2mbn3BDwQsjEv4CfRORq8DsMBrghIgve+0+A14C6NfJrkYg9XCy6+WSyW1bDyXvfQylkKpETkQ9bWpp/nJmZc+3te4z3WhUiqkp7+x4/NJRREflOVV8Bdq9R6XDO9wCDAJF4vJFEos1ms7kU1XG6LCIfq+q52dn5LuDNycmppg0sttls7lcR+VNVP6ogBbCqmkok2s40NjaUvCwajT4NjAFaMdL19du2GCMHgOkQeeVYBv57iHws4Co5V5B7qywRkd+Wlpb/VeV4iAVh2ArEHiJvCrhWw6meB7l3LaLW2t2q+kwNpGX8A9wCwkrVVh4UFzDGvAgshhxNHsgBf9dwzOVxxlq7W0S+DpEtBlyrRWKJUpXZXrHDxmDUDBG55ZybEZFCiPh+wFU6amvtIqXSthFWgkmbYVqEc/X127aoameIfCHgItLff0yCIj4OhCnfFpGvgJ2q+hLgNiBdEJHvvddflpfvvw4cDNEZb21tyXd27pdIPn+PbDbnRCStqidYH8szIvKWqo4ePpySyckbppzy1sIY0cnJKb9rV7Odm5s/rqpfAtsq1JyIpLPZnEsk2h5krqBzmGB9ytyhqm8bYxYuXsw0Ac8CnhCISMPs7NxBIAU0hKhMBBylr2SyW1KpQxJMfj84ykpv/B2YonbPrhwuWJtU6pAkk91ioJRnVZVoNDIIXAjZ7XNAogbn2ggXotHIYJkH1tTj3t4uWVkp5I0xJ4Hrj0FSiXFjzMmVlUK+t7dr1UFWiY0xJJPd4r2fMEbefULk48bIe977iWSye13HWdVP9fX1iPd61RjzBnCeDZxpE3jgvDFmwHu92tfXWxUKVV2mqpJItMnU1M07sVh0yHudBVqAHWze+Dnguoh8FotFPy0W3e1ksju0ua+poY9EbLNzT7ahl83eTpVPmOnp2dAnTGtryyM9YTZ9O6kq5c01Njb4bDZ3F7hbeTqdnfulfG2bkQL8D4gjM220sbbXAAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDIxLTAxLTA3VDE3OjM2OjU5KzAwOjAwmFfAwAAAACV0RVh0ZGF0ZTptb2RpZnkAMjAyMS0wMS0wN1QxNzozNjo1OSswMDowMOkKeHwAAAAASUVORK5CYII='

rep1_img = 'iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH5QEHESQ7d+3wXQAABIxJREFUSMetl01sVFUUx3/n3jfTQgkdFQOVNEyeIZpQUYgRXCD9mElJCLqAlW3iiujOjStMXJiIG1cmLAgbFpaYiAtDiGmmH4ALiNEGoYnG2KHQ1AJKMygtdPrePS7mdRjevLYDeJKbTN45c/73fN37v5LLdQoNSibTyunT32mS7tChd6RUutuoK7zVDESEQmFUAXw/a1OpVCYMw2eBlshkzlo7Ozb2S6lYnAwB8vkuUdWV/S4XsXOO4eHzKiJYa9ucc92qmge2AxuBNZHpfeAWcEVECtaakSAIZ1SVnp69Yox5vIhHRi5oU1M6IyJ9YRgeBjoAm2D6DPACsENV+4MgHBeRE01N6YFyebG0XGDW97OPKKw1FAqjaozZFgThMeBDoA1I3vqjYoBNwL4wdB3GmKsTE9dub93q16W+ztng4IiKyG7n3CngQIOASRs44Jw7ZYy8OTg4okkG1ZoODZ1TY8w2VT0e1fJp5RXn9LgxpmNo6Jw65+qBh4fPazqdyjjnPn8K0Cngej24O5pOpzLDw+erkXtQGZlo9QH7ExzOAz+IyCXgnxXS+5uI3HTOfQLsA1KRbv/iYtAnIsfy+S5UFZa6zlrbBlwGNLamRaR/3bqW5kbDFpG3gBsxP5c9z7ZBBbM6Ts65biojUysPROSIqn41P3//DRHpU9W2BCwFrIj8BPypqh8D7TGbjjB03cAAgJfJtOL7WVssTuapn9NLzc1N3ywslHdGXf5ijS6oLReAqvZGKV+bsDmrqnnfz37d2rq+0mWpVOo5YCyeZhH5Ikrd0XjaRKRXRPqB2YTyLLfGIqxKV0dn78akFHqet0FVt8Rq+K2qDorIj0C50doDGyOsihhjXltm538BvwKl2PefrbVZY8xLwM3HiHg2wlr1dtoQrbi0q2pT5Cwud4GZFf5LNdXAHJVbplFxVJorTNCd9Txvj4icTNDdj7AqEVtrZ51zt6jcMo1IWlV3Lf2uVYjI9SAI/haRpFvpVoRVYQ6+n7XASZavzTzwb+zbYrRqv/1hjNm5Zk3zWmA0wc9J38/agwffFq9UukuxOBmKSEFV+6mf5d+jcWpT1dej9NZFIyIzIjLgnBt78GDhPWB3zCQUkUKxOBn6fvbhyRUxh3Hg1RrjKRE5rKoXVsu9qtLSsrZ5bm6+X1WPAvEjdjzCoFrjfL5LCoXRGRE5oapf8rDpNqnqR8aYeVXdBLwcNVaStN67N7cL2EP9yeVE5EQQhDNLfMxb2q2qEtGVXioEACq3ywHn3PZoM+08mZxNpbyBhYUy+XwX1ERGT89eKZcXS8aYI8DV2B+3PAXoFWPMkXJ5sdTTs7faG1VgYwy5XKc458aNkfcTwJ8QVD5wzo3ncp2PMM46PtXb2y3O6UVjzLvAGZav6UrigDPGmD7n9GJvb0/dFNSxTFXF97MyMXHtdjqd+t45nQY2A8+zOvELgasi8lk6nfo0CMIbuVxnIrlviNB7nm0Lw/+X0Mtqb6f4E2ZqajrxCdPevvmxnjCrvp1UtcrLWlvXu2Jx8g5wJ56dHTu2y1LZVgMF+A/ttjltfXuhUAAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMS0wMS0wN1QxNzozNjo1OSswMDowMJhXwMAAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMjEtMDEtMDdUMTc6MzY6NTkrMDA6MDDpCnh8AAAAAElFTkSuQmCC'

rand_img = 'iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH5QEHESQ7d+3wXQAABINJREFUSMfFl09oXHUQxz/ze+9tlPzZTTZBYyldntRLYyEHwZ6aZneJUGqF9GSKFxHFi/deioJ61YOH0ksFUzy0YCmthE3SxEsPYq1tQT1kG1pCadNstyRtcfe933jY97abzcZNNOAX5rDMvN/3N/ObmZ2RXG5E2CJSqSTnzl3QVrpjx45Kufx4q0fhtjMQEQqFKwrg+xnH87xUGIZ9QGdk8sRxnNK1a7+Vi8XFECCfPySq+s/nbuaxtZaZmXkVERzHGbTWjqpqHtgPvAS8GJk+A+4DN0Sk4DhmNgjCe6pKNntQjDHb83h29ift6EikRGQiDMMPgCHAaWHaC7wCDKvq8SAIb4nI6Y6OxGSlUi1v5pjj+5l1CscxFApX1BizLwjCb4BPgEGg9dXXwwAvA2+FoR0yxtxcWLj9YO9ef0PoNxw2NTWrIvKmtfYscGSLhK0ucMRae9YYOTA1NautDOpvOj09p8aYfap6KnrL/4rXrdVTxpih6ek5tdZuJJ6ZmddEwktZa7/cIdIGcvtFIuGlZmbm654bqJWMiFCtBhPA4R0kjXG4Wg0mYh4A4qxzHGcQuA5oJBYIW4huIrHeAr8Afzbpr7uuMxhz1svJWjtKrWRiXBaRb4HmcuhT1XEgG/2eFpHzwKM4iiLyBxBYa08CRwEPGApDOwpMAripVBLfzzjF4mKehjoVkYW+vt4fKpXKuqxeXV37y3Xd80EQfAeEruu+FwTBw+7urg4AVUine4PFxTuhMeaCquaAFOCoat73M98nkz1WADzPS1er1QIw3MCxBBSbvDUiMpdO9326slJ6QwTt7+//eXn54UlVPRSF2YjINOCp6scRaYxfPc/LV6vVldppxuyNiHQLsiYi+YbIZIHVJptn0SWav12KuOrl1Mnz3tsOnar6fjLZk0gmexKq+gHQ1WTzQovcIOLobCT+f7DNUK9G4Y1DnQfWthtqF8BxnJK19j61f5kYmyXXlYGB/vnl5YcHAEmn++ZWVkpfqeoI7ZPrfsRVmxx8P+MAZxpvJyJfp9N9Xnd3V0ejALiu2w9cBqZc1x0AiPVdXV0de/bsdlQVETlOrb7jc8/4fsYZH39b3HL5McXiYigiBVU9TlTLqvpqqfToneYkEZHeIAjGgRxAEARnReT82tqTUhyVp0+f/u44TqiqR3k+qYQiUigWF0Pfz0i9ZUbt7Do70zKv0aZlGqjNSEEQ3hOR09GHRJ6aFrJpjkYi1BrRaw06KyKngyC8l88fktgYVUVV8Tx3Erj0r8tjc1zyPHcy5qkTA2SzB6VSqZaNMSeAmztIesMYc6JSqZaz2YP1fKkTG2PI5UbEWnvLGPlwh8hvGCMfWWtv5XIj6ybODW82NjYq1upVY8y7wEWev/l2YIGLxpgJa/Xq2Fh2Q/vcMGWqKr6fkYWF2w8SCe9Ha3UJ2AUM0L7FhsBNEfk8kfA+C4LwTi430nK439JA77rOYBju7EAv7Xan5hXm7t2llivM7t27trXCtN2dVLXeZJLJHlssLq4AK83RGR7eL/GztSMF+But+UKChACi7wAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMS0wMS0wN1QxNzozNjo1OSswMDowMJhXwMAAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMjEtMDEtMDdUMTc6MzY6NTkrMDA6MDDpCnh8AAAAAElFTkSuQmCC'

vol0_img = 'iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH5QEGFw4a6N43/AAABDtJREFUSMetl81vVFUYxn/vOXOnQoWOgJSKTYZL2EjFlJUmJpTOjDUhSJRutMaFkcjOpQkxLsTPP8BExCAxATdsDCGm6UwBo7KyIjS4akv4CLEGUxZtdeae87qYO9PpzNDpaJ/kbua+c37n4znPPUey2QFhlUqlujh37jtt9m54+JDMzT1YbVMkWhWICGNjFxUgDNM2CIKUc24T0BmXzFtr/5qY+G1uevqmA8jl9ouqrtzuw0bsvadQuKwigrW2x3s/qKo5YA/QDayLSxeBP4BrIjJmrRmPIndPVclk9okxpr0Rj4//oB0dyZSIjDjnjgB9gG1S+hjwBNCvqq9HkZsUkZMdHckzxWJp7mEDs2GYXvbCWsPY2EU1xuyOIvc58A7QAzTv+nIZYBvwonO+zxhzfWpqZnbXrrBh6hsaGx0dVxF51nt/Fji4SmCzDhz03p81Rp4bHR3XZgXVNc3nL6kxZreqnojX8v/qae/1hDGmL5+/pN77RnChcFmTySDlvf9kjaA1cP9xMhmkCoXL1ZEbKG8ZEaFUikaAA2sIrehAqRSNVDgAVFxnre0BrgLa4lkERilvoVa1tc/VRML2VJi1azxIecuspAkRedNaexS43+ao+5zzg9WpTqW6CMO0jcOhfp+WgAXgroh8aK09pKrfisgCUNmG/wA/xzNR0VXgTl1bVlVzYZi2XV0by78EQbAZmGgyPV+LyPPGmKf27n2mOjuJRGIb8DugIvJlEASbROT9uBN5a00oIq8AD+ram4hZZXPF2dtdPzciMqOqP3rvb/T2btdMZl9DCqlq6L3fuGHDo5+KyBFjzNEtW7bcAnYDHXXl3TGrup06WcreWpmKGebnF5YcuVwZ59xX8/MLW1X1m507d0zPzv75rqq+1wS8Lmb9p1RaE1XA8yw3R0UeIJ+/pJ2d63nIp65grX2rs3P9rIi8MTU1E3Z3b/1MRI5TXvNaLcasslYw16lW5gLqzVWIzfUyK5iL4eFDEoZpC5xuAi7GPbwjIsettU/G4O4a8N/AT3Fd5X+/ArebtHc6DNP28OGXpJpcIjICRKycPr+IyKvW2h3ADdpLrihmLE8ua804MNnCE3tV9ZRz7gtgc5t+mowZS+bK5fZLFLl7InKyYqgV9AjwArC1DagXkZNR5O7lcvulClZVVJUgSJwBLrQ5ktXoQhAkzlQ4VTBAJrNPisXSnDHmGHB9DaHXjDHHisXSXG3yVcHGGLLZAfHeTxojb68R/JoxctR7P5nNDiw7cTYk19DQoHivV4wxrwHnab3mzeSB88aYEe/1ytBQpiFrG06ZqkoYpmVqamY2mQy+917vAtuBx2kdsQ64LiIfJZPBB1HkbmWzA00P96s60CcStse5tT3QS6u7U/0V5vbtu02vML2929u6wrS8O6lqNd26ujb66emb96k79njv6e/fI5VlawUF+BcpQwHu9dQSjAAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMS0wMS0wNlQyMzoxNDoyNiswMDowMCrzDhAAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMjEtMDEtMDZUMjM6MTQ6MjYrMDA6MDBbrrasAAAAAElFTkSuQmCC'

vol1_img = 'iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH5QEGFw4a6N43/AAABBRJREFUSMetl01sVFUUx3/n3PdmQjB00BiphDh5CcGUirLDREPpzKQaggRpXFhdGtwoxh3oykTdG10gGxKFjURjCNGmH4AxwVVTSkPctJSPBiUBx0TEzrx3j4t5M7R0pjPV/pPZvHfe+d17z8ecK8Vin9ChcrkuTp/+3pq9GxzcL+Xyn526ImhnICKMjJwzgCjKuzAMc0mSPAqsT03uOefuTkxcKs/OziUApdIeMbOV/bbasfeesbELJiI457q99/1mVgJ2AE8A61LT+8DvwJSIjDin43Gc3DIzCoXdoqqr2/H4+E+WzWZyIjKUJMlbQC/gmphuBJ4EdprZG3GcTIvI8Ww2c7JSqZZbbcxFUX7JC+eUkZFzpqrb4zj5AjgMdAPNl75UCmwCXkoS36uql2dmrt7eujVadvTLnA0Pj5uI7PLenwL2dQhstoB93vtTqvL88PC4NTNoxHR09Lyp6nYzO5bG8v/qGe/tmKr2jo6eN+/9cvDY2AXLZMKc9/7TNYIugvtPMpkwNzZ2obFzhVrJiAjVajwE7F1DaF17q9V4qM4BoJ51zrluYBKwDn5/AT8Cdzu0N2AyCFx3nbk4xv3USqadfhGRN1X1cLqAayLyLvAltXpupd4k8f2No87luoiivEubQ7M6rQB/p4APgyA4YGbficg/aajKQRB8DRwSkdeAqRZgZ2alKMq7rq4NtSdhGD4GTDQ7IhH5XEReUNVtR46836h551weuAbcA86IyAEAESkCd1oc90TKSretuhWYbwF+r5EhewdkUU7kgblFtndF5OWenqcV+KYFeD5lNcppPQ9678PSekIsLCysFPuNZvbqlSu/ehGZbGGzLmX9p660JqqD71H7l2kmDzA6et6y2exKvv4QkW97erapmT3XwuZ+yqpp5eRitclVoJPkGhzcL1GUd8CJFsYLqfM5EfkgCIJNKfgp4CYwGYbhxhT6InCJ1k3kRBTl3cGDr0ijc4nIEBDTvgNdFJEDqroNuJ4u6B0RjgG/rfBdnDIoFvukMQikk8M08GybvNhlZl+Z2c/AI9Sy+bMO8mk6ZTxIrlJpj8RxcktEjteTqY3WAwPUpo9O5EXkeBwnt0qlPdIAmxlmRhgGJ4GzHTpbjc6GYXCyzmmAAQqF3VKpVMuqehS4vIbQKVU9WqlUy4XC7kZVNMCqSrHYJ977aVU5tEbwKVV523s/XSz2LZk4l3WugYF+8d4uqurrwBk6i/nD8sAZVR3y3i4ODBSWTZrLpkwzI4ryMjNz9XYmE/7gvc0Dm4HHad9iE+CyiHycyYQfxXFyvVjsazrcdzTQB4HrTpK1Heil3d3p4SvMjRvzTa8wW7ZsXtUVpu3dycwa3a2ra4OfnZ27Q60XLzmdnTt3SD1s7aAA/wL6S/b0DJZNZwAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMS0wMS0wNlQyMzoxNDoyNiswMDowMCrzDhAAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMjEtMDEtMDZUMjM6MTQ6MjYrMDA6MDBbrrasAAAAAElFTkSuQmCC'

vol2_img = 'iVBORw0KGgoAAAANSUhEUgAAAB4AAAAeCAYAAAA7MK6iAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAABmJLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH5QEGFw4a6N43/AAABOlJREFUSMetl01sVFUUx3/n3PemtiR0ChqoWBgHWShfdkN0YQr9CEaCmFA2VhIkgeDKGFkorjQBFkpkI8R0IYmBhFgTDUFDSovVBW6sCCQuzAABSYEEKCJFZ967x8W8GcrM9Es9ydvc97/3f8/H/d9zpbNztTBNS6cb6ev72mr96+7eIKOjd6a7FMFUABGhv/+UAWSzGReGYTqO4znArARyzzl3a3j4l9ELFy7FAF1da8TMJl93Io+99wwMDJmI4Jxr9t63m1kXsAKYB9Qn0PvAdeCsiPQ7p4NRFI+YGR0dbaKqM/N4cPB7q6tLpUWkJ47jbcAywNWANgGPA61m9loUxedFpLeuLnU4ny+MTuSYy2YzD/1wTunvP2WqujSK4k+AN4FmoPbWHzYF5gMvxrFfpqrncrmLN5YsyVaFvmqxEycGTUSe894fAdZPk7DWBtZ774+oyvMnTgxWJbzscSmnqrrUzA4luZzM/gCOAr8lROkam5xnxipV/SGXu3gjk1koIvKwxwMDQ5ZKhWnv/d5pkALcds69B2wKArdGRLYCP9bALffe70mlwvTAwFDZc4XikRERCoWoB1g3zXDO8T7eJSLbvLcmM/s8CIJXRDgIRBXYdYVC1FPiAaBUdc65ZuAMYJN8fwP9wNWK8RER2RuGwdxZsxrqRThQY+6ZIHDNJc5yqL337RSPzER2XkR2OOe2AteA2yKyU0T2AwUze6dQiD7N5/MNzgXv1wj7sjj27eVQp9ONZLMZl4jD+HNaAMaAayLykXNuvZl95pzeTVI0pqpfmtlbqroe+B7YGEXxziiKrovIgYqQOzPrymYzrrFxdnEkDMO5wHBFaI6KyAuqurylZYEDMLtHGIZNCbYAnBSRLYsWLXSquhK4DIyo6tNB4OYDv1asOZxwJW6rLqnMm4jsK/3v7t4gHR1tYvZnifincdj7IrIlKdL9ydztQ0PfAPRVEF9NuMrHaRYPtLdkUiqE0dE7D6qx2h4xs02LFz/pgJ+TsWxb20uIyEgFtj7h+leqNAOb+IYqEd+jeMtUzTp58jtLpxuZ5Jr7S0S+yOUuxkBrMpYbHDyGGc0V2PsJV9GmLq4nJi2uTGahU9VnmUlxdXdvkGw244BDFaB8srsREfnQOZcBSKXCdJLL30tjCekQxcLaCyAim5PNjV/zUDabcRs3vixl5RKRHornbiLVOicirzvnWihW9S0ReVtEPk48NaAvDIO5QRDMA05XzI8SjiJniTiRszP8R8lsaGioh2lKZlfXGomieEREegE/SZmmgE6KHcddEQ6KyHZVbTezd80IxsbG9gHbKuZ5EemNonikq2uNlKvazDAzwjA4DBxnenZL1e0xs15VuS0im6Mo+gp4g+qW6ngYBodLPIwHdHS0ST5fGFXVXd77DLB8CuKmOI53Aw1RFC8DnqJ2D3dWVXfl84XR8c1fuQMREbLZjORyF2+oyhkzVlHsJieyOmAl8AzwKLXF6Kyq7PDehjs7V8t49asCr13bLt7baVV9FTg2Rc4nMg8cU9Ue7+302rUdVXpb1WWaWdnzVCr81nu7CiwAHmNqiY0pHrvdqVT4QRTFlzs7V9ds7qfV0AeBa47j/7ehl6neTpVPmCtXrtZ8wrS0LJjRE2bKt5OZlUWmsXG2v3Dh0k3gZmV0WltXSCltU5EC/APj9EXjY/OiLAAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMS0wMS0wNlQyMzoxNDoyNiswMDowMCrzDhAAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMjEtMDEtMDZUMjM6MTQ6MjYrMDA6MDBbrrasAAAAAElFTkSuQmCC'


#Upload Images
#pause_bt_img = PhotoImage(file='Desktop/mp3/buttons/30x30/pause_media_music_player-512.png')
pause_bt_img = PhotoImage(data=base64.b64decode(pause_img))
#unpause_bt_img = PhotoImage(file='Desktop/mp3/buttons/30x30/play_pause_media_player_music-512.png')
unpause_bt_img = PhotoImage(data=base64.b64decode(unpause_img))
#play_bt_img = PhotoImage(file='Desktop/mp3/buttons/30x30/play_music_media_player-512.png')
play_bt_img = PhotoImage(data=base64.b64decode(play_img))
#stop_bt_img = PhotoImage(file='Desktop/mp3/buttons/30x30/stop_music_media_player-512.png')
stop_bt_img = PhotoImage(data=base64.b64decode(stop_img))
#prox_bt_img = PhotoImage(file='Desktop/mp3/buttons/30x30/forward_rewind_music_media-512.png')
prox_bt_img = PhotoImage(data=base64.b64decode(next_img))
#ante_bt_img = PhotoImage(file='Desktop/mp3/buttons/30x30/rewind_previous_music_media_-512.png')
ante_bt_img = PhotoImage(data=base64.b64decode(prev_img))

#add_bt_img = PhotoImage(file='Desktop/mp3/buttons/30x30/add_plus_media-512.png')
add_bt_img = PhotoImage(data=base64.b64decode(add_img))
#del_bt_img = PhotoImage(file='Desktop/mp3/buttons/30x30/close_exit_media_player-512.png')
del_bt_img = PhotoImage(data=base64.b64decode(del_img))
#rep_bt_img = PhotoImage(file='Desktop/mp3/buttons/30x30/repeat_all_music_media_player-512.png')
rep_bt_img = PhotoImage(data=base64.b64decode(rep_img))
#rep1_bt_img = PhotoImage(file='Desktop/mp3/buttons/30x30/repeat_one_repeat_music_media_-512.png')
rep1_bt_img = PhotoImage(data=base64.b64decode(rep1_img))
#rand_bt_img = PhotoImage(file='Desktop/mp3/buttons/30x30/shuffle_music_media_track-512.png')
rand_bt_img = PhotoImage(data=base64.b64decode(rand_img))

#vol0 = PhotoImage(file='Desktop/mp3/buttons/30x30/silent_sound_off_media_music-512.png')
vol0 = PhotoImage(data=base64.b64decode(vol0_img))
#vol1 = PhotoImage(file='Desktop/mp3/buttons/30x30/sound_down_volume_music_media_-512.png')
vol1 = PhotoImage(data=base64.b64decode(vol1_img))
#vol2 = PhotoImage(file='Desktop/mp3/buttons/30x30/sound_up_volume_music_media_-512.png')
vol2 = PhotoImage(data=base64.b64decode(vol2_img))

img_01 = 'iVBORw0KGgoAAAANSUhEUgAAACAAAAAUCAQAAABGmPfEAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAAmJLR0QA/4ePzL8AAAAJcEhZcwAAAEgAAABIAEbJaz4AAAAHdElNRQflAQcUCRtqYkiRAAACzElEQVQ4y42TX0hkZRjGf+93znjGGVNJDbdohb3YyM3FSxP/oelN7BJLLioxxLIEgUVdbIGiUlAXXkSBEQSBebF0UQYWrBs4uSxEu1hE204ssRJDLIaWuen8OTPne7s44+6MZPRcfbzfc37f8768R7inbvJs8gCGH6hUM058a5Fo82ndSR+4M/ePV7mOV9UrHjMHTH+yGfOPFlv2ajJwOKCGutb1T+fPXEOANk5ynE56AcWiCirCcTroKgO4ANOA5S3khD0laT67w5Ps0CY/VX2Tr3hON3nI+7ai5sIIbyCAwQIK+HikSI8WRhovFG91kETDuLb2zC/n6l4PbnYhKMv7LQi1/fGZR+v3CT6/AZk+/1T28QzL+Puvid/nP/136x7LXKKeBGO4Dp+jRJ/3n7uTxIbGi2FeBbUNR/6aiHyZWyv1AFj7cOP2VGTlkyUAExvznpo16qotOKEp4cRfjJ8fcgAk2GvPje8+UzEJu9Waezl3dtypScQm3b0F8/1HQ6UmATTZlHvNZq8uhjU1YEWlnFA0Gqh8VZt7NWg31lEv45QBKBpEJWc4VAKggcEo/2H7fzImkHwsoCyia1HRqD38IwUQx2IFE0/EJs7fLQNI/2Z0tvqdnp2wJhaMipYDXCuO6OBd793olJu56HKBqaIYJygCsBDwAVxGAHWqvyvMRb7IVaRuTG2/F0m+H/AxuAHPItTNu7cbbqQHQsdZ1lhHRBGzveG/lMVtuj8+Yza27CtZxvgdCf8FRZIks+FeCsRoYZ3q1WJz9OcIA6yUNqyoVat6LJqydCNss7KfaYJJphHMMOrNwQt0coJRafPC+whuEynn14ZH4AmvcqAuwNsA1ODczC5VfZ3nCB9ykpT6+W4iJMsWoIlCvpMIVyoBoXYh9djwYOEaCvwIwK1S54IIiGqpwr8BevDZ8FcR3jxgehCT+SNNNL6rHNQ/aswIpDXuJtQAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjEtMDEtMDdUMjA6MDk6MjArMDA6MDBu8ZIFAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIxLTAxLTA3VDIwOjA5OjIwKzAwOjAwH6wquQAAAFR0RVh0c3ZnOmJhc2UtdXJpAGZpbGU6Ly8vaG9tZS9kYi9zdmdfaW5mby9zdmcvZDQvZGMvZDRkYzM2OGU1YTQzOTJiNDc1MGM4MTkwMTQwNTdkMzkuc3Zn7QjXCQAAAABJRU5ErkJggg=='

img_02 = 'iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAMAAAC6V+0/AAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAn1BMVEUAAABEREBDQz9OTkmMjIQMDAxCQj5zc20CAgIBAQEAAAAAAAAAAAB0dG0EBAQBAQEAAAADAwIAAAAAAABNTUkAAAAAAAAAAAAAAAAAAAAAAAAAAAAHBwYBAQEAAAACAgIDAwMAAAAAAAABAQEAAAAAAACHh38CAgIBAQEAAAANDQxra2UAAABHR0IAAAABAQEAAAAAAABycmsAAAD///9SHUsLAAAAM3RSTlMAAQEBAQYBASVlmbGYARV/3yK0tQHszOfxzeuiDYzDJiGonIH1zgEzZ8QGAZoBuEr9+QF14IKDAAAAAWJLR0Q0qbHp/QAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB+UBBxQeAZKDNX0AAADVSURBVBjTbZGJDoIwEERHzlZOEfG+b7xQ/v/fnLZoMPElhOyjtLNbdIhlA47rOoBtqRp8PPhCdoMglCKCZ6SHOElrTZrEyoKul9Vf+j1aWIhbjjamsv2k/iGJckBwv0ExHI0LMuG+AoDk1+lsvliuyJqFZL4u3xtsd/sx4co6PMANtDyeNGcWQdnICwxXI51QSf+m2rv5G/O7PuiK1koepCPdHw13E8mOGL56NlQM/8pVm/12Q5lqUw2kZTM9kP+jUzYSMtRDfn2GzOvgXA5lyXy5vo43zLknp8p3BzsAAAAldEVYdGRhdGU6Y3JlYXRlADIwMjEtMDEtMDdUMjA6Mjk6NDkrMDA6MDBlameQAAAAJXRFWHRkYXRlOm1vZGlmeQAyMDIxLTAxLTA3VDIwOjI5OjQ5KzAwOjAwFDffLAAAAABJRU5ErkJggg=='

img_03 = 'iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAMAAAC6V+0/AAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAbFBMVEUAAABEREBDQz9OTkmMjIQMDAxCQj5zc20CAgIBAQEAAAAAAAAAAAB0dG0EBAQBAQEAAAADAwIAAAAAAABNTUkAAAAAAAAAAAAAAAABAQEAAAAAAAACAgIAAACHh38CAgINDQxycmsAAAD///9G/Og0AAAAInRSTlMAAQEBAQYBASVlmbGYARV/3yK0tQH81+zwP6PvMp0BMwYB69YocAAAAAFiS0dEIypibDoAAAAJcEhZcwAACxMAAAsTAQCanBgAAAAHdElNRQflAQcUHgDlhAXrAAAAr0lEQVQY022Rhw7DIAxEr5kQIHsnZP3/R9Y4apVWnIRkHsKcD7xIQQhEcRwBYeD2oJUgFTJTSkthkNwwQV6UF6ssckdBrKqvr5qKKALkD0Y0JxSmxfWjwrSA4H5dPwx9x30FAMnn4zTP08ilJH8ZV8tq7bpwqTfE6oa7tfsN1eGHkfZc9z7ktRSaf/Nn68Zsnqx2Y7pAHrTmQPzROWqE1Bzy+QmZvoNy2Y6D/LX8HW/FuyAZnjOEAgAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMS0wMS0wN1QyMDoyOTo0OCswMDowMMMdbCQAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMjEtMDEtMDdUMjA6Mjk6NDgrMDA6MDCyQNSYAAAAAElFTkSuQmCC'

img_04 = 'iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAMAAAC6V+0/AAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAY1BMVEUAAAD///VEREBDQz9OTkmMjIQMDAxCQj5zc20CAgIBAQEAAAAAAAAAAAB0dG0EBAQBAQEAAAADAwIAAAAAAABNTUkAAAAAAAAAAAADAwMGBgUFBQWHh38NDQxycmsAAAD///+/2J+wAAAAH3RSTlMAAAEBAQEGAQElZZmxmAEVf98itLUB9dDNIBARAQYByNgcpAAAAAFiS0dEILNrPYAAAAAJcEhZcwAACxMAAAsTAQCanBgAAAAHdElNRQflAQcUHgDlhAXrAAAAsklEQVQY022RiQ6DIBBEB8UDRMETxev//7K7NG1swyQkyyMsswMyUi6BoiwLQOa8B60KtdKNMa1WHao3rGBdf0f1zjIFsWG8v5oGoshhH4yoJSRrd//IdTOguN/iV5JfuK8CoPnYb2Hfw+a51uSv4WINEAJh5bo9UJoId5FlYo/QnGlYtInryYeSlmT3b/6aeczpyUYekwN50DEGko6Oaad0G0O+PiHTd1Aux3mSvzl+xwvv5ByRxOBYWQAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMS0wMS0wN1QyMDoyOTo0OSswMDowMGVqZ5AAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMjEtMDEtMDdUMjA6Mjk6NDkrMDA6MDAUN98sAAAAAElFTkSuQmCC'

img_05 = 'iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAMAAAC6V+0/AAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAWlBMVEUAAABEREBDQz9OTkmMjIQMDAxCQj5zc20CAgIBAQEAAAAAAAAAAAB0dG0EBAQBAQEAAAADAwIAAAAAAAAAAABNTUkBAQEBAQEBAQGHh38NDQxycmsAAAD///+FXodDAAAAHHRSTlMAAQEBAQYBASVlmbGYARV/3yK0tfsBjl1gAQYBayAzhgAAAAFiS0dEHesDcZEAAAAJcEhZcwAACxMAAAsTAQCanBgAAAAHdElNRQflAQcUHgGSgzV9AAAAq0lEQVQY022RCQ7DIAwEtyEHhCsnkKT/f2dtQquowhLCHonFXuNF0Qig7boWEA3XoNNjkGrU2ihp0d+wh/PTO8fkHVMQm5f3L9aZKBq4ByPqCInB39W23be3OyCLXghFVwJQ5V2MJVHU31jylEpiDnSa9UJMUqYYWFefddiayvPqR9WWhP1v/tp5zPU55sJjsiEPumRD6tYxtVKZbPL1NZnWQb4c50n97XkdHxSeG33yBDDEAAAAJXRFWHRkYXRlOmNyZWF0ZQAyMDIxLTAxLTA3VDIwOjI5OjQ5KzAwOjAwZWpnkAAAACV0RVh0ZGF0ZTptb2RpZnkAMjAyMS0wMS0wN1QyMDoyOTo0OSswMDowMBQ33ywAAAAASUVORK5CYII='

img_06 = 'iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAMAAAC6V+0/AAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAAAOpgAAA6mAAAF3CculE8AAAAflBMVEUAAABEREBDQz9OTkmMjIQMDAxCQj5zc20CAgIBAQEAAAAAAAAAAAB0dG0EBAQBAQEAAAADAwIAAAAAAABNTUkAAAAAAAAAAAADAwMBAQEAAAABAQADAwMBAQEAAACHh38GBgUAAAANDQwBAQEAAAAAAAAAAABycmsAAAD///+demq5AAAAKHRSTlMAAQEBAQYBASVlmbGYARV/3yK0tQHkt/sek/6TGpGSARCRBpK2/OMBwWijIwAAAAFiS0dEKcq3hSQAAAAJcEhZcwAACxMAAAsTAQCanBgAAAAHdElNRQflAQcUHgGSgzV9AAAAzUlEQVQY022Riw6CMAxFrzw3eUxeQxEEQWX//4W2U8w0NlnSnWXt7S12FJ4PBGEYAL7Hd9CJEAu5T5JUigzRC0bI1cHYOKicKYgVpflEVRCFh9xhRHNCfqzMV6isBgTXa3RrTKsbrisASH7Wx1PXnY+ac0n69py0p34Y+kvLeToiTGylbpima2fTZHbh8IFBar+f++vSL9v3rdGFG93ejRxJd/14S/KzX/FrzWNWLit5TDbEoaU15L91TDMhU2vyuplM6yBfxnkmfbVdxxOebyOyOvpEKQAAACV0RVh0ZGF0ZTpjcmVhdGUAMjAyMS0wMS0wN1QyMDoyOTo0OSswMDowMGVqZ5AAAAAldEVYdGRhdGU6bW9kaWZ5ADIwMjEtMDEtMDdUMjA6Mjk6NDkrMDA6MDAUN98sAAAAAElFTkSuQmCC'

#sound_wave_img = PhotoImage(file='Desktop/mp3/buttons/20x20/65-651653_soundwave-sound-wave-free-png.png')
sound_wave_img = PhotoImage(data=base64.b64decode(img_01))
#open_file_img = PhotoImage(file='Desktop/mp3/buttons/20x20/folder_documents_media_browse-512.png')
open_file_img = PhotoImage(data=base64.b64decode(img_02))
#paused_img = PhotoImage(file='Desktop/mp3/buttons/20x20/pause_media_music_player-512.png')
paused_img = PhotoImage(data=base64.b64decode(img_03))
#stopped_img = PhotoImage(file='Desktop/mp3/buttons/20x20/stop_music_media_player-512.png')
stopped_img = PhotoImage(data=base64.b64decode(img_04))
#adding_music_img = PhotoImage(file='Desktop/mp3/buttons/20x20/add_plus_media-512.png')
adding_music_img = PhotoImage(data=base64.b64decode(img_05))
#deleting_music_img = PhotoImage(file='Desktop/mp3/buttons/20x20/close_exit_media_player-512.png')
deleting_music_img = PhotoImage(data=base64.b64decode(img_06))

#Control Buttons Frame
controle_frame = Frame(janela)
controle_frame.pack()

play_button = Button(controle_frame, image=play_bt_img, bd=0, command=lambda: play(playing))
pause_button = Button(controle_frame, image=pause_bt_img, bd=0, command=lambda: pause(paused))
stop_button = Button(controle_frame, image=stop_bt_img, bd=0, command=stop)
prox_button = Button(controle_frame, image=prox_bt_img, bd=0, command=next_song)
ante_button = Button(controle_frame, image=ante_bt_img, bd=0, command=previous_song)

add_button = Button(controle_frame, image=add_bt_img, bd=0, command=add_song)
del_button = Button(controle_frame, image=del_bt_img, bd=0, command=remove_song)
repeat_button = Button(controle_frame, image=rep_bt_img, bd=0, command=lambda: repeat_music(re_music))
repeat_1_button = Button(controle_frame, image=rep1_bt_img, bd=0, command=lambda: repeat_1_music(repeat))
randon_button = Button(controle_frame, image=rand_bt_img, bd=0, command=lambda: randon(rand))

ante_button.grid(row=0, column=0, padx=5)
play_button.grid(row=0, column=1, padx=5)
pause_button.grid(row=0, column=2, padx=5)
stop_button.grid(row=0, column=3, padx=5)
prox_button.grid(row=0, column=4, padx=5)

add_button.grid(row=1, column=0, padx=5)
del_button.grid(row=1, column=1, padx=5)
repeat_button.grid(row=1, column=2, padx=5)
repeat_1_button.grid(row=1, column=3, padx=5)
randon_button.grid(row=1, column=4, padx=5)

#Janela menu
menu = Menu(janela)
janela.config(menu=menu)

fileMenu = Menu(menu, tearoff=0)
menu.add_cascade(label='Arquivo', menu=fileMenu)
fileMenu.add_command(label='Abrir arquivo', command=add_song)
fileMenu.add_command(label='Abrir arquivos', command=add_songs)
fileMenu.add_command(label='Abrir diretório', command=open_directory)
fileMenu.add_separator()
fileMenu.add_command(label='Remover música', command=remove_song)
fileMenu.add_command(label='Remover todas as música', command=remove_all_songs)
fileMenu.add_separator()
fileMenu.add_command(label='Sair', command=janela.quit)

playbakMenu = Menu(menu, tearoff=0)
menu.add_cascade(label='Reproduzir', menu=playbakMenu)
aprsubMenu = Menu(playbakMenu, tearoff=0)
playbakMenu.add_cascade(label='Após reprodução', menu=aprsubMenu)
aprsubMenu.add_command(label='Não fazer nada', command=music_none)
aprsubMenu.add_command(label='Reproduzir a próxima música', command=menu_next_song)
aprsubMenu.add_command(label='Fechar programa', command=exit_song)

helpMenu = Menu(menu, tearoff=0)
menu.add_cascade(label='Ajuda', menu=helpMenu)
helpMenu.add_command(label='Instruções', command=instrucao)

song_status_frame = Frame(janela, bd=1, relief=GROOVE)
song_status_frame.pack(fill=X, side=BOTTOM, ipady=2)

#Song Status Bar
song_wave = Label(song_status_frame, image=open_file_img, anchor=W)
song_wave.pack(side=LEFT)
song_status = Label(song_status_frame, text='Abrindo arquivo', anchor=W)
song_status.pack(side=LEFT)

status_bar = Label(song_status_frame, text='', anchor=E)
status_bar.pack(side=RIGHT)

#Time / Song length
#status_bar = Label(janela, text='', bd=1, relief=GROOVE, anchor=E)
#status_bar.pack(fill=X, side=BOTTOM, ipady=2)

#Divisoria
separar_01 = Label(controle_frame, text='')
separar_01.grid(row=0, column=5, padx=20)

#Volume Control
volume_button = Button(controle_frame, image=vol2, bd=0, command=lambda: mute(muted))
volume_button.grid(row=0, column=6, padx=5)

volume_slider = ttk.Scale(controle_frame, from_=0, to=1, orient=HORIZONTAL, value=0.5, command=volume, length=50)
volume_slider.grid(row=0, column=7, pady=5)

janela.mainloop()