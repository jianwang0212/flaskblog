import os
os.environ['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
SECRET_KEY = os.environ.get('SECRET_KEY')
print(SECRET_KEY)
