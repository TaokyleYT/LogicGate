cd ~/LogicGate/LogicGate
rm -r dist
poetry update
poetry build
poetry publish -u __token__ -p $PYPI_API_KEY