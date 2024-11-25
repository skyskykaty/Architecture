import grpc
from concurrent import futures
import time
import score_pb2
import score_pb2_grpc

# ScoreRequest = score_pb2._globals.get('ScoreRequest')
# ScoreResponse = score_pb2._globals.get('ScoreResponse')

SCORES = {
    'sasha': 5,
    'masha': 7,
    'dasha': 3
}

class ScoreService(score_pb2_grpc.ScoreServiceServicer):
    def GetScore(self, request, context):
        username = request.username
        score = SCORES.get(username, 0)
        return score_pb2.ScoreResponse(score=score)
        # return ScoreResponse(score=score)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    score_pb2_grpc.add_ScoreServiceServicer_to_server(ScoreService(), server)
    server.add_insecure_port('[::]:5001')
    server.start()
    print("Score gRPC server running on port 5001...")
    server.wait_for_termination()

if __name__ == '__main__':
    serve()