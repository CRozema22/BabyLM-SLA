# A Second Language Acquisition-Inspired Curriculum Learning Approach to Training a BabyLM

This repository contains the code for a thesis submitted for the ReMA Humanities (Human Language Technology) at VU University Amsterdam. The project works in the context of the [BabyLM shared task](https://babylm.github.io/) and applies a curriculum learning approach inspired by second and first language acquisition. All files are Jupyter Notebooks using Python 3.10 and have been ran using Colab Pro. Requirements are installed per notebook.

Author: Celonie Rozema

Date: August 2024

## Usage

### Data
[BabyPreprocessing.ipynb](BabyPreprocessing.ipynb) cleans and preprocesses the BabyLM 10M dataset by creating sequences

[BabyDev.ipynb](BabyDev.ipynb) prepares the preprocessed BabyLM 10M dataset for unsupervised POS-tagging by reformatting. POS-tagging is done using Linux.

[BabyDifficultyScoring.ipynb](BabyDifficultyScoring.ipynb) takes the POS-tagged data and scores and ranks this data for all models. These datasets are also available in /data

[Levels_BabyDifficultyScoring.ipynb](Levels_BabyDifficultyScoring.ipynb) can also be used to make a level-based curriculum, rather than based on difficulty scores. It largely overlaps with BabyDifficultyScoring.ipynb but only saves data for a SLA-based model.

### Training and evaluating
[BabyTraining.ipynb](BabyTraining.ipynb) trains a model on the given dataset, filepath can be changed in cell 3

Evaluation is done with [the BabyLM evaluation pipeline](https://github.com/babylm/evaluation-pipeline-2024)






