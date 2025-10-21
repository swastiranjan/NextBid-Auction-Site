NextBid
NextBid is a dynamic online auction platform that allows users to list items, place bids, and compete in real time for unique products. With a clean interface and robust backend, NextBid brings the excitement of traditional auctions to the web.

Tech Stack
Frontend: HTML, CSS, JavaScript
Backend: Python, Flask
Database: SQLite

Installation
Clone the repository:

bash
git clone https://github.com/yourusername/nextbid.git
cd nextbid
Set up a Python virtual environment:

bash
python -m venv venv
source venv/bin/activate   # On Windows use: venv\Scripts\activate
Install dependencies:

bash
pip install -r requirements.txt
Run the application:

bash
flask run
Access the site at http://localhost:5000.

Usage
Create an account to start bidding or list your own items.

Browse current auctions or use the search feature to find specific items.

Place a bid before the countdown ends; highest bid wins!

Folder Structure
website/ – HTML, CSS, JS files

main.py – Flask application

instance/ – SQLite database

final_env/ – (optional) Python virtual environment
