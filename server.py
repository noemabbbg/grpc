# server.py
import grpc
from concurrent import futures
import service_pb2
import service_pb2_grpc
from kafkab import KafkaProducer, KafkaConsumer

class MyServiceServicer(service_pb2_grpc.MyServiceServicer):
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers='localhost:9092')
        self.consumer = KafkaConsumer(
            'factorial_responses',
            bootstrap_servers='localhost:9092',
            group_id='factorial_requests',
            auto_offset_reset='latest'
        )

    def ComputeGCD(self, request, context):
    # Получение параметров из запроса
        id = request.id
        par_1 = request.par_1
        par_2 = request.par_2

        # Отправка параметров в Kafka-топик
        message = f"{id},{par_1},{par_2}"
        self.producer.send("factorial_requests", value=message.encode())

        # Получение ответа из Kafka-топика
        while True:
            messages = self.consumer.poll(timeout_ms=1000)  # Получение сообщений с таймаутом 1 секунда
            for tp, msgs in messages.items():
                for msg in msgs:
                    print(msg.value.decode())
                    response_parts = msg.value.decode().split(",")
                    if response_parts[0] == str(id):
                        gcd_result = int(response_parts[1])
                        response = service_pb2.Response(
                            id=id,
                            par_1=par_1,
                            par_2=par_2,
                            gcd_result=gcd_result
                        )
                        print(response)
                        return response


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    service_pb2_grpc.add_MyServiceServicer_to_server(MyServiceServicer(), server)
    server.add_insecure_port('[::]:60079')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
