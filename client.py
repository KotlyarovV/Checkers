from socket import *
import sys



def send_state(string, board, host):
    #host = "localhost"
    #host = "192.168.1.127"
    port = 33892
    addr = (host,port)

    tcp_socket = socket(AF_INET, SOCK_STREAM)

    connected = False
    while connected == False:
        try:
            tcp_socket.connect(addr)
        except BaseException:
            
            try:
                board.window.update()
            except Exception:
                pass
            continue
        connected = True


    data = str.encode("")

    while data != "get it":
        #encode - перекодирует введенные данные в байты, decode - обратно
        tcp_socket.send(str.encode(string))
        data = tcp_socket.recv(1024)
        data = data.decode('utf8')
        try:
            board.window.update()
        except Exception:
            pass
    tcp_socket.close()


def get_state(board,host):

    #host = "192.168.1.127"
    port = 33892
    addr = (host,port)

    tcp_socket = socket(AF_INET, SOCK_STREAM)

    connected = False
    while connected == False:
        try:
            tcp_socket.connect(addr)
        except BaseException:
            try:
                board.window.update()
            except Exception:
                pass
            continue
        connected = True


    data = ""

    while len(data) < 2:
        #encode - перекодирует введенные данные в байты, decode - обратно
        data = tcp_socket.recv(1024)
        data = data.decode('utf8')
        try:
            board.window.update()
        except Exception:
            pass
    tcp_socket.send(str.encode("get it"))
    tcp_socket.close()
    return data


def check_connection(host):
    port = 33892
    addr = (host,port)

    tcp_socket = socket(AF_INET, SOCK_STREAM)

    try:
        tcp_socket.connect(addr)
        tcp_socket.send(str.encode("allright"))
        tcp_socket.close()
        return True
    except BaseException:
        return False
        

