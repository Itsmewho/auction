# Main loop
from utils.helpers import *


def main():

    input_masking("password:", color=red)
    input_masking("password:", typing_effect=True)
    input_masking("password:", typing_effect=True, color=blue)
    sleep()
    handle_quit()


if __name__ == "__main__":
    main()
