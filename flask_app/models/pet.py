from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash


db = "pets"


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
                JOIN users on pets.user_id = users.id;
                """
        results = connectToMySQL(db).query_db(query)
        pets = []
        for row in results:
            # create Pet instance and add creator User instance
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
    def get_by_id(cls, data):
        query = """
                SELECT * FROM pets
                JOIN users on pets.user_id = users.id
                WHERE pets.id = %(id)s;
                """
        result = connectToMySQL(db).query_db(query, data)
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
                INSERT INTO pets (name,food,notes,date,potty,user_id)
                VALUES (%(name)s,%(food)s,%(notes)s,%(date)s,%(potty)s,%(user_id)s);
                """
        return connectToMySQL(db).query_db(query, form_data)

    @classmethod
    def update(cls, form_data):
        query = """
                UPDATE pets
                SET name = %(name)s,
                food = %(food)s,
                notes = %(notes)s ,
                date = %(date)s
                potty = %(potty)s
                WHERE id = %(id)s;
                """
        return connectToMySQL(db).query_db(query, form_data)

    @classmethod
    def destroy(cls, data):
        query = """
                DELETE FROM pets
                WHERE id = %(id)s;
                """
        return connectToMySQL(db).query_db(query, data)

    @staticmethod
    def validate_pet(form_data):
        is_valid = True

        if len(form_data['name']) < 2:
            flash("Name must be at least 2 characters long.")
            is_valid = False
        if len(form_data['food']) < 3:
            flash("Food description must be at least 3 characters long.")
            is_valid = False
        if len(form_data['notes']) < 3:
            flash("Notes must be at least 3 characters long.")
        if form_data['date'] == '':
            flash("Pick a date.")
            is_valid = False
        if 'potty' not in form_data:
            flash("Pick whether they went potty or not.")
            is_valid = False

        return is_valid
