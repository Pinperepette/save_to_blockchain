#!/usr/bin/env python
from hashlib import sha256
from datetime import datetime
from flask import Flask, jsonify, request, render_template
from pymongo import MongoClient
import json
import uuid

class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.id = str(uuid.uuid4())
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        message = str(self.index) + str(self.timestamp) + str(self.data) + str(self.previous_hash)
        return sha256(message.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

        # Connect to MongoDB database
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client['blockchain']
        self.blocks = self.db['blocks']

    def create_genesis_block(self):
        return Block(0, datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f'), "Genesis Block", "0".encode())

    def add_block(self, block):
        block.previous_hash = self.chain[-1].hash
        block.hash = block.calculate_hash()
        self.chain.append(block)

        # Save block data to MongoDB
        block_data = {
            'id': block.id,
            'block_index': block.index,
            'timestamp': block.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'data': block.data,
            'previous_hash': block.previous_hash,
            'hash': block.hash
        }
        self.blocks.insert_one(block_data)

        return block.id

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/add_block', methods=['POST'])
def add_block():
    data = request.json
    block = Block(len(blockchain.chain), datetime.now(), data['data'], blockchain.chain[-1].hash)
    block_id = blockchain.add_block(block)

    response = {
        'message': f'Block {block.index} added to the blockchain',
        'block_id': block_id
    }
    print(block_id)
    return jsonify(response), 200

@app.route('/get_chain', methods=['GET'])
def get_chain():
    # Retrieve chain data from MongoDB
    chain_data = blockchain.blocks.find()
    chain = []
    for block_data in chain_data:
        block = Block(block_data['block_index'], datetime.strptime(block_data['timestamp'], '%Y-%m-%d %H:%M:%S'), json.loads(block_data['data']), block_data['previous_hash'])
        block.id = block_data['id']
        block.hash = block_data['hash']
        chain.append(block)

    response = {
        'chain': [vars(block) for block in chain]
    }
    return jsonify(response), 200

@app.route('/get_block/<block_id>', methods=['GET'])
def get_block(block_id):
    # Retrieve block data from MongoDB
    block_data = blockchain.blocks.find_one({'id': block_id})
    if block_data is None:
        response = {
            'error': f'Block {block_id} not found in the blockchain'
        }
        return jsonify(response), 404

    block = Block(block_data['block_index'], datetime.strptime(block_data['timestamp'], '%Y-%m-%d %H:%M:%S'), json.loads(block_data['data']), block_data['previous_hash'])
    block.id = block_data['id']
    block.hash = block_data['hash']

    return render_template('block.html', block=block)

if __name__ == '__main__':
    # run Flask server
    app.run(port=5000)
