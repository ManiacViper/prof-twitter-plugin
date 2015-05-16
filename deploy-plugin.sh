#!/bin/bash          

rm -rf ~/.local/share/profanity/plugins/lib/
rm -rf ~/.local/share/profanity/plugins/src/main-twitter.py
rm -rf ~/.local/share/profanity/plugins/src/main-twitter.pyc

cp -r src/ ~/.local/share/profanity/plugins/main-twitter.py
cp -r lib/ ~/.local/share/profanity/plugins/

