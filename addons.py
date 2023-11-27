def type_to_int(t:str):
    match t:
        case "Imporant and Urgent":
            return 3
        case "Urgent":
            return 2
        case "Important":
            return 1
        case "Leisure":
            return 0
    return -1



def overlaping_ranges(range1: tuple[int, int], range2: tuple[int, int]):
    # Check if a new session hour range overlaps a previous session hour range
    f_in = lambda a, b, c: a < c < b
    for number1 in range1:
        if f_in(range2[0], range2[1], number1):
            return True
    for number2 in range2:
        if f_in(range1[0], range1[1], number2):
            return True
    return False


def validate_deadline(new_value):
    # Make sure that the date given is valid
    import datetime
    # Check if the new value has a length less than or equal to 8
    if len(new_value) <= 10 and (len(new_value) < 6 or (new_value[2] == '\\' and new_value[5] == '\\')):
        if len(new_value) == 8:
            comps = new_value.split("\\")
            day_in_range = 1 <= int(comps[0]) <= 31
            month_in_range = 1 <= int(comps[1]) <= 12
            return day_in_range and month_in_range
        return True
    return False


def validate_session(hour_range):
    separator = ":"
    # Make sure that the session given is valid
    if len(hour_range) > 2:
        if hour_range[2] != separator:
            return False
    if len(hour_range) > 4:
        start_hour = hour_range[:2]
        finish_hour = hour_range[3:]
        if not (start_hour.isnumeric() or finish_hour.isnumeric()):
            return False
        start_hour = int(start_hour)
        finish_hour = int(finish_hour)
        if not (0 < start_hour < 23 or 0 < finish_hour < 23):
            return False
        if start_hour > finish_hour:
            return False
    return True


def parse_schedule(schedule: str):
    """

    :param schedule: a string representing the schedule after it has been created by the exe
    :return: a lst of dictionaries representing events
    """
    events = schedule.split("\n")
    schedule_lst = []
    for event in events[:-2]:  # dont include /n
        event_data = parse_event(event)

        schedule_lst.append(event_data)
    return schedule_lst


def parse_event(event: str) -> dict:
    data = event.split(",")
    hour, name = ":".join(data[0].split(":")[0:2]), data[0].split(":")[2]
    type_event = data[1].split(":")[1]
    deadline = data[2].split(":")[1]
    description = data[3]
    time = str(int(data[4]) / 60)

    event_data = {"hour": hour, "name": name, "type": type_event, "deadline": deadline, "description": description,
                  "time": time}
    return event_data


def write_dictionary(dic: dict, path: str):
    # write dictionary to file in path
    with open(path, "w") as fd:
        s = ''
        for key in dic.keys():
            s += f"{key}\n"
            s += str(dic[key])
            s += "\n"
        fd.write(s)


def reset_event_lst(events: str, current_events: dict):
    print(events)
    print(current_events)
    new_events = dict()
    for key in current_events.keys():
        new_events[key] = ''
    lines = events.split("\n")
    lines = filter(lambda x: x != '', lines)
    prev = ''
    for line in lines:
        if line[:-1] in current_events.keys(): # dont include the ":" in the original text
            prev = line[:-1]
        elif prev in current_events.keys():
            line_fixed = "00:00:" + line
            event_dict = parse_event(line_fixed)
            simple_str = f"{event_dict["name"]} {event_dict["description"]} {event_dict["deadline"]} {event_dict["time"]}"
            new_events[prev] +=  simple_str
    print(new_events)
    return new_events










