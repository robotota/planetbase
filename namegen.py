import random

names = ['Alan', 'Ada', 'Adeline', 'Boris', 'Blake', 'Barbara', 'Charlie', 'Chuck', 'Cheese', 'Dick', 'Daniel', 'Eliah',
         'Esther', 'Euremiah', 'Falcon', 'Freddie', 'George', 'Georgiy', 'Grounge', 'Henry', 'Harry', 'Ira', 'Ida',
         'John', 'Jennifer', 'Jenny', 'Jack', 'Jonny', 'Kale', 'Kate', 'Kira', 'Konstantin', 'Larry', 'Leonid',
         'Michael', 'Mary', 'Margareth', 'Nina', 'Nick', 'Oprah', 'Oleg', 'Petr', 'Peter', 'Rostislav', 'Rick',
         'Rodney', 'Steve', 'Samuel', 'Tom', 'Thomas', 'Tamara', 'Tina', 'Uvar', 'Vera', 'Veronica', 'Victor', 'Wane',
         'Will', 'William', 'Xenia', 'Yve', 'Zeta']
surnames = ['Abramovich', 'Borisov', 'Blake', 'Blane', 'Boldwin', 'Bold', 'Chen', 'Charlston', 'Chelsea', 'Carpenter',
            'Down', 'Drown', 'Deary', 'Dreason', 'Drake', 'Ear', 'East', 'Eastwood']


def createName():
    return random.choice(names) + " " + random.choice(surnames)
