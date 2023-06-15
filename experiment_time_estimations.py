import numpy as np


def print_time_passed(time, day, time_day_start, experiments_done):
    time_passed = time - time_day_start
    print(f"Time required (day {day}): {int(time_passed/60)} hours, {int(time_passed % 60)} minutes.\n"
          f"\t{experiments_done} concentration-combinations tried.")


def calculate_experimental_time(i, experiment, last_experiment):
    # uses 20 minutes to empty, clean and refil the column
    # 5 minutes to change the concentration (c)
    # 30 seconds to change the flow rate (f)
    # 3 minutes to change detector position (p)
    # short measurement (130 Hz) is assumed to take 10 seconds
    # long measurement (22 Hz) is assumed to take 180 seconds
    # dark measurement is assumed to take 2 seconds
    reset_c = 20        # minutes
    change_c = 5        # minutes
    change_f = .5
    change_p = 3
    t_short_measurement = 10/60     # seconds to minutes
    frames_short_measurement = t_short_measurement * 60 * 130
    t_long_measurement = 120/60     # seconds to minutes
    frames_long_measurement = t_long_measurement * 60 * 22
    t_transfer_short = t_short_measurement
    t_transfer_long = t_long_measurement
    t_dark_measurement = 2/60       # seconds to minutes

    # gas flow rates in l/min
    flow_rates = [0, 20, 40]

    # detector positions (measurement height in the column)
    positions = ["high"]

    time = 0
    n_datasets = 0
    n_frames = 0
    vials_used = 0
    amounts_used = [0, 0, 0, 0]

    if i == 0:
        time += reset_c
        time += change_c
    elif any(experiment < last_experiment):
        # if any values from the current row are less than that of a previous one, we have to add time to reset_c
        # TODO investigate if it pays off to search for experiments that don't need cleaning the column
        time += reset_c
        time += change_c
        amounts_used = last_experiment
        vials_used += np.count_nonzero(experiment)
    elif not all(experiment == last_experiment):
        # if concentrations have changed, we have to add time to change_c
        time += change_c
        increased_concentrations = experiment > last_experiment
        vials_used += np.count_nonzero(increased_concentrations)

    for position in positions:
        time += change_p
        for flow_rate in flow_rates:
            time += change_f
            n_datasets += 1
            if flow_rate == 0:
                time += t_dark_measurement
            else:
                time += t_short_measurement
                time += t_transfer_short
                n_frames += frames_short_measurement
                time += t_long_measurement
                time += t_transfer_long
                n_frames += frames_long_measurement

    return time, n_datasets, n_frames, amounts_used, vials_used


def add_experimental_time(days_passed, time_day, experiments_done, time_next, cleanup=False):
    if time_day + time_next > 320:
        days_passed += 1
        print_time_passed(time_day, days_passed, 0, experiments_done)
        time_day = time_next
        experiments_done = 1 if not cleanup else 0
    else:
        time_day += time_next
        experiments_done += 1

    if cleanup:
        days_passed += 1
        print_time_passed(time_day, days_passed, 0, 0)

    return time_day, experiments_done, days_passed


if __name__ == "__main__":
    design = np.loadtxt("design.txt", dtype=np.int8, delimiter=" ")

    # duration in minutes of each step in the experimental plan
    alignment = 360     # minutes
    cleanup = 360

    n_datasets = 0
    days_passed = 0
    time_day = 0
    experiments_done = 0
    n_frames = 0
    amount_used = np.array([0, 0, 0, 0])
    total_vials = 0
    last_experiment = []

    # add alignment time to time_day
    time_day += alignment

    for i, experiment in enumerate(design):
        time_next, n_new_datasets, new_frames, amounts_added, vials_used = calculate_experimental_time(i, experiment,
                                                                                                       last_experiment)
        time_day, experiments_done, days_passed = add_experimental_time(days_passed, time_day, experiments_done,
                                                                        time_next)
        n_frames += new_frames
        amount_used += amounts_added
        total_vials += vials_used
        n_datasets += n_new_datasets
        last_experiment = experiment

    # last concentrations are not taken into account yet, add them here.
    if amounts_added == [0, 0, 0, 0]:
        amount_used += last_experiment

    time_day, experiments_done, days_passed = add_experimental_time(days_passed, time_day, experiments_done, cleanup,
                                                                    cleanup=True)

    # n_frames = n_datasets * 1300

    print(f"Checked {design.shape[0]} different concentrations in {days_passed} days")
    print(f"Obtained {n_datasets} datasets, or {n_frames} frames.")

    dataset_size_MB = n_frames * 3 * 0.908
    dataset_size_TB = dataset_size_MB / 1024 / 1024
    print(f"Raw data will take up {dataset_size_TB:.3f} TB of disk space")
    # assuming 5 seconds reconstruction time per frame
    time_s_per_frame = 5
    reconstruction_time = n_frames * time_s_per_frame / 60
    print(f"Requires {int(reconstruction_time / 60 / 24) + 1} days of reconstruction "
          f"at {time_s_per_frame} s per reconstruction")

    print(f"Total amounts of solutes used (mol parts): {amount_used / 4}")
    print(f"Total number of vials: {total_vials}")
