import os
import shutil
import json
import matplotlib.pyplot as plt
import jinja2


def init():
    if not os.path.isdir('static'):
        os.mkdir('static')


def parse_tests(allure_path):
    init()
    parsed_tests = []
    summary = {}

    for filename in os.listdir(allure_path):
        f = os.path.join(allure_path, filename)
        # checking if it is a file
        if f.endswith("-result.json") and os.path.isfile(f):

            with open(f, 'rb') as in_file:
                test_result = json.load(in_file)
                test_status = test_result['status']

                if test_status not in summary:
                    summary[test_status] = 1
                else:
                    summary[test_status] += 1
                parsed_tests.append(test_result)

        if f.endswith("-attachment") and os.path.isfile(f):
            shutil.copy(f, "static/" + filename)

    return parsed_tests, summary


def generate_chart(summary):
    labels = summary.keys()
    sizes = summary.values()

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    chart_path = 'static/pie_chart.png'
    plt.savefig(chart_path)

    return chart_path


def render_template(out, results, report_path, chart_path):
    template_loader = jinja2.FileSystemLoader(searchpath="templates")
    template_env = jinja2.Environment(loader=template_loader)

    template = template_env.get_template('template.html')
    html = template.render(tests=results, path=report_path, summary=chart_path)

    with open(out, 'w') as f:
        f.write(html)