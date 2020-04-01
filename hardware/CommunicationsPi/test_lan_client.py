from sys import argv
import lan_server_class

if __name__ == "__main__":

    if len(argv) == 2:
        # log_file_name and port are configurable for lan_server
        lan_server_class.run(port=int(argv[1]))
    else:
        lan_server_class.run()
