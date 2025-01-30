# PDFTranslator
A software that uses deepl's translation api to translate pdf documents

If you want to use this program, you need to make an account at deepl.com and get an API key.

Remove this line:

```Python
from config import api_key as key
```

In the translate() function you can change this line

```Python
api_key = key
```

To

```Python
api_key = "your-api-key-here"
```

-------------------------------------------------------------------------------------
#How it works

Takes in a PDF File

![Image](https://github.com/user-attachments/assets/e6e121a6-5b7d-4462-a0d4-aff365a10fe6)

![Image](https://github.com/user-attachments/assets/0a25397c-0e16-4286-a778-28651ebd0779)

Choose a language

![Image](https://github.com/user-attachments/assets/51ff7b46-65c5-450d-b2d6-edc5d6c55a69)

Translate

![Image](https://github.com/user-attachments/assets/e451da54-c639-4060-8385-00cd2178a97b)

And you have a translated version of the document!

![Image](https://github.com/user-attachments/assets/ee89b196-a9ed-442e-9221-8e8e64fd97a0)
