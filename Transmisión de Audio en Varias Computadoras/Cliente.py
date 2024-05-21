import socket
import pygame
import threading

# Lista de direcciones IP de los nodos a los que se conectará el cliente
nodos = ['192.168.1.1', '192.168.1.2', '192.168.1.3']

# Se crea una lista de sockets, uno por cada nodo
sockets = [socket.socket(socket.AF_INET, socket.SOCK_STREAM) for _ in nodos]

# Inicialización del mixer de pygame para reproducir música
pygame.mixer.init()

# Carga el archivo de música
pygame.mixer.music.load('Audio.mp3')

# Función para reproducir la música según los comandos recibidos del servidor
def play_music(sock):
    while True:
        try:
            data = sock.recv(1024)  # Recibe datos del servidor
            if data == b'play':
                pygame.mixer.music.play()
            elif data == b'pause':
                pygame.mixer.music.pause()
            elif data == b'unpause':
                pygame.mixer.music.unpause()
            elif data == b'stop':
                pygame.mixer.music.stop()
        except Exception as e:
            print(f'Error: {e}')
            break

# Función para enviar comandos al servidor
def send_command(sock):
    while True:
        command = input('Ingrese un comando: ')
        if command == 'exit':
            sock.sendall(command.encode())  # Envía el comando al servidor
            sock.close()
            break
        elif command in ['play', 'pause', 'unpause', 'stop']:
            sock.sendall(command.encode())  # Envía el comando al servidor
        else:
            print('Comando no reconocido')

# Conexión a cada nodo y ejecución de las funciones en hilos separados
for nodo, sock in zip(nodos, sockets):
    try:
        sock.connect((nodo, 12345))  # Conecta con el nodo en el puerto 12345
        threading.Thread(target=play_music, args=(sock,)).start()  # Inicia el hilo para reproducir música
        threading.Thread(target=send_command, args=(sock,)).start()  # Inicia el hilo para enviar comandos
    except Exception as e:
        print(f'Error al conectar con el nodo {nodo}: {e}')
