import os
import json
import time

import jinja2
import shutil
import matplotlib.pyplot as plt


if __name__ == '__main__':

    start = time.time()

    if not os.path.isdir('static'):
        os.mkdir('static')

    template_loader = jinja2.FileSystemLoader(searchpath="templates")
    template_env = jinja2.Environment(loader=template_loader)

    template = template_env.get_template('template.html')

    report_path = '/Users/simone/Develop/buildsystem/AutomaticTests/allure-results'

    print('Reading tests...')

    tests = []
    for filename in os.listdir(report_path):
        f = os.path.join(report_path, filename)
        # checking if it is a file
        if f.endswith("-result.json") and os.path.isfile(f):
            tests.append(f)
        if f.endswith("-attachment") and os.path.isfile(f):
            shutil.copy(f, "static/" + filename)

    summary = {}
    results = []
    for file in tests:
        with open(file, 'rb') as in_file:
            test_result = json.load(in_file)
            test_status = test_result['status']

            if test_status not in summary:
                summary[test_status] = 1
            else:
                summary[test_status] += 1
            results.append(test_result)

    labels = summary.keys()
    sizes = summary.values()

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    chart_path = 'static/pie_chart.png'
    plt.savefig(chart_path)

    html = template.render(tests=results, path=report_path, summary=chart_path)

    print(summary)

    # 5. Write the template to an HTML file
    with open('html_report_jinja.html', 'w') as f:
        f.write(html)

    print('HTML generated!')
    print('Time elapsed in seconds: ' + str(time.time()-start))
