import httpx
from fastapi import HTTPException
from app.models.kong_consumer import KongConsumerAttributes, CreateKongConsumer, KongConsumer

async def create_kong_consumer(kong_consumer_to_be_created: CreateKongConsumer):
    """Function to create a kong consumer

    Args:
        new_kong_consumer: CreateKongConsumer model
        model location: app/models/kong_consumer.py
    Returns:
        KongConsumer model with the created consumer
        model location: app/models/kong_consumer.py
    """
    try:
        kong_consumer = {
            KongConsumerAttributes.username.value: kong_consumer_to_be_created.username,
            KongConsumerAttributes.custom_id.value: kong_consumer_to_be_created.custom_id
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://kong:8001/consumers",
                data=kong_consumer
            )
        
        if response.status_code == 201:
            created_consumer = KongConsumer.parse_raw(response.text)
            return created_consumer
        
        if response.status_code == 409:
            raise HTTPException(status_code=409, detail="create_kong_consumer: Kong consumer already exists")
        

    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"create_kong_consumer: {e}")