import genanki

with open('deck_templates/front.html', encoding='utf-8') as f:
    front_template = f.read()

with open('deck_templates/back.html', encoding='utf-8') as f:
    back_template = f.read()

with open('deck_templates/style.css', encoding='utf-8') as f:
    my_style = f.read()

my_model = genanki.Model(
  283560401,
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
    283560401,
    '一站到底',
    description='⭐️整理by麦花⭐️<br>on麦花板v10<br>with genanki')