import genanki
import html
import os
from PIL import Image
import io
import requests


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
    20482048,
    '麦花板v10',
    description='示例牌组⭐️整理by麦花⭐️<br>with genanki<br>点击答案页计时条可以暂停计时 可随时退出<br><a href="https://github.com/ystkc/Anki-Cereanilla">Github项目地址</a><br>qq 1612162886 请备注anki')



fields = [html.escape(f) for f in [f'33554432', f'(13111)[中华文化] 独化{{c1::}}', '', f'Self-driven Development||Overly Crafted -- 画工||Aesthetic Conception -- 意境||Latent Sentiment and Evident Beauty -- 隐秀', '1', '可以使用数字键盘1-4选选项、选择重来-简单、数字键盘0可打开设置页面（需要保持Num灯熄灭状态）', '示例单选 time_limit=30 review_limit=30']]
my_note = MyNote(
    model=my_model,
    fields=fields)
my_deck.add_note(my_note)



image_path = 'https://profile-avatar.csdnimg.cn/160b0897281f4c639395ebf6b0434848_qq_41019645.jpg!1'
thumb_name = f'thumb.jpg' 
thumb_path = f'./{thumb_name}'
if not os.path.exists(thumb_name):
    response = requests.get(image_path)
    image = Image.open(io.BytesIO(response.content))
    # 获取略缩图
    thumb_image = image.copy()
    thumb_image.thumbnail((100, 100))
    # 转换成RGB模式
    thumb_image = thumb_image.convert('RGB')
    thumb_image.save(thumb_path, 'JPEG')


fields = [html.escape(f) for f in [f'33554433', f'(11393)keen{{c1::}}', '', f'enthusiastic||passionate||megalith -- 巨石||eager', '1||2||4', 'keen有热情、渴望的意思，其中AB选项有热情含义、D有渴望含义，所以答案为ABD', '示例多选']]
fields[2] = f'<img src="{thumb_name}" onclick="updateImage(this, \'{thumb_name}\')">' # img要绕过escape，其他建议escape，updateImage用于加载网络原图，选填

media_files = [thumb_path]
# 重要！ anki的图片不含有任何路径，但mediafiles是包含路径的
my_note = MyNote(
    model=my_model,
    fields=fields)
my_deck.add_note(my_note)

# 输出文件名
my_package = genanki.Package(my_deck)
my_package.media_files = media_files
my_package.write_to_file(f'麦花板-v10.apkg')