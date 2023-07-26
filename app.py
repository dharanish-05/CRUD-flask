from flask import Flask, jsonify, request
import csv

app = Flask(__name__)

# Define the path to the CSV file
CSV_FILE = 'stores.csv'

#function to read data from CSV file
def read_csv():
    with open(CSV_FILE, 'r') as file:
        reader = csv.DictReader(file)
        stores = list(reader)
    return stores

#function to write data to CSV file
def write_csv(stores):
    fieldnames = ['id', 'name', 'location', 'type']
    with open(CSV_FILE, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(stores)


# GET /stores: Retrieves data of  all stores
@app.route('/stores', methods=['GET'])
def get_stores():
    stores = read_csv()
    return jsonify(stores), 200

# GET /stores/<store_id>: Retrieve a specific store by passing the id in the route
@app.route('/stores/<string:store_id>', methods=['GET'])
def get_store(store_id):
    stores = read_csv()
    for store in stores:
        if store['id'] == store_id:
            return jsonify(store), 200
    return jsonify({'message': 'Store not found'}), 404

# POST /stores: Create a new store by entering the store details 
@app.route('/stores', methods=['POST'])
def create_store():
    stores = read_csv()
    new_store = {
        'id': request.json['id'],
        'name': request.json['name'],
        'location': request.json['location'],
        'type': request.json['type']
    }
    for store in stores:#to ensure no two stores have same id
        if int(store['id']) == int(new_store['id']):
            return jsonify("error id already present give another id"),400 # bad request error

    stores.append(new_store)
    write_csv(stores)
    return jsonify({'message': 'Store created successfully'}), 201

# PUT /stores/<store_id>: Update an existing store using the id by passing it in the route
@app.route('/stores/<string:store_id>', methods=['PUT'])
def update_store(store_id):
    stores = read_csv()
    for store in stores:
        if store['id'] == store_id:
            store['name'] = request.json.get('name')
            store['location'] = request.json.get('location')
            store['type'] = request.json.get('type')
            write_csv(stores)
            return jsonify({'message': 'Store updated successfully'}), 200
    return jsonify({'message': 'Store not found'}), 404

# DELETE /stores/<store_id>: Delete a store using the id pssing it in the route
@app.route('/stores/<string:store_id>', methods=['DELETE'])
def delete_store(store_id):
    stores = read_csv()
    for store in stores:
        if store['id'] == store_id:
            stores.remove(store)
            write_csv(stores)
            return jsonify({'message': 'Store deleted successfully'}), 200 # succesful
    return jsonify({'message': 'Store not found'}), 404 #not found error

#SEARCH /stores/search/<store_word>: search the stores using the name of the store or location or type of the store
@app.route('/stores/search/<string:store_word>',methods=['GET'])
def dearch_stores(store_word):
    stores=read_csv()
    search_results=[]
    for store in stores:
        if( (store['name'] == store_word) or (store['location'] == store_word) or (store['type']== store_word)):
            search_results.append(store)#to display if mutliple stores exist for the search word
    if len(search_results) != 0:
        return(search_results)
    else:
        return({'message':'No Results Found'}),404
# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)