# Worm Diary

Here’s a sentence that conveys your message:

You can log in to [https://wormdiary.streamlit.app/](https://wormdiary.streamlit.app/) to view my worm diary, which records each feeding and the decomposition timeline. This is a record of my worm farming journey, and I hope it serves as a useful reference for others.

This introduction invites others to explore your worm diary while providing context about its purpose.

## Features

- **Data Viewing**: Both guests and admins can view and filter the worm feeding records.
- **Data Entry**: Only admins can add new feeding records.
- **User Login**: The application supports user login, with guests able to view data without logging in, while only admins can add data.
- **Login and Logout**: Users can switch between login and logout modes at any time.

## Project Structure

```
worm_diary/
│
├── worm_diary.csv 
├── main_page.py
└── README.md 
```


## Dependencies

Before running this project, make sure you have the following dependencies installed:

- Python 3.x
- Streamlit
- Pandas

You can install the required dependencies with the following command:

```bash
pip install streamlit pandas