# opensearch-hybrid-search-optimization
This repository is a set of notebooks to optimize hybrid search settings for OpenSearch. It covers a grid search approach to identify a good parameter set and a model-based approach that dynamically identifies good hybrid search settings for a query.

## Introduction

This repository is a set of notebooks implementing the ideas in the [Hybrid Search Optimizer RFC](https://github.com/opensearch-project/neural-search/issues/934).

### Hybrid Search as a Parameter Optimization Problem

By treating hybrid search optimization as a parameter optimization problem we basically do a grid search over a set of parameter combinations. For each parameter combionation we run all queries from a query set, calculate the metrics for the results (DCG, NDCG, precision) and finally compare all hybrid search configurations by looking at their search metrics.

### Bayesian Optimization to Identify the Best Hybrid Search Configuration

Not yet implemented.

## Run the Notebooks

### Run OpenSearch

Execute the following command to fire up OpenSearch and OpenSearch dashboards:

```
docker compose up -d
```

### Install Requirements and Start Jupyter

Create a virtual environment:

```
python3 -m venv .venv
```

Activate the virtual environment:
```
source .venv/bin/activate
```

Install the requirements:
```
pip3 install -r requirements.txt
```

Start Jupyter:
```
jupyter notebook
```

Open http://localhost:8888 in your browser (you might need to go for http://127.0.0.1:8888)

## Notebooks

This repository packages a couple of notebooks that help you understand hybrid search in OpenSearch and provide support to find the best configuration for your application.

### Prepare OpenSearch

To enable hybrid search queries in OpenSearch a few requirements must be met. This notebook handles the necessary steps: from enabling the ML Commons plugin to creating an ingest pipeline taking care of creating and indexing embeddings.

### Index Product Data

This notebook handles the indexing side. It creates an index with the appropriate settings and ingests the data.

### Baseline Search and Metrics

We want to know which hybrid search settings perform best. We also want to figure out how much better the "best" hybrid search settings perform. To do this we need a baseline to compare it with. The baseline is set up in this notebook.

### Best Hybrid Search Config

This notebook iterates over a set of hybrid search configuration combinations, executes queries against these and calculates metrics for each confguration.
Looking at the metric let's us decide which configuration worked best.

### Query Result and Judgement Analysis

This notebook provides help to analyze hybrid search configuration results and the calculated metrics.

### Single Query Drill Down

Aggregated views sometimes hide specific insights. This notebook provides means to look into specific queries.

### Dynamic Optimization Feature Engineering

This notebook guides you through a feature engineering process to follow a dynamic way of identifying good configuration parameters for hybrid search instead of predicting a global configuration.

### Generate Training Data

Dedicated notebook to generate training data for the dynamic, model-based approach. Similar to the notebook identifying the best hybrid search config it executes a set of queries against several hybrid search settings and stores the results for training and test data generation.

### Run Queries with Dynamic Optimizer

Evaluation notebook for the dynamic, model-based approach.

## Requirements

* Docker to run OpenSearch and OpenSearch Dashboards
* Python and pip
* Dataset: the notebooks assume the ESCI dataset to be downloaded. You can change the path to where the dataset can be found in the notebooks accordingly.

## Experiment Results

With a query set of 5,000 randomly sampled queriesfrom the ESCI dataset we started out with a relatively simple BM25 query using OpenSearch's `multi_match` query (`best_fields`) across some of the indexed fields with pragmatically chosen field weights.

```
"query": {
    "multi_match" : {
        "type": "best_fields",
        "fields": [
            "product_id^100",
            "product_bullet_point^3",
            "product_color^2",
            "product_brand^5",
            "product_description",
            "product_title^10"
        ],
        "operator": "and",
        "query": query
    }
}

```

Our global hybrid search optimization notebook tried out 66 parameter combinations for hybrid search with the following set:
* normalization technique: [`l2`, `min_max`]
* combination technique: [`arithmetic_mean`, `harmonic_mean`, `geometric_mean`]
* keyword search weight: [`0.0`, `0.1`, `0.2`, `0.3`, `0.4`, `0.5`, `0.6`, `0.7`, `0.8`, `0.9`, `1.0`]
* neural search weight: [`1.0`, `0.9`, `0.8`, `0.7`, `0.6`, `0.5`, `0.4`, `0.3`, `0.2`, `0.1`, `0.0`]

Neural and keyword search weights always add up to `1.0`, so a keyword search weight of `0.1` automatically comes with a neural search weight of `0.9`, a keyword search weight of `0.2` comes with a neural search weight of `0.8`, etc.

Calculating the metrics DCG, NDCG and precision for each configuration and comparing them to each other and the baseline the following hybrid search configuration turned out to be the best:

* normalization technique: [`l2`, `min_max`]
* combination technique: [`arithmetic_mean`, `harmonic_mean`, `geometric_mean`]
* keyword search weight: [`0.0`]
* neural search weight: [`1.0`]

Of course, not all queries benefit from this search configuration. After identifying this "globally best hybrid search configuration" we explored ways for a more dynamic approach.

After some exploration we trained several models with query, keyword search result and neural search result features (see the notebooks for more details) which enabled a more dynamic approach, predicting the neural search weight (the "neuralness") of a search query.

| Metric    | Baseline BM25 | Global Hybrid Search Optimizer | Dynamic Hybrid Search Optimizer |
| -------- | ------- | ------- | ------- |
| DCG  | 5.69    |     | 6.03    |
| NDCG | 0.25    |     | 0.27    |
| Precision    | 0.28    |     | 0.31    |

Methodolody: we used the same 4,000 queries to train and 1,000 queries to test the different approaches. 

Running on a smaller dataset (250 queries):

| Metric    | Baseline BM25 | Global Hybrid Search Optimizer | Dynamic Hybrid Search Optimizer - Linear Model | Dynamic Hybrid Search Optimizer - Random Forest Model |
| -------- | ------- | ------- | ------- | ------- |
| DCG  | 6.03    | 6.27    | 6.11    | 6.30
| NDCG | 0.26    | 0.28    | 0.27    | 0.30
| Precision    | 0.30    | 0.32    | 0.31    | 0.32

## Applying the Notebooks to your Application

While the notebooks aim to provide a working example we do encourage adaption of this notebook to your application.
What you need:
* An OpenSearch installation with your data indexed
* You might need to prepare some steps to enable everything necessary for hybrid search. You can find these steps in notebook 1
* Change the cells where the notebooks interact with a locally installed OpenSearch instance to interact with your OpenSearch isntance.
* Change the fields used in the queries and the fields used in the response that are specific to the used dataset.