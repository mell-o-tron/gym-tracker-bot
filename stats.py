import numpy as np
import matplotlib.pyplot as plt
import datetime

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

def compute_n_ex_per_muscle_group(rows):
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
            chest += 1
        elif r[0].startswith("bicep"):
            biceps += 1
        elif r[0].startswith("tricep"):
            triceps += 1
        elif r[0].startswith("shoulder"):
            shoulders += 1
        elif r[0].startswith("lat"):
            back += 1
        elif r[0].startswith("back"):
            back += 1
        elif r[0].startswith("row"):
            back += 1
        elif r[0].startswith("abs"):
            abss += 1
        elif r[0].startswith("squat"):
            legs += 1
        elif r[0].startswith("leg"):
            legs += 1
        elif r[0].startswith("pushup"):
            vol = 1
            # idk I am completely inventing these numbers, but they sound ok
            chest += vol * .75
            triceps += vol * .25
            abss += vol * .25
        else:
            other += 1

    return (["chest", "biceps", "triceps", "shoulders", "back", "legs", "abs", "other"], [chest, biceps, triceps,shoulders,back,legs,abss,other])


def is_in_current_week(dt):
    today = datetime.datetime.now()

    # Get the start of the current week (Monday at midnight)
    start_of_week = today.replace(hour=0, minute=0, second=0, microsecond=0) - datetime.timedelta(days=today.weekday())

    # Get the end of the current week (Monday at midnight of next week)
    end_of_week = start_of_week + datetime.timedelta(days=7)

    # Check if dt is within this range
    return start_of_week <= dt < end_of_week


def compute_volume_per_muscle_group_week(rows):
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
            chest += (float(r[1]) * float(r[2])) if is_in_current_week(datetime.datetime.strptime(r[3], "%Y-%m-%d %H:%M:%S.%f")) else 0
        elif r[0].startswith("bicep"):
            biceps += (float(r[1]) * float(r[2])) if is_in_current_week(datetime.datetime.strptime(r[3], "%Y-%m-%d %H:%M:%S.%f")) else 0
        elif r[0].startswith("tricep"):
            triceps += (float(r[1]) * float(r[2])) if is_in_current_week(datetime.datetime.strptime(r[3], "%Y-%m-%d %H:%M:%S.%f")) else 0
        elif r[0].startswith("shoulder"):
            shoulders += (float(r[1]) * float(r[2])) if is_in_current_week(datetime.datetime.strptime(r[3], "%Y-%m-%d %H:%M:%S.%f")) else 0
        elif r[0].startswith("lat"):
            back += (float(r[1]) * float(r[2])) if is_in_current_week(datetime.datetime.strptime(r[3], "%Y-%m-%d %H:%M:%S.%f")) else 0
        elif r[0].startswith("back"):
            back += (float(r[1]) * float(r[2])) if is_in_current_week(datetime.datetime.strptime(r[3], "%Y-%m-%d %H:%M:%S.%f")) else 0
        elif r[0].startswith("row"):
            back += (float(r[1]) * float(r[2])) if is_in_current_week(datetime.datetime.strptime(r[3], "%Y-%m-%d %H:%M:%S.%f")) else 0
        elif r[0].startswith("abs"):
            abss += (float(r[1]) * float(r[2])) if is_in_current_week(datetime.datetime.strptime(r[3], "%Y-%m-%d %H:%M:%S.%f")) else 0
        elif r[0].startswith("squat"):
            legs += (float(r[1]) * float(r[2])) if is_in_current_week(datetime.datetime.strptime(r[3], "%Y-%m-%d %H:%M:%S.%f")) else 0
        elif r[0].startswith("leg"):
            legs += (float(r[1]) * float(r[2])) if is_in_current_week(datetime.datetime.strptime(r[3], "%Y-%m-%d %H:%M:%S.%f")) else 0
        elif r[0].startswith("pushup"):
            vol = (float(r[1]) * float(r[2])) if is_in_current_week(datetime.datetime.strptime(r[3], "%Y-%m-%d %H:%M:%S.%f")) else 0
            # idk I am completely inventing these numbers, but they sound ok
            chest += vol * .75
            triceps += vol * .25
            abss += vol * .25
        else:
            other += (float(r[1]) * float(r[2])) if is_in_current_week(datetime.datetime.strptime(r[3], "%Y-%m-%d %H:%M:%S.%f")) else 0

    return (["chest", "biceps", "triceps", "shoulders", "back", "legs", "abs", "other"], [chest, biceps, triceps,shoulders,back,legs,abss,other])

def compute_avg_volume_per_exercise(rows):
    total_volume    = compute_volume_per_muscle_group(rows)
    n_exercises     = compute_n_ex_per_muscle_group(rows)
    biceps          = (total_volume[1][1] / n_exercises[1][1]) if (n_exercises[1][0] != 0) else 0
    chest           = (total_volume[1][0] / n_exercises[1][0]) if (n_exercises[1][1] != 0) else 0
    triceps         = (total_volume[1][2] / n_exercises[1][2]) if (n_exercises[1][2] != 0) else 0
    shoulders       = (total_volume[1][3] / n_exercises[1][3]) if (n_exercises[1][3] != 0) else 0
    back            = (total_volume[1][4] / n_exercises[1][4]) if (n_exercises[1][4] != 0) else 0
    legs            = (total_volume[1][5] / n_exercises[1][5]) if (n_exercises[1][5] != 0) else 0
    abss            = (total_volume[1][6] / n_exercises[1][6]) if (n_exercises[1][6] != 0) else 0
    other           = (total_volume[1][7] / n_exercises[1][7]) if (n_exercises[1][7] != 0) else 0

    return (["chest", "biceps", "triceps", "shoulders", "back", "legs", "abs", "other"], [chest, biceps, triceps,shoulders,back,legs,abss,other])

def compute_target_volume(rows):
    target_weekly_sets_per_mg = [14, 6, 6, 8, 14, 10, 6, 0]
    avg_vol = compute_avg_volume_per_exercise(rows)

    target_vol = [
        target_weekly_sets_per_mg[0] * avg_vol[1][0],
        target_weekly_sets_per_mg[1] * avg_vol[1][1],
        target_weekly_sets_per_mg[2] * avg_vol[1][2],
        target_weekly_sets_per_mg[3] * avg_vol[1][3],
        target_weekly_sets_per_mg[4] * avg_vol[1][4],
        target_weekly_sets_per_mg[5] * avg_vol[1][5],
        target_weekly_sets_per_mg[6] * avg_vol[1][6],
        target_weekly_sets_per_mg[7] * avg_vol[1][7]
        ]

    return (["chest", "biceps", "triceps", "shoulders", "back", "legs", "abs", "other"], target_vol)


def make_target_plot (categories, values, targets):
    done_remaining = {
        'Done': np.array(values),
        'Remaining': np.maximum(np.array(targets) - np.array(values), 0),
    }
    width = 0.6


    fig, ax = plt.subplots()
    bottom = np.zeros(len(categories))

    for done, remaining in done_remaining.items():
        p = ax.bar(categories, remaining, width, label=done, bottom=bottom)
        bottom += remaining

        ax.bar_label(p, label_type='center')

    ax.set_title('Weekly target volume')
    ax.legend()

    plt.savefig("plot.png")

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


