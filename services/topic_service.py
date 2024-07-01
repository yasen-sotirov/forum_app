from data.database import read_query,insert_query, update_query
from my_models.model_topic import Topic
from datetime import datetime,date
from services.user_service import find_by_username
from services.category_service import category_exists
from fastapi import Response
from services import user_service

def read_topic():
    data = read_query('SELECT * FROM new_topic')
    return data


def find_by_id_topic(id_of_topic: int) -> Topic | None:
    id = 'SELECT * FROM new_topic WHERE id_of_topic'
    new_paramater = (id_of_topic,)

    new_result = read_query(id,new_paramater)

    if new_result:
        return new_result[0]
    else:
        return None

def sort_by_topic(sort):
    if sort == 'Ascending':
       something = read_query('SELECT * FROM new_topic ORDER BY title ASC')
    elif sort == 'Descending':
       something = read_query('SELECT * FROM new_topic ORDER BY title DESC')
    return something

def search_by_topic(search):
    search_data = read_query('SELECT * FROM new_topic WHERE title LIKE ?',(f'%{search}%',))
    return search_data

def topic_exists(by_title: str):
    check = read_query('SELECT title FROM new_topic WHERE title = ?',(by_title,))

    return bool(check)

def find_id_nickname(nickname):
    check = read_query('SELECT id_of_user FROM new_user WHERE nickname = ?', (nickname,))
    return check

def create_topic(title: str, topic_text: str, date_of_creation: date, name_of_category: str, username: str) -> Topic | None:

    get_author_id = find_id_nickname(username)
    getting_it = get_author_id[0][0]
    check_category = ""

    if category_exists(name_of_category):
        check_category = name_of_category
    else:
        return Response(status_code=400, content='There is no such category')
    createtopic = insert_query('INSERT INTO new_topic(title, topic_text,date_of_creation,category_name_of_category,id_of_author) VALUES (?,?,?,?,?)',
                               (title,topic_text,date_of_creation,name_of_category,getting_it,))
    
    return Topic(title=title,topic_text=topic_text,date_of_creation=date_of_creation,name_of_category=check_category,id_of_author=getting_it)



def find_topic_id_by_name(topic_name: str):
    result_tuple = read_query('''SELECT id_of_topic FROM new_topic
                        WHERE title = ?''', (topic_name,))
    return result_tuple[0][0]

def view_topic_with_reply(id: int):
    something = read_query('SELECT * FROM new_topic WHERE id_of_topic = ?',(id,))
    return something

def select_upvote_downvote(id: int):
    something = read_query('SELECT UpVote,DownVote from reactions_of_replies where new_user_id = ?',(id,))
    return something

def upvote_count(reply_id: int):
    something = read_query('SELECT UpVote from reactions_of_replies WHERE id_of_replies = ? AND UpVote = 1',(reply_id,))
    return len(something)

def downvote_count(reply_id: int):
    something = read_query('SELECT DownVote from reactions_of_replies WHERE id_of_replies = ? AND DownVote = -1',(reply_id,))
    return len(something)

def view_reply_by_topic(id: int):
    nothing = read_query('SELECT * FROM replies WHERE new_topic_id = ?',(id,))
    replies = [{'Id_of_Reply': row[0], 'Text_Reply': row[1],'Reply Creator': user_service.find_user_by_id(row[3]),'Reactions':f' UpVote {upvote_count(row[0])} / DownVote {downvote_count(row[0])}'} for row in nothing]
    return replies



def get_topic_author(topic_title: str):
    data = read_query('SELECT id_of_author FROM new_topic WHERE title = ?',
                           (topic_title,))
    author_id = data[0][0]
    author_name = user_service.get_username_by_user_id(author_id)

    return author_name



def add_reply_id_to_topic(topic_title: str, best_reply_id: int):
    update_query('UPDATE new_topic SET best_reply_id = ? WHERE title = ?',
                 (best_reply_id, topic_title))





























