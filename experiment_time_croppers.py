
n_FP_pos = 5

find_max_amps = 3
empty_measurement = 10/60   # seconds to minutes
full_measurement = 10/60
flow_measurement = 2
flow_transfer = flow_measurement * 2
FP_measurement = n_FP_pos * (2 + 30/60)    # 2 minutes per position, 30 s adjustment
scatter_measurements = 3 * 30/60
scatter_transfer = scatter_measurements * 2
fill_column = 10
empty_column = 10

datarate = 300     # MB / s

empty_data = empty_measurement * 60 * datarate
full_data = full_measurement * 60 * datarate
flow_data = flow_measurement * 60 * datarate
scatter_data = scatter_measurements * 60 * 2/3 * datarate

crops = ["noColim", "openColim", "fullviewColim", "narrowColim", "slitColim"]
volts = [120, 150]
flowrates = [80, 100, 150]

t = 0.0
d = 0.0

for c in crops:
    for v in volts:
        t += find_max_amps

        t += empty_measurement
        d += empty_data
        t += scatter_measurements
        t += scatter_transfer
        d += scatter_data

        t += fill_column

        t += full_measurement
        d += full_data
        t += scatter_measurements
        t += scatter_transfer
        d += scatter_data

        for f in flowrates:
            t += scatter_measurements
            t += scatter_transfer
            d += scatter_data

            t += flow_measurement
            t += flow_transfer
            d += flow_data

            t += FP_measurement
        t += empty_column

print("Measurement time (hours):")
print(f"{t / 60:.1f}")

print("Data (GB):")
print(f"{d / 1000:.0f}")
