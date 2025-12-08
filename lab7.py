from flask import Blueprint, render_template, request

lab7 = Blueprint('lab7', __name__)

@lab7.route('/lab7/')
def lab():
    return render_template('lab7/lab7.html')



films = [
    {
        "title": "Inception",
        "title_ru": "Начало",
        "year": 2010,
        "description": "Кобб — профессиональный вор, извлекающий секреты из подсознания во сне. "
                       "Ему предлагают невозможное — не украсть идею, а внедрить её, чтобы получить "
                       "шанс вернуться к детям."
    },
    {
        "title": "Spirited Away",
        "title_ru": "Унесённые призраками",
        "year": 2001,
        "description": "Девочка Тихиро попадает в мир духов и богов и вынуждена работать в волшебной купальне, "
                       "чтобы спасти своих родителей и найти дорогу домой."
    },
    {
        "title": "The Dark Knight",
        "title_ru": "Тёмный рыцарь",
        "year": 2008,
        "description": "Бэтмен сталкивается с новым противником — Джокером, чья цель не деньги и власть, "
                       "а полный хаос. Герою приходится выбирать между принципами и спасением города."
    },
    {
        "title": "Your Name",
        "title_ru": "Твоё имя",
        "year": 2016,
        "description": "Двое подростков из разных городов начинают загадочно меняться телами. "
                       "Пытаясь разобраться в происходящем, они постепенно понимают, что связаны "
                       "куда глубже, чем им казалось."
    },
    {
        "title": "Whiplash",
        "title_ru": "Одержимость",
        "year": 2014,
        "description": "Молодой барабанщик мечтает стать великим музыкантом и попадает в ансамбль "
                       "к жесткому и требовательному преподавателю, который доводит учеников до предела."
    }
]



@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return films



@lab7.route('/lab7/rest-api/films/<int:id>/', methods=['GET'])
def get_film(id):
    if id < 0 or id >= len(films):
        return '', 404
    return films[id]



@lab7.route('/lab7/rest-api/films/<int:id>/', methods=['DELETE'])
def del_film(id):
    if id < 0 or id >= len(films):
        return '', 404

    del films[id]
    return '', 204



@lab7.route('/lab7/rest-api/films/<int:id>/', methods=['PUT'])
def put_film(id):

    if id < 0 or id >= len(films):
        return '', 404

    film = request.get_json()

    if film.get('description', '') == '':
        return {'description': 'Заполните описание'}, 400

    if film.get('title') == '' and film.get('title_ru'):
        film['title'] = film['title_ru']

    films[id] = film
    return films[id]



@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()

    if film.get('title') == '' and film.get('title_ru'):
        film['title'] = film['title_ru']
        
    films.append(film)
    return str(len(films) - 1)
