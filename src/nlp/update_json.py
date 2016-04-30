import sys
sys.path.append("../")
from web_util import load_json, write_json

'''
category = {
    '0': '美食',
    '1': '景點',
    '2': '購物',
    '3': '攝影',
    '4': '古蹟',
    '5': '慶典'
}

term = {
    '一蘭拉麵': {
        'topic': ['美食'],
        'synonym': [],
        'coord': (32.1123123123, 34.12321334),
        'popularity': 50,
    },
    '淺草寺': {
        'topic': ['景點', '攝影', '古蹟'],
        'synonym': [],
        'coord': (32.1123123123, 34.12321334),
        'popularity': 200,
    }
}
'''

'''
category = load_json('category.json')
# do what you want about category
write_json(category, 'category.json')
'''

term = load_json('term.json')
for key in term.keys():
    term[key]['ref'] = [
        'https://www.ptt.cc/bbs/Japan_Travel/M.1461767347.A.EF8.html',
        'https://www.ptt.cc/bbs/Japan_Travel/M.1461767347.A.EF8.html',
        'https://www.ptt.cc/bbs/Japan_Travel/M.1461767347.A.EF8.html'
    ]

write_json(term, 'term.json')
