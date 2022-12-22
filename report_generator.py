import time

import argparse
import report_utils

if __name__ == '__main__':
    my_parser = argparse.ArgumentParser(description='Generate HTML report for Allure results')

    # Add the arguments
    my_parser.add_argument('allure_result_path',
                           type=str,
                           help='Allure result path')
    my_parser.add_argument('-o', '--output', help='Output filename (default: index.html)')

    # TODO: add filters
    # my_parser.add_argument('-f', '--filters', help='Label filters')

    args = my_parser.parse_args()

    start = time.time()

    result, summary = report_utils.parse_tests(args.allure_result_path)
    chart = report_utils.generate_google_chart(summary)
    report_utils.render_template(args.output or 'index.html', result, summary, chart)

    print('HTML generated!')
    print('Time elapsed in seconds: ' + str(time.time() - start))
