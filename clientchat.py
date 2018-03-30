# coding=UTF-8
from Tkinter import *
from socket import *
from thread import *

client_socket = socket(AF_INET, SOCK_STREAM)
remote_ip_c = '127.0.0.1'
remote_port_c = 10317
client_socket.connect((remote_ip_c, remote_port_c))

root = Tk()
root.title('和Alice聊天中')
root.geometry("450x500")

Label(root, text='聊天记录:').grid(row=0, sticky=W, padx=5, pady=5)

# record text
r_frame = Frame(root)
r_frame.grid(row=1, sticky=W)
r_text = Text(r_frame, width=60, height=20)
r_s_bar = Scrollbar(r_frame, command=r_text.yview, orient=VERTICAL)
r_text.config(yscrollcommand=r_s_bar.set)
r_text.bind("<KeyPress>", lambda e: 'break')
r_text.pack(side=LEFT, fill=BOTH)
r_s_bar.pack(side=RIGHT, fill=Y)

Label(root, text='请输入聊天信息:').grid(row=3, sticky=W, padx=5, pady=5)
# type text
t_frame = Frame(root)
t_frame.grid(row=4, sticky=W)
t_text = Text(t_frame, width=60, height=8)
t_s_bar = Scrollbar(t_frame, command=t_text.yview, orient=VERTICAL)
t_text.config(yscrollcommand=t_s_bar.set)
t_text.pack(side=LEFT, fill=BOTH)
t_s_bar.pack(side=RIGHT, fill=Y)


def send_chat(event):
    data = t_text.get(1.0, 'end').strip().encode('utf-8')
    r_text.insert('end', 'Randy:' + data + '\n')
    client_socket.send(data)
    t_text.delete(1.0, 'end')
    return 'break'


t_text.bind('<Return>', send_chat)


def receive_thread(so):
    while True:
        buf = so.recv(256)
        if not buf:
            break
        r_text.insert('end', 'Alice:' + buf + '\n')
        so.close()


start_new_thread(receive_thread, (client_socket,))
root.mainloop()
