import random
from flask import Flask, render_template, request

app = Flask(__name__)

# ------------------------------------------------------------------
# 食物資料庫 ( List 包 Dict )
# 欄位：名稱、價格、熱量(kcal)、蛋白質(g)、國健署順序分類(豆/魚/蛋/肉)
# ------------------------------------------------------------------
FOOD_DATABASE = [
    {"name": "高纖無糖豆漿", "price": 25, "calories": 160, "protein": 15, "category": "豆"},
    {"name": "涼拌毛豆仁", "price": 35, "calories": 110, "protein": 9, "category": "豆"},
    {"name": "滷豆腐", "price": 20, "calories": 90, "protein": 7, "category": "豆"},
    {"name": "水煮鮭魚菲力", "price": 85, "calories": 220, "protein": 24, "category": "魚"},
    {"name": "鮮魚味噌湯", "price": 45, "calories": 120, "protein": 12, "category": "魚"},
    {"name": "茶葉蛋", "price": 13, "calories": 75, "protein": 7, "category": "蛋"},
    {"name": "石安牧場溫泉蛋", "price": 32, "calories": 80, "protein": 8, "category": "蛋"},
    {"name": "即食舒肥雞胸肉", "price": 59, "calories": 140, "protein": 23, "category": "肉"},
    {"name": "美式烤雞腿", "price": 65, "calories": 280, "protein": 20, "category": "肉"},
    {"name": "經典牛丼便當", "price": 95, "calories": 650, "protein": 25, "category": "肉"}
]

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    error_message = None
    warning_message = None
    recommended_item = None

    if request.method == 'POST':
        budget_raw = request.form.get('budget', '').strip()
        max_calories_raw = request.form.get('max_calories', '').strip()
        preferred_category = request.form.get('category', 'ALL')

        # 防呆驗證
        if not budget_raw or not max_calories_raw:
            error_message = "請完整輸入預算與熱量上限！"
        else:
            try:
                budget = int(budget_raw)
                max_calories = int(max_calories_raw)

                if budget <= 0 or max_calories <= 0:
                    error_message = "預算與熱量必須為大於 0 的正整數！"
                elif max_calories < 300:
                    warning_message = "健康提醒：成年人單餐熱量建議不低於 300 大卡，過度節食可能影響健康喔！"
            except ValueError:
                error_message = "請輸入有效的數字（不可以填寫文字或符號）！"

        # 資料篩選邏輯
        if not error_message:
            for food in FOOD_DATABASE:
                if food['price'] <= budget and food['calories'] <= max_calories:
                    if preferred_category == 'ALL' or food['category'] == preferred_category:
                        results.append(food)

            if results:
                recommended_item = random.choice(results)
            else:
                warning_message = "在您設定的條件下找不到合適的餐點，建議提高預算或放寬熱量限制！"

    return render_template(
        'index.html',
        results=results,
        error_message=error_message,
        warning_message=warning_message,
        recommended_item=recommended_item
    )

if __name__ == '__main__':
    app.run(debug=True)
