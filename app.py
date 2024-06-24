# I am still confused with flask and sql, but i guess with more practice I can grab the concepts.

from flask import Flask, request, jsonify
from flask_marshmallow import Marshmallow
import mysql.connector

app = Flask(__name__)
ma = Marshmallow(app)

# Database configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'your_username'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'fitness_center'

# Establish the connection
def create_connection():
    return mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DB']
    )

# Define schemas
class MemberSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'email', 'membership_start', 'membership_end')

class WorkoutSessionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'member_id', 'session_date', 'session_type', 'duration')

member_schema = MemberSchema()
members_schema = MemberSchema(many=True)
workout_session_schema = WorkoutSessionSchema()
workout_sessions_schema = WorkoutSessionSchema(many=True)

# Routes for Members
@app.route('/members', methods=['POST'])
def add_member():
    name = request.json['name']
    email = request.json['email']
    membership_start = request.json['membership_start']
    membership_end = request.json['membership_end']

    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO Members (name, email, membership_start, membership_end) VALUES (%s, %s, %s, %s)",
        (name, email, membership_start, membership_end)
    )
    connection.commit()
    cursor.close()
    connection.close()

    return member_schema.jsonify({"message": "Member added successfully"}), 201

@app.route('/members/<int:id>', methods=['GET'])
def get_member(id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Members WHERE id = %s", (id,))
    member = cursor.fetchone()
    cursor.close()
    connection.close()

    if member:
        return member_schema.jsonify(member), 200
    else:
        return jsonify({"message": "Member not found"}), 404

@app.route('/members/<int:id>', methods=['PUT'])
def update_member(id):
    name = request.json['name']
    email = request.json['email']
    membership_start = request.json['membership_start']
    membership_end = request.json['membership_end']

    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE Members SET name=%s, email=%s, membership_start=%s, membership_end=%s WHERE id=%s",
        (name, email, membership_start, membership_end, id)
    )
    connection.commit()
    cursor.close()
    connection.close()

    return member_schema.jsonify({"message": "Member updated successfully"}), 200

@app.route('/members/<int:id>', methods=['DELETE'])
def delete_member(id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM Members WHERE id=%s", (id,))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "Member deleted successfully"}), 200

# Routes for Workout Sessions
@app.route('/workout_sessions', methods=['POST'])
def add_workout_session():
    member_id = request.json['member_id']
    session_date = request.json['session_date']
    session_type = request.json['session_type']
    duration = request.json['duration']

    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO WorkoutSessions (member_id, session_date, session_type, duration) VALUES (%s, %s, %s, %s)",
        (member_id, session_date, session_type, duration)
    )
    connection.commit()
    cursor.close()
    connection.close()

    return workout_session_schema.jsonify({"message": "Workout session scheduled successfully"}), 201

@app.route('/workout_sessions/<int:id>', methods=['PUT'])
def update_workout_session(id):
    member_id = request.json['member_id']
    session_date = request.json['session_date']
    session_type = request.json['session_type']
    duration = request.json['duration']

    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute(
        "UPDATE WorkoutSessions SET member_id=%s, session_date=%s, session_type=%s, duration=%s WHERE id=%s",
        (member_id, session_date, session_type, duration, id)
    )
    connection.commit()
    cursor.close()
    connection.close()

    return workout_session_schema.jsonify({"message": "Workout session updated successfully"}), 200

@app.route('/members/<int:member_id>/workout_sessions', methods=['GET'])
def get_workout_sessions_for_member(member_id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM WorkoutSessions WHERE member_id = %s", (member_id,))
    sessions = cursor.fetchall()
    cursor.close()
    connection.close()

    return workout_sessions_schema.jsonify(sessions), 200

@app.route('/workout_sessions/<int:id>', methods=['GET'])
def get_workout_session(id):
    connection = create_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM WorkoutSessions WHERE id = %s", (id,))
    session = cursor.fetchone()
    cursor.close()
    connection.close()

    if session:
        return workout_session_schema.jsonify(session), 200
    else:
        return jsonify({"message": "Workout session not found"}), 404

@app.route('/workout_sessions/<int:id>', methods=['DELETE'])
def delete_workout_session(id):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM WorkoutSessions WHERE id=%s", (id,))
    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "Workout session deleted successfully"}), 200

# if __name__ == '__main__':
#     app.run(debug=True)
