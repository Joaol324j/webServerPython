import socket
import os

def main():
    # Configurações básicas
    HOST = '127.0.0.1'  # Endereço IP do servidor
    PORT = 5500        # Porta para escutar as conexões

    # Cria um socket TCP
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Liga o socket ao endereço e porta especificados
    server_socket.bind((HOST, PORT))

    # Escuta por até 5 conexões simultâneas
    server_socket.listen(5)
    print(f"Servidor escutando em {HOST}:{PORT}...")

    while True:
        # Aceita uma conexão de entrada do cliente
        client_connection, client_address = server_socket.accept()
        print(f"Conexão recebida de {client_address}")

        # Recebe a requisição HTTP do cliente
        request = client_connection.recv(1024).decode()
        print("Requisição recebida:")
        print(request)

        # Analisa a requisição para determinar o arquivo específico solicitado
        filename = request.split()[1][1:]

        # Verifica se o arquivo solicitado existe no sistema de arquivos do servidor
        if os.path.isfile(filename):
            # Abre o arquivo e lê o conteúdo
            with open(filename, 'rb') as file:
                content = file.read()

            # Prepara uma resposta HTTP com cabeçalhos apropriados
            response_headers = "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n"
            response = response_headers.encode() + content
        else:
            # Retorna uma mensagem de erro "404 Not Found"
            response = "HTTP/1.1 404 Not Found\r\n\r\n<h1>404 Not Found</h1>".encode()

        # Envia a resposta pela conexão TCP ao navegador requisitante
        client_connection.sendall(response)

        # Fecha a conexão com o cliente
        client_connection.close()

    # Encerra o servidor
    server_socket.close()

if __name__ == "__main__":
    main()
