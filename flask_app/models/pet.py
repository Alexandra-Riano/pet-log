from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

db = "recipes"


class Pet:
    def __init__(self, db_data):
        self.id = db_data['id']
        self.name = db_data['name']
        self.food = db_data['food']
        self.notes = db_data['notes']
        self.date = db_data['date']
        self.potty = db_data['potty']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user_id = db_data['user_id']
        self.creator = None


# get all pets from database and join them with users table


    @classmethod
    def get_all(cls):
        query = """
                SELECT * FROM pets
                LEFT JOIN users on pets.user_id = users.id;
                """
        results = connectToMySQL(db).query_db(query)
        if not results:
            return []
        pets = []
        for row in results:
            # create pet instance and add creator User instance
            this_pet = cls(row)
            user_data = {
                "id": row['users.id'],
                "first_name": row['first_name'],
                "last_name": row['last_name'],
                "email": row['email'],
                "password": "",
                "created_at": row['users.created_at'],
                "updated_at": row['users.updated_at']
            }
            this_pet.creator = user.User(user_data)
            pets.append(this_pet)
        return pets

# get pet by id from database and join it with users table
    @classmethod
    def get_by_id(cls, petID):
        query = """
                SELECT * FROM pets
                JOIN users on pets.user_id = users.id
                WHERE pets.id = %(id)s;
                """
        dataMap = {
            'id': petID
        }
        result = connectToMySQL(db).query_db(query, dataMap)
        if not result:
            return False

        result = result[0]
# create pet instance and add creator User instance
        this_pet = cls(result)
        user_data = {
            "id": result['users.id'],
            "first_name": result['first_name'],
            "last_name": result['last_name'],
            "email": result['email'],
            "password": "",
            "created_at": result['users.created_at'],
            "updated_at": result['users.updated_at']
        }
        this_pet.creator = user.User(user_data)
        return this_pet

    @classmethod
    def save(cls, form_data):
        query = """
                INSERT INTO pet (name,food,notes,date,potty,user_id)
                VALUES (%(name)s,%(food)s,%(notes)s,%(date)s,%(potty)s,%(user_id)s);
                """
        return connectToMySQL(db).query_db(query, form_data)

    @classmethod
    def update(cls, form_data):
        query = """
                UPDATE pets
                SET name = %(name)s,
                description = %(food)s,
                instructions = %(notes)s ,
                date_made = %(date)s,
                under_30 = %(potty)s
                WHERE id = %(id)s;
                """
        return connectToMySQL(db).query_db(query, form_data)

    @classmethod
    def destroy(cls, petID):
        query = """
                DELETE FROM pets
                WHERE id = %(id)s;
                """
        dataMap = {
            'id': petID
        }
        return connectToMySQL(db).query_db(query, dataMap)

    @staticmethod
    def validate_pet(form_data):
        is_valid = True

        if len(form_data['name']) < 3:
            flash("Name must be at least 3 characters long.")
            is_valid = False
        if len(form_data['food']) < 3:
            flash("Food description must be at least 3 characters long.")
            is_valid = False
        if len(form_data['notes']) < 3:
            flash("Notes must be at least 3 characters long.")
            is_valid = False
        if form_data['date'] == '':
            flash("Pick a date.")
            is_valid = False
        if 'Potty' not in form_data:
            flash("Pick whether your pet went potty or not.")
            is_valid = False

        return is_valid
