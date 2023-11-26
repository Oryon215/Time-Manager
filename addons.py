
def overlaping_ranges(range1: tuple[int], range2: tuple[int]):
    f_in = lambda a, b, c: a < c < b
    for number1 in range1:
        if f_in(range2[0], range2[1], number1):
            return True
    for number2 in range2:
        if f_in(range1[0], range1[1], number2):
            return True
    return False

def validate_deadline(new_value):
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


def parse_schedule(schedule: str):
    events = schedule.split("\n")
    schedule_lst = []
    for event in events[:-2]:  # dont include /n
        data = event.split(",")
        print("data:",data)
        hour, name = ":".join(data[0].split(":")[0:2]), data[0].split(":")[2]
        type_event = data[1].split(":")[1]
        deadline = data[2].split(":")[1]
        description = data[3]
        time = data[4]

        event_data = {"hour": hour, "name": name, "type": type_event, "deadline": deadline, "description": description, "time": time}

        schedule_lst.append(event_data)
    return schedule_lst