'''
This function assumes no merges are allowed, only breaks
'''

from math import gcd
import numpy as np
from chocolate import factoring


# returns a dictionary with dimensions of one-break approximations of desired area for each dimension
def approximateOneBreaks(width, height, desired_area):
    return {
        "width_preserving_break-width": width,
        "width_preserving_break-height": (desired_area // width),
        "height_preserving_break-width": (desired_area // height),
        "height_preserving_break-height": height
    }

# PRECONDITION: The width w and height h are whole numbers
#			    representing the dimensions of the given chocolate bar
# PRECONDITION: The desired area, m, is a whole number such that m <= w*h
def breakBar(w, h, desired_area, sequence, spaceLeft=1):
    # If no space left in collection, stop
    if (spaceLeft == 0):
        return -1

    # Redefined for simplicity in code
    m = desired_area

    # Check that preconditions are met
    if (min(m, w, h) < 1 or m > w * h):
        sequence.append("Now wait a minute, that's not possible!")
        sequence.append("I'm a bot, not a miracle worker!")
        return -1

    # ---Sa(Solvable immediately?): Zero breaks are needed
    # Check if m equals the area of the original chocolate bar!
    # This checks for a zero-break case
    if m == w * h:
        sequence.append("No breaks needed to obtain the desired area of {} from a {}-by-{} piece of chocolate".format(m, w, h))
        return 0

    sequence.append("We are now breaking up a {}-by-{} chocolate bar to obtain the desired area of {}".format(w, h, m))

    # Check if m can be achieved by splitting chocolate bar in two
    # This checks for a one-break case
    if m % w == 0:
        sequence.append("The desired area of {} can be obtained by breaking off a {}-by-{} piece from the bottom".format(m, w, m // w))
        return 1

    if m % h == 0:
        sequence.append("The desired area of {} can be obtained by breaking off a {}-by-{} piece from the left side".format(m, h, m // h))
        return 1
    if m % h == 0:
        return 1

    # If the chocolate bar cannot be split once to yield desired area
    # We must make two consecutive breaks to yield a rectangle with the desired area

    # Find factors of m that fit in given chocolate bar
    factors_list = [(m_1, m_2) for (m_1, m_2) in factoring.factorPairs(m) if
                    (max(m_1, m_2) <= max(w, h)) and (min(m_1, m_2) <= min(w, h))]

    # DIVIDE-AND-CONQUER occurs here
    # No valid factor pairs could be found, so we must divide-and-conquer
    if len(factors_list) == 0:
        breakConstants = approximateOneBreaks(w, h, m)
        new_width = breakConstants["height_preserving_break-width"]
        new_height = breakConstants["width_preserving_break-height"]

        # ---Sb1: Remove a rectangular piece along the width
        # Determine number of breaks needed if we first do a width-preserving one-break
        width_sequence = ["We are breaking off a {}-by-{} piece of chocolate from the bottom".format(w, new_height)]
        width_sequence.append("The remaining desired area is thus reduced to {}".format(m - (w * new_height)))
        subproblem_width = breakBar(w,h - new_height, m - (w * new_height), width_sequence, spaceLeft-1)
        width_preserving_breaks = 1 + subproblem_width

        # ---Sb2: Remove a rectangular piece along the height
        # Determine number of breaks needed if we first do a height-preserving one-break
        height_sequence = ["We are breaking off a {}-by-{} piece of chocolate from the left".format(new_width, h)]
        height_sequence.append("The remaining desired area is thus reduced to {}".format(m - (new_width * h)))
        subproblem_height = breakBar(w - new_width, h, m - (new_width * h), height_sequence, spaceLeft - 1)
        height_preserving_breaks = 1 + subproblem_height

        # This occurs if neither one-break yields a valid solution
        if (width_preserving_breaks == 0) and (height_preserving_breaks == 0):
            sequence.append("Oh dear, this is simply not possible!")
            return -1
        # Append the sequence with fewer steps
        elif (width_preserving_breaks < height_preserving_breaks):
            sequence += width_sequence
        else:
            sequence += height_sequence

        return min(width_preserving_breaks, height_preserving_breaks)

    # if there exists a pair of factors of m that fit in the chocolate bar
    # make two breaks and you're done!
    sequence.append("The desired area {} can be obtained by breaking off a {}-by-{} piece of chocolate with two breaks".format(m, factors_list[0][0],factors_list[0][1]))
    return 2

# return number of breaks


# POSTCONDITION: Return a whole number representing the minimum number
# of breaks needed to obtain desired area from the original chocolate bar, if possible
# POSTCONDITION: Return a list with the steps needs to obtain desired area,
# or state if it is impossible (for ReMBot to display)


if __name__ == "__main__":
    seq = []
    numBreaks = breakBar(8, 5, 13, seq, 2)
    for s in seq:
        print(s)