from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

def get_day_of_week(day, month, year):
    last_year = year - 1
    cycles_of_400 = last_year // 400
    remaining_years = last_year % 400

    if remaining_years < 100:
        major_year = remaining_years
    elif remaining_years >= 300:
        major_year = 300
    elif remaining_years >= 200:
        major_year = 200
    else:
        major_year = 100

    leap_years = major_year // 4 - major_year // 100 + major_year // 400
    non_leap_years = major_year - leap_years
    odd_days_from_major = (leap_years * 2 + non_leap_years) % 7

    remaining_after_major = remaining_years - major_year
    leap_years_left = remaining_after_major // 4 - remaining_after_major // 100 + remaining_after_major // 400
    non_leap_years_left = remaining_after_major - leap_years_left
    odd_days_from_left = (leap_years_left * 2 + non_leap_years_left) % 7

    total_odd_days = (odd_days_from_major + odd_days_from_left) % 7

    days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    
    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
        days_in_month[1] = 29
    
    days_up_to_month = sum(days_in_month[:month - 1]) + day
    odd_days_in_month = days_up_to_month % 7

    final_day = (total_odd_days + odd_days_in_month) % 7
    
    day_names = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    
    return day_names[final_day]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_day", methods=["POST"])
def get_day():
    data = request.get_json()
    day = int(data["date"])
    month = int(data["month"])
    year = int(data["year"])

    day_name = get_day_of_week(day, month, year)
    return jsonify(message=day_name)

if __name__ == "__main__":
    app.run(debug=True)
