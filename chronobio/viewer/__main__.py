import argparse
import logging

from chronobio.viewer.constants import constants

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
    "-p", "--port", type=int, help="location where server listens", default=16210
)
parser.add_argument("--width", type=int, help="width of the window", default=1777)
parser.add_argument("--height", type=int, help="height of the window", default=1000)
args = parser.parse_args()
constants.resize(args.width, args.height)

try:
    from chronobio.viewer.viewer import Viewer

    Viewer(args.address, args.port)
except Exception:  # noqa: PIE786,PLW718
    logging.exception("uncaught exception")
