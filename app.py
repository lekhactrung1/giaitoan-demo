from flask import Flask, render_template, request
import numpy as np
import scipy.stats as stats
import re

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    problem_type = request.form['problem_type']
    
    if problem_type == 'simple_probability':
        favorable = int(request.form['favorable'])
        total = int(request.form['total'])
        result = favorable / total
        return render_template('result.html', result=f"Xác suất xảy ra sự kiện là: {result:.4f}")

    elif problem_type == 'mean_variance_std':
        data = list(map(float, request.form['data'].split()))
        mean = np.mean(data)
        variance = np.var(data)
        std_deviation = np.std(data)
        return render_template('result.html', result=f"Kỳ vọng: {mean:.4f}, Phương sai: {variance:.4f}, Độ lệch chuẩn: {std_deviation:.4f}")

    elif problem_type == 'binomial':
        n = int(request.form['n'])
        p = float(request.form['p'])
        k = int(request.form['k'])
        binom_prob = stats.binom.pmf(k, n, p)
        return render_template('result.html', result=f"Xác suất nhị thức là: {binom_prob:.4f}")

    elif problem_type == 'normal_distribution':
        mean = float(request.form['mean'])
        std_dev = float(request.form['std_dev'])
        x = float(request.form['x'])
        norm_prob = stats.norm.cdf(x, mean, std_dev)
        return render_template('result.html', result=f"Xác suất chuẩn là: {norm_prob:.4f}")

    elif problem_type == 'poisson':
        lambda_value = float(request.form['lambda'])
        k = int(request.form['k'])
        poisson_prob = stats.poisson.pmf(k, lambda_value)
        return render_template('result.html', result=f"Xác suất Poisson là: {poisson_prob:.4f}")

    elif problem_type == 'text_problem':
        text_input = request.form['text_input']
        result = process_text_problem(text_input)
        return render_template('result.html', result=result)

    return render_template('result.html', result="Chưa xác định được kết quả.")

def process_text_problem(text_input):
    text_input = text_input.lower()

    if 'xác suất' in text_input and 'kết quả thuận lợi' in text_input:
        favorable = extract_number_from_text(text_input, 'kết quả thuận lợi')
        total = extract_number_from_text(text_input, 'tổng số kết quả')
        if favorable is not None and total is not None:
            result = favorable / total
            return f"Xác suất xảy ra sự kiện là: {result:.4f}"

    elif 'kỳ vọng' in text_input and 'phương sai' in text_input:
        data = extract_numbers_from_text(text_input)
        if data:
            mean = np.mean(data)
            variance = np.var(data)
            std_deviation = np.std(data)
            return f"Kỳ vọng: {mean:.4f}, Phương sai: {variance:.4f}, Độ lệch chuẩn: {std_deviation:.4f}"

    return "Không thể nhận diện bài toán từ văn bản."

def extract_number_from_text(text, keyword):
    match = re.search(rf"{keyword}\s*(\d+)", text)
    if match:
        return int(match.group(1))
    return None

def extract_numbers_from_text(text):
    return list(map(float, re.findall(r"\d+", text)))

if __name__ == '__main__':
    app.run(debug=True)
