from dataclasses import dataclass
from typing import List, Dict, Union
from flask import Flask, request, jsonify
import re

# ==== Type Definitions, feel free to add or modify ===========================
@dataclass
class CookbookEntry:
	name: str

@dataclass
class RequiredItem():
	name: str
	quantity: int

@dataclass
class Recipe(CookbookEntry):
	required_items: List[RequiredItem]

@dataclass
class Ingredient(CookbookEntry):
	cook_time: int


# =============================================================================
# ==== HTTP Endpoint Stubs ====================================================
# =============================================================================
app = Flask(__name__)

# Store your recipes here!
cookbook = {}

# Task 1 helper (don't touch)
@app.route("/parse", methods=['POST'])
def parse():
	data = request.get_json()
	recipe_name = data.get('input', '')
	parsed_name = parse_handwriting(recipe_name)
	if parsed_name is None:
		return 'Invalid recipe name', 400
	return jsonify({'msg': parsed_name}), 200

# [TASK 1] ====================================================================
# Takes in a recipeName and returns it in a form that 
def parse_handwriting(recipeName: str) -> Union[str | None]:
	# TODO: implement me
	g = recipeName
	g = re.sub(r'[-_]', ' ', g)
	g = re.sub(r'[^A-Za-z ]', '', g)
	g = g.lower()
	g = g.title()
	g = re.sub(r'\s{2,}', ' ', g)
	g = g.strip()
	

	if (len(recipeName) <= 0):
		return None

	return g


# [TASK 2] ====================================================================
# Endpoint that adds a CookbookEntry to your magical cookbook
@app.route('/entry', methods=['POST'])
def create_entry():
	# TODO: implement me``

	data = request.json
	t = data.get('type')
	cookTime = data.get('cookTime')
	  
	for thing in cookbook.values():
		if (thing.get('name') == data.get('name')):
			return 'not implemented', 400

	if (t not in ['recipe', 'ingredient']):
		return 'not implemented', 400
	
	if (t == 'ingredient' and cookTime < 0):
		return 'not implemented', 400
	
	if (t == 'recipe'):
		itemNames = []
		r = data.get('requiredItems')

		for item in r:
			itemNames.append(item.get('name'))

		if (len(itemNames) != len(set(itemNames))):
			return 'not implemented', 300
	
	cookbook[data.get('name')] = data

	return '', 200


# [TASK 3] ====================================================================
# Endpoint that returns a summary of a recipe that corresponds to a query name
@app.route('/summary', methods=['GET'])
def summary():
	# TODO: implement me
	name = request.args.get('name')
	ingredients = {}
	ingredientsJSON = []
	cooktime = 0

	if len(cookbook) == 0:
		return '', 400
	
	if name not in cookbook:
		return '', 400
	
	if cookbook[name].get('type') == 'ingredient':
		return '', 400

	code = recursion(name, ingredients, 1)

	if code == 0:
		return '', 400

	# Update ingredients set
	# recursion(name, ingredients, 1)

	for k in ingredients:
		ingredientsJSON.append({
			"name": k,
			"quantity": ingredients[k]
		})
		cooktime += cookbook[k].get('cookTime') * ingredients[k]	

	summary = {
		"name": name,
		"cookTime": cooktime,
		"ingredients": ingredientsJSON
	}

	return summary, 200

def recursion(name, ingredients, mult):
	if name not in cookbook:
		return 0 # fail case

	item = cookbook[name]

	if item.get('type') == 'ingredient':
		if name not in ingredients:
			ingredients[name] = 0
		return 2
	
	requiredItems = item.get('requiredItems')

	for reqItem in requiredItems:
		reqName = reqItem.get('name')
		quantity = reqItem.get('quantity') 

		if reqName not in cookbook:
			return 0

		if recursion(reqName, ingredients, quantity) == 2:
			ingredients[reqName] += quantity * mult

	return 1


# =============================================================================
# ==== DO NOT TOUCH ===========================================================
# =============================================================================

if __name__ == '__main__':
	app.run(debug=True, port=8080)
