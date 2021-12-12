""" Log files analyzer for queen algorihm performance. """
import os
import re
import json


def get_value_for_key(text_buffer, key):
    """Parsing value from a line with key=value"""
    for match in re.finditer("%s=(?P<value>.*)" % key, text_buffer):
        return match.group('value')
    return ""


def process_buffer(text_buffer, language, distribution, url):
    """ parse log files for queen algorithm performance details. """
    data = []
    print("language={0}, distribution={1}, url={2}"
          .format(language, distribution, url))

    source = get_value_for_key(text_buffer, 'SOURCE')
    assert len(source) > 0
    version = get_value_for_key(text_buffer, 'VERSION')
    assert len(version) > 0
    timestamp = get_value_for_key(text_buffer, 'TIMESTAMP')

    if len(timestamp) == 0:
        timestamp = "0"

    expression = r"Queen raster \((?P<n1>\d*)x(?P<n2>\d*)\)"
    expression += r"\n...took (?P<duration>\d*\.\d*) seconds."
    expression += r"\n...(?P<solutions>\d*) solutions found."

    for match in re.finditer(expression, text_buffer):
        data.append({
            'language': language,
            'url': url,
            'distribution': distribution,
            'chessboard-width': int(match.group("n1")),
            'durations': {str(timestamp): float(match.group('duration'))},
            'solutions': int(match.group('solutions')),
            'source': source,
            'version': version
        })

    assert len(data) > 0
    return data


def process_descriptor(text_buffer, descriptor):
    """ parsing test buffer for details. """
    return process_buffer(text_buffer,
                          descriptor['language'],
                          descriptor['distribution'],
                          descriptor['url'])

def find_data(all_data, entry):
    for data in all_data:
        if data["chessboard-width"] != entry["chessboard-width"]:
            continue
        if data["language"] != entry["language"]:
            continue
        if data["version"] != entry["version"]:
            continue
        if data["source"] != entry["source"]:
            continue
        return data
    return None


def update_data(old_data, new_data):
    """Updating existing or adding new data."""
    for new in new_data:
        old = find_data(old_data, new)
        if old:
            old['durations'].update(new['durations'])
        else:
            old_data.append(new)


def main():
    """ application entry point. """
    options = json.loads(open("analyse.json").read())
    descriptors = options['descriptors']

    if os.path.isfile("results/results.json"):
        data = json.loads(open("results/results.json").read())
    else:
        data = []

    for entry in os.listdir("results"):
        if entry.endswith(".log"):
            full = os.path.join(os.getcwd(), "results", entry)
            text_buffer = open(full).read()

            for descriptor in descriptors:
                if entry.find(descriptor['key']) >= 0:
                    update_data(data, process_descriptor(text_buffer, descriptor))
                    break

    with open("results/results.json", "w") as handle:
        handle.write(json.dumps(data, indent=2))

if __name__ == "__main__":
    main()
