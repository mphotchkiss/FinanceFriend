# FinanceFriend
A locally running python GUI tool to upload, edit, and visualize transactions. The tool uses keywords and google search requests to dynamically categorize financial transactions into categories: food, transportation, housing, entertainment, miscellaneous, and education.

The project is a proof of concept, but nevertheless it's functional with a few bugs here and there. And the GUI isn't styled to be pretty - just functiona. Certainly an exploratory learning project.

## What I Learned
- Basic Python
- using Tkinter
- sqlite
- OFX file formatting
- using BeautifulSoup

## How To Use

1. Install homebrew and python: https://docs.python-guide.org/starting/install3/osx/#install3-osx
2. Install tkinter: `brew install python-tk@3.9`
3. Install all of the following dependencies using `pip install`
- beautifulsoup4
- Pillow
- numpy
- matplotlib
- ofxparse
- tkcalendar
- google

Run the command
`
python3 app.py
`

The GUI frame should automatically launch and the main page of the application should be presented by default. The navigation panel is on the left to go between different pages. 

The main page presents graphical data of the existing transactions. Upon first launch, there will evidently be no data. 

The management page is an index page that allows filtering, editing, and deleting of existing transactions.

Lastly, the upload page allows uploading in two ways: manual uploading and ofx uploading. OFX is a standardized file format used for financial transactional data that can often be downloaded from online bank systems. 

The functionality is pretty easy explorable, and while the categorization functionality isn't fast, it's fun to see it at work. This functionality could be better implemented with a simple AI/Machine Learning algorithm, such as a Bayes Classifier.
