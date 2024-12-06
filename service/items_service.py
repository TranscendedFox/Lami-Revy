from typing import Optional
from repository import items_repository
from fastapi import Query
import re


async def get_all_items():
    return await items_repository.get_all_items()


async def get_items_by_search(search: str):

    # Regular expression to extract the item names before any condition
    item_names = re.split(r'amount|price', search)[0].strip()

    # Regular expression to extract amount and price conditions with values
    conditions = re.findall(r'(amount|price)\s*([<>]=?|=?)\s*(\d+)', search)

    # Prepare a dictionary to hold the item names and conditions
    extracted_data = {
        "item_names": [name.strip() for name in item_names.split(',')],
        "conditions": [{"type": condition[0], "operator": condition[1], "value": condition[2]} for condition in
                       conditions]
    }
    return await items_repository.get_items_by_search(extracted_data["item_names"], extracted_data["conditions"])