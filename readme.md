Waveform Necklace
=================

Installation
------------
If you're running on OS X:

1. brew install libsndfile
2. conda install --file mac-conda-requirements.txt

If you're running Linux:

1. conda install --file conda-requirements.txt

For everyone:

1. virtualenv ENV --system-site-packages
2. source ENV/bin/activate
3. pip install -r requirements.txt
4. pip install scikits.audiolab
  * (This isn't in the main pip requirements as it breaks Heroku)
