#Phase 5 python program
# import mysql.connector
# from mysql.connector import Error

# def connect():
#     """Establish a connection to the MySQL database."""
#     try:
#         connection = mysql.connector.connect(
#             host='localhost:3306',
#             database='bookfetch',
#             user='root',
#             password='O15mp8dk!202020'
            
#         )
#         if connection.is_connected():
#             print('Connected to MySQL database')
#             return connection
#     except Error as e:
#         print(f"Error: {e}")
#         return None

import mysql.connector
from mysql.connector import errorcode

#---- FOR CREATION! ----#

def connectToDB():
    try:
        reservationConnection = mysql.connector.connect(
            user='root',
            password='O15mp8dk!202020',
            host='localhost',
            database='bookfetch'
        )
        print("Successfully connected to the database!")
        return reservationConnection

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print('Invalid credentials')
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print('Database not found')
        else:
            print('Cannot connect to database:', err)
        return None

    else:
    # Execute database operations...
        reservationConnection.close()


def newStudent(reservationConnection):
    cursor = reservationConnection.cursor()
    
    studentID = int(input("Please enter a studentID: "))
    universityID = int(input("Please enter a universityID: "))
    firstName = input("Please enter a first name: ")
    lastName = input("Please enter a last name: ")
    email = input("Please enter an email address: ")
    phone = int(input("Please enter a phone number: "))
    birthDate = input("Please enter a birthdate (xxxx-xx-xx): ")
    major = input("Please enter a major: ")
    status = input("Please enter a status: ")
    year = input("Please enter a year: ")

    try: 
        insertQuery = "INSERT INTO Student (StudentID, universityID, firstName, lastName, email, address, phone, birthDate, major, status, year) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(insertQuery(studentID, universityID, firstName, lastName, email, phone, birthDate, major, status, year))
        reservationConnection.commit()
        print("You successfully added a student to the database :0 ")

    except errorcode as err:
        print("There was an issue with your insertion...")

    finally:
        cursor.close()

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def createCart(reservationConnection):
    cursor = reservationConnection.cursor()

    showBookQuery = "SELECT * FROM Book"
    cursor.execute(showBookQuery)
    result = cursor.fetchall
    
    print("\nAvailable Books:")
    print("ISBN-13 | Type | Price | Title | Author | Publisher | PublishDate | Edition | Language | Format | Weight")

    for row in result:
        print(f"{row[0]} | {row[1]} | ${row[2]:.2f} | {row[3]} | {row[4]} | {row[5]} | {row[6]} | {row[7]} | {row[8]} | {row[9]} | {row[10]:.2f}")

    isbn_13 = input("Enter the ISBN-13 of the book you want to add to the cart: ")

    try:
        # Check if the book exists
        verifyQuery = "SELECT * FROM Book WHERE ISBN_13 = ?"
        showBookQuery(cursor, verifyQuery, (isbn_13,))
        book = cursor.fetchone()

        if book:
            cartQuery = "INSERT INTO Cart (studentID, dateCreated, dateUpdated, associatedBooks) VALUES (%s, %s, %s, %s)"
            studentID = int(input("Enter your studentID: "))
            dateCreated = input("Enter the date: ")
            dateUpdated = input("Enter the date you finished: ")
            associatedBooks = book
            #Might need to make sure that the associated books is retrieving the books they specified

            cartQuery(cursor, cartQuery, (studentID, dateCreated, dateUpdated, associatedBooks, isbn_13))
            reservationConnection.commit()
            print("Book added to the cart successfully!")
        else:
            print("Invalid ISBN-13. Book not found.")

    except errorcode as e:
        print("Error creating cart: ")

    finally:
        cursor.close()

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#def createOrder:

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#def submitOrder:

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def createRating(reservationConnection):
    cursor = reservationConnection.cursor()

    #need to change review to Rating in the database!!!
    ISBN_13 = int(input("Please enter the ISBN_13: "))
    studentID = int(input("Please enter your studentID: "))
    rating = int(input("Please enter a rating for the book (1-5): "))
    description = input("Please write a description: ")

    try:
        bookRatingQuery = "INSERT INTO Rating (ISBN_13, studentID, rating, description) VALUES (%s, %s, %s, %s)"
        data = (ISBN_13, studentID, rating, description)
        cursor.execute(bookRatingQuery, data)
        reservationConnection.commit()
        print("Your review has been submitted.")
    
    except errorcode as err:
        print("There was an issue with your review. Please try again.")

    finally:
        cursor.close()
    

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#Customer Service Module!

#def createTrouble:

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#Admin Module!

def createNewBook(reservationConnection):

    cursor = reservationConnection.cursor()

    isbn_13 = int(input("Please enter an ISBN_13: "))
    type = input("Please enter a type: ")
    price = float(input("Please enter the price of the book: "))
    title = input("Please enter the book title: ")
    author = input("Please enter the author of the book: ")
    publisher = input("Please enter the publisher: ")
    publishDate = input("Please enter the published date: ")
    edition = input("Please enter the edition of the book: ")
    language = input("Please enter the language: ")
    format = input("Please enter the format (printed or electronic): ")
    weight = float(input("Please enter the weight of the book (lbs): "))

    try:
        insertQuery = "INSERT INTO Book (ISBN_13, type, price, title, author, publisher, publishDate, edition, language, format, weight) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(insertQuery(isbn_13, type, price, title, author, publisher, publishDate, edition, language, format, weight))
        reservationConnection.commit()
        print("You successfully added a book to the database!")

    except errorcode as err:
        print("There was an issue with your insertion...")

    finally: 
        cursor.close()


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#I WILL COME BACK TO
'''
def newUniversity(reservationConnection):
    cursor = reservationConnection.cursor()

    universityID = int(input("Please enter a universityID: "))
    name = input("Please enter the university name: ")
    address = input("Please enter the address: ")
    contactFirstName = input("Please enter the university contact first name: ")
    contactLastName = input("Pleas enter the university contact last name: ")
    contactEmail = input("Please enter the contact email: ")
    contactPhone = int(input("Please enter the contact phone number (xxxxxxxxxx): "))
    cursor.execute("INSERT INTO University (universityID, name, address, contactFirstName, contactLastName, contactEmail, contactPhone) VALUES (%s, %s, %s, %s, %s, %s, %s)", (universityID, name, address, contactFirstName, contactLastName, contactEmail, contactPhone))

    for i in range(150):
        iteration = input("Do you want to continue adding departments (yes/no): ")

        if iteration.lower() == "no":
            print("You have added all of your departments.")
            break

        departmentID = int(input("Please enter the departmentID: "))
        name = input("Please enter the department name: ")
        uID = universityID
        instructorID = int(input("Please enter the instructor"))
        universityAssoc = universityID
        cursor.execute("INSERT INTO Department (departmentID, name, universityID) VALUES (%s, %s, %s)", (departmentID, name, universityAssoc))

        for j in range(20):
            iteration = input("Do you have more professors to enter (yes/no): ")

            if iteration.lower() == "no":
                print("You have added all professors to the department.")
                break

            instructorID = int(input("Please enter the instructorID: "))
            professorName = input("Please enter the professor name: ")
            cursor.execute("INSERT INTO Professor (instructorID, name) VALUES (%s, %s)", (instructorID, professorName))

    

    reservationConnection.commit()
    reservationConnection.close()
'''
    


#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#SUPER ADMIN!

def createNewEmployee(reservationConnection):
    cursor = reservationConnection.cursor()

    employeeID = int(input("Please enter the employeeID: "))
    firstname = input("Please enter the employee first name: ")
    lastName = input("Please enter the employee last name: ")
    ssn = int(input("Please enter the employee SSN: "))
    salary = float(input("Please enter the employee salary: "))
    gender = input("Please enter the employee gender: ")
    email = input("Please enter the employee email: ")
    address = input("Please enter the employee address: ")

    try:
        addEmployee = "INSERT INTO Employee (employeeID, firstName, lastName, SSN, salary, gender, email, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(addEmployee(employeeID, firstname, lastName, ssn, salary, gender, email, address))
        reservationConnection.commit()
        print("Successfully addded the employee.")

    except errorcode as err:
        print("There was an issue with the insertion...")

    finally: 
        cursor.close()

#----FOR UPDATES----#

#Student updates cart#
#def updateCart:

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#customer service updates a trouble ticket
#def updateTT:

#----FOR DELETES----#

#Student cancels an order
#def cancelOrder:

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#Admin module where SA can deactivate admin (delete from DB?)
def deleteAdmin(reservationConnection):
    cursor = reservationConnection.cursor()

    deletedEiD = int(input("Please enter the administratorID of the admin you wish to delete: "))
    findQuery = "SELECT * FROM Administrator WHERE administratorID = %s"

    cursor.execute(findQuery(deletedEiD))
    admin = cursor.fetchall()

    if not admin:
        print("Sorry, no admin matching that ID was found.")

    else:
        print("Admin/s Found:")
        print("administratorID | employeeID | assignedTo | permissions | title")

        for admin in admin: 
            print("| {0:12d} | {1:10i} | {2:10s} | {3:10s} | {4:10s}".format(admin[0], admin[1], admin[2], admin[3], admin[4]))

        delete_id = input("\nEnter administratorID to delete (or leave blank to cancel): ")
        if delete_id:
            deleteQuery = "DELETE FROM Administrator WHERE AdministratorID = %s"
            cursor.execute(deleteQuery, (delete_id,))
            cursor.commit()
            print("Employee with ID", delete_id, "deleted successfully.")
        else:
            print("Deletion cancelled.")

    cursor.close()

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#----CODE FOR THE SEARCH QUERIES----#


def main():
    try:
        with connectToDB() as reservationConnection:
            if reservationConnection:
                while True:
                    print("---WELCOME TO THE UNIVERSITY BOOK DATABASE---")
                    print("Here are your options for where to go:")
                    print("1. Add to the book database")
                    print("2. Update the book database")
                    print("3. Delete from the book database")
                    print("4. See reports about the database")

                    choice = input("Enter your choice (1-4): ")

                    if choice == "1":
                        print("YOU CHOSE OPTION 1. NOW CHOOSE WHICH USER TYPE YOU ARE:")
                        print("=======================================================")
                        print("1. Student user")
                        print("2. Customer Service User")
                        print("3. Administrator")
                        print("4. Super Administrator")
                        
                        secondChoice = input("Enter your choice (1-4): ")
                        if secondChoice == "1":
                            print("YOU CHOSE OPTION 1. NOW CHOOSE WHAT YOU WANT TO ADD:")
                            print("=======================================================")
                            print("1. Create a new student")
                            print("2. Create cart for a student")
                            print("3. Create a new order")
                            print("4. Submit order")
                            print("5. Create a new book rating")

                            thirdChoice = input("Enter your choice (1-5): ")
                            if thirdChoice == "1":
                                newStudent(reservationConnection)
                            elif thirdChoice == "2":
                                createCart(reservationConnection)
                            # elif thirdChoice == "3":
                            #     ##
                            # elif thirdChoice == "4":
                            #     ##Submit order
                            else: 
                                createRating(reservationConnection)
                        
                        elif secondChoice == "2":
                            print("YOU CHOSE OPTION 2:")
                            print("=======================================================")
                            #troubleTicket(reservationConnection)

                        elif secondChoice == "3": 
                            print("YOU CHOSE OPTION 3. NOW CHOOSE WHAT YOU WANT TO ADD:")
                            print("=======================================================")
                            print("1. Create new book")
                            print("2. Create a new university")

                            fifthChoice = input("Enter your choice (1 or 2): ")
                            if fifthChoice == "1":
                                createNewBook(reservationConnection)
                            else:
                                #createUniversity(reservationConnection)
                                print("will do")

                        else: 
                            print("YOU CHOSE OPTION 4: \n")
                            createNewEmployee(reservationConnection)




                        #newStudent(reservationConnection)
                    elif choice == "2":
                        createCart(reservationConnection)
                    elif choice == "3":
                        createNewBook(reservationConnection)
                    elif choice == "4":
                        createRating(reservationConnection)
                    else:
                        print("Invalid choice. Please enter a number between 1 and 4.")

    except mysql.connector.Error as err:
        print("Error:", err)
    
if __name__ == "__main__":
    main()

