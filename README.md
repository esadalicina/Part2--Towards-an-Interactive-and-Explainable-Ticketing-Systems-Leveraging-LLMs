# Master Thesis Part 2: Towards an Interactive and Explainable Ticketing System Leveraging Large Language Models (LLMs)


This is a **Ticketing System** web application built using **Streamlit**. 
It is the second part of my **Master's Thesis Project**, focusing on implementing a complete ticketing management solution with a explainable and interactive user-friendly interface. 
The application allows users to create, manage, and track tickets, handle user roles (Admin/User/Support Staf), and offers real-time ticket management.


Master Thesis Part 1 - The focus is on dataset preprocessing steps for the ticketing system to optimize ticket classification by comparing different machine learning, deep learning, and large language models.: 

https://github.com/esadalicina/Part2--Towards-an-Interactive-and-Explainable-Ticketing-Systems-Leveraging-LLMs

Master Thesis Part 3 - The focus is on the integration of a Discord community with task-specific bots: 

https://github.com/esadalicina/part-3.git


## Features

- Admin Role: 
- Support Staff Role: 
- User Role:
  

## Installation

### Prerequisites

- **Python 3.8+** installed on your machine

### Setup Instructions

1. **Clone the repository** to your local machine:

    ```bash
    git clone https://github.com/esadalicina/Part2--Towards-an-Interactive-and-Explainable-Ticketing-Systems-Leveraging-LLMs.git
    cd Part2--Towards-an-Interactive-and-Explainable-Ticketing-Systems-Leveraging-LLMs
    ```

2. **Create a virtual environment** (optional but recommended):

    ```bash
    python -m venv venv
    ```

3. **Activate the virtual environment**:

    - On **Windows**:

      ```bash
      venv\Scripts\activate
      ```

    - On **macOS/Linux**:

      ```bash
      source venv/bin/activate
      ```

4. **Install the required dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

5. **Set up environment variables**:
   
   Create a `.env` file in the root directory of your project with the necessary environment variables (if applicable):

    ```plaintext
    Comapny_App_Passowrd=your_secret_key
    ```

## Running the Project (User Role)

To run the Streamlit Ticketing System locally:

1. **Navigate to the project directory**:

- User Role:
  
    ```bash
    cd Part2--Towards-an-Interactive-and-Explainable-Ticketing-Systems-Leveraging-LLMs/User
    ```
- Support Staff Role:
    ```bash
    cd Part2--Towards-an-Interactive-and-Explainable-Ticketing-Systems-Leveraging-LLMs/Agent
    ```
- Admin Role:
   ```bash
    cd Part2--Towards-an-Interactive-and-Explainable-Ticketing-Systems-Leveraging-LLMs/Agent
    ```

2. **Run the Streamlit app**:

- User Role:
    ```bash
    streamlit run User_correct.py
    ```
- Support Staff Role:
    ```bash
    streamlit run Support_correct.py
    ```
- Admin Role:
   ```bash
    streamlit run Support_correct.py
    ```

3. **Access the application**:
   - It will automataclly open the browser
   - If not: Open your browser and go to `http://localhost:8501` to access the Ticketing System UI.
  
4. Login (already cretaed for testing)

- User Role:
    Username: user
    Password: user
- Support Staff Role:
    Username: Agent1
    Password: agent
- Admin Role:
    Username: Admin
    Password: adminpass

## Deployment

Simply follow their respective guides for deploying a Streamlit app.

https://docs.streamlit.io/deploy/tutorials


