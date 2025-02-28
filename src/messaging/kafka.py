"""
Kafka messaging utilities for the Aika AI System.
"""

import json
from typing import Any, Callable, Dict, List, Optional

from confluent_kafka import Consumer, Producer
from confluent_kafka.admin import AdminClient, NewTopic

from ..utils.config import get_settings
from ..utils.logging import get_logger

# Get logger
logger = get_logger(__name__)

# Get settings
settings = get_settings()

# Kafka producer instance
_producer: Optional[Producer] = None

# Kafka consumer instances
_consumers: Dict[str, Consumer] = {}

# Required topics
REQUIRED_TOPICS = [
    "agent.requests",
    "agent.responses",
    "orchestrator.commands",
    "system.events",
]


def get_producer() -> Producer:
    """
    Get the Kafka producer instance.
    
    Returns:
        Kafka producer
    """
    global _producer
    
    if _producer is None:
        try:
            logger.info("Initializing Kafka producer")
            _producer = Producer({
                "bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVERS,
                "client.id": "aika-producer",
            })
            logger.info("Kafka producer initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Kafka producer: {e}")
            raise
    
    return _producer


def get_consumer(group_id: str) -> Consumer:
    """
    Get a Kafka consumer instance for the specified group.
    
    Args:
        group_id: Consumer group ID
        
    Returns:
        Kafka consumer
    """
    if group_id not in _consumers:
        try:
            logger.info(f"Initializing Kafka consumer for group '{group_id}'")
            _consumers[group_id] = Consumer({
                "bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVERS,
                "group.id": group_id,
                "auto.offset.reset": "earliest",
            })
            logger.info(f"Kafka consumer for group '{group_id}' initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Kafka consumer for group '{group_id}': {e}")
            raise
    
    return _consumers[group_id]


def ensure_topics_exist() -> None:
    """
    Ensure that all required topics exist.
    """
    try:
        logger.info("Ensuring required Kafka topics exist")
        admin_client = AdminClient({"bootstrap.servers": settings.KAFKA_BOOTSTRAP_SERVERS})
        
        # Get existing topics
        metadata = admin_client.list_topics(timeout=10)
        existing_topics = metadata.topics.keys()
        
        # Create missing topics
        topics_to_create = []
        for topic in REQUIRED_TOPICS:
            if topic not in existing_topics:
                logger.info(f"Topic '{topic}' does not exist, will create")
                topics_to_create.append(NewTopic(
                    topic,
                    num_partitions=3,
                    replication_factor=1,
                ))
        
        if topics_to_create:
            futures = admin_client.create_topics(topics_to_create)
            for topic, future in futures.items():
                try:
                    future.result()
                    logger.info(f"Topic '{topic}' created successfully")
                except Exception as e:
                    logger.error(f"Failed to create topic '{topic}': {e}")
        else:
            logger.info("All required topics already exist")
    except Exception as e:
        logger.error(f"Failed to ensure topics exist: {e}")
        raise


def publish_message(topic: str, message: Dict[str, Any], key: Optional[str] = None) -> None:
    """
    Publish a message to the specified topic.
    
    Args:
        topic: Topic name
        message: Message to publish
        key: Message key (optional)
    """
    producer = get_producer()
    
    try:
        # Convert message to JSON
        message_json = json.dumps(message).encode("utf-8")
        
        # Publish message
        producer.produce(
            topic=topic,
            value=message_json,
            key=key.encode("utf-8") if key else None,
            callback=_delivery_report,
        )
        
        # Flush to ensure message is sent
        producer.flush()
    except Exception as e:
        logger.error(f"Failed to publish message to topic '{topic}': {e}")
        raise


def _delivery_report(err, msg) -> None:
    """
    Callback for message delivery reports.
    
    Args:
        err: Error (if any)
        msg: Message
    """
    if err is not None:
        logger.error(f"Message delivery failed: {err}")
    else:
        logger.debug(f"Message delivered to {msg.topic()} [{msg.partition()}]")


def consume_messages(
    topics: List[str],
    group_id: str,
    callback: Callable[[Dict[str, Any], str], None],
    timeout: float = 1.0,
) -> None:
    """
    Consume messages from the specified topics.
    
    Args:
        topics: List of topic names
        group_id: Consumer group ID
        callback: Callback function to process messages
        timeout: Polling timeout in seconds
    """
    consumer = get_consumer(group_id)
    
    try:
        # Subscribe to topics
        consumer.subscribe(topics)
        
        # Poll for messages
        while True:
            msg = consumer.poll(timeout)
            
            if msg is None:
                continue
                
            if msg.error():
                logger.error(f"Consumer error: {msg.error()}")
                continue
                
            try:
                # Parse message value
                message_json = msg.value().decode("utf-8")
                message = json.loads(message_json)
                
                # Get message key
                key = msg.key().decode("utf-8") if msg.key() else None
                
                # Process message
                callback(message, key)
            except Exception as e:
                logger.error(f"Failed to process message: {e}")
    except KeyboardInterrupt:
        logger.info("Stopping consumer")
    finally:
        # Close consumer
        consumer.close()
