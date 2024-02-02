import sqlite3
import streamlit as st
from pydantic import BaseModel, validator
import streamlit_pydantic as sp
from typing import Optional
from datetime import datetime

# Connect to our database
con = sqlite3.connect("todoapp.sqlite", isolation_level=None)
cur = con.cursor()

# Create the table
cur.execute(
    """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY,
        name TEXT,
        description TEXT,
        created_at TEXT, 
        category TEXT,
        due_date TEXT,
        state TEXT
        finished BOOLEAM

    )
    """
)

# Define our Form
class Task(BaseModel):
    name: str
    description: str
    category: Optional[str] = None # school, work, personal
    finished: bool
    

# This function will be called when the check mark is toggled, this is called a callback function
def toggle_is_done(finished, row):
    cur.execute(
        """
        UPDATE tasks SET finished = ? WHERE id = ?
        """,
        (finished, row[0]),
    )

def main():
    st.title("Todo App")
    
    created_at = st.date_input("Created At", value=datetime.now())
    due_date = st.date_input("Due Date")
    state = st.selectbox("State", ["planned", "in-progress", "done"])
    
    # Format these dates immediately after collecting them
    formatted_created_at = created_at.strftime('%Y-%m-%d')
    formatted_due_date = due_date.strftime('%Y-%m-%d')
    

    # Create a Form using the streamlit-pydantic package, just pass it the Task Class
    data = sp.pydantic_form(key="task_form", model=Task)
    if data:
        cur.execute(
            """
            INSERT INTO tasks (name, description, created_at, category, due_date, finished) VALUES (?, ?, ?, ?, ?, ?)
            """,
            (data.name, data.description, formatted_created_at, data.category, formatted_due_date, data.finished ),
        )

    data = cur.execute(
        """
        SELECT * FROM tasks
        """
    ).fetchall()
    # HINT: how to implement a Edit button?
    # if st.query_params.get('id') == "123":
    #     st.write("Hello 123")
    #     st.markdown(
    #         f'<a target="_self" href="/" style="display: inline-block; padding: 6px 10px; background-color: #4CAF50; color: white; text-align: center; text-decoration: none; font-size: 12px; border-radius: 4px;">Back</a>',
    #         unsafe_allow_html=True,
    #     )
    #     return

    cols = st.columns(7)
    cols[0].write("Finished?")
    cols[1].write("Name")
    cols[2].write("Description")
    cols[3].write("Created At")
    cols[4].write("Category")
    cols[5].write("Due Date")
    cols[6].write("State")

    for row in data:
        cols = st.columns(7)
        State = row[6]
        created_at = datetime.strptime(row[3], '%Y-%m-%d').strftime('%Y-%m-%d')
        due_date = datetime.strptime(row[5], '%Y-%m-%d').strftime('%Y-%m-%d')
        cols[0].checkbox('finished', row[7], label_visibility='hidden', key=row[0], on_change=toggle_is_done, args=(not row[7], row))
        cols[1].write(row[1])
        cols[2].write(row[2])
        cols[3].write(created_at)
        cols[4].write(row[4])
        cols[5].write(due_date)
        cols[6].write(row[6])




main()