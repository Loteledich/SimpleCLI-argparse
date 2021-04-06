import socket
import ast
import click
import argparse
import sys

msg = {
    "module_from": "",
    "module_to": "front_app",
    "code": "",
    "data": {
        "status": "",
        "code": "",
        "details": "",
        "payload": {}
    }
}
parser = argparse.ArgumentParser()
parser.add_argument('device', type=str, choices=['card_dispenser', 'printer'])
parser.add_argument('status', type=str, choices=['status_ok', 'status_err','read_magnetic_card_ok','read_magnetic_card_err'])
args = parser.parse_args()


def cli():

    client = WSClient('192.168.0.40', 33000)

    if args.device == 'card_dispenser':
        client.send_message(1024,dispenser(args.status,msg))

    if  args.device == 'printer':
        client.send_message(1024,printer(args.status,msg))


def dispenser(status,message):
    message["module_from"] = "cds"

    if status == 'status_ok':
        message["code"] = "get_status_res"
        message["data"]["status"] = "ok"

    if status == 'status_err':
        message["code"] = "get_status_res"
        message["data"] = {
                "status": "error",
                "code": "serialport_error",
                "details": "Serial port error occured",
                "payload": "null"
            }

    if status == 'read_magnetic_card_ok':
        message["code"] = "read_magnetic_card_res"
        message["data"]["payload"]= {
                    "track_1": "123412341234",
                    "track_2": "123131231313",
                    "track_3": "112233112233"
                }

    if status == 'read_magnetic_card_err':
        message["code"] = "read_magnetic_card_res"
        message["data"]= {
            "status": "error",
            "code": "serialport_error",
            "details": "Serialport error occured",
            "payload": "null"
            }
    return message

def printer(status,message):

    message["module_from"] = "tps"

    if status == 'status_ok':
        message["code"]= "get_status_res"
        message["data"]["status"] = "ok"

    if status == 'status_err':
        message["code"] = "get_status_res"
        message["data"] = {
            "status": "error",
            "code": "printer_error",
            "details": "Unknown error occured",
            "payload": "null"
        }

class WSClient:

    def __init__(self, host, port):

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((host, port))

    def send_message(self, buffer,message):

        send = str(str(message).replace("\'", "\""))
        self.client_socket.send(str.encode(send))
        print(self.client_socket.recv(buffer).decode())


cli()