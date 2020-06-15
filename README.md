## The Chat without borders

This is a chat that utilises pretrained Hugging Face models to translate the message of a user 
and suggest the next word when the user is typing a message. The current supported translations 
can be found in `supported_languages.json` file.


### How does the translation work ?

The app uses the MarianMT model https://huggingface.co/transformers/model_doc/marian.html
from Hugging Face and pretrained weights from Helsinki-NLP https://huggingface.co/Helsinki-NLP`
to translate the messages of the users.


### How do you predict the next word?

For the prediction of the next word, 
we use GPT-2 model https://huggingface.co/transformers/model_doc/gpt2.html 
from Hugging face that has been developed by OpenAI.

#### Technologies

- Flask
- ReactJS
- PyTorch

#### Languages

- Python
- Javascript


### How can I run it?

#### API
First you need to install all the required libraries. Get inside the api folder and type:
```
pip install -r requirements.txt
```
And then start the app:
```
python -m src.app
```
#### UI
Similarly here you need first to get the ui folder and install the required libraries. In order to do that type:
```
npm install
```
And when this is done run the ui:
```
npm start
```

Now you just go to the http://localhost:3000 and enjoy :) 

### What is next ?

- Authentication of the user
