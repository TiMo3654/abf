import random
from matplotlib import pyplot as plt, patches

# Test functions

def generate_participant() -> dict:

    xmin        = random.randint(1,100)
    ymin        = random.randint(1,100)

    width       = random.randint(1,20)
    height      = random.randint(1,20)


    participant = {
        "xmin":         xmin,
        "ymin":         ymin,
        "width":        width,
        "height":      height,
        "clashes":      {},
        "aversions":    {},
        "inference":    0,
        "connections":  {},
        "turmoil":      0,
        "wounds":       []
    }

    return participant


def plot_participants(participants):

    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True

    figure, ax = plt.subplots(1)
    ax.plot([0], c='white')

    for key in participants:

        p = participants[key]

        origin = (p['xmin'], p['ymin'])

        rectangle = patches.Rectangle(origin, p['width'], p['height'], edgecolor='orange',
        facecolor="green", linewidth=1)

        ax.add_patch(rectangle)

    plt.grid()
    plt.show()

    return 0
