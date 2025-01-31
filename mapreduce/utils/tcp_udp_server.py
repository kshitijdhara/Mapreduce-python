import socket
import datetime
import logging
import json

LOGGER = logging.getLogger(__name__)

def udp_server(host,port, alive):
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    serverSocket.bind((host,port))
    LOGGER.info(f"UDP Server running on {host}:{port}")
    while alive:
        data, addr = serverSocket.recvfrom(1024)
        try:
            msg = json.loads(data)
        except json.JSONDecodeError:
            LOGGER.warning("Received invalid JSON data")
        except Exception as e:
            LOGGER.error(f"Error in UDP server: {e}")
    serverSocket.close()

def tcp_server(host,port, alive):
    serverSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    serverSocket.bind((host, port))
    LOGGER.info(f"TCP server running on {host}:{port}")
    serverSocket.listen()
    while alive:
        try:
            conn, addr = serverSocket.accept()
            with conn:
                LOGGER.info(f"Connected by {addr}")
                while alive:
                    data = conn.recv(1024)
                    if not data:
                        break
                    conn.sendall(data)
        except json.JSONDecodeError:
            LOGGER.warning("Received invalid JSON data")
        except Exception as e:
            LOGGER.error(f"Error in TCP server: {e}")
    serverSocket.close()
        