# If On A Winters Night a Traveler

## Casual NLG GUI app

Easy to use GUI wrapper for running NLG models from HuggingFace locally. 

![Screenshot](/UI.png?raw=true)

Main third party libraries are PySimpleGUI and
aitextgen

Provide a string of text as a prompt (or don't), modify the generator's parameters, and press "Generate." Can generate up to 20 strings at a time of 750 word length without modification. The more strings and the longer they are, the more time is required.

The models run on your CPU (for now) and can be quite large, so I deliberately restricted the list of available models, but you could easily expand it. This app lets you choose where models are stored as well.

Please remember to use a virtual environment. 
