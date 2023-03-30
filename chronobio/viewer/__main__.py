import argparse
import logging

from chronobio.viewer.viewer import Viewer

logging.basicConfig(
    filename="viewer.log",
    encoding="utf-8",
    level=logging.INFO,
    format=(
        "%(asctime)s [%(levelname)-8s] %(filename)20s(%(lineno)3s):%(funcName)-20s :: "
        "%(message)s"
    ),
    datefmt="%m/%d/%Y %H:%M:%S",
)
logging.info("Launching viewer")

parser = argparse.ArgumentParser(description="Game client.")
parser.add_argument(
    "-a",
    "--address",
    type=str,
    help="name of server on the network",
    default="localhost",
)
parser.add_argument(
    "-p",
    "--port",
    type=int,
    help="location where server listens",
    default=16210,
)
args = parser.parse_args()

try:
    Viewer(args.address, args.port).run()
except Exception:  # noqa: PIE786,PLW718
    logging.exception("uncaught exception")
