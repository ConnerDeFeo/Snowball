# Snowball
AI Value Investment Assistant. Snowball is designed at a high level to do the following

## Step 1. Document Retrieval 

### 1.1 Overview
Retrieve the past 6 years of 10k's, 10Q', Proxy Statements, and Earning Calls

---

## Step 2. LLM Rankings

### 2.1 Overview
Feed into LLM to output a variety of rankings of various metrics based on readings

### 2.2 AI Hindsight

**Problem**: The first challenge is the processing of documents into realevant stats such as a score for managmenet.
This is due to the model having hindsight bias, it already knows that Apple is worth 3T modern day,
so asking it to output values that will be used for training the final model will be filled with
bias.

**Soultion**: Use the LLM to extract the valuage vauge variables that people read filing for. For instance, a customer 
being 20% of a companies profit is a super important note that will not be found elsewhere but the financial statments.
This data will then be used to train the model. This will then be consolidated using a rubric given to the LLM. The LLM
will follow the rubric and output deterministic variables based on the rubric.

---

## Step 3. Model Prediction
### 3.1 Overview
Feed variables from LLM into trained model to output predicted future free cash flow of company
