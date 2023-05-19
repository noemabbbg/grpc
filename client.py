import grpc
import service_pb2
import service_pb2_grpc
import psycopg2
while True:
    def get_data_from_database():
        # Подключение к базе данных
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="test5",
            user="postgres",
            password="2312"
        )
        cursor = conn.cursor()

        # Выполнение запроса к базе данных для получения данных
        cursor.execute("SELECT id, par_1, par_2 FROM factorial_calculation ORDER BY id DESC LIMIT 1")
        result = cursor.fetchone()
        print(result)

        # Закрытие соединения с базой данных
        cursor.close()
        conn.close()

        return result

    def run():
        # Получение данных из базы данных
        data = get_data_from_database()
        if data:
            id, par_1, par_2 = data

            # Установка соединения с gRPC-сервером
            channel = grpc.insecure_channel('localhost:60079')
            stub = service_pb2_grpc.MyServiceStub(channel)

            # Создание запроса
            request = service_pb2.Request(
                id=int(id),
                par_1=int(par_1),
                par_2=int(par_2)
            )

            # Отправка запроса и получение ответа
            response = stub.ComputeGCD(request)
            print("GCD Result:", response.gcd_result)

    if __name__ == '__main__':
        run()
