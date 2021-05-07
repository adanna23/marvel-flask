from flask import Blueprint, request, jsonify
from marvel_inventory.helpers import token_required
from marvel_inventory.models import User, Drone, drone_schema, drones_schema, db


api = Blueprint('api', __name__, url_prefix='/api' )

@api.route('/getdata')
def getdata():
    return { 'some' : 'value'}

#create drone endpoint
@api.route('/drones', methods = ['POST'])
@token_required
def create_car(current_user_token):
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    color =  request.json['color']
    max_speed = request.json['max_speed']
    weight = request.json['weight']
    cost_of_prd = request.json['cost_of_prd']
    series = request.json['series']
    dimensions =request.json['dimensions']
    user_token = current_user_token.token

    drone = Drone(name,description,price,color,max_speed,dimensions, weight,cost_of_prd,series,user_token = user_token )
    db.session.add(drone)
    db.session.commit()

    response = drone_schema.dump(drone)
    return jsonify(response)

    #retrieve all car endpoints
@api.route('/drones', methods = ['GET'])
@token_required
def get_cars(current_user_token):
    owner = current_user_token.token
    drones = Drone.query.filter_by(user_token = owner).all()
    response = drones_schema.dump(drones)
    return jsonify(response)


@api.route('/drones/<id>', methods = ['GET'])
@token_required
def get_car(current_user_token, id):
    drone = Drone.query.get(id)
    response = drone_schema.dump(drone)
    return jsonify(response)

@api.route('/drones/<id>', methods = ['POST', 'PUT'])
@token_required
def update_drone(current_user_token, id):
    drone = Drone.query.get(id) #getting an instance

    drone.name = request.json['name']
    drone.description = request.json['description']
    drone.price = request.json['price']
    drone.color = request.json['color']
    drone.max_speed = request.json['max_speed']
    drone.dimensions = request.json['dimensions']
    drone.weight = request.json['weight']
    drone.cost_of_prd = request.json['cost_of_prd']
    drone.series = request.json['series']
    drone.user_token = current_user_token.token

    db.session.commit()
    response = drone_schema.dump(drone)
    return jsonify(response)

    # delete endpoint
@api.route('/drones/<id>', methods = ['DELETE'])
@token_required
def delete_drone(current_user_token, id):
    drone = Drone.query.get(id)
    db.session.delete(drone)
    db.session.commit()
    response = drone_schema.dump(drone)
    return jsonify(response)