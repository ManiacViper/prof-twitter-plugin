#!/bin/bash          

echo Removing plugin deployment in profanity plugins folder
rm -rf ~/.local/share/profanity/plugins/lib/
rm -rf ~/.local/share/profanity/plugins/src/*.py
rm -rf ~/.local/share/profanity/plugins/src/*.pyc
ls  ~/.local/share/profanity/plugins/

echo Copying plugin to profanity plugins folder
cp -r src/*.py ~/.local/share/profanity/plugins/
cp -r lib/*.py ~/.local/share/profanity/plugins/
ls  ~/.local/share/profanity/plugins/

