
# CODE TO READ FROM SERVER AND WRITE TO SERVER VALUES


import c104
import time

def main():
    client = c104.Client()
    connection = client.add_connection(ip="127.0.0.1", port=2404, init=c104.Init.ALL)
    station = connection.add_station(common_address=1)

    voltage_point = station.add_point(io_address=11, type=c104.Type.M_ME_NC_1)

    voltage_setpoint = station.add_point(io_address=1, type=c104.Type.C_SE_NC_1)

    trip_status = station.add_point(io_address=13, type=c104.Type.C_SC_NA_1)
    client.start()

    while connection.state != c104.ConnectionState.OPEN:
        print(f"Waiting for connection to {connection.ip}:{connection.port}")
        time.sleep(1)

    if voltage_point:
        print(f"Voltage: {voltage_point.value} V")

    if voltage_setpoint:
        new_voltage = 250.0  
        print(f"Setting new voltage setpoint: {new_voltage} V")

        voltage_setpoint.value = new_voltage

        # Use appropriate command mode and cause of transmission
        voltage_setpoint.command_mode = c104.CommandMode.DIRECT  # Using DIRECT mode

        # Transmit the updated value to the server
        voltage_setpoint.transmit(cause=c104.Cot.ACTIVATION)
        print(f"New voltage setpoint is set to: {voltage_setpoint.value} V")
        print("Value transmitted to the server with ACTIVATION cause.")
    else:
        print("Setpoint with io_address 12 not found.")

    if voltage_point.value>250:
        new_trip_status=True
        print("Tripping the connection")
        trip_status.value  = new_trip_status
        trip_status.command_mode = c104.CommandMode.DIRECT
        trip_status.transmit(cause=c104.Cot.ACTIVATION)
        print("Successfully tripped")
    else:
        new_trip_status=False
        trip_status.value  = new_trip_status
        trip_status.command_mode = c104.CommandMode.DIRECT
        trip_status.transmit(cause=c104.Cot.ACTIVATION)
        print("Trip status not changed")

    # Step 7: Disconnect after some time
    time.sleep(10)
    connection.disconnect()
    print("Disconnected from server.")

if __name__ == "__main__":
    main()
