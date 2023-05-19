# kafka_broker.py
from kafka import KafkaConsumer, KafkaProducer

def compute_gcd(par_1, par_2):
    while par_2 != 0:
        par_1, par_2 = par_2, par_1 % par_2
    return par_1

def start_kafka_consumer():
    consumer = KafkaConsumer(
        'factorial_requests',
        bootstrap_servers='localhost:9092',
        group_id='factorial_requests',
        auto_offset_reset='latest'
    )
    producer = KafkaProducer(bootstrap_servers='localhost:9092')

    for message in consumer:
        request_parts = message.value.decode().split(",")
        id = request_parts[0]
        par_1 = int(request_parts[1])
        par_2 = int(request_parts[2])

        # Вычисление НОД
        gcd_result = compute_gcd(par_1, par_2)

        # Отправка ответа в Kafka-топик
        response_message = f"{id},{gcd_result}"
        producer.send("factorial_responses", value=response_message.encode())

if __name__ == '__main__':
    start_kafka_consumer()
