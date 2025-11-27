# Twitter Community Detection with Complex Edge Weight Assignment
## Purpouse
The point of this implementation is to calculate the complex edge weights between users, by making use of three distinct graphs: a mentions graph, a hashtag graph and a topic graph. The three graphs are aggregated following a formula to make the final relationship graph. 
## Usage 
To use the code in this repository you will have to set up a virtual environment after cloning with:
```
python3 -m venv .venv
```
Once created make sure to activate it with:

```
source .venv/bin/activate
```
and then install the requirements with 
```
pip install -r requirements.txt
```
After installing the requirements make sure to be in the `src` folder from where you can then run the main file:
```
python main.py
```
This will currently load in the data and generate three processed files: `mentions_small.csv`, `hashtags_bipartite_small.csv`, `hashtags_projected_small.csv`, the last of which is around 4.55GB in size, so make sure to have some space, the graph is very dense!  

## To do
- Topic modelling
- Weight calculation