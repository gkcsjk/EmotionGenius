import csv
import os

fieldnames = ["Location", "Date", "Time",
              "neutral", "fear/stress", "happiness/surprise",
              "sadness/disgust", "anger"]


def save_result(result, path):
    try:
        with open(path, "ab") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            for row in result:
                writer.writerow(row)
    except Exception:
        return False
    else:
        return True


def create_csv(path):
    path = os.path.join(path, "results.csv")
    with open(path, 'wb+') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
    return path


def process_results(location, date, time, results):
    ans_rows = []
    ans_row = {}
    for result in results:
        ans_row['Location'] = location
        ans_row['Date'] = date
        ans_row['Time'] = time
        ans_row['neutral'] = result['scores']['neutral'] + result['scores']['contempt']
        ans_row['fear/stress'] = result['scores']['fear']
        ans_row['happiness/surprise'] = result['scores']['happiness'] + result['scores']['surprise']
        ans_row['sadness/disgust'] = result['scores']['sadness'] + result['scores']['disgust']
        ans_row['anger'] = result['scores']['anger']
        ans_rows.append(ans_row)

    return ans_rows
