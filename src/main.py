from App import App
from sys import argv
from check_input_devices import check_devices

if __name__ == "__main__":
    if len(argv) > 1:
        if argv[1] == 'check':
            check_devices()
        else:
            print("Undefined command. Commands: check")
    else:
        app = App()
        app.start_app()
