"""MapReduce framework Manager node."""
import os
import tempfile
import logging
import json
import time
import click
import mapreduce.utils
import threading

import mapreduce.utils.tcp_udp_server


# Configure logging
LOGGER = logging.getLogger(__name__)


class Manager:
    """Represent a MapReduce framework Manager node."""

    def __init__(self, host, port):
        """Construct a Manager instance and start listening for messages."""

        LOGGER.info(
            "Starting manager host=%s port=%s pwd=%s",
            host, port, os.getcwd(),
        )
        self.port = port
        self.host = host
        self.alive = True
        
        self.udp_thread = threading.Thread(target=self.run_udp_server, daemon = True)
        self.udp_thread.start()
        
        self.tcp_thread = threading.Thread(target=self.run_tcp_server, daemon=True)
        self.tcp_thread.start()

        LOGGER.info("Manager node initialized and servers started.")
        
        self.udp_thread.join()
        self.udp_thread.join()
        LOGGER.info("Manager has shut down.")

        # TODO: you should remove this. This is just so the program doesn't
        # exit immediately!

    def run_udp_server(self):
        try:
            LOGGER.info(f"UDP server starting...")
            mapreduce.utils.tcp_udp_server.udp_server(self.host, self.port, self.alive)
            LOGGER.info(f"UDP server running on {self.host}:{self.port}")
        except Exception as e:
            LOGGER.error(f"UDP server error {e}")

    def run_tcp_server(self):
        try:
            LOGGER.info(f"TCP server starting...")
            mapreduce.utils.tcp_udp_server.tcp_server(self.host, self.port, self.alive)
            LOGGER.info(f"TCP server running on {self.host}:{self.port}")
        except Exception as e:
            LOGGER.error(f"TCP server error {e}")
@click.command()
@click.option("--host", "host", default="localhost")
@click.option("--port", "port", default=6000)
@click.option("--logfile", "logfile", default=None)
@click.option("--loglevel", "loglevel", default="info")
@click.option("--shared_dir", "shared_dir", default=None)
def main(host, port, logfile, loglevel, shared_dir):
    """Run Manager."""
    tempfile.tempdir = shared_dir
    if logfile:
        handler = logging.FileHandler(logfile)
    else:
        handler = logging.StreamHandler()
    formatter = logging.Formatter(
        f"Manager:{port} [%(levelname)s] %(message)s"
    )
    handler.setFormatter(formatter)
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(loglevel.upper())
    Manager(host, port)


if __name__ == "__main__":
    main()
