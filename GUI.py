from tkinter import *
import tkinter as tk
from addons import *

# GLOBALS
root = Tk()
main_frame = None
types = {"Important and Urgent":r"Gama lol 26\11\2023 3", "Urgent":r"", "Important":r"", "Leisure":r""}
free_sessions = "2 8\\2 11"
settings = {"Frequency": 24, "break length": 30}


# add events frame
def start_type_windows():
    global main_frame
    global root
    global types

    f = Frame(root, bg="light green", height=600, width=520)
    lst = Listbox(f, selectmode="single", width=20, height=8)
    for t in types:
        lst.insert(END, t)
    lst.place(x=60, y=10)
    l = Label(f, width=17, height=5)
    l.place(x=60, y=85)

    def lst_box(t):
        i = lst.curselection()
        l.config(text=types[lst.get(i)].replace("$", "\n"), anchor="center")
    lst.bind("<<ListboxSelect>>", lst_box)

    def back_button():
        f.forget()
        start_main()
    b = Button(f, text="back", command= lambda: back_button())
    b.place(x=10, y=290)

    event_params = ["name", "description", "deadline", "time"]
    event_entries = []

    x = 60
    y = 170

    for param in event_params:
        l1 = Label(f, text=param, height=1, width=8)
        l1.place(x=x, y=y)
        e1 = Entry(f, validate="key", validatecommand=(root.register(validate_deadline), '%P'))
        e1.place(x=x + 70, y=y)
        if param == "deadline":
            e1.insert(0, "11\\11\\1111")
        event_entries.append(e1)
        y += 20

    def save_button():
        string = ""
        for entry in event_entries:
            string += entry.get() + " "
        count_dollar = 0 if len(types[lst.get(ACTIVE)]) == 0 else 1
        types[lst.get(ACTIVE)] += "$ "*count_dollar + string[:-1]

        lst_box(0)  # 0 is not an important value
    b = Button(f, text="save", command=save_button)
    b.place(x=126, y=260)

    f.pack()
    main_frame.forget()


# add session frame
def session_button():
    global main_frame
    global root
    global free_sessions

    f = Frame(root, bg="orange", height=600, width=520)
    mylist = Listbox(f)
    for session in free_sessions.split("\\"):
        components = session.split(" ")
        mylist.insert(END, f"{components[1]}:{int(components[0]) + int(components[1])}")
    mylist.place(x = 80, y= 10)
    e1 = Entry(f)
    e1.insert(0, "00:00")
    e1.place(x=80, y=150)

    def back_button():
        f.forget()
        start_main()
    b = Button(f, text="back", command=back_button)
    b.place(x=10, y=290)

    def save_button():
        global free_sessions
        text = e1.get()
        if ":" in text:
            parts = text.split(":")
            length = int(parts[1]) - int(parts[0])
            length = str(length)
            start = str(int(parts[0]))
            components = free_sessions.split("\\")
            for i in range(len(components)):
                length2, start2 = components[i].split(" ")
                end2 = start2 + length2
                if not overlaping_ranges((start2, end2), (start, start+length)):

                    if int(start2) > int(start):
                        components.insert(i, f"{length} {start}")
                        free_sessions = "\\".join(components)
                        mylist.delete(0, END)
                        for session in free_sessions.split("\\"):
                            components = session.split(" ")
                            mylist.insert(END, f"{components[1]}:{int(components[0]) + int(components[1])}")
                        return
            components.append(f"{length} {start}")
            free_sessions = "\\".join(components)
            mylist.delete(0, END)
            for session in free_sessions.split("\\"):
                components = session.split(" ")
                mylist.insert(END, f"{components[1]}:{int(components[0]) + int(components[1])}")
    B = Button(f,bg="gray", text="add", command=save_button)
    B.place(x=80, y=180)

    f.pack()
    main_frame.forget()


# start menu frame
def start_main():
    global main_frame
    global root
    main_frame = Frame(root, bg="light blue", height=600, width=520)
    x = 10
    y = 10
    B1 = Button(main_frame, text="add events", height=2, width=30, bg="light gray", command= start_type_windows)
    B1.place(x=x, y=y)
    y += 60
    B2 = Button(main_frame, text="add free sessions", height=2, width=30, bg="light gray", command=session_button)
    B2.place(x=x, y=y)
    y += 60

    B3 = Button(main_frame, text="schedule", height=2, width=30, bg="light gray", command=schedule_day)
    B3.place(x=x, y=y)
    y += 60

    B4 = Button(main_frame, text="settings", height=2, width=30, bg="light gray", command=setting_button)
    B4.place(x=x, y=y)
    main_frame.pack()


# schedule option frame
def schedule_day():
    global settings
    global main_frame
    global root
    global types
    global free_sessions
    import subprocess

    listevents = ""
    importance = 3
    for t in types.keys():
        st = types[t]
        if st != "":
            st = st.replace("$", f"${importance}")
            listevents += f"${importance} " + st
            importance -= 1
    text = subprocess.run(["TimeManagementSource.exe", "", listevents, free_sessions], capture_output = True, text=True)

    f = Frame(root, bg="light blue", height=1000, width=1000)
    print(text.stderr)

    schedule_data = parse_schedule(text.stdout)

    header = ["Time", "Event", "Type", "Deadline", "Duration"]
    for i, text in enumerate(header):
        Label(f, text=text, font=("Helvetica", 10, "bold")).grid(row=0, column=i, padx=5, pady=5)
    for row, data in enumerate(schedule_data, start=1):
        tk.Label(f, text=data["hour"]).grid(row=row, column=0, padx=5, pady=5)
        tk.Label(f, text=data["name"]).grid(row=row, column=1, padx=5, pady=5)
        tk.Label(f, text=data["type"]).grid(row=row, column=2, padx=5, pady=5)
        tk.Label(f, text=data["deadline"]).grid(row=row, column=3, padx=5, pady=5)
        tk.Label(f, text=str(data["time"])).grid(row=row, column=4, padx=5, pady=5)
    f.pack()
    main_frame.forget()


    def back_button():
        f.forget()
        start_main()
    b = Button(f, text="back", command=back_button)
    b.place(x=0, y=290)
    f.pack()
    main_frame.forget()


# settings option
def setting_button():
    global main_frame
    global settings

    f = Frame(root, bg="gray", height =600, width=520)
    y = 10
    entry_widgets = []
    for setting in settings.keys():
        l = Label(f, text=f"{setting}:")
        l.place(x=10, y=y)
        e = Entry(f, width = 2)
        entry_widgets.append((setting, e))
        e.insert(0, f"{settings[setting]}")
        e.place(x=90, y=y)
        y += 40

    def save_button():
        for entry in entry_widgets:
            settings[entry[0]] = entry[1].get()
    B = Button(f,bg="orange", text="save", command=save_button)
    B.place(x=10, y=y)

    def back_button():
        f.forget()
        start_main()
    b = Button(f, text="back", command=back_button)
    b.place(x=10, y=290)

    f.pack()
    main_frame.forget()


def main():
    global free_sessions
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
            if prev[:-1] in list(types.keys()):
                types[prev[:-1]] = line[:-1]
            prev = line

    # Place initial buttons
    x = 20
    y = 10
    start_main()
    tk.mainloop()
    with open("./save_files/settings.txt", "w") as fd:
        s = ''
        for key in settings.keys():
            s += f"{key}\n"
            s += str(settings[key]) + "\n"
        fd.write(s)

    with open("./save_files/sessions.txt", "w") as fd:
        fd.write(free_sessions)

    with open("./save_files/events.txt", "w") as fd:
        s = ''
        for key in types.keys():
            s += f"{key}\n"
            s += types[key]
            s += "\n"
        fd.write(s)
