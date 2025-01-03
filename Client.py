import c104
import time

# Voltage and current threshold values
VOLTAGE_THRESHOLD = 100  # Example threshold for voltage
CURRENT_THRESHOLD = 10  # Example threshold for current

def main():
    # Client, connection, and station preparation
    client = c104.Client()
    connection = client.add_connection(ip="127.0.0.1", port=2404, init=c104.Init.ALL)
    station = connection.add_station(common_address=47)

    # Monitoring points for voltage and current
    voltage_point = station.add_point(io_address=1, type=c104.Type.M_ME_NA_1)
    current_point = station.add_point(io_address=2, type=c104.Type.M_ME_NA_1)
    status_point = station.add_point(io_address=3, type=c104.Type.M_SP_NA_1)  # Circuit breaker status

    # Command point for controlling the circuit breaker
    command_point = station.add_point(io_address=4, type=c104.Type.C_SC_NA_1)
    
    # Start the client
    client.start()

    # Wait for connection to be established
    while connection.state != c104.ConnectionState.OPEN:
        print(f"Waiting for connection to {connection.ip}:{connection.port}")
        time.sleep(1)

    print("Connection established!")

    # Main loop to monitor and control the system
    while True:
        # Read voltage, current, and status
        if voltage_point.read():
            print(f"Voltage: {voltage_point.value} V")
        else:
            print("Failed to read voltage!")

        if current_point.read():
            print(f"Current: {current_point.value} A")
        else:
            print("Failed to read current!")

        if status_point.read():
            status = "ON" if status_point.value == 1 else "OFF"
            print(f"Circuit Breaker Status: {status}")
        else:
            print("Failed to read circuit breaker status!")

        # Check conditions to update the circuit breaker
        if voltage_point.value > VOLTAGE_THRESHOLD or current_point.value > CURRENT_THRESHOLD:
            # If voltage or current exceeds the threshold, close the circuit breaker
            print("Threshold exceeded! Closing circuit breaker.")
            command_point.value = 0  # Close the circuit breaker (set value to 0)
            if command_point.transmit(cause=c104.Cot.ACTIVATION):
                print("Circuit breaker closed successfully!")
            else:
                print("Failed to close circuit breaker.")
        else:
            # If below threshold, open the circuit breaker
            print("Conditions normal. Opening circuit breaker.")
            command_point.value = 1  # Open the circuit breaker (set value to 1)
            if command_point.transmit(cause=c104.Cot.ACTIVATION):
                print("Circuit breaker opened successfully!")
            else:
                print("Failed to open circuit breaker.")

        # Wait for a while before checking again
        time.sleep(3)


if __name__ == "__main__":
    # Uncomment for debugging if necessary
    # c104.set_debug_mode(c104.Debug.Client|c104.Debug.Connection|c104.Debug.Point|c104.Debug.Callback)
    main()
