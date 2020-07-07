import pandas as pd
import io
import requests
import urllib
from datetime import datetime
import matplotlib.pyplot as plt
import bs4

def get_table():
    url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSXOMQqsU8jk06Kre9A7QgRiAEw6GbLOWn0G75zzOMRbijlelTiuOMRHW43n6IMGtFlchdMjcR2uXAU/pub?output=csv'
    s = requests.get(url).content
    df = pd.read_csv(io.StringIO(s.decode('utf-8')))

    return df

def get_imgs():
    df = get_table().to_dict()

    for i in range(len(df['img'])):
        try:
            img = urllib.request.urlopen(df['img'][i]).read()
            f = open('img/' + df['ans'][i] + '.jpg','w')
            f.close()
            f = open('img/' + df['ans'][i] + '.jpg', 'rb+')
            f.write(img)
            f.close()
            print(df['ans'][i], ' - ok')
        except:
            print(df['ans'][i], ' - error with', df['img'][i])


def add_result(user_id, score):
    url = 'data/score.pickle'
    try:
        df = pd.read_pickle(url)
    except:
        df = pd.DataFrame(columns=['id', 'result', 'time']).set_index('time')
    df = df.append({'id': user_id, 'result': score, 'time': datetime.today()}, ignore_index=True)

    df.to_pickle(url)


def get_history(user_id):
    url = 'data/score.pickle'
    try:
        df = pd.read_pickle(url)
    except:
        df = pd.DataFrame(columns=['id', 'result', 'time']).set_index('time')
        print('\033[0;31m', url, ' - opening error', '\033[0m')

    df = df.loc[df.id == user_id, ['result']]
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.plot(df, 'o-')
    plt.xticks(rotation=60)
    fig.tight_layout()

    plt.savefig('img/%s.png' % user_id, dpi=100)
    plt.show()

def get_user_name_from_vk_id(user_id):
    request = requests.get("https://vk.com/id" + str(user_id))
    bs = bs4.BeautifulSoup(request.text, "html.parser")

    user_name = _clean_all_tag_from_str(bs.findAll("title")[0])

    return user_name.split("|")[0]


def _clean_all_tag_from_str(string_line):

    result = ""
    not_skip = True
    for i in list(string_line):
        if not_skip:
            if i == "<":
                not_skip = False
            else:
                result += i
        else:
            if i == ">":
                not_skip = True

    return result




