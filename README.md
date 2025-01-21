# Master Thesis Part 1: Towards an Interactive and Explainable Ticketing System Leveraging Large Language Models (LLMs)

## Data Preprocessing and Model Training for automated ticket (text) classification 

This repository contains the code, data, and resources for Part 1 of the master thesis titled "Towards an Interactive and Explainable Ticketing System Leveraging Large Language Models (LLMs)". 
The repository focuses on data preprocessing, model training, and optimization for classifying ticketing system data. 
It compares a variety of machine learning models, including traditional algorithms and modern LLMs to improve system performance.
If you seek for more clearity and information, you are welcome to have a look over the report and videos (Folder: Master Thesis Report and Video/) 


GitHub of Master Thesis Part 2: https://github.com/esadalicina/Part2--Towards-an-Interactive-and-Explainable-Ticketing-Systems-Leveraging-LLMs


## The repository consists of two main sections:

- Data Preprocessing and Analysis: Steps to clean, preprocess, and transform ticketing data for model training.
- Model Training and Comparison: Implementation of multiple classification models, including traditional approaches, deep learning models and Language Models, with a focus on hyperparameter optimization and explainability techniques.

## Models Implemented

### Traditional Machine Learning Models
- Support Vector Machine (SVM)
- Random Forest (RF)
- Logistic Regression (LR)
- NaiveBayes (NB)
- Decision Tree (DT)
  
### Traditional Deep Learning Models
- Convolutional Neural Networks (CNN) 
- Hierarchical Neural Networks (HNN)
- Recurrent Neural Networks (RNN)

### Large Language Models (LLMs)
- Bidirectional Encoder Representations from Transformers (BERT)
- Robustly Optimized BERT Pretraining Approach (RoBerta)
- Cross Network for Text Classification (XNet)

## Model Optimization
- Grid Search & Random Search: Hyperparameter tuning techniques used for optimizing traditional models.
- HuggingFace: Pretrained LLM models were used on our dataset from the HuggingFace company (https://huggingface.co/models)

## Text representation techniques
- Word to vector (W2V)
- Term Frequency-Inverse Document Frequency (Tf-idf)

## The performance of each model is evaluated based on:

- Accuracy: Correctly classified tickets.
- F1-Score: Balance between precision and recall.
- Time: The training and testing time
- Explainability: Techniques such as SHAP (SHapley Additive exPlanations) are used to explain model decisions for ticket classification.
The results and comparison charts are stored in the results/ directory.


## Repository Contents

- Dataset/: Contains the raw (complaints-2021-05-14_08_16.json) and preprocessed data (Cleaned_Dataset.csv) used for model training and evaluation in this project.
            The dataset includes labeled ticketing data for classification tasks. There exist also a knowledge base datset demo version (KB_dataset.csv) to test it on the ticketing system website.
- Diagrams/: Includes all the visual representations of the dataset balance of ticket labels and model loos-plots for evaluation.
- Master Thesis Report and Video/: Holds the link of the final thesis report and accompanying presentation video, outlining the research, methodology, results, and conclusions of the project.
- Source/: Contains the source code for the data preprocessing (Ticket-Analysing/) and model training (Ticket-Classification/).
- README.md: Instructions for accessing and using the code on the Iris Cluster.

## Prerequisites

Before getting started, ensure you have the following installed:

- Python (>= 3.8)
- Visual Studio Code: Recommended for easier code management and Git integration in HPC
- HPC Access: Iris Cluster for running high-performance jobs (https://ulhpc-tutorials.readthedocs.io/en/latest/)
- Visual Studio Code: Installed on your local machine.
- Remote - SSH extension in VSC: To connect to the Iris Cluster from VSC. SSH Access to the Iris Cluster (HPC).
- Git installed on the HPC (usually available by default, but you can check by running git --version).


## Connecting to the HPC via SSH in Visual Studio Code

To manage your Git repository stored on the HPC, first, set up SSH access in VSC to allow remote connections.

### Setting Up SSH in Visual Studio Code:
1. Install the Remote - SSH Extension in Visual Studio Code:
  - Open Visual Studio Code.
  - Go to the Extensions tab (left-hand sidebar).
  - Search for "Remote - SSH" and click Install.
2. Add the HPC Connection:
  - Press Ctrl + Shift + P (or Cmd + Shift + P on Mac) to open the Command Palette.
  - Type "Remote-SSH: Add New SSH Host" and press enter.
3. Enter the SSH connection details to the Iris Cluster:
  - ssh yourusername@iris-cluster
  - It will prompt you to choose the SSH configuration file (e.g., ~/.ssh/config).
  - Save the connection details.
4. Connect to the HPC:
  - Press Ctrl + Shift + P (or Cmd + Shift + P) again, type "Remote-SSH: Connect to Host", and select your newly configured HPC host (iris-cluster).
  - Enter your password or use an SSH key to log in.

Once connected, you will have access to the Iris Cluster filesystem directly in Visual Studio Code and can use the built-in terminal.

### Cloning the Git Repository on the HPC

Now that you are connected to the HPC from VSC, let's store the repository directly on the HPC.

Steps to Clone the Git Repository on the HPC:
- Open the VSC Terminal: Go to View -> Terminal in Visual Studio Code to open the terminal.
- Navigate to the Desired Directory on the HPC:
-     cd /home/users/yourusername
  Navigate to your home directory or wherever you want to store the project
- Clone the Repository on the HPC:
-     git clone https://github.com/esadalicina/Part1--Towards-an-Interactive-and-Explainable-Ticketing-Systems-Leveraging-LLMs.git
- Navigate to the Cloned Repository:
-     cd Part1--Towards-an-Interactive-and-Explainable-Ticketing-Systems-Leveraging-LLMs

Now, your Git repository is stored on the HPC, and you can work with it directly from the HPC using the terminal in VSC.

### Managing Git from the HPC in Visual Studio Code

Since you're now connected to the HPC via SSH in VSC, you can easily manage your Git repository directly on the HPC. Here’s how you can handle Git commands:

1. Committing and Pushing Changes: Edit Files in the repository using VSC. Your changes will be saved directly on the HPC.
- Add Changes: In the VSC terminal, run:
-     git add .
- Commit Changes:
-     git commit -m "Your commit message"
- Push Changes to the remote GitHub repository:
-     git push origin main

2. Pulling Updates from GitHub:

- If you want to pull the latest changes from GitHub onto your repository stored on the HPC, run:
-      git pull origin main

3. Using Git in VSC:
You can also use the Source Control tab in Visual Studio Code to manage your repository. Changes, commits, and pushes can all be done from this UI, just like when working locally.



### Set Up and Activate a Conda Environment on the HPC

Once the repository is cloned, you'll need to set up a Python environment to install all required dependencies, ensuring your project runs smoothly.

1. Using Conda:
- Load Conda on the HPC (if available):
-      module load conda
  This may vary based on the HPC setup; consult your HPC documentation.
- Create a new Conda environment:
-     conda create --name myenv python=3.8
- Activate the Conda environment:
-     conda activate myenv
- Install the required packages: Make sure your requirements.txt file lists all the necessary Python packages.
-     pip install -r requirements.txt

2. Using Virtualenv (if preferred over Conda):
- Create a virtual environment:
-      python3 -m venv venv
- Activate the virtual environment:
-     source venv/bin/activate
- Install the required packages:
-      pip install -r requirements.txt


## Running Code/files in HPC

To efficiently handle large datasets and run resource-intensive models, the Iris Cluster is used. 

### Accessing the Cluster

- Connect to the HPC: Press Ctrl + Shift + P (or Cmd + Shift + P) again, type "Remote-SSH: Connect to Host", and select your newly configured HPC host (iris-cluster). Enter your password or use an SSH key to log in.
- Navigate to the repository directory:
-      cd Part1--Towards-an-Interactive-and-Explainable-Ticketing-Systems-Leveraging-LLMs

### Submitting Jobs on the Cluster

Create a shell script (train.sh) to train various models, an example can be found in the folder (Source/launch.sh)

```
#!/bin/bash
#SBATCH --job-name=model-training       # Job name
#SBATCH --output=logs/train_out.txt     # Output log file
#SBATCH --error=logs/train_err.txt      # Error log file
#SBATCH --time=04:00:00                 # Wall time (4 hours)
#SBATCH --cpus-per-task=16              # Number of CPUs
#SBATCH --mem=64GB                      # Memory required
#SBATCH --partition=gpu                 # Use GPU partition

# Load necessary modules (e.g., TensorFlow, PyTorch)
module load python/3.8
module load tensorflow/2.4.1            # Example for TensorFlow


# Activate the environment
-      source /home/users/elicina/.virtualenvs/Master-Thesis/bin/activate

# Run the model training script
-      python scripts/train_model.py --model BERT --epochs 5
```

### To submit the training job:

-     sbatch train.sh

### (Optional) Real-Time GPU Session (Interactive Mode)

- For debugging or running models in real-time with GPU resources, you can request an interactive session:

-      si-gpu -G 1 -c 8 -t 120
  This will give you an interactive environment where you can manually run scripts and test models.
