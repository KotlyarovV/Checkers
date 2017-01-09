import socket


def send_state(string,board):
        host = ''
        port = 33892

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(1)
        sock, addr = s.accept()
        buf = str.encode("")
        while buf.decode('utf8') != "get it":
                sock.send(str.encode(string))
                buf = sock.recv(1024)
                try:
                        board.window.update()
                except Exception:
                        pass
        sock.close()
        






def get_state(board):
        host = ''
        port = 33892

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(1)
        sock, addr = s.accept()
        buf = str.encode("")
        while len(buf.decode('utf8'))<2:
                buf = sock.recv(1024)
                try:
                        board.window.update()
                except Exception:
                        pass
        sock.send(str.encode("get it"))
        sock.close()
        return buf.decode('utf8')


def wait_connection(board):
        host = ''
        port = 33892

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((host, port))
        s.listen(1)
        sock, addr = s.accept()
        buf = str.encode("")
        while buf.decode('utf8') != "allright":
                buf = sock.recv(1024)
                try:
                        board.window.update()
                except Exception:
                        pass
        sock.close()
