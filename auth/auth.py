import grpc
from concurrent import futures
import time
import auth_pb2 as auth__pb2
import auth_pb2_grpc

# AuthRequest = auth__pb2._globals.get('AuthRequest')
# AuthResponse = auth__pb2._globals.get('AuthResponse')

PASSWDS = {
    'sasha': 'qwerty123',
    'masha': '12345',
    'dasha': 'qwerty',
    'katya': 'humble'
}

class AuthService(auth_pb2_grpc.AuthServiceServicer):
    def Auth(self, request, context):
        username = request.username
        password = request.password
        if PASSWDS.get(username) == password:
            return auth__pb2.AuthResponse(auth=True)
            # return AuthResponse(auth=True)
        return auth__pb2.AuthResponse(auth=False)
        # return AuthResponse(auth=False)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    auth_pb2_grpc.add_AuthServiceServicer_to_server(AuthService(), server)
    server.add_insecure_port('[::]:5002')
    server.start()
    print("Auth gRPC server running on port 5002...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()

'python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. auth.proto'