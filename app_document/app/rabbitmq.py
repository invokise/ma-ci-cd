from datetime import datetime
import aio_pika
import json
import traceback
from asyncio import AbstractEventLoop
from aio_pika.abc import AbstractRobustConnection
from aio_pika import IncomingMessage
from uuid import UUID
from app.settings import settings
from app.services.document_service import DocumentService
from app.repositories.db_document_repo import DocumentRepo


async def send_to_document_queue(data: dict):
    try:
        # Установка соединения с RabbitMQ
        connection = await aio_pika.connect_robust(settings.amqp_url)

        async with connection:
            # Создание канала
            channel = await connection.channel()

            # Объявление очереди, если её нет
            queue = await channel.declare_queue('document_created_queue', durable=True)

            for key, value in data.items():
                if isinstance(value, UUID):
                    data[key] = str(value)
                elif isinstance(value, datetime):
                    data[key] = value.isoformat()

            # Отправка данных в очередь
            await channel.default_exchange.publish(
                aio_pika.Message(body=json.dumps(data).encode()),
                routing_key='document_created_queue'
            )
            print(" [x] Sent %r" % data)

    except aio_pika.exceptions.AMQPError as e:
        print(f"Error occurred while sending data to queue: {e}")

    finally:
        # Закрытие соединения после отправки данных в очередь
        await connection.close()


async def process_created_document(msg: IncomingMessage):
    try:
        data = json.loads(msg.body.decode())
        print("\n/// process_created_document ///\n ")
        DocumentService(DocumentRepo()).create_document(
            data['id'], data['doc'], data['customer'])
        await msg.ack()
    except:
        traceback.print_exc()
        await msg.ack()


async def consume(loop: AbstractEventLoop) -> AbstractRobustConnection:
    connection = await aio_pika.connect_robust(settings.amqp_url, loop=loop)
    channel = await connection.channel()

    document_created_queue = await channel.declare_queue('document_created_queue', durable=True)

    await document_created_queue.consume(process_created_document)

    print('Started RabbitMQ consuming...')

    return connection
