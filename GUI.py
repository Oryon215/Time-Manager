from tkinter import *
import tkinter as tk
from addons import *

# GLOBALS
root = Tk()
main_frame = None
type_events = {"Important and Urgent": r"Gama lol 26\11\2023 3", "Urgent": r"", "Important": r"", "Leisure": r""}
free_sessions = "2 8\\2 11"
settings = {"Frequency": 24, "break length": 30}


def back_button(frame):
    # a general pattern for creating the backward button
    frame.forget()
    start_main()
# done


# add events frame
def start_type_windows():
    global main_frame
    global root
    global type_events

    f = Frame(root, bg="light green", height=600, width=520)
    lst = Listbox(f, selectmode="single", width=20, height=8)

    for t in type_events:
        lst.insert(END, t)
    lst.place(x=60, y=10)
    label_for_events = Label(f, width=17, height=5)
    label_for_events.place(x=60, y=85)

    def lst_box(interrrupt):
        i = lst.curselection()
        print(lst.get(i))
        label_for_events.config(text=type_events[lst.get(i)].replace("$", "\n"), anchor="center")

    lst.bind("<<ListboxSelect>>", lst_box)

    back = Button(f, text="back", command=lambda: back_button(f))
    back.place(x=10, y=290)

    event_params = ["name", "description", "deadline", "time"]
    event_entries = []

    x = 60
    y = 170

    for param in event_params:
        param_label = Label(f, text=param, height=1, width=8)
        param_label.place(x=x, y=y)
        e1 = Entry(f)
        if param == "deadline":
            e1 = Entry(f, validate="key", validatecommand=(root.register(validate_deadline), '%P'))
            # %P - the value that the text will have if allowed
            # "KEY" - validate whenever a keystroke changes the widget's contents
            e1.insert(0, "11\\11\\1111")  # Default value
        e1.place(x=x + 70, y=y)
        event_entries.append(e1)
        y += 20

    def save_button():
        string = ""
        for entry in event_entries:
            string += entry.get() + " "
        count_dollar = 0 if len(type_events[lst.get(ACTIVE)]) == 0 else 1  # Count how many separators are necessary
        type_events[lst.get(ACTIVE)] += "$ " * count_dollar + string[:-1]

        lst_box(0)  # 0 is not an important value

    save = Button(f, text="save", command=save_button)
    save.place(x=126, y=260)

    f.pack()
    main_frame.forget()
# done


# add session frame
def session_button():
    global main_frame
    global root
    global free_sessions

    f = Frame(root, bg="orange", height=600, width=520)
    mylist = Listbox(f)

    def print_lst():
        global free_sessions
        mylist.delete(0, END)
        for session in free_sessions.split("\\"):
            components = session.split(" ")
            start_hour = components[1]
            finish_hour = int(components[0]) + int(components[1])
            mylist.insert(END, f"{start_hour}:{finish_hour}")
    print_lst()

    mylist.place(x=80, y=10)
    new_session_entry = Entry(f, validate="key", validatecommand=(root.register(validate_session), '%P'))
    new_session_entry.insert(0, "00:00")
    new_session_entry.place(x=80, y=150)

    back = Button(f, text="back", command=lambda: back_button(f))
    back.place(x=10, y=290)

    def save_button():
        global free_sessions
        text = new_session_entry.get()
        hours = text.split(":")
        start_hour = int(hours[0])
        end_hour = int(hours[1])
        length_session = int(end_hour) - int(start_hour)

        sessions = free_sessions.split("\\")
        for i in range(len(sessions)):
            components = sessions[i].split(" ")
            length_old = int(components[0])
            start_hour_old = int(components[1])
            end_hour_old = start_hour_old + length_old

            if start_hour_old > start_hour:
                if not overlaping_ranges((start_hour_old, end_hour_old), (start_hour, end_hour)):
                    sessions.insert(i, f"{length_session} {start_hour}")
                    free_sessions = "\\".join(sessions)
                    print_lst()
                    new_session_entry.delete(0, END)
                    return
        if not overlaping_ranges((start_hour, end_hour), (int(components[1]), int(components[1]) + int(components[0]))):
            sessions.append(f"{length_session} {start_hour}")
        free_sessions = "\\".join(sessions)
        new_session_entry.delete(0, END)
        print_lst()

    save = Button(f, bg="gray", text="add", command=save_button)
    save.place(x=80, y=180)

    f.pack()
    main_frame.forget()
# make sure last range doesn't overlap with new one


# start menu frame
def start_main():
    global main_frame
    global root
    main_frame = Frame(root, bg="light blue", height=600, width=520)
    buttons = {"add events": start_type_windows, "add free sessions": session_button, "schedule": schedule_day,
               "settings": setting_button}

    # set initial starting position
    x = 10
    y = 10

    for button_text in buttons.keys():
        button_function = buttons[button_text]
        button = Button(main_frame, text=button_text, height=2, width=30, bg="light gray", command=button_function)
        button.place(x=x, y=y)
        y += 60

    main_frame.pack()
# done


# schedule option frame
def schedule_day():
    global settings
    global main_frame
    global root
    global type_events
    global free_sessions
    import subprocess

    listevents = ""
    importance = 3
    for t in type_events.keys():
        st = type_events[t]
        if st != "":
            st = st.replace("$", f"${importance}")
            listevents += f"${importance} " + st
            importance -= 1
    listevents += "$"
    text = subprocess.run(["TimeManagementSource.exe", "", listevents, free_sessions], capture_output=True, text=True)
    return_value = text.stdout.split("-") # split into actual schedule and left events
    schedule_data = parse_schedule(return_value[0])
    if len(return_value) > 1:
        type_events = reset_event_lst(return_value[1], type_events) # reset events based on what has been finished

    f = Frame(root, bg="light blue", height=1000, width=1000)
    header = ["Time", "Event", "Type", "Deadline", "Duration"]
    for i in range(len(header)):
        Label(f, text=header[i], font=("Helvetica", 10, "bold")).grid(row=0, column=i, padx=5, pady=5)
        # set table labels

    for row in range(1, len(schedule_data) + 1):
        data = schedule_data[row - 1]
        Label(f, text=data["hour"]).grid(row=row, column=0, padx=5, pady=5)
        Label(f, text=data["name"]).grid(row=row, column=1, padx=5, pady=5)
        Label(f, text=data["type"]).grid(row=row, column=2, padx=5, pady=5)
        Label(f, text=data["deadline"]).grid(row=row, column=3, padx=5, pady=5)
        Label(f, text=str(data["time"])).grid(row=row, column=4, padx=5, pady=5)

    back = Button(f, text="back", command=lambda: back_button(f))
    back.place(x=0, y=290)
    f.pack()
    main_frame.forget()
# done

# settings option
def setting_button():
    global main_frame
    global settings

    f = Frame(root, bg="gray", height=600, width=520)
    y = 10
    entry_widgets = []
    for setting in settings.keys():
        setting_label = Label(f, text=f"{setting}:")
        setting_label.place(x=10, y=y)
        e = Entry(f, width=2)
        entry_widgets.append((setting, e))
        e.insert(0, f"{settings[setting]}")
        e.place(x=90, y=y)
        y += 40

    def save_button():
        for entry in entry_widgets:
            settings[entry[0]] = entry[1].get()

    save = Button(f, bg="orange", text="save", command=save_button)
    save .place(x=10, y=y)

    back = Button(f, text="back", command=lambda: back_button(f))
    back.place(x=10, y=290)

    f.pack()
    main_frame.forget()
# done - but make sure to add implementation of settings to exe and schedule day


def main():
    global free_sessions
    global settings

    root.title("Time Manager")
    root.geometry("300x360")
    root.configure(bg="light blue")

    with open("./save_files/settings.txt", "r") as fd:
        lines = fd.readline()
        prev = ''
        for line in lines:
            if prev in settings.keys():
                settings[prev] = int(line)
            prev = line
    free_sessions = open("./save_files/sessions.txt", "r").read()

    with open("./save_files/events.txt") as fd:
        lines = fd.readlines()
        prev = ''
        for line in lines:
            if prev[:-1] in list(type_events.keys()):
                type_events[prev[:-1]] = line[:-1]
            prev = line

    start_main()
    tk.mainloop()
    # save info to files
    write_dictionary(settings, r"./save_files/settings.txt")
    with open("./save_files/sessions.txt", "w") as fd:
        fd.write(free_sessions)
    write_dictionary(type_events, r"./save_files/events.txt")
