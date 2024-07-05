import pandas as pd

#DATA_FILE = '/Users/esada/Documents/UNI.lu/MICS/Sem4/Ticketing-System/Data/tickets.csv'
DATA_FILE = '/mount/src/ticketing-system/Data/tickets.csv'


def load_tickets():
    return pd.read_csv(DATA_FILE)


def save_tickets(tickets):
    tickets.to_csv(DATA_FILE, index=False)


def add_ticket(ticket):
    tickets = load_tickets()
    tickets = pd.concat([tickets, pd.DataFrame([ticket])], ignore_index=True)
    save_tickets(tickets)


def update_ticket(ticket_id, status, update_data):
    tickets = load_tickets()
    tickets.loc[tickets['id'] == ticket_id, status] = update_data
    save_tickets(tickets)


def get_ticket(ticket_id):
    tickets = load_tickets()
    return tickets[tickets['id'] == ticket_id]


def get_email_address(ticket_id):
    tickets = load_tickets()
    email = tickets.loc[tickets['id'] == ticket_id, 'Email']
    if not email.empty:
        return email.values[0]
    else:
        return None
