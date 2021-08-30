"""Reads input arguments when running the app"""
import argparse


def get_input_args():
    """Read input arguments"""
    parser = argparse.ArgumentParser(description="Python app for scrapping news pages and dumping data to file.")
    parser.add_argument('-c', '--config', help='Path to config with www pages metadata', required=True)
    return vars(parser.parse_args())
