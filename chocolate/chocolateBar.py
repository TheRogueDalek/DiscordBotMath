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
def breakBar(width, height, desired_area, spaceLeft=1):
    # If no space left in collection, stop
    if (spaceLeft == 0):
        return -1

    # Redefined for simplicity in code
    w = width
    h = height
    m = desired_area

    # Check that preconditions are met
    if (min(m, w, h) < 1 or m > w * h):
        return -1

    # Check if m equals the area of the original chocolate bar!
    # This checks for a zero-break case
    if m == w * h:
        return 0

    # Check if m can be achieved by splitting chocolate bar in two
    # This checks for a one-break case
    if m % w == 0:
        return 1
    if m % h == 0:
        return 1

    # If the chocolate bar cannot be split once to yield desired area
    # We must make two consecutive breaks to yield a rectangle with the desired area

    # Find factors of m that fit in given chocolate bar
    factors_list = [(m_1, m_2) for (m_1, m_2) in factoring.factorPairs(m) if
                    (max(m_1, m_2) <= max(w, h)) and (min(m_1, m_2) <= min(w, h))]
    print(factors_list)  # DEBUG

    # DIVIDE-AND-CONQUER occurs here

    # No valid factor pairs could be found, so we must divide-and-conquer
    if len(factors_list) == 0:
        breakConstants = approximateOneBreaks(w, h, m)
        print(breakConstants)
        new_width = breakConstants["height_preserving_break-width"]
        new_height = breakConstants["width_preserving_break-height"]

        # Determine number of breaks needed if we first do a width-preserving one-break
        subproblem_width = breakBar(w,h - new_height, m - (w * new_height), spaceLeft-1)
        width_preserving_breaks = 1 + subproblem_width

        # Determine number of breaks needed if we first do a height-preserving one-break
        subproblem_height = breakBar(w - new_width, h, m - (new_width * h), spaceLeft - 1)
        height_preserving_breaks = 1 + subproblem_height
        print(width_preserving_breaks, height_preserving_breaks)
        return min(width_preserving_breaks, height_preserving_breaks)

    # if there exists a pair of factors of m that fit in the chocolate bar
    # make two breaks and you're done!
    return 2

# return number of breaks


# POSTCONDITION: Return a whole number representing the minimum number 
# of breaks needed to obtain desired area from the original chocolate bar, OR...
# "IMPOSSIBLE" if the desired area cannot be obtained


if __name__ == "__main__":
    print("HI")
    print(breakBar(8, 3, 16, 2))
