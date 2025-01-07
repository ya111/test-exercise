import argparse
import asyncio
from enum import Enum

from src.ws_client_ab_test import compare_connections as run_ws_ab
from src.ws_client import ws_reader as run_ws
from src.ws_client_perf_test import perf_test as run_ws_perf


class Command(Enum):
    WS = "ws"
    WS_AB = "ws_ab"
    WS_PERF = "ws_perf"


def main():
    parser = argparse.ArgumentParser(description="WS reader and test application")
    
    subparsers = parser.add_subparsers(dest="command", help="allowed commands")

    parser_ws = subparsers.add_parser(Command.WS.value, help="Run ws reader")
    parser_ws.add_argument("--total_messages", type=int, default=None, 
                           help="Total number of matching messages to process")

    parser_ab = subparsers.add_parser(Command.WS_AB.value, help="Run ab test")
    parser_ab.add_argument("--total_messages", type=int, default=10, help="Total number of messages to process")
    
    parser_perf = subparsers.add_parser(Command.WS_PERF.value, help="Run performance test")
    parser_perf.add_argument("--total_messages", type=int, default=10, help="Total number of messages to process")

    args = parser.parse_args()

    if args.command == Command.WS.value:
        asyncio.run(run_ws(args.total_messages))
    elif args.command == Command.WS_AB.value:
        asyncio.run(run_ws_ab(args.total_messages))
    elif args.command == Command.WS_PERF.value:
        asyncio.run(run_ws_perf(args.total_messages))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()