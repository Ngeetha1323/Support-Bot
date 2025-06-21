import socket
import threading
import json
import sys


class ChatClient:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.socket = None
        self.username = ""
        self.connected = False
        
    def connect(self):
        """Connect to the chat server"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.host, self.port))
            self.connected = True
            print(f"Connected to chat server at {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            return False
    
    def start(self):
        """Start the chat client"""
        if not self.connect():
            return
        
        # Start thread to receive messages
        receive_thread = threading.Thread(target=self.receive_messages)
        receive_thread.daemon = True
        receive_thread.start()
        
        # Get username from user
        self.get_username()
        
        # Main input loop
        self.input_loop()
    
    def get_username(self):
        """Get username from user and send to server"""
        while True:
            username = input().strip()
            if username:
                self.username = username
                username_data = {
                    'type': 'username',
                    'username': username
                }
                self.send_message(username_data)
                break
            else:
                print("Username cannot be empty. Please try again:")
    
    def receive_messages(self):
        """Receive messages from server"""
        while self.connected:
            try:
                data = self.socket.recv(1024).decode('utf-8')
                if not data:
                    break
                
                message = json.loads(data)
                self.display_message(message)
                
            except Exception as e:
                if self.connected:
                    print(f"Error receiving message: {e}")
                break
        
        self.connected = False
    
    def display_message(self, message):
        """Display received message"""
        msg_type = message.get('type', '')
        timestamp = message.get('timestamp', '')
        
        if msg_type == 'system':
            if timestamp:
                print(f"[{timestamp}] {message.get('message', '')}")
            else:
                print(message.get('message', ''))
                
        elif msg_type == 'message':
            username = message.get('username', 'Unknown')
            msg_text = message.get('message', '')
            print(f"[{timestamp}] {username}: {msg_text}")
    
    def send_message(self, message_data):
        """Send message to server"""
        try:
            message_json = json.dumps(message_data)
            self.socket.send(message_json.encode('utf-8'))
        except Exception as e:
            print(f"Error sending message: {e}")
            self.connected = False
    
    def input_loop(self):
        """Main input loop for user messages"""
        print("\n" + "="*50)
        print("Chat started! Type your messages below.")
        print("Commands: /users, /help, /quit")
        print("="*50)
        
        while self.connected:
            try:
                user_input = input().strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.startswith('/'):
                    if user_input == '/quit':
                        break
                    else:
                        command_data = {
                            'type': 'command',
                            'command': user_input
                        }
                        self.send_message(command_data)
                else:
                    # Regular message
                    message_data = {
                        'type': 'message',
                        'message': user_input
                    }
                    self.send_message(message_data)
                    
            except KeyboardInterrupt:
                break
            except EOFError:
                break
        
        self.disconnect()
    
    def disconnect(self):
        """Disconnect from server"""
        self.connected = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        print("\nDisconnected from chat server. Goodbye!")

def main():
    print("=" * 50)
    print("          PYTHON CHAT CLIENT")
    print("=" * 50)
    
    # Get server details
    host = input("Enter server host (default: localhost): ").strip()
    if not host:
        host = 'localhost'
    
    port_input = input("Enter server port (default: 12345): ").strip()
    if port_input:
        try:
            port = int(port_input)
        except ValueError:
            print("Invalid port number. Using default 12345.")
            port = 12345
    else:
        port = 12345
    
    # Create and start client
    client = ChatClient(host, port)
    client.start()

if __name__ == "__main__":
    main()