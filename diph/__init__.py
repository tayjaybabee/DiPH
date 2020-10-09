from threading import Thread
import PySimpleGUI as gui

to_server = None

def __get_buffer__():
    return to_server

def __set_buffer__(new_buffer):
    global to_server
    to_server = new_buffer

class Server(Thread):
    def __init__(self):



