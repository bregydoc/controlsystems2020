rm -rfd dist/*
python setup.py sdist bdist_wheel
python -m twine upload dist/*
sleep 25
pipenv update control2020