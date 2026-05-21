import numpy as np
import matplotlib.pyplot as plt

def compute_volume_per_muscle_group(rows):
    chest = 0
    biceps = 0
    triceps = 0
    shoulders = 0
    back = 0
    legs = 0
    abss = 0
    other = 0
    for r in rows:
        if r[0].startswith("chest"):
            chest += (float(r[1]) * float(r[2]))
        elif r[0].startswith("bicep"):
            biceps += (float(r[1]) * float(r[2]))
        elif r[0].startswith("tricep"):
            triceps += (float(r[1]) * float(r[2]))
        elif r[0].startswith("shoulder"):
            shoulders += (float(r[1]) * float(r[2]))
        elif r[0].startswith("lat"):
            back += (float(r[1]) * float(r[2]))
        elif r[0].startswith("back"):
            back += (float(r[1]) * float(r[2]))
        elif r[0].startswith("row"):
            back += (float(r[1]) * float(r[2]))
        elif r[0].startswith("abs"):
            abss += (float(r[1]) * float(r[2]))
        elif r[0].startswith("squat"):
            legs += (float(r[1]) * float(r[2]))
        elif r[0].startswith("leg"):
            legs += (float(r[1]) * float(r[2]))
        elif r[0].startswith("pushup"):
            vol = (float(r[1]) * float(r[2]))
            # idk I am completely inventing these numbers, but they sound ok
            chest += vol * .75
            triceps += vol * .25
            abss += vol * .25
        else:
            other += (float(r[1]) * float(r[2]))

    return (["chest", "biceps", "triceps", "shoulders", "back", "legs", "abs", "other"], [chest, biceps, triceps,shoulders,back,legs,abss,other])


def make_star_plot (categories, values):
    if len(categories) == len(values):
        # Convert category indices to angles
        num_vars = len(categories)
        angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

        # Close the chart (connect the last point to the first)
        values += values[:1]
        angles += angles[:1]

        # Create the figure
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw={'projection': 'polar'})

        # Plot the data
        ax.fill(angles, values, color='salmon', alpha=0.4)  # Fill area
        ax.plot(angles, values, color='red', linewidth=2)  # Outline

        # Add category labels
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)

        # Customize grid and labels
        ax.set_yticklabels([])  # Remove y-axis labels
        ax.set_title("Volume Distribution by Muscle Group", fontsize=14)

        # Show the radar chart
        plt.savefig("plot.png")
    else:
        print("ERROR LOG: wrong input to plot function")
