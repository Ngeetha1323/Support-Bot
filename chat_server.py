import socket
import threading
import json
from datetime import datetime

class ChatServer:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.clients = {}  # {socket: username}
        self.server_socket = None
        
    def start(self):
        """Start the chat server"""
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            print(f"Chat server started on {self.host}:{self.port}")
            print("Waiting for connections...")
            
            while True:
                client_socket, address = self.server_socket.accept()
                print(f"Connection from {address}")
                
                # Start a new thread to handle this client
                client_thread = threading.Thread(
                    target=self.handle_client, 
                    args=(client_socket, address)
                )
                client_thread.daemon = True
                client_thread.start()
                
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            self.shutdown()
    
    def handle_client(self, client_socket, address):
        """Handle individual client connections"""
        username = None
        
        try:
            # First, get the username
            welcome_msg = {
                'type': 'system',
                'message': 'Welcome! Please enter your username:'
            }
            self.send_message(client_socket, welcome_msg)
            
            # Receive username
            data = client_socket.recv(1024).decode('utf-8')
            if data:
                username_data = json.loads(data)
                username = username_data.get('username', f"User_{address[1]}")
                
                # Add client to the list
                self.clients[client_socket] = username
                
                # Notify all clients about new user
                join_msg = {
                    'type': 'system',
                    'message': f"{username} joined the chat",
                    'timestamp': datetime.now().strftime("%H:%M:%S")
                }
                self.broadcast_message(join_msg, exclude_client=client_socket)
                
                # Send confirmation to the new user
                confirm_msg = {
                    'type': 'system',
                    'message': f"Welcome {username}! You are now connected to the chat.",
                    'timestamp': datetime.now().strftime("%H:%M:%S")
                }
                self.send_message(client_socket, confirm_msg)
                
                # Send list of current users
                user_list = list(self.clients.values())
                users_msg = {
                    'type': 'system',
                    'message': f"Users online: {', '.join(user_list)} ({len(user_list)} total)",
                    'timestamp': datetime.now().strftime("%H:%M:%S")
                }
                self.send_message(client_socket, users_msg)
            
            # Handle incoming messages
            while True:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    break
                
                try:
                    message_data = json.loads(data)
                    
                    if message_data.get('type') == 'message':
                        # Regular chat message
                        chat_msg = {
                            'type': 'message',
                            'username': username,
                            'message': message_data.get('message', ''),
                            'timestamp': datetime.now().strftime("%H:%M:%S")
                        }
                        self.broadcast_message(chat_msg, exclude_client=client_socket)
                        
                    elif message_data.get('type') == 'command':
                        # Handle special commands
                        self.handle_command(client_socket, username, message_data.get('command', ''))
                        
                except json.JSONDecodeError:
                    continue
                    
        except Exception as e:
            print(f"Error handling client {address}: {e}")
        finally:
            # Clean up when client disconnects
            if client_socket in self.clients:
                username = self.clients[client_socket]
                del self.clients[client_socket]
                
                # Notify other clients
                leave_msg = {
                    'type': 'system',
                    'message': f"{username} left the chat",
                    'timestamp': datetime.now().strftime("%H:%M:%S")
                }
                self.broadcast_message(leave_msg)
                
            client_socket.close()
            print(f"Client {address} disconnected")
    
    def handle_command(self, client_socket, username, command):
        """Handle special commands"""
        if command == '/users':
            user_list = list(self.clients.values())
            users_msg = {
                'type': 'system',
                'message': f"Users online: {', '.join(user_list)} ({len(user_list)} total)",
                'timestamp': datetime.now().strftime("%H:%M:%S")
            }
            self.send_message(client_socket, users_msg)
        
        elif command == '/help':
            help_msg = {
                'type': 'system',
                'message': "Available commands: /users (list online users), /help (show this help), /quit (leave chat)",
                'timestamp': datetime.now().strftime("%H:%M:%S")
            }
            self.send_message(client_socket, help_msg)
    
    def send_message(self, client_socket, message):
        """Send a message to a specific client"""
        try:
            message_json = json.dumps(message)
            client_socket.send(message_json.encode('utf-8'))
        except Exception as e:
            print(f"Error sending message: {e}")
    
    def broadcast_message(self, message, exclude_client=None):
        """Send a message to all connected clients"""
        disconnected_clients = []
        
        for client_socket in self.clients:
            if client_socket != exclude_client:
                try:
                    self.send_message(client_socket, message)
                except Exception as e:
                    print(f"Error broadcasting to client: {e}")
                    disconnected_clients.append(client_socket)
        
        # Remove disconnected clients
        for client in disconnected_clients:
            if client in self.clients:
                del self.clients[client]
            client.close()
    
    def shutdown(self):
        """Shutdown the server"""
        print("Shutting down server...")
        if self.server_socket:
            self.server_socket.close()
        
        for client_socket in list(self.clients.keys()):
            client_socket.close()
        
        self.clients.clear()

if __name__ == "__main__":
    server = ChatServer()
    try:
        server.start()
    except KeyboardInterrupt:
        print("\nServer stopped by user")
        server.shutdown()