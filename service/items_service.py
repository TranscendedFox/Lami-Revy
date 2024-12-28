from repository import items_repository
import re


async def get_all_items():
    return await items_repository.get_all_items()


async def get_items_by_search(search: str):

    item_names = re.split(r'amount|price', search)[0].strip()

    conditions = re.findall(r'(amount|price)\s*([<>]=?|=?)\s*(\d+)', search)

    extracted_data = {
        "item_names": [name.strip() for name in item_names.split(',')],
        "conditions": [{"type": condition[0], "operator": condition[1], "value": condition[2]} for condition in
                       conditions]
    }
    return await items_repository.get_items_by_search(extracted_data["item_names"], extracted_data["conditions"])
