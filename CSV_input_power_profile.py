import Maynuo, time, sys, csv, os, signal

ENABLE_HARDWARE = True  # Set to True if connected to hardware, False otherwise

register_write_delay = 0.004 # Minimum step time in seconds, this is generated from update_speed_test_script.py
time_between_cycles = 10 # Allow the battery to recover between test cycles
total_cycle_count = 2 # Number of test cycles to do (0 indexed so 0 would be 1 cycle, 1 would be 2 cycles, etc.)
csv_file_path = 'power_steps.csv' # Path to the power step input file, first row should be "Power (W), Time (S), Description", it will be auto-generated if it does not exist

def signal_handler(sig, frame):
    print("Ctrl+C pressed. Exiting gracefully...")
    if ENABLE_HARDWARE:
            load.setCPower(0)
            time.sleep(0.1)
            load.setInputOff
    print('Load off')
    sys.exit(0)

# Check if the CSV file exists
if not os.path.exists(csv_file_path):
    # If the file doesn't exist, create it and write the default values
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ['Power (W)', 'Time (S)', 'Description', 'Time between cycles (S)', 'Total cycle count']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        # Write the header
        writer.writeheader()

        # Write the default values
        writer.writerows([
            {'Power (W)': 0, 'Time (S)': 1, 'Description': '', 'Time between cycles (S)': time_between_cycles, 'Total cycle count': total_cycle_count},
            {'Power (W)': 0.95, 'Time (S)': 1.3, 'Description': '', 'Time between cycles (S)': '', 'Total cycle count': ''},
            {'Power (W)': 3.95, 'Time (S)': 0.016, 'Description': '', 'Time between cycles (S)': '', 'Total cycle count': ''},
            # ... other default values
        ])

def read_csv():
    power_time_list = []
    time_between_cycles = 10  # Default value for time_between_cycles
    total_cycle_count = 1  # Default value for total_cycle_count

    # Read the CSV file and convert it to a list of tuples
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:

            time_between_cycles_str = row['Time between cycles (S)']
            # Check if the 'total_cycle_count' string is not blank or contains only whitespace
            if time_between_cycles_str.strip():
                # If not blank, convert the string to an integer and update 'total_cycle_count'
                time_between_cycles = int(time_between_cycles_str)

            total_cycle_count_str = row['Total cycle count']
            # Check if the 'total_cycle_count' string is not blank or contains only whitespace
            if total_cycle_count_str.strip():
                # If not blank, convert the string to an integer and update 'total_cycle_count'
                total_cycle_count = int(total_cycle_count_str)


            power_time_list.append((float(row['Power (W)']), float(row['Time (S)'])))
    
    return power_time_list, time_between_cycles, total_cycle_count


def main():
    try:
        signal.signal(signal.SIGINT, signal_handler)

        power_time_list, time_between_cycles, total_cycle_count = read_csv()
        #print(power_time_list)
        #print(time_between_cycles)
        #print(total_cycle_count)
        print('ENABLE_HARDWARE =' + str(ENABLE_HARDWARE))
        if ENABLE_HARDWARE:
            load = Maynuo.Maynuo('COM8',115200,1,register_write_delay)
            load.setCPower(0)
            load.setInputOn()
            time.sleep(0.1)

        if not power_time_list:
            # If there was an issue with the CSV, use default values
            print("There is an issue with CSV. Ensure the headers look like this:")
            print('Power (W), Time (S), Description, Time between cycles (S), Total cycle count')
            print('If you delete the file the script will auto-generate an example')
            input("Press Enter to exit...")


        for i in range(1, total_cycle_count+1): # This code runs when total cycle count is greater than 0
            for power, delay_time in power_time_list:
                if ENABLE_HARDWARE:
                    load.setCPower(power)
                print(str(power) + 'W  for ' + str(delay_time) + ' seconds')
                time.sleep(delay_time)
            if time_between_cycles != 0:
                if ENABLE_HARDWARE:
                    load.setCPower(0)
                print('Load off. Waiting for battery recovery for ' + str(time_between_cycles) + ' seconds')
                time.sleep(time_between_cycles)
            print('Cycle #' + str(i) + ' complete')
        if total_cycle_count == 0: # This code runs infinitely when total cycle count is 0
            print('Looping forever, Ctrl+C to exit')
            while(1):
                for power, delay_time in power_time_list:
                    if ENABLE_HARDWARE:
                        load.setCPower(power)
                    print(str(power) + 'W  for ' + str(delay_time) + ' seconds')
                    time.sleep(delay_time)
                print('Looping forever, Ctrl+C to exit')
        if ENABLE_HARDWARE:
            load.setCPower(0)
            time.sleep(0.1)
            load.setInputOff
        print('Load off')
        print('Cycles complete')
        input("Press Enter to exit...")

    except Exception as e:
        # Handle the exception here, print an error message, or perform cleanup
        if ENABLE_HARDWARE:
            load.setCPower(0)
            time.sleep(0.1)
            load.setInputOff
        print('Load off')
        print(f"An error occured: {e}")

if __name__ == '__main__':
    main()
