****Map Visualization Tool:****

This is standalone visualisation tool to generate spatial analysis for journalists. The tool translates demographic data into maps and charts that journalists can directly utilise in their articles. 

**Folder/file contents and description:**
 -  Boundaries-20240419T224611Z-001 : Shapefiles of Greater Manchester and West Midlands
 -  Collective_census_2021_folder_filtered-20240419T224609Z : 2021 Census data of different demographic categories at LSOA, MSOA and LTLA levels
 -  static: Contains the javascript and css files used to design the UI.
 -  templates: Contains HTML files used to render pages of the UI.
 -  EDA on demographic data.ipynb: Python notebook used to perfom EDA
 -  Filer_data.ipynb: Python notebook used to perform data filtering
 -  app.py: Python file consisting flask servers to support routing
 -  map_creation.py: Python file that has the mail application logic
 -  requirements.txt: File that includes all the packages required to run the applocation
 -  Procfile, app.yaml, runtime.txt, vercel.json: Files created to deploy the app on multiple platforms

**Steps to get the appliction up and running:**
1. Download this zip file into your system and upzip it.
2. Open the folder on Visual Studio Code or any other platform of your choice.
3. Install at the necessary packages from the requirements.txt file:

       pip install -r requirements.txt
5. Run the app.py file

       python run app.py
7. Copy paste the url generated on a browser.


**App deployed on Heroku**

https://the-mill-app-1a3201f18a65.herokuapp.com/

Current status: Loads Maps for certain categories of West Midlands only, (West Midlands- LTLA- Ethnic Group)
