import socket
import threading

# server data
server_ip = '127.0.0.1'
server_port = 12345

# create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# connect to server
s.connect((server_ip, server_port))

# get client name
client_name = input("Enter your name: ")
# send client name to server
s.send(client_name.encode())

while True:
  # print opening message
  print("1. Connect to a group chat")
  print("2. Create a group chat")
  print("3. Exit the server")
  # get option from user
  option = input("Enter your option: ")
  # send option to server
  s.send(option.encode())

  if option == "1":
    # get group id and password from user
    group_id = input("Enter group id: ")
    password = input("Enter password: ")
    # send group id and password to server
    s.send(f"{group_id},{password}".encode())
    # receive response from server
    response = s.recv(1024).decode()
    print(response)

  elif option == "2":
    # get password from user
    password = input("Enter password: ")
    # send password to server
    s.send(password.encode())
    # receive group id from server
    group_id = s.recv(1024).decode()
    print(group_id)

  elif option == "3":
    # disconnect from server
    s.close()
    exit()

  else:
    print("Invalid option")

  while True:
    # get message from user
    message = input()
    # send message to server
    s.send(f"{group_id},{password},{message}".encode())
    # receive message from server
    message = s.recv(1024).decode()
    print(message)
