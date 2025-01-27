"""
ChronoWeek 核心服务
作者：liqian_liukaining
日期：2025-01-27
"""
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import re

app = Flask(__name__)


# 日期验证器
class DateValidator:
    @staticmethod
    def validate(date_str):
        """执行双重日期验证"""
        # 格式校验
        if not re.match(r'^\d{4}[-\/]\d{2}[-\/]\d{2}$', date_str):
            return False, "格式错误：请使用YYYY-MM-DD或YYYY/MM/DD"

        # 物理日期校验
        try:
            date = datetime.strptime(date_str.replace('/', '-'), '%Y-%m-%d')
            if date.year > 9999 or date.year < 1:
                raise ValueError("年份超出范围")
            return True, date
        except ValueError:
            return False, "非法日期：日期不存在"


# 星期转换器
class WeekdayConverter:
    WEEKDAY_MAP = {
        "Monday": "星期一",
        "Tuesday": "星期二",
        "Wednesday": "星期三",
        "Thursday": "星期四",
        "Friday": "星期五",
        "Saturday": "星期六",
        "Sunday": "星期日"
    }

    @classmethod
    def to_chinese(cls, date_obj):
        """转换日期对象为中文星期"""
        return cls.WEEKDAY_MAP[date_obj.strftime("%A")]


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        date_str = request.form.get('date', '')
        is_valid, result = DateValidator.validate(date_str)

        if is_valid:
            return jsonify({
                'success': True,
                'date': result.strftime("%Y年%m月%d日"),
                'weekday': WeekdayConverter.to_chinese(result)
            })
        else:
            return jsonify({'success': False, 'error': result})
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)