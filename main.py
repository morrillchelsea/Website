'''
Created on Jul 4, 2022

@author: chelseanieves

Purpose: Creation of "My Pets" website
'''
from website import create_app
app = create_app()

if __name__ == "__main__":
    app.run(debug = True)
    