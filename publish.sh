cd ~/LogicGate/LogicGate
poetry update
poetry build
poetry publish -u __token__ -p $PYPI_API_KEY