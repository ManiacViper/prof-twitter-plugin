#!/bin/bash          

echo Removing plugin deployment in profanity plugins folder
rm -rf ~/.local/share/profanity/plugins/lib/
rm -rf ~/.local/share/profanity/plugins/src/main-twitter.py
rm -rf ~/.local/share/profanity/plugins/src/main-twitter.pyc
ls  ~/.local/share/profanity/plugins/

echo Copying plugin to profanity plugins folder
cp -r src/ ~/.local/share/profanity/plugins/main-twitter.py
cp -r lib/ ~/.local/share/profanity/plugins/
ls  ~/.local/share/profanity/plugins/

