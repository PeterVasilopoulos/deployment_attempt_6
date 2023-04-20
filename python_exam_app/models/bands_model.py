from python_exam_app.config.mysqlconnection import connectToMySQL

from python_exam_app.models import users_model

from flask import flash

from python_exam_app import DATABASE

class Band:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.genre = data['genre']
        self.city = data['city']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

        # For many to many
        self.members = []

    # Create band
    @classmethod 
    def create(cls, data):
        query = """
            INSERT INTO bands
            (name, genre, city, user_id)
            VALUES 
            (%(name)s, %(genre)s, %(city)s, %(user_id)s);
        """

        return connectToMySQL(DATABASE).query_db(query, data)
    
    # Validate new band
    @classmethod
    def validate_band(cls, data):
        is_valid = True

        # Name validation
        if len(data['name']) < 2:
            flash("Band name too short")
            is_valid = False
        
        # Genre validation
        if len(data['genre']) < 2:
            flash("Genre too short")
            is_valid = False 

        # City validation
        if len(data['city']) < 1:
            flash("Must enter a city")
            is_valid = False

        return is_valid

    # Join band
    @classmethod 
    def join_band(cls, band_id, user_id):
        data = {
            'band_id' : band_id,
            'user_id' : user_id
        }

        query = """
            INSERT INTO joins(band_id, user_id) 
            VALUES(%(band_id)s, %(user_id)s)
        """

        connectToMySQL(DATABASE).query_db(query, data)

    # Quit band
    @classmethod 
    def quit_band(cls, band_id, user_id):
        data = {
            'band_id' : band_id,
            'user_id' : user_id
        }

        query = """
            DELETE FROM joins WHERE
            band_id = %(band_id)s AND
            user_id = %(user_id)s;
        """

        connectToMySQL(DATABASE).query_db(query, data)

    # Get all bands with users attached (black belt)
    @classmethod 
    def get_all_bands_bb(cls):
        query = """
            SELECT * FROM bands LEFT JOIN joins 
            ON bands.id = joins.band_id 
            LEFT JOIN users ON joins.user_id = users.id;
        """

        results = connectToMySQL(DATABASE).query_db(query)

        bands = []
        band_ids = []

        if results:
            for row in results:
                if row['id'] not in band_ids:
                    new_band = cls(row)

                    data = {
                        'band_id' : row['id']
                    }

                    query = """
                        SELECT * FROM bands LEFT JOIN joins 
                        ON bands.id = joins.band_id LEFT JOIN users 
                        ON joins.user_id = users.id 
                        WHERE bands.id = %(band_id)s;
                    """

                    members = connectToMySQL(DATABASE).query_db(query, data)

                    # Add all members to band
                    if members:
                        for member in members:
                            member_data = {
                                **member,
                                'id' : member['users.id'],
                                'created_at' : member['users.created_at'],
                                'updated_at' :member['users.updated_at']
                            }

                            band_member = users_model.User(member_data)

                            new_band.members.append(band_member)

                    # Run query to get band creator
                    data = {
                        'band_id' : row['id']
                    }

                    query = """
                        SELECT * FROM bands JOIN users ON 
                        bands.user_id = users.id 
                        WHERE bands.id = %(band_id)s;
                    """

                    creator = connectToMySQL(DATABASE).query_db(query, data)

                    if creator:
                        for item in creator:
                            creator_data = {
                                **item,
                                'id' : item['users.id'],
                                'created_at' : item['users.created_at'],
                                'updated_at' :item['users.updated_at']
                            }

                            print("pog")

                            band_creator = users_model.User(creator_data)

                            new_band.user = band_creator
                    
                
                    band_ids.append(row['id'])
                    bands.append(new_band)

        return bands

    # Get all bands with user attached
    @classmethod 
    def get_all_bands(cls):
        query = """
            SELECT * FROM bands JOIN
            users ON bands.user_id = users.id;
        """

        results = connectToMySQL(DATABASE).query_db(query)

        bands = []

        if results:
            for row in results:
                new_band = cls(row)

                user_data = {
                    **row,
                    'id' : row['users.id'],
                    'created_at' : row['created_at'],
                    'updated_at' : row['updated_at']
                }

                band_creator = users_model.User(user_data)

                new_band.user = band_creator

                bands.append(new_band)
        
        return bands
    
    # Get single band from id
    @classmethod 
    def get_one_band(cls, id):
        data = {
            'id' : id
        }

        query = """
            SELECT * FROM bands WHERE id = %(id)s;
        """

        results = connectToMySQL(DATABASE).query_db(query, data)

        if results:
            return results[0]
        else:
            return False
        
    # Update band
    @classmethod
    def update(cls, data):
        query = """
            UPDATE bands SET
            name = %(name)s, genre = %(genre)s, city = %(city)s
            WHERE id = %(band_id)s;
        """

        connectToMySQL(DATABASE).query_db(query, data)

    # Delete band
    @classmethod
    def delete(cls, id):
        data = {
            'id' : id
        }

        query = """
            DELETE FROM bands WHERE id = %(id)s;
        """

        connectToMySQL(DATABASE).query_db(query, data)

    # Get one band with user attached
    @classmethod 
    def get_one_with_user(cls, id):
        data = {
            'id' : id
        }

        query = """
            SELECT * FROM bands
            JOIN users ON bands.user_id = user.id 
            WHERE bands.id = %(id)s;
        """

        results = connectToMySQL(DATABASE).query_db(query, data)

        bands = []

        if reuslts:
            for row in results:
                band = cls(row)

                user_data = {
                    'id' : row['users.id'],
                    'created_at' : row['users.created_at'],
                    'updated_at' : row['users.updated_at']
                }

                band_creator = users_model.User(user_data)

                band.user = band_creator

                bands.append(band)

        return bands[0]

    # Get all bands from user id
    @classmethod 
    def get_bands_from_user(cls, user_id):
        data = {
            'id' : user_id
        }

        query = """
            SELECT * FROM bands WHERE user_id = %(id)s;
        """

        return connectToMySQL(DATABASE).query_db(query, data)