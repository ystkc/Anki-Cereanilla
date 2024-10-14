import genanki

with open('deck_templates/front.html', encoding='utf-8') as f:
    front_template = f.read()

with open('deck_templates/back.html', encoding='utf-8') as f:
    back_template = f.read()

with open('deck_templates/style.css', encoding='utf-8') as f:
    my_style = f.read()

my_model = genanki.Model(
  283560010,
  '选择题by麦花⭐️(on麦花板v10)',
  fields=[
    {'name': 'yzdd_id'},
    {'name': 'question'},
    {'name': 'image'},
    {'name': 'options'},
    {'name': 'answer'},
    {'name': 'notes'},
    {'name': 'Tags'}
  ],
  templates=[
    {
      'name': '选择题by麦花⭐️(on麦花板v10)',
      'qfmt': front_template,
      'afmt': back_template,
    },
  ],
  css=my_style)

class MyNote(genanki.Note):
  @property
  def guid(self):
    return genanki.guid_for(self.fields[0], self.fields[1])
  
my_deck = genanki.Deck(
    20242048,
    '单词竞赛2024',
    description='BCZ_NCSVC2024<br>⭐️整理by麦花⭐️<br>with genanki<br>点击答案页计时条可以暂停计时 可随时退出')


def has_chinese(s):
    for ch in s:
        if '\u4e00' <= ch <= '\u9fff':
            return True
    return False

import sqlite3
import html
import os

conn = sqlite3.connect('../BCZ-Automata/puzzle.db')
c = conn.cursor()
# 加载整个数据库，便于反相查找（即查找干扰项作为答案时对应的题目）
c.execute("SELECT QUESTION, ANSWER FROM BCZ_NCSVC")
rows = c.fetchall()
cor_word_dict = {}
for row in rows:
    row_0 = row[0].strip()
    row_1 = row[1].strip()
    if '{t3}' in row_0:
        continue
    elif '{' in row_0:
        # 提取出{}中的内容
        row_0 = row_0[row_0.index('{')+1:row_0.index('}')]
    elif '[' in row_0:
        row_0 = row_0[7:]
    elif has_chinese(row_0):
        ...
    elif has_chinese(row_1):
        ...
    else:
        continue
    if row_0 in cor_word_dict:
        if row_1 not in cor_word_dict[row_0].split(' | '):
            cor_word_dict[row_0] += f' | {row_1}'
    else:
        cor_word_dict[row_0] = row_1
    if row_1 in cor_word_dict:
        if row_0 not in cor_word_dict[row_1].split(' | '):
            cor_word_dict[row_1] += f' | {row_0}'
    else:
        cor_word_dict[row_1] = row_0

def get_cor_word(s):
    result = cor_word_dict.get(s, '')
    return f' -- {result}' if result else ''


# 查询数据条数
c.execute("SELECT COUNT(*) FROM BCZ_NCSVC")
count = c.fetchone()[0]
id_start = input("请输入起始ID(最低1):")
id_end = input(f"请输入结束ID({count}):")
c.execute("SELECT * FROM BCZ_NCSVC WHERE INDEX_ID >= ? AND INDEX_ID <= ?", (id_start, id_end))
rows = c.fetchall()

media_files = []
cloze_str = '{{c1::}}'


for row in rows:
    id = row[0]
    qid = row[1]
    title = row[2]
    chn_mean = row[3]
    answer = row[4]
    option_2 = row[5]
    option_3 = row[6]
    option_4 = row[7]
    topic_id = row[8]
    # print('id:', id)
    # print('qid:', qid)
    # print('title:', title)
    # print('answer:', answer)
    # print('option_2:', option_2)
    # print('option_3:', option_3)
    # print('option_4:', option_4)
    # 构造卡片
    tag = ''
    if '{t3}' in title: # 例句填词
        tag = '1例句填词 time_limit=6 review_limit=0.7,5,5' # review_limit实际上3个参数，默认为-1,-1,-1，表示暂停
    elif '{' in title: # 例句选义
        tag = '2例句选义 time_limit=6 review_limit=0.7,5,5'
    elif '[' in title: # 中华文化
        tag = '3中华文化 time_limit=6 review_limit=5,5,5'
    elif has_chinese(title): # 中文选词
        tag = '4中文选词 time_limit=6 review_limit=0.7,5,5'
    elif has_chinese(answer): # 单词选义
        tag = '5单词选义 time_limit=6 review_limit=0.7,5,5'
    else : # 同义替换
        tag = '6同义替换 time_limit=6 review_limit=0.7,5,5'
    
    option_2 += get_cor_word(option_2)
    option_3 += get_cor_word(option_3)
    option_4 += get_cor_word(option_4)
    fields = [html.escape(f) for f in [f'{id}', f'({qid}){title}{cloze_str}', '', f'{answer}||{option_2}||{option_3}||{option_4}', '1', '', tag]]
    my_note = MyNote(
        model=my_model,
        fields=fields)
    my_deck.add_note(my_note)
    print(f'已添加第{id}/{id_end}个卡片({qid})')
    # if input("按任意键继续...") == 'q':
    #     break
    


import time
time_str = time.strftime('第%U周', time.localtime(time.time()))
# 输出文件名    
my_package = genanki.Package(my_deck)
my_package.media_files = media_files
os.makedirs('apkg', exist_ok=True)
my_package.write_to_file(f'apkg/{time_str}-BCZ-NCSVC2024({id_start}-{id_end}-v10).apkg')