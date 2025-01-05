import argparse
import asyncio

from src.ws_client_ab_test import compare_connections as run_ws_ab
from src.ws_client import ws_reader as run_ws
from src.ws_client_perf_test import perf_test as run_ws_perf


def main():
    parser = argparse.ArgumentParser(description="WS reader and test application")
    
    subparsers = parser.add_subparsers(dest='command', help='Subcommands for different functionalities')

    parser_ws = subparsers.add_parser('ws', help='Run ws reader')
    parser_ws.add_argument('--total_messages', type=int, default=None, help='Total number of matching messages to process')

    parser_ab = subparsers.add_parser('ws_ab', help='Run ab test')
    parser_ab.add_argument('--total_messages', type=int, default=10, help=f'Total number messages to process')
    
    parser_perf = subparsers.add_parser('ws_perf', help='Run perfomance test')
    parser_perf.add_argument('--total_messages', type=int, default=10, help=f'Total number messages to process')

    args = parser.parse_args()

    if args.command == 'ws':
        asyncio.run(run_ws(args.total_messages))
    elif args.command == 'ws_ab':
        asyncio.run(run_ws_ab(args.total_messages)) 
    elif args.command == 'ws_perf':
        asyncio.run(run_ws_perf(args.total_messages))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()