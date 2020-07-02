# Intent: Sort a list of events by their end times
# Precondition 1: events is a non-empty list of 2-element tuples of floats
# Precondition 2: For each tuple (s,f) in events, 9 <= s < f <= 17,
#   where s and f refer to the start and end times of an event in 24-hr time
def sortByEndTime(events):
    if not (checkFormat(events)):
        return

    # TODO: Create sorting function from scratch, according to Dr. Braude (1 Jul 2020)
    events.sort(key=lambda x: x[1])


# INVARIANT: events_sorted contains the same tuples as events

# POSTCONDITION: events are sorted by their end time

# ==============================================================

# Checks that input list is a list of only tuples of floats/ints

def checkFormat(events):
    validity = [(isinstance(x, tuple)) and (len(x) == 2)
                and (isinstance(x[0], int) or isinstance(x[0], float))
                and (isinstance(x[1], int) or isinstance(x[1], float))
                for x in events]
    print(validity)
    return all(validity)

def parseStr(in_str):
    raw_list = in_str.split()
    processed_list = []
    try:
        processed_list = list(map(int, raw_list))
    except ValueError:
        return

    if len(processed_list) % 2 == 1:
        return

    events = []
    for i in range(0, len(processed_list), 2):
        events.append((processed_list[i], processed_list[i+1]))
    print(events)

# ==============================================================




if __name__ == '__main__':

    parseStr("1 2 3 4 5 8 5 8")

    print("===============")

    events = [(1, 2), (1.0, 2), (1.0, 2.0), (5,7), (4,6)]
    print(checkFormat(events))
    sortByEndTime(events)
    print(events)
