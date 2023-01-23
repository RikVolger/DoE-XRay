import numpy as np


def print_time_passed(time, day, time_day_start):
    time_passed = time - time_day_start
    print(f"Time required (day {day + 1}): {int(time_passed/60)} hours, {int(time_passed % 60)} minutes")

if __name__ == "__main__":
    # concentrations relative to literature values of the transition concentration
    concentrations = [0, 0.3, 0.6, 0.9, 1.2]

    # gas flow rates in l/min
    flow_rates = [0, 113, 226, 339]

    # detector positions (measurement height in the column)
    positions = ["low", "med", "high"]

    measurement_cycles = 3
    measurement_days = 10

    # duration in minutes of each step in the experimental plan
    alignment = 360     # minutes
    cleanup = 360
    reset_c = 20        # minutes
    change_c = 5       # minutes
    change_f = .5
    change_p = 3
    t_single_measurement = 10/60

    time = 0
    concentrations_checked = 0
    n_datasets = 0

    for day in range(measurement_days):
        time_day_start = time
        # align on the first measurement day
        if day == 0:
            time += alignment
            print_time_passed(time, day, time_day_start)
            continue
        # cleanup on the last day
        if day == measurement_days -1:
            time += cleanup
            print_time_passed(time, day, time_day_start)
            continue
        
        for i in range(measurement_cycles):
            time += reset_c
            for concentration in concentrations:
                concentrations_checked += 1
                time += change_c
                for position in positions:
                    time += change_p
                    for flow_rate in flow_rates:
                        time += change_f
                        if flow_rate == 0:
                            time += 2/60
                        else:
                            time += t_single_measurement
                        n_datasets += 1
        
        print_time_passed(time, day, time_day_start)
    
    print(f"Checked {concentrations_checked} different concentrations in {measurement_days} days")
    print(f"Obtained {n_datasets} datasets, or {n_datasets * 1300} frames.")

    n_frames = n_datasets * 1300
    dataset_size_MB = n_frames * 3 * 0.908
    dataset_size_TB = dataset_size_MB / 1024 / 1024
    print(f"Raw data will take up {dataset_size_TB:.3f} TB of disk space")
    # assuming 5 seconds reconstruction time per frame
    time_s_per_frame = 5
    reconstruction_time = n_frames * time_s_per_frame / 60
    print(f"Requires {int(np.ceil(reconstruction_time / 60 / 24))} days of reconstruction "
          f"at {time_s_per_frame} s per reconstruction")
