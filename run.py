from boid_flockers.server import server

# print(server)

server.port = 9061 # default = 8521
server.launch(open_browser=False)