from flask_app.config.MySQLConnection import connectToMySQL
from flask_app.models.models_users import User
from flask import flash

class Blog:
    db = "personal_portfolio"
    def __init__(self,data):
        self.id = data['id']
        self.title = data['post_title']
        self.post_text = data['post_text']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data ['user_id']

    @classmethod
    def create_post(cls,data):
        query = """
        INSERT INTO blogs (post_title, post_text, user_id)
        VALUES (%(title)s, %(post_text)s, %(user_id)s)
        """
        results = connectToMySQL(cls.db).query_db(query,data)
        return results

    @classmethod
    def get_posts_with_users(cls):
        query = "SELECT * FROM blogs JOIN users ON users.id = blogs.user_id"
        results = connectToMySQL(cls.db).query_db(query)
        user_posts = []
        for obj in results:
            blog = cls(obj)
            user_data = {
                'id' : obj['users.id'],
                'first_name' : obj['first_name'],
                'last_name' : obj['last_name'],
                'email' : obj ['email'],
                'password' : obj['password'],
                'created_at' : obj['users.created_at'],
                'updated_at' : obj['users.updated_at']
            }
            blog.user_posts = User(user_data)
            user_posts.append(blog)
        return user_posts

    @classmethod
    def get_one_post(cls,data):
        query = "SELECT * FROM blogs WHERE id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query,data)
        return cls(results[0])

    @classmethod
    def update(cls,data,post_id):
        query = f'UPDATE blogs SET post_title = %(post_title)s, post_text = %(post_text)s WHERE id = {post_id}'
        return connectToMySQL(cls.db).query_db(query,data)
    
    @classmethod
    def delete(cls,post_id):
        data = {
            'id' : post_id
        }
        query = "DELETE FROM blogs WHERE id = %(id)s"
        return connectToMySQL(cls.db).query_db(query,data)
