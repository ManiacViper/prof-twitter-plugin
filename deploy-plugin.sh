#!/bin/bash          

echo Removing plugin deployment in profanity plugins folder
rm -rf ~/.local/share/profanity/plugins/lib/
rm -rf ~/.local/share/profanity/plugins/*.py
rm -rf ~/.local/share/profanity/plugins/*.pyc
ls  ~/.local/share/profanity/plugins/

echo Copying plugin to profanity plugins folder
mkdir -p ~/.local/share/profanity/plugins/lib
cp -r lib/*.py ~/.local/share/profanity/plugins/lib/
cp -r src/*.py ~/.local/share/profanity/plugins/
ls -R ~/.local/share/profanity/plugins/

