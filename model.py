import genanki

chinese_vocab_model = genanki.Model(
  1607392320,
  'Chinese Vocab Model',
  fields=[
    {'name': 'Word'},
    {'name': 'Meaning'},
    {'name': 'ColorWord'},
    {'name': 'ColorPinyin'}
  ],
  templates=[
    {
      'name': 'Recognition',
      'qfmt': '''
        <div class="card-container">
          <div class="question">{{Word}}</div>
        </div>
      ''',
      'afmt': '''
        {{FrontSide}}
        <hr>
        <div class="card-container answer-side">
          <div class="colored-word">{{ColorWord}}</div>
          <div class="colored-pinyin">{{ColorPinyin}}</div>
          <div class="meaning">{{Meaning}}</div>
        </div>
      '''
    },
  ],
  css="""
    .card {
      font-family: 'Arial', sans-serif;
      font-size: 24px;
      color: #333;
      background-color: white;
      text-align: center;
      padding: 20px;
    }

    .card-container {
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
    }

    .question {
      font-size: 48px;
      font-weight: bold;
      margin: 30px 0;
    }

    .answer-side {
      margin-top: 40px;
    }

    .colored-word span,
    .colored-pinyin span {
      font-size: 42px;
      font-weight: bold;
      margin: 0 5px;
    }

    .meaning {
      font-size: 20px;
      color: #666;
      margin-top: 25px;
    }
  """
)
