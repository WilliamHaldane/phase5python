import mysql.connector
from mysql.connector import errorcode

#---- FOR CREATION! ----#

def connectToDB():
    try:
        reservationConnection = mysql.connector.connect(
            user='root',
            password='O15mp8dk!202020',
            host='localhost',
            database='mark24'
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
    email = input("Please enter an email: ")
    address = input("Please enter an address: ")
    phone = int(input("Please enter a phone number: "))
    birthDate = input("Please enter a birthdate (xxxx-xx-xx): ")
    major = input("Please enter a major: ")
    status = input("Please enter a status: ")
    year = input("Please enter a year: ")

    try: 
        insertQuery = "INSERT INTO Student (StudentID, universityID, firstName, lastName, email, address, phone, birthDate, major, status, year) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(insertQuery, (studentID, universityID, firstName, lastName, email, address, phone, birthDate, major, status, year))
        reservationConnection.commit()
        print("You successfully added a student to the database :0 ")

    except mysql.connector.Error as err:
        print("There was an issue with your insertion...1" + err)

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

    except errorcode as err:
        print("Error creating cart: " + err)

    finally:
        cursor.close()

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def createOrder(reservationConnection):
    try:
        cursor = reservationConnection.cursor()

        cartID = int(input("Enter the cartID to create an order: "))

        getQuery = "SELECT * FROM Cart WHERE cartID = %s"
        cursor.execute(getQuery, (cartID))
        cart = cursor.fetchone()

        if not cart:
            print("Cart not found.")
            return
        
        cartID = cart[1]
        isbn_13 = cart[2]
        quantity = cart[3]
        studentID = cart[4]

        dateCreated = input("Enter the date: ")
        date_fulfilled = None
        shipping_type = input("Enter shipping type: ")
        creditName = input("Enter credit card name: ")
        creditType = input("Enter credit card type: ")
        orderStatus = "In-progress"

        orderQuery = "INSERT INTO `Order` (cartID, studentID, dateCreated, dateFulfilled, bookList, shippingType, creditName, creditType, orderStatus) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(orderQuery, (cartID, isbn_13, quantity, studentID, dateCreated, date_fulfilled, shipping_type, creditName, creditType, orderStatus))
       
        print("Order created successfully.")
        reservationConnection.commit()

    except errorcode as err:
        print("Error creating order:", err)

    finally:
        cursor.close()

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

def createTrouble(reservationConnection):
    cursor = reservationConnection.cursor()

    ticketID = int(input("Please enter a ticketID: "))
    studentID = int(input("Please enter the studentID for the ticket: "))
    assignedTo = int(input("Please enter the employeeID of who the ticket is assigned to: "))
    dateLogged = input("Please enter the date of creation (2017-06-15): ")
    dateCompleted = input("Please enter the date of completion (2017-06-15): ")
    title = input("Please enter the title of the ticket: ")
    status = input("Please enter the status (new, in-progress, resolved): ")
    description = input("Please write the described issue: ")

    try: 
        ticketQuery = "INSERT INTO TroubleTicket (ticketID, studentID, assignedTo, dateLogged, dateCompleted, title, status, description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor.execute(ticketQuery(ticketID, studentID, assignedTo, dateLogged, dateCompleted, title, status, description))
        reservationConnection.commit()
        print("You successfully added a new ticket to the database!")

    except errorcode as err:
        print("There was an issue with your trouble ticket...")

    finally:
        cursor.close()


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
def updateCart(reservationConnection):
    try:
        cursor = reservationConnection.cursor()

        studentID = int(input("Enter your studentID: "))
        displayQuery = "SELECT * FROM Cart WHERE studentID = %s"
        cursor.execute(displayQuery, (studentID,))
        cartItems = cursor.fetchall()

        if not cartItems:
            print("No items in the cart.")
            return

        print("Current Cart Items:")
        for item in cartItems:
            print(item)

        choice = input("You have three options. 1. Do you want to modify an existing item? Enter modify. 2. Do you want to add a new item? Enter add. 3. Do you want to delete an item? Enter delete").lower()

        if choice == "modify":
            cartID = int(input("Enter the cartID of the item you want to modify: "))
            newQuantity = int(input("Enter the new quantity: "))
            updateItemQuery = "UPDATE Cart SET Quantity = %s WHERE cartID = %s"
            cursor.execute(updateItemQuery, (newQuantity, cartID))
            print("Cart item updated successfully.")

        elif choice == "add":
            cartID = int(input("Enter the cartID for the new item: "))
            isbn_13 = int(input("Enter the ISBN-13 of the new item: "))
            quantity = int(input("Enter the quantity: "))
            studentID = int(input("Enter the studentID: "))
            dateCreated = input("Enter the date the cart was created: ")
            dateUpdated = input("Enter the date the cart was last updated: ")

            insertItemQuery = "INSERT INTO Cart (cartID, ISBN_13, quantity, studentID, dateCreated, dateUpdated) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(insertItemQuery, (cartID, isbn_13, quantity, studentID, dateCreated, dateUpdated))
            print("New item added to the cart successfully.")

        elif choice == "delete":
            isbn_13 = int(input("Enter the ISBN-13 of the item you want to delete: "))
            deleteItemQuery = "DELETE FROM Cart WHERE studentID = %s AND ISBN_13 = %s"
            cursor.execute(deleteItemQuery, (studentID, isbn_13))
            print("Cart item deleted successfully.")

        else:
            print("Invalid action. Please choose 'modify', 'add' or 'delete'")

        reservationConnection.commit()

    except errorcode as err:
        print("Error updating cart: ", err)

    finally:
        cursor.close()

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

def updateTTicket(reservationConnection):
    try:
        cursor = reservationConnection.cursor()

        displayTicketsQuery = "SELECT * FROM TroubleTicket"
        cursor.execute(displayTicketsQuery)
        troubleTickets = cursor.fetchall()

        if not troubleTickets:
            print("No trouble tickets.")
            return

        print("Current Trouble Tickets:")
        for ticket in troubleTickets:
            print(ticket)

        ticketID = int(input("Enter the ticketID you want to update: "))

        adminID = int(input("Enter the adminID to assign the ticket to: "))
        assignQuery = "UPDATE TroubleTicket SET assignedTo = %s WHERE ticketID = %s"
        cursor.execute(assignQuery, (adminID, ticketID))
        print("Ticket assigned to admin successfully.")

        description = input("Enter the description for the assignment: ")
        descriptionQuery = "UPDATE TroubleTicket SET description = %s WHERE ticketID = %s"
        cursor.execute(descriptionQuery, (description, ticketID))
        print("Ticket description updated successfully.")

        reservationConnection.commit()

    except errorcode as err:
        print("Error updating trouble ticket:", err)

    finally:
        cursor.close()

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

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


                    if choice == "2":
                        print("YOU CHOSE OPTION 2. NOW CHOOSE WHICH USER TYPE YOU ARE:")
                        print("=======================================================")
                        print("1. Student user")
                        print("2. Customer Service User")

                        choicesix = input("Enter your user type (1 or 2): ")

                        if choicesix == "1": 
                            print("YOU CHOSE STUDENT USER. THE ONLY OPERATION IS UPDATE A CART")
                            #updateCart(reservationConnection)
                        else: 
                            print("YOU CHOSE CUSTOMER SERVICE USER. THE ONLY OPERATION IS UPDATING A TROUBLE TICKET")
                            #updateTicket(reservationConnection)

                    if choice == "3": 
                        print("YOU CHOSE OPTION 3. NOW CHOOSE WHICH USER TYPE YOU ARE:")
                        print("=======================================================")
                        print("1. Student user")
                        print("2. Adminstrator User")

                        choiceSeven = input("Enter your user type (1 or 2): ")

                        if choiceSeven == "1":
                            print("YOU CHOSE STUDENT USER. THE ONLY OPERATION IS CANCEL ORDER")
                            #deleteOrder(reservationConnection)
                        else:
                            print("YOU CHOSE ADMIN USER. THE ONLY OPERATION IS TO DELETE AN ADMIN USER")
                            deleteAdmin(reservationConnection)

                    if choice == "4":
                        print("YOU CHOSE OPTION 4. NOW CHOOSE WHICH REPORT YOU WANT TO SEE:")
                        print("=======================================================")
                        print("1. List details of students attending 'UST' - Student attributes")
                        print("2. List details of graduate students from all universities - Student attributes")
                        print("3. List details of Computer Science majors buying more than two books - Student attributes")
                        print("4. List books that have sold or rented the most - Book title, book PK")
                        print("5. List books by category and subcategories - Category, subcategory, book title, book PK")
                        print("6. List book names required for a course (excluding 'Computer Science' category) - Course name, book title")
                        print("7. List books bought by students not associated with a university course - Book title, book PK")
                        print("8. List books and count of courses each book has been associated with - Book title, PK, count of courses")
                        print("9. List book titles related to 'Linear Algebra' - Book title")
                        print("10. List books with overall ratings higher than 3 - Book titles")
                        print("11. Show books, count of purchases, and overall rating for each book, ordered by rating - Book title, count of purchases, overall rating")
                        print("12. List average number of books students buy grouped by book category - Category, average number of books")
                        print("13. List details of each university, including departments, courses, and instructors per course - University name, department name, course name, count of instructors per course")
                        print("14. For each university, find total number of associated books - University name, count of books, total sum of book costs")
                        print("15. List customer service employees and total number of tickets they created - CS name and PK, count of tickets created")
                        print("16. List administrators ordered by salary - Admin name and salary, ordered")
                        print("17. List administrators and total tickets closed - Admin name, count of tickets closed")
                        print("18. List tickets grouped by state, total number created by students and customer support - State, total number")
                        print("19. Find average time for a ticket from created to closed - Average time")
                        print("20. For each closed ticket, show ticket history ordered by ticket - Ticket title/PK, ticket attributes, including state")
                        print("21. List recommended books for each student - Students name, recommended book titles")
                        print("22. For each book, list total count of students who purchased books with at least one common keyword - Book title, count of students")
                        print("23. List books by overall ratings and by number of students who rated them - Rating, book titles, number of students who rated each book")
                        print("24. List books with a rating of 5 and students who rated them, along with students universities - Book title, rating, student name, university name")
                        print("======================================================= \n")

                        choiceFinal = input("Enter which report you want to see (1-24) and 25 to exit: ")

                        if choice == "25":
                            print("Exiting the program. Goodbye!")
                            break
                            
                        else:
                            cursor = reservationConnection.cursor()
                            if choiceFinal == "1":
                                query = "SELECT * FROM Student WHERE universityID = (SELECT universityID FROM University WHERE name = 'UST')"
                                cursor.execute(query)
                            elif choiceFinal == "2":
                                query = "SELECT * FROM Student WHERE status = 'Graduate'" 
                            elif choiceFinal == "3":
                                query = "SELECT s.* FROM Student s JOIN PlaceOrder o ON s.StudentID = o.studentID JOIN Course c ON s.universityID = c.universityID JOIN Department d ON c.departmentID = d.departmentID WHERE d.name = 'Computer Science' GROUP BY s.StudentID HAVING AVG(o.quantity) > 2"
                            elif choiceFinal == "4":
                                query = "SELECT b.title, b.ISBN_13 FROM Book b JOIN PlaceOrder o ON b.ISBN_13 = o.bookList GROUP BY b.title, b.ISBN_13 ORDER BY SUM(o.quantity) DESC"
                            elif choiceFinal == "5":
                                query = "SELECT b.title, b.ISBN_13, b.type AS category, b.format AS subcategory FROM Book b"
                            elif choiceFinal == "6":
                                query = "SELECT c.name AS course_name, b.title AS book_title FROM Course c JOIN Book b ON c.courseID = b.ISBN_13 WHERE c.name != 'Computer Science'"
                            #elif choiceFinal == "7":

                            elif choiceFinal == "8":
                                query = "SELECT b.title, b.ISBN_13, COUNT(c.courseID) AS course_count FROM Book b LEFT JOIN Course c ON b.ISBN_13 = c.courseID GROUP BY b.title, b.ISBN_13"
                            #elif choiceFinal == "9":

                            elif choiceFinal == "10":
                                query = "SELECT b.title FROM Book b JOIN Rating r ON b.ISBN_13 = r.ISBN_13 GROUP BY b.title HAVING AVG(r.rating) > 3"
                            elif choiceFinal == "11":
                                query = "SELECT b.title AS book_title, COUNT(DISTINCT o.orderID) AS count_of_purchases, COALESCE(AVG(r.rating), 0) AS overall_rating FROM Book b LEFT JOIN CartBookAssociation cba ON b.ISBN_13 = cba.ISBN_13 LEFT JOIN Cart c ON cba.cartID = c.cartID RIGHT JOIN PlaceOrder o ON c.cartID= o.cartID LEFT JOIN Rating r ON b.ISBN_13 = r.ISBN_13 GROUP BY b.title ORDER BY overall_rating DESC"
                            #elif choiceFinal == "12":

                            elif choiceFinal == "13": 
                                query = "SELECT u.name AS university_name, d.name AS department_name, c.name AS course_name, COUNT(i.instructorID) AS count_of_instructors FROM University u JOIN Department d ON u.universityID = d.universityID JOIN Course c ON d.departmentID = c.departmentID LEFT JOIN Instructor i ON c.courseID = i.courseID GROUP BY u.name, d.name, c.name"
                            elif choiceFinal == "14": 
                                query = "SELECT u.name AS university_name, COUNT(DISTINCT b.ISBN_13) AS count_of_books, SUM(b.price * b.quantity) AS total_book_cost FROM University u JOIN Department d ON u.universityID = d.universityID JOIN Course c ON d.departmentID = c.departmentID LEFT JOIN CartBookAssociation cba ON c.courseID = cba.ISBN_13 LEFT JOIN Book b ON cba.ISBN_13 = b.ISBN_13 GROUP BY u.name"
                            elif choiceFinal == "15":
                                query = "SELECT e.firstName, e.lastName COUNT(t.ticketID) AS count_of_tickets_created FROM Employee e RIGHT JOIN CustomerSupportUser CS ON e.employeeID = CS.employeeID LEFT JOIN TroubleTicket t ON cs.employeeID = t.employeeID GROUP BY e.employeeID"
                            elif choiceFinal == "16":
                                query = "SELECT e.firstName, e.lastName, e.salary FROM Employee e WHERE e.employeeID IN (SELECT employeeID FROM Administrator) ORDER BY e.salary"
                            elif choiceFinal == "17": 
                                query = "SELECT e.firstName, e.lastName, COUNT(t.ticketID) AS count_of_tickets_closed FROM Employee e RIGHT JOIN Administrator a ON e.employeeID = a.employeeID LEFT JOIN Ticket t ON a.administratorID = t.assignedTo WHERE t.status=’Closed’ GROUP BY e.employeeID"
                            elif choiceFinal == "18": 
                                query = "SELECT t.status, COUNT(CASE WHEN t.studentID IS NOT NULL THEN t.ticketID END) AS count_by_student, COUNT(CASE WHEN t.employeeID IS NOT NULL THEN t.ticketID END) AS count_by_customer_support FROM Ticket t GROUP BY t.status"
                            elif choiceFinal == "19": 
                                query = "SELECT AVG(DATEDIFF(t.dateClosed, t.dateLogged)) AS avg_ticket_duration FROM Ticket t"
                            elif choiceFinal == "20":
                                query = "SELECT (*) FROM Ticket t WHERE t.status = 'closed' ORDER BY t.ticketID"
                            #elif choiceFinal == "21": 

                            #elif choiceFinal == "22":

                            elif choiceFinal == "23":
                                query = "SELECT b.title AS book_title, AVG(r.rating) AS overall_rating, COUNT(DISTINCT r.studentID) AS count_of_students_rated FROM Book b LEFT JOIN Rating r ON b.ISBN_13 = r.ISBN_13 GROUP BY b.title ORDER BY overall_rating DESC, count_of_students_rated DESC"
                            elif choiceFinal == "24":
                                query = "SELECT b.title AS book_title, r.rating, s.firstName AS student_first_name, s.lastName AS student_last_name, u.name AS university_name FROM Book b LEFT JOIN Rating r ON b.ISBN_13 = r.ISBN_13 LEFT JOIN Student s ON r.studentID = s.studentID LEFT JOIN University u ON s.universityID = u.universityID WHERE r.rating = 5"
                            else:
                                print("Please enter a valid number.")

                            cursor.execute(query)
                            result = cursor.fetchall()
                        
                            print(f"Result for option {choice}:")
                            for row in result:
                                print(row)

                            cursor.close()
                    else:
                        print("Invalid choice. Please enter a number in the correct domain")

    except mysql.connector.Error as err:
        print("Error:", err)
    
if __name__ == "__main__":
    main()

