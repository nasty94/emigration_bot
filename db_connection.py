import sqlite3
conn = sqlite3.connect('data/database.db')
c = conn.cursor()

# Create table
# c.execute('''CREATE TABLE users
#              (id text, additional_info text, age integer, gender text,
#              profession text, country text, current_question text,
#              previous_question text, children boolean)''')
# conn.commit()
#
# c.execute('''CREATE TABLE users_additional_questions
#              (id text, answer)''')
# conn.close()

def update_user_info(user):
    c = conn.cursor()
    c.execute("""UPDATE users SET additional_info = :additional_info,
                age = :age, gender = :gender, profession = :profession,
                country = :country, current_question = :current_question,
                previous_question = :previous_question,
                children = :children
                WHERE id = :id""",
              {'id': user.id,
               'additional_info': user.additional_info,
               'age': user.age,
               'gender': user.gender,
               'profession': user.profession,
               'country': user.country,
               'current_question': user.current_question,
               'previous_question': user.previous_question,
               'children': user.children})
    conn.commit()

def insert_user_info(user):
    c.execute(
        "INSERT INTO users VALUES (:id, :additional_info, :age, :gender, :profession, :country, :current_question, :previous_question, :children)",
        {'id': user.id, 'additional_info': user.additional_info,
         'age': user.age, 'gender': user.gender,
         'profession': user.profession, 'country': user.country,
         'current_question': user.current_question,
         'previous_question': user.previous_question,
         'children': user.children})

    conn.commit()

def get_user_from_db(id):
    # Read and print user
    c.execute("SELECT * FROM users WHERE id=:id", {'id': id})
    user_from_db = c.fetchone()
    print(user_from_db)

def insert_user_additional_questions(id, text, answer):
    c.execute(
        "INSERT INTO users_additional_questions VALUES (:id, :text, :answer)",
        {'id': id,
         'text': text,
         'answer': answer })

    conn.commit()

