import csv
import json
import time
from io import StringIO


TR_FRI = '''bread,10,slices,25/12/2019
cheese,10,slices,25/12/2019
butter,250,grams,25/12/2019
peanut butter,250,grams,2/12/2019
mixed salad,150,grams,26/12/2018
'''

TR_FRI_MOD = '''bread,10,slices,25/12/2019
cheese,10,slices,25/12/2019
butter,250,grams,25/12/2019
peanut butter,250,grams,2/12/2019
mixed salad,150,grams,26/12/2018
'''

TR_HEAD = '''item, amount, unit, use-by'''

TR_RCP = '''[
    {
        "name": "grilled cheese on toast", 
        "ingredients": [
            {"item":"bread", "amount":"2", "unit":"slices"},
            {"item":"cheese", "amount":"2", "unit":"slices"}
        ]
    },{
        "name": "salad sandwich",
        "ingredients": [
            {"item":"bread", "amount":"2", "unit":"slices"},
            {"item":"mixed salad", "amount":"100", "unit":"grams"}
        ]
    }
]
'''

NO_RCP_MSG = "Order Takeout"


# function for parsing fridge
def parse_fridge(fridge):
    # fridge = TR_HEAD + fridge
    fridge_stream = StringIO(fridge)
    reformatted = dict()
    for i in csv.reader(fridge_stream):
        if i[0] not in reformatted:
            reformatted[i[0]] = []
        reformatted[i[0]].append({"amount": i[1], "unit": i[2], "used-by": i[3]})
    return reformatted


def parse_recipe(recipe):
    return json.loads(recipe)


def main(fridge, recipe):
    parsed_fridge = parse_fridge(fridge)
    parsed_recipe = parse_recipe(recipe)
    filter_fridge(parsed_fridge)

    matched = first_match_recipes(parsed_fridge, parsed_recipe)

    if len(matched) != 0:
        return sorted(matched, key = for_sorting)[0][0]
    else:
        return NO_RCP_MSG


def first_match_recipes(parsed_fridge, parsed_recipe):
    matched = []
    for i in parsed_recipe:
        ingredient_count = 0
        tmp_usedby_diffs = []
        for ingredient in i["ingredients"]:
            checked = check_ingredient_in_fridge(parsed_fridge, ingredient)
            if checked[0]:
                ingredient_count += 1
                tmp_usedby_diffs += checked[1]
        if ingredient_count == len(i["ingredients"]):
            matched.append((i["name"], tmp_usedby_diffs))
    return matched


def check_ingredient_in_fridge(parsed_fridge, ingredient):
    condition = True
    total_amount = 0
    usedby = []
    if ingredient["item"] in parsed_fridge:
        amount = int(ingredient["amount"])
        unit = ingredient["unit"]

        for fridge_item in parsed_fridge[ingredient["item"]]:
            fridge_unit = fridge_item["unit"]

            if unit == fridge_unit:
                total_amount += int(fridge_item["amount"])
                usedby.append(date_to_timestamp(fridge_item["used-by"]))

        condition = condition and \
                    (amount <= total_amount)
    else:
        condition = False

    return condition, usedby


def filter_fridge(fridge):
    now_time = time.mktime(time.localtime())
    to_be_deleted = []
    for item, infolist in fridge.items():
        i = 0
        while(i != len(infolist)):
            item_ub = date_to_timestamp(infolist[i]["used-by"])
            if item_ub < now_time:
                infolist.pop(i)
            else:
                i += 1

        if len(fridge[item]) == 0:
            to_be_deleted.append(item)
    
    for i in to_be_deleted:
        fridge.pop(i)


def date_to_timestamp(date_str):
    if date_str[-1] == '"':
        date_str = date_str.replace('"', '')
    return time.mktime(time.strptime(date_str, "%d/%m/%Y"))


def for_sorting(recipe):
    return min(recipe[1])



if __name__ == "__main__":
    print(main(TR_FRI_MOD, TR_RCP))