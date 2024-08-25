#!/bin/bash

echo "Running setup script..."

pipx install poetry
pip install typing-extensions
poetry init -n
git clone https://github.com/algorandfoundation/algokit-utils-py.git
cd algokit-utils-py
pip install .
cd ..

echo "Setup completed."
