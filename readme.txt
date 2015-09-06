brew install libsndfile
conda install --file mac-conda-requirements.txt
virtualenv ENV --system-site-packages
source ENV/bin/activate
pip install -r requirements.txt
pip install scikits.audiolab

https://github.com/thenovices/heroku-buildpack-scipy

/usr/local/Library/Taps/homebrew/homebrew-python

https://github.com/kennethreitz/conda-buildpack
https://binstar.org/weiyan/scikit-audiolab

heroku run bash
conda install --channel https://conda.binstar.org/weiyan scikit-audiolab -y
conda list -e

https://github.com/palfrey/conda-buildpack
