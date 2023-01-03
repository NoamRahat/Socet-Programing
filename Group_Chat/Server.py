import socket
import threading

# server data
server_ip = '127.0.0.1'
server_port = 12345

# create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# bind socket to address and port
s.bind((server_ip, server_port))
# listen for incoming connections
s.listen(5)
print("Server listening for incoming connections...")

# group chats data
group_chats = {}

def handle_client(client):
  # get client name
  client_name = client.recv(1024).decode()
  # get option from client
  option = client.recv(1024).decode()
  if option == "1":
    # get group id and password from client
    data = client.recv(1024).decode()
    group_id, password = data.split(",")
    # check if group chat exists
    if group_id in group_chats:
      # check if password is correct
      if password == group_chats[group_id]["password"]:
        # add client to group chat
        group_chats[group_id]["clients"].append(client)
        client.send("You are now connected to the group chat".encode())
      else:
        client.send("Invalid password".encode())
    else:
      client.send("Group chat does not exist".encode())
  elif option == "2":
    # get password from client
    password = client.recv(1024).decode()
    # generate group id
    group_id = str(len(group_chats)+1)
    # add group chat to group chats
    group_chats[group_id] = {"password": password, "clients": [client]}
    client.send(f"Your group id is {group_id}".encode())
  elif option == "3":
    client.close()

  while True:
    # get data from client
    data = client.recv(1024).decode()
    if not data:
      break
    # get group id, password, and message from data
    group_id, password, message = data.split(",")
    # check if group chat exists
    if group_id in group_chats:
      # check if password is correct
      if password == group_chats[group_id]["password"]:
        # send message to all clients in group chat
        for c in group_chats[group_id]["clients"]:
          c.send(f"{client_name}: {message}".encode())
      else:
        client.send("Invalid password".encode())
    else:
      client.send("Group chat does not exist".encode())

# accept incoming connections
while True:
  client, address = s.accept()
  print(f"Connected to {address}")
  # handle client in separate thread
  thread = threading.Thread(target=handle_client, args=(client,))
  thread.start()
