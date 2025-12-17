from flask import Blueprint, render_template, session, jsonify, request
from flask_login import login_required, current_user
import random

lab9 = Blueprint('lab9', __name__)

BOX_COUNT = 10
BOX_SIZE = 120  
VIP_BOXES = {8, 9, 10}  

wishes = {
    1: "Желаю счастья, крепкого здоровья и душевного тепла в новом году!",
    2: "Пусть новый год принесёт радость, удачу и исполнение заветных желаний",
    3: "Желаю успехов в учёбе и работе, уверенности в себе и вдохновения!",
    4: "Пусть каждый день нового года будет наполнен улыбками и хорошими новостями",
    5: "Желаю любви, гармонии и тепла в доме весь год!",
    6: "Пусть все мечты, даже самые смелые, начнут сбываться уже в этом году",
    7: "Желаю финансового благополучия, стабильности и уверенности в завтрашнем дне",
    8: "Пусть новый год подарит новые возможности и приятные сюрпризы!",
    9: "Желаю ярких эмоций, путешествий и незабываемых впечатлений",
    10: "Пусть в новом году рядом будут только искренние и добрые люди"
}
boxes = {
    i: {
        "opened": False,
        "text": wishes[i],
        "gift": f"lab9/gift{i}.jpg",
        "box": f"lab9/box{i}.png"
    }
    for i in range(1, BOX_COUNT + 1)
}

def intersects(a, b):
    return not (
        a['left'] + BOX_SIZE < b['left'] or
        a['left'] > b['left'] + BOX_SIZE or
        a['top'] + BOX_SIZE < b['top'] or
        a['top'] > b['top'] + BOX_SIZE
    )

def generate_positions():
    positions = {}
    for i in range(1, BOX_COUNT + 1):
        while True:
            pos = {"top": random.randint(80, 600 - BOX_SIZE), "left": random.randint(90, 1200 - BOX_SIZE)}
            if all(not intersects(pos, positions[j]) for j in positions):
                positions[i] = pos
                break
    return positions

@lab9.route('/lab9')
def lab9_page():
    session.setdefault('opened_count', 0)

    # Проверка типа данных, чтобы избежать ошибок
    if 'positions' not in session or not isinstance(session['positions'], dict):
        positions = generate_positions()
        session['positions'] = {str(k): v for k, v in positions.items()}
    else:
        try:
            positions = {int(k): v for k, v in session['positions'].items()}
        except Exception:
            positions = generate_positions()
            session['positions'] = {str(k): v for k, v in positions.items()}

    unopened_count = sum(not b['opened'] for b in boxes.values())
    return render_template(
        'lab9/index.html',
        boxes=boxes,
        positions=positions,
        unopened_count=unopened_count
    )

@lab9.route('/lab9/open', methods=['POST'])
def open_box():
    box_id = int(request.json['box_id'])

    if box_id in VIP_BOXES and not current_user.is_authenticated:
        return jsonify({"error": "Этот подарок доступен только авторизованным пользователям"})

    if session.get('opened_count', 0) >= 3:
        return jsonify({"error": "Можно открыть не более 3 подарков"})

    if boxes[box_id]['opened']:
        return jsonify({"error": "Этот подарок уже забрали"})

    boxes[box_id]['opened'] = True
    session['opened_count'] += 1

    return jsonify({
        "text": boxes[box_id]['text'],
        "gift": boxes[box_id]['gift'],
        "opened_left": sum(not b['opened'] for b in boxes.values())
    })

@lab9.route('/lab9/reset', methods=['POST'])
@login_required
def reset_boxes():
    for box in boxes.values():
        box['opened'] = False
    session['opened_count'] = 0
    session.pop('positions', None)
    return jsonify({"ok": True})
