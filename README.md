# Master Thesis Part 2: Towards an Interactive and Explainable Ticketing System Leveraging Large Language Models (LLMs)


This is a **Ticketing System** web application built using **Streamlit**. 
It is the second part of my **Master's Thesis Project**, focusing on implementing a complete ticketing management solution with a explainable and interactive user-friendly interface. 
The application allows users to create, manage, and track tickets, handle user roles (Admin/User/Support Staf), and offers real-time ticket management.


Master Thesis Part 1 - This repository involves preprocessing the dataset for the ticketing system to improve ticket classification through the evaluation and comparison of machine learning, deep learning, and large language models:

https://github.com/esadalicina/Part1--Towards-an-Interactive-and-Explainable-Ticketing-Systems-Leveraging-LLMs.git

Master Thesis Part 3 - This repository involves integrating a Discord community with task-specific bots:

https://github.com/esadalicina/Part3--Towards-an-Interactive-and-Explainable-Ticketing-Systems-Leveraging-LLMs.git


## Features

- Admin Role:
    - Full access to all tickets and user data.
    - Ability to create, edit, and delete tickets.
    - Manage user roles (assign and modify Support Staff).
    - Assign tickets to Support Staff.
    - View ticket status and progress across the system.
    - Generate reports on ticket statistics and user activity.
    - Access the Admin dashboard for an overview of the system's performance and data.
    - Have a chat with the support staff
- Support Staff Role:
    - View and manage tickets assigned to them.
    - Update the status of tickets (e.g., mark as in-progress, resolve, close).
    - Communicate with users to gather more information about tickets.
    - Can only access tickets within their responsibility, not the entire ticket pool.
    - Can have chat with team members
    - Can mark ticket as "wrong classified" (The admin will have a look and reclassify it)
    - Have an translator for better understanding
    - Acces on user feedback
- User Role:
    - Submit new tickets for issues or requests.
    - View the status of their own submitted tickets.
    - Can only interact with their own tickets.
    - Receive email notifications when a ticket is updated or resolved (only if you have registered with your email).
    - Have access to a chatbot for question and help
    - Have access to the Discord Community through an invitation link (Suppoprt by other users)

  
## Repository Contents

- Agent/: It contains all the python files that are used for the backend and frontend of the Admin and Support Staff interface.
- Data/: It contains a knowledge database (KB_dataset.csv) that is used on the User Interface such that they get existing solutions for their resquest (the data is only a demo, not useful in real life). The folder contains also the created tickets (tickets.csv) and the created account information of the Support Staff and Admin (users.csv).
- Model/: It contains the classification model files.
- Resources/: It contains the files for the chat fucntion between the User-Agent (support staff) and Agent-Agent. Additionaly it contains the file to control and modfiy the tickets.csv file.
- User: It contains all the python files that are used for the backend and frontend of the User interface.
- chat.db: Database of the chat information/content from the user-agent interaction
- chat_agent.db: Database of the chat information/content from the agent-agent interaction
- users.db: Registration information of the users.
- README.md: Instructions for accessing the Ticketing System


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

## Running the Project

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
  
    - Username: user
  
    - Password: user
  
- Support Staff Role:
  
    - Username: Agent1
  
    - Password: agent
  
- Admin Role:
  
    - Username: Admin
  
    - Password: adminpass

## Deployment

Simply follow their respective guides for deploying a Streamlit app.

https://docs.streamlit.io/deploy/tutorials


