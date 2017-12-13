from collections import defaultdict
from urllib.request import urlopen
from bs4 import BeautifulSoup
from nltk import tokenize
import sys
import json
import markovify

URL = 'https://www.helpingwritersbecomeauthors.com/book-storystructure/story-structure-database-index/'

plot_points = [
    'Inciting Event',
    'First Plot Point',
    'First Pinch Point',
    'Midpoint',
    'Second Pinch Point',
    'Third Plot Point',
    'Climax',
    'Climactic Moment',
    'Resolution',
    'Notes',
]

query_formats = [
    'inciting-event',
    'first-plot-point',
    'first-pinch-point',
    'midpoint',
    'second-pinch-point',
    'third-plot-point',
    'climax',
    'climactic-moment',
    'resolution',
    'notes',
]

ignore = [
    'https://www.helpingwritersbecomeauthors.com/book-storystructure/story-structure-database-index/#books',
    'https://www.helpingwritersbecomeauthors.com/book-storystructure/story-structure-database-index/#movies',
    'https://www.helpingwritersbecomeauthors.com/book-storystructure/story-structure-database-index/#shorts',
    'https://www.helpingwritersbecomeauthors.com/book-storystructure/story-structure-database-index/#games'
]


def soupify(url):
    html = urlopen(url)
    soup = BeautifulSoup(html, 'lxml')
    return soup


def get_links(soup):
    link_list = []
    for data in soup.find_all('div', class_='entry-content'):
        for a in data.find_all('a'):
            href = a.get('href')
            if href is not None and href not in ignore:
                link_list.append(href)
    return link_list


def build_plot_dict(link_list):
    plot_dict = defaultdict(list)
    count = 0
    for link in link_list:
        print(count, '/', len(link_list))
        html = urlopen(link)
        soup = BeautifulSoup(html, 'lxml')
        for data in soup.find_all('div', class_='entry-content'):
            plot_point = ''
            for p in data.find_all('p'):
                text = p.text
                for point in plot_points:
                    if point in text:
                        plot_point = point
                if plot_point != '':
                    processed_text = process_text(text, plot_point)
                    if processed_text:
                        plot_dict[plot_point] = (
                            plot_dict[plot_point]
                            + processed_text
                        )
        count += 1

    return plot_dict


def process_text(text, plot_point):
    processed_text = None
    skip = False
    text = text.replace(plot_point + ': ', "")
    if text != 'None':
        for point in plot_points:
            if point in text:
                skip = True
        if 'Submitted' in text:
            skip = True
        if not skip:
            processed_text = tokenize.sent_tokenize(text)
    return processed_text


def process_plot_dict(plot_dict):
    for key in plot_dict:
        array = plot_dict[key]
        plot_dict[key] = list(set(array))
    return plot_dict


def write_plot_dict(file_name, plot_dict):
    with open(file_name, 'w') as f:
        json.dump(plot_dict, f)


def read_plot_dict(file_name):
    with open(file_name, 'r') as f:
        plot_dict = json.load(f)
    return plot_dict


def write_model(file_name, model):
    model_json = model.to_json()
    with open(file_name, 'w') as f:
        json.dump(model_json, f)


def read_model(file_name):
    with open(file_name, 'r') as f:
        model_json = json.load(f)
        model = markovify.NewlineText.from_json(
            model_json
        )
        return model


def build_model(plot_dict):
    for plot_point in plot_dict:
        text_list = plot_dict[plot_point]
        newline_text = '\n'.join(text_list)
        model = markovify.NewlineText(newline_text)
        file_name = plot_point.lower().replace(' ', '_') + '_model.json'
        write_model(file_name, model)


def build_sentence(model):
    sentence = model.make_sentence()
    return sentence


def get_plot_dict():
    file_name = 'plot_dict.json'
    try:
        plot_dict = read_plot_dict(file_name)
    except Exception:
        soup = soupify(URL)
        link_list = get_links(soup)
        plot_dict = build_plot_dict(link_list)
        plot_dict = process_plot_dict(plot_dict)
        write_plot_dict(file_name, plot_dict)
    return plot_dict


def get_model(plot_point):
    try:
        model = read_model(plot_point)
    except Exception:
        plot_dict = get_plot_dict()
        build_model(plot_dict)
        model = read_model(plot_point)
    return model


def main(ppoint):
    if ppoint:
        plot_point = ppoint
        if plot_point in query_formats:
            plot_point = plot_point.replace('-', '_') + '_model.json'
        model = get_model(plot_point)
        sentence = build_sentence(model)
        return sentence
    else:
        plot_dict = get_plot_dict()
        build_model(plot_dict)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        plot_point = sys.argv[1]
        if plot_point in query_formats:
            plot_point = plot_point.replace('-', '_') + '_model.json'
    sentence = main(plot_point)
    print(sentence)
