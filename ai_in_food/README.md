Desarrollo de nuevos productos alimenticios funcionales con ingredientes endémicos de México, utilizando inteligencia artificial (IA)
==============================

En México se desperdician alrededor de 28 millones de toneladas de alimentos al año. Según la SEDESOL, 
esta cantidad de alimento serviría para alimentar a 7 millones de mexicanos y disminuir la inseguridad
alimentaria. La población en esta condición aunada a aquella con recursos, pero con una mala educación
alimentaria, resulta en individuos con sobre peso u obesidad vulnerables a enfermedades crónicodegenerativas.
La ingesta de alimentos funcionales y nutritivos podría prevenir estas enfermedades.
Para aportar soluciones innovadoras, al alcance de todos, para esta problemática se requiere un enfoque
interdisciplinario como el uso de la inteligencia artificial (IA) en la ingeniería de alimentos. Por lo tanto,
el objetivo de este proyecto es aplicar técnicas de IA para el diseño de alimentos con beneficios para la
salud, proporcionados por ingredientes endémicos de México con componentes bioactivos, a precios
accesibles y sensorialmente acordes con las expectativas de los consumidores.

Organización del Proyecto:
------------

    ├── LICENSE
    ├── Makefile           <- Makefile with commands like `make data` or `make train`
    ├── README.md          <- The top-level README for developers using this project.
    ├── data
    │   ├── data_dict      <- Generated dictionaries with categories.
    │   ├── external       <- Data from investigators (third party sources.)
    │   ├── interim        <- Intermediate data that has been transformed.
    │   ├── processed      <- The final, canonical data sets for modeling.
    │   └── raw            <- The original, immutable data dump.
    │
    ├── models             <- Trained and serialized models, model predictions, or model summaries
    │
    ├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                         the creator's initials, and a short `-` delimited description, e.g.
    │                         `1-DHM-initial-data-exploration`.
    │
    ├── references         <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures        <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py           <- makes project pip installable (pip install -e .) so src can be imported
    ├── src                <- Source code for use in this project.
    │   ├── __init__.py    <- Makes src a Python module
    │   │
    │   ├── data           <- Scripts to download process and generate data
    │   │
    │   ├── features       <- Scripts to turn raw data into features for modeling
    │   │
    │   ├── models         <- Scripts to train models and then use trained models to make
    │   │   │                 predictions
    │   │   ├── predict_model.py
    │   │   └── train_model.py
    │   │
    │   └── visualization  <- Scripts to create exploratory and results oriented visualizations
    │            └── visualize.py
    │
    └── tox.ini            <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>

How to execute successfully the scripts?
--------
1. Download data from the following [link](https://fdc.nal.usda.gov/download-datasets.html), by going to the `Latest Downloads` section, into the `Full Download of All Data Types` where the release date is `10/2023` and included it in the corresponding folder path:
`ai_in_food/data/raw` it should have the name  `FoodData_Central_csv_2023-04-20.zip` or something similar (*Note that the date in the file name might change due to upgrades on the information, if so please save or rename information with the above name in the same location).
2. Extract the zip files, into a folder in the same location keeping the same name `FoodData_Central_csv_2023-04-20` but without the .zip segment.
3. There are some additional files that must be downloaded, these files are files that the `food engineering` team manage to produce from a previous anaylsis, and must be in the following path `ai_in_food/data/external/created_by_members` with their original names, 
for now the most important files are the following 3 files: `Base de datos FAI RZR.xlsx`, `Base de datos FAI XVR.xlsx` and `depuración.csv`. These files from the `food engineering` team are found in the conversations and chats of the FAI group. (*Note, this should be enough to execute the programs). 
5. In order to manage correctfully the dependencies versions, make an empty virtual environment for the project and install the corresponding dependencies: `pip install -r requirements.txt`
6. Run the `general_pipeline.py` python script. 
7. Now in the `ai_in_food/data/interim` path there should be an additional file with the name interim.csv, which is until now, the representation of what the model will consume. 