import time
import math
import random
import matplotlib.pyplot as plt

# constants
TRACK_LENGTH = 160
count = 0

# train variables
dest_pos = 70
train_pos = 0
v = 0

# PID
kp = 0.2
kd = 1.2
ki = 0
err = 0
perr = 0
total_err = 0
demand = dest_pos

def gen_points():
    return ["|"] + ("- " * (TRACK_LENGTH - 2)).split() + ["|"]

def print_train(points, count, dest_pos, train_pos):
    global v

    to_disp = points.copy()
    to_disp[round(dest_pos)] = "*"
    to_disp[round(train_pos)] = "#"
    to_disp = [str(count).ljust(3)] + to_disp

    for p in to_disp:
        print(p, end="")

    print(f"{v:.2f}", end="")
    print()

def pid(kp, kd, ki, err, perr, total_err):
    return kp * err + kd * (err - perr) + ki * total_err

# -lim < x < lim
def constrain(x, lim):
    if x < -lim:
        return -lim
    elif x > lim:
        return lim
    else:
        return x

def run_pid(pid_coeffs, wind_value, t=1000):
    pos = []
    steps = t

    dest_pos = 70
    train_pos = 0
    v = 0

    err = 0
    perr = 0
    total_err = 0

    kp, kd, ki = pid_coeffs

    while steps > 0:
        err = dest_pos - train_pos
        total_err = total_err + err
        a = pid(kp, kd, ki, err, perr, total_err)
        a = constrain(a, 0.45)

        a += wind_value
        perr = err

        v = v + a
        train_pos = v + train_pos
        pos.append(train_pos)

        steps = steps - 1

    return pos

kp_values = []
for i in range(500):
    kp = 0.01 + i * 0.002
    kp_values.append((kp, 0.4, 0.0001))

kd_values = []
for i in range(500):
    kd = 0.01 + i * 0.004
    kd_values.append((0.4, kd, 0.0001))

ki_values = []
for i in range(500):
    ki = 0.00001 + i * 0.000002
    ki_values.append((0.4, 0.4, ki))


def draw_chart(ax, values, wind_value, title, param_idx, chart_type):
    x_axis = []
    y_axis = []
    
    for pid_coeffs in values:
        plot = run_pid(pid_coeffs, wind_value)

        x_axis.append(pid_coeffs[param_idx])

        if chart_type == "amp":
            steady_pos = plot[-1]
            amp = 0
            for p in plot:
                diff = abs(p - steady_pos)
                if diff > amp:
                    amp = diff
            y_axis.append(amp)
        
        if chart_type == "len":
            length = 1000
            for i in range(len(plot) - 10, -1, -1):
                window = plot[i : i+10]
                
                total = 0
                for w in window:
                    total = total + w
                avg = total / 10
                
                diff_total = 0
                for w in window:
                    diff_total = diff_total + abs(w - avg)
                avg_diff = diff_total / 10
                
                if avg_diff > 0.1:
                    length = i + 10
                    break
            y_axis.append(length)

    ax.plot(x_axis, y_axis, label=title)
    ax.set_title(title)
    ax.grid(True)
    ax.set_xlabel("Value") 
    if chart_type == "amp":
        ax.set_ylabel("Amplitude")
    else:
        ax.set_ylabel("Time Step")



fig, axes = plt.subplots(
    2,
    3,
    figsize=(18, 10)
)


draw_chart(axes[0, 0], kp_values, -0.2, "Kp vs Amplitude", 0, "amp")
draw_chart(axes[0, 1], kd_values, -0.2, "Kd vs Amplitude", 1, "amp")
draw_chart(axes[0, 2], ki_values, -0.2, "Ki vs Amplitude", 2, "amp")


draw_chart(axes[1, 0], kp_values, -0.2, "Kp vs Transient Length", 0, "len")
draw_chart(axes[1, 1], kd_values, -0.2, "Kd vs Transient Length", 1, "len")
draw_chart(axes[1, 2], ki_values, -0.2, "Ki vs Transient Length", 2, "len")

plt.tight_layout()

plt.savefig(
    "pid_subplot_grid.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()
