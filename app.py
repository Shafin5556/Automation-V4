from flask import Flask, render_template, request, jsonify
import json
import os

app = Flask(__name__)

def load_schedule():
    if os.path.exists('schedule.json'):
        with open('schedule.json', 'r') as json_file:
            return json.load(json_file)
    else:
        return {"schedule": []}

def save_schedule(schedule):
    with open('schedule.json', 'w') as json_file:
        json.dump(schedule, json_file, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate_json', methods=['POST'])
def generate_json():
    schedule = load_schedule()
    day_schedule = None
    
    for key, value in request.form.items():
        if key.startswith('day'):
            day = value
            day_schedule = None
            # Check if the day already exists in the schedule
            for entry in schedule["schedule"]:
                if entry["day"] == day:
                    day_schedule = entry
                    break
            # If the day doesn't exist, create a new day schedule entry
            if day_schedule is None:
                day_schedule = {"day": day, "time_slots": []}
                schedule["schedule"].append(day_schedule)
            continue
        
        # Skip if day_schedule is not set yet
        if day_schedule is None:
            continue
            
        if key.startswith('room'):
            room_num = key[len('room'):]
            room = value
            course = request.form.get(f'course{room_num}')
            teacher = request.form.get(f'teacher{room_num}')
            time_slot = request.form.get(f'time_slot{room_num}')
            if room and course and teacher and time_slot:
                # Find or create a time slot entry for the given time
                time_slot_entry = None
                for slot in day_schedule["time_slots"]:
                    if slot["time"] == time_slot:
                        time_slot_entry = slot
                        break
                if time_slot_entry is None:
                    time_slot_entry = {"time": time_slot, "rooms": []}
                    day_schedule["time_slots"].append(time_slot_entry)
                
                # Add room, course, and teacher to the time slot entry
                time_slot_entry["rooms"].append({
                    'room': room,
                    'course': course,
                    'teacher': teacher
                })

    save_schedule(schedule)
    
    return jsonify(schedule)


if __name__ == "__main__":
    app.run(debug=True)
