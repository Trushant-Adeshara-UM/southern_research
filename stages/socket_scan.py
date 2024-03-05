import socket

def scan_ports(host='127.0.0.1', start_port=1, end_port=1024):
    """Scans the specified host for open ports within the given range."""
    open_ports = []
    for port in range(start_port, end_port + 1):
        try:
            # Create a new socket for each port
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)  # Timeout for each attempt (in seconds)
                # Attempt to connect to the port
                result = s.connect_ex((host, port))
                if result == 0:
                    print(f"Port {port} is open")
                    open_ports.append(port)
                else:
                    print(f"Port {port} is closed")
        except Exception as e:
            print(f"An error occurred: {e}")
    return open_ports

# Example usage
host_to_scan = '141.212.84.36'  # Localhost
start_port = 1
end_port = 1024
open_ports = scan_ports(host_to_scan, start_port, end_port)
print(f"Open ports on {host_to_scan}: {open_ports}")

