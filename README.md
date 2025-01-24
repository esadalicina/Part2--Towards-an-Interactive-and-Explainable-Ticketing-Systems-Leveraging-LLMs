# Master Thesis Part 2: Towards an Interactive and Explainable Ticketing System Leveraging Large Language Models (LLMs)


This is a **Ticketing System** web application built using **Streamlit**. 
It is the second part of my **Master's Thesis Project**, focusing on implementing a complete ticketing management solution with a explainable and interactive user-friendly interface. 
The application allows users to create, manage, and track tickets, handle user roles (Admin/User/Support Staf), and offers real-time ticket management.


Master Thesis Part 1 - The focus is on dataset preprocessing steps for the ticketing system to optimize ticket classification by comparing different machine learning, deep learning, and large language models.: 

https://github.com/esadalicina/Part2--Towards-an-Interactive-and-Explainable-Ticketing-Systems-Leveraging-LLMs

Master Thesis Part 3 - The focus is on the integration of a Discord community with task-specific bots: 

https://github.com/esadalicina/part-3.git

## Table of Contents

- [About the Project](#about-the-project)
- [Features](#features)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Technologies Used](#technologies-used)
- [Contributing](#contributing)
- [License](#license)

## About the Project

This project is the second part of my **Master's Thesis**, where I develop a complete Ticketing System to demonstrate practical implementation of a web-based application for managing tasks and issues. The focus of this part is on building the interactive interface and implementing real-time ticket tracking using **Streamlit**, integrating both frontend and backend into a single application.

The first part of the thesis covered the theoretical aspects and system architecture design, while this second part brings the concepts to life through code.

## Features

- User authentication and role-based access (Admin/User)
- Create, update, and delete tickets
- Track ticket statuses (open, in-progress, closed)
- Simple, interactive UI with real-time updates
- Ticket filtering and sorting options
- Admin dashboard to manage tickets and users

## Installation

### Prerequisites

- **Python 3.8+** installed on your machine
- **pip** for managing Python packages

### Setup Instructions

1. **Clone the repository** to your local machine:

    ```bash
    git clone https://github.com/your-username/ticketing-system.git
    cd ticketing-system
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
    SECRET_KEY=your_secret_key
    DATABASE_URL=sqlite:///tickets.db  # or your preferred database connection
    ```

   Note: If you're using Streamlit's built-in features and SQLite, you may not need many environment variables.

## Running the Project

To run the Streamlit Ticketing System locally:

1. **Navigate to the project directory**:

    ```bash
    cd ticketing-system
    ```

2. **Run the Streamlit app**:

    ```bash
    streamlit run app.py
    ```

3. **Access the application**:
   - Open your browser and go to `http://localhost:8501` to access the Ticketing System UI.

## Technologies Used

- **Streamlit** - for building the web interface and backend logic
- **SQLite** or any preferred database - for ticket and user data storage
- **Python** - core programming language
- **Pandas** - for data manipulation and management
- **Streamlit Authentication** - for user roles and login functionality (or any custom auth system)
- **Other Libraries**: Include any other dependencies listed in your `requirements.txt`

## Deployment

To deploy the application, you can use any cloud platform that supports Streamlit applications, such as:

- **Streamlit Cloud** (for free hosting of Streamlit apps)
- **Heroku**
- **AWS/Google Cloud** (using Docker for containerized deployment)

Simply follow their respective guides for deploying a Streamlit app.

## Contributing

Contributions are welcome! Follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Make your changes and commit them (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-name`).
5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
