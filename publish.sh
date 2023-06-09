cd ~/LogicGate/LogicGate
rm -r dist
poetry update
poetry publish --build -vvv -u __token__ -p $PYPI_API_KEY