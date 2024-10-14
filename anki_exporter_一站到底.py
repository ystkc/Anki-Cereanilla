import genanki

with open('deck_templates/front.html', encoding='utf-8') as f:
    front_template = f.read()

with open('deck_templates/back.html', encoding='utf-8') as f:
    back_template = f.read()

with open('deck_templates/style.css', encoding='utf-8') as f:
    my_style = f.read()

my_model = genanki.Model(
  283560010,
  '选择题by麦花⭐️(v10)',
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
      'name': '选择题by麦花⭐️(v10)',
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
    283560401,
    '一站到底',
    description='⭐️整理by麦花⭐️<br>on麦花板v10<br>with genanki')

import sqlite3
import requests
import html
import os
from PIL import Image

conn = sqlite3.connect('../BCZ-Automata/yzdd.db')
c = conn.cursor()
# 查询数据条数
c.execute("SELECT COUNT(*) FROM yzdd")
count = c.fetchone()[0]
id_start = input("请输入起始ID(最低1):")
id_end = input(f"请输入结束ID({count}):")
c.execute("SELECT * FROM yzdd WHERE INDEX_ID >= ? AND INDEX_ID <= ?", (id_start, id_end))
rows = c.fetchall()
# 添加教程卡片

media_files = []
cloze_str = '{{c1::}}'
for row in rows:
    id = row[0]
    qid = row[1]
    image_url = row[2]
    title = row[3]
    answer = row[4]
    option_2 = row[5]
    option_3 = row[6]
    option_4 = row[7]
    detail = row[8]
    print('id:', id)
    print('qid:', qid)
    print('image_url:', image_url)
    print('title:', title)
    print('answer:', answer)
    print('option_2:', option_2)
    print('option_3:', option_3)
    print('option_4:', option_4)
    print('detail:', detail)
    # 下载图片到本地，压缩到100px * 100px再写入文件
    img_format = image_url.split('.')[-1]
    img_name = str(qid) + '.' + img_format
    img_path = os.path.join('download', img_name)
    img_compressed_name = str(qid) + '_compressed.' + img_format
    img_compressed_path = os.path.join('download', img_compressed_name)
    if not os.path.exists(img_path):
        r = requests.get(image_url, stream=True)
        with open(img_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
    # 压缩图片
    if not os.path.exists(img_compressed_path):
        img = Image.open(img_path)
        img.thumbnail((100, 100))
        img.save(img_compressed_path)
    media_files.append(img_compressed_path)
    # 构造卡片
    fields = [html.escape(f) for f in [f'{id}', f'({qid}){title}{cloze_str}', '', f'{answer}||{option_2}||{option_3}||{option_4}', '1', detail, 'tag time_limit=9 review_limit=9']]
    # 图片居中显示
    fields[2] = f'<img style="width:100px;margin:10px;" src="{img_compressed_name}" onclick="updateImage(this, \'{image_url}\')">'
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
my_package.write_to_file(f'apkg/2024一站到底-{time_str}({id_start}-{id_end}).v10.apkg')