from tkinter import *
import math

# ---------------------------- CONSTANTS ------------------------------- #
ORANGE = "#bd7700"
RED = "#a30303"
GREEN = "#457a12"
YELLOW = "#f7f5dd"
BROWN = "#522503"
FONT_NAME = "Courier"
TIMER_DEFAULT = "00:00"
STUDY_TEXT = "S T U D Y"
BREAK_TEXT = "B R E A K"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
click = 0
timer_track = 0
flag = False
start = False
timer = None

# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    global reps, timer_track, start, flag, click

    if start:
        window.after_cancel(timer)
        canvas.itemconfig(timer_text, text=TIMER_DEFAULT)
        title_label.config(text="POMODORO TIMER", fg=GREEN)
        check_mark.config(text="")
        reps = 0
        timer_track = 0
        flag = False
        start = False
        click = 0

# ---------------------------- PAUSE MECHANISM ------------------------------- #
def pause_timer():
    global click, flag, start
    click += 1

    if click % 2 == 0 and start:
        flag = False
        count_down(timer_track)
    else:
        flag = True

# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps, start
    start = True
    reps += 1

    work_time = WORK_MIN * 60
    short_break = SHORT_BREAK_MIN * 60 + 1
    long_break = LONG_BREAK_MIN * 60 + 1

    if reps == 1:
        title_label.config(text=STUDY_TEXT, fg=GREEN)
        count_down(work_time)
    elif reps % 8 == 0:
        title_label.config(text=BREAK_TEXT, fg=RED)
        count_down(long_break)
    elif reps % 2 == 0:
        title_label.config(text=BREAK_TEXT, fg=ORANGE)
        count_down(short_break)
    else:
        title_label.config(text=STUDY_TEXT, fg=GREEN)
        count_down(work_time + 1)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    global reps, timer, flag, timer_track
    count_min = math.floor(count / 60)
    count_secs = count % 60

    if count_secs < 10:
        count_secs = f"0{count_secs}"
    else:
        count_secs

    if count > 0 and not flag:
        timer = window.after(1000, count_down, count - 1)
    elif flag:
        timer_track = count
        return timer_track
    elif count == 0:
        add_check_mark = ""
        work_sessions = math.floor(reps/2)
        for _ in range(work_sessions):
            add_check_mark += "✓"
        check_mark.config(text=add_check_mark)
        count_secs = "00"
        start_timer()
    canvas.itemconfig(timer_text, text=f"{count_min}:{count_secs}")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)

title_label = Label(text="POMODORO TIMER", fg=GREEN, bg=YELLOW, font=(FONT_NAME, 33))
title_label.grid(column=1, row=0)

canvas = Canvas(width=290, height=270, bg=YELLOW, highlightthickness=0)
tomato_img = PhotoImage(file="tomato.png")
canvas.create_image(136, 135, image=tomato_img)
timer_text = canvas.create_text(136, 150, text=TIMER_DEFAULT, fill=BROWN, font=(FONT_NAME, 40, "bold"))
canvas.grid(column=1, row=1)

start_button = Button(text="Start", highlightthickness=0, command=start_timer)
start_button.grid(column=0, row=2)

pause_button = Button(text="Pause/Unpause", highlightthickness=0, command=pause_timer)
pause_button.grid(column=2, row=1)

reset_button = Button(text="Reset", highlightthickness=0, command=reset_timer)
reset_button.grid(column=2, row=2)

check_mark = Label(fg=GREEN, bg=YELLOW)
check_mark.grid(column=1, row=3)

window.mainloop()