


## DocGPT- A medical chatbot

DocGPT is a robust web application tailored for the medical industry, equipped with tons of features. Its primary function is to address user queries, particularly those pertaining to medical concerns or patient ailments.
\
\
With its advanced capabilities, DocGPT efficiently processes and responds to user inquiries. One of DocGPT’s standout features is its memory, which retains past conversations between users and the system. This enables it to provide more personalized and contextually relevant responses by considering previous interactions. Additionally, DocGPT allows users to seamlessly navigate through previous conversations and even continue them if desired.
\
\
 This feature enhances user
experience and streamlines communication. Users also have the option to augment the existing database of medical documents by adding their own data or create entirely new databases tailored to their specific needs. Furthermore, DocGPT offers functionalities
such as speech-to-text input and text-to-speech output, catering to users who require alternative means of interaction. In summary, DocGPT is a comprehensive solution designed to facilitate medical inquiries and streamline communication between users and the system, offering advanced features for enhanced usability and effectiveness.

## Implementation

To present this medical question-answering model to the end user, I have developed a web application. The front end of the website was created using HTML, CSS, and JavaScript to provide a user-friendly interface. The front end allows users to input their queries and interact with the system seamlessly.
On the backend, I implemented the application using Flask, a lightweight Python web framework. Flask handles the incoming requests from the web server and interacts with
the Llama 2 model and the MongoDB database to process and retrieve the relevant information. \
\
The backend Python code includes functions to connect to the MongoDB server, perform CRUD (Create, Read, Update, Delete) operations on the database, and manage the data retrieval process. When a user submits a query through the web interface, Flask uses
these functions to retrieve the relevant information from the database and pass it to the Llama 2 model for processing.

### Landing Page

Shown figure is the landing page of the DocGPT it Displays suggestions for types of questions users can ask DocGPT.


![App Screenshot](https://raw.githubusercontent.com/SpartaNeel1010/DocGPT--A-Medical-Chatbot/main/Images/Landing%20page.png)

This is the chat page of the application. Chats are displayed as shown in the figure. 
\
\
![App Screenshot](https://raw.githubusercontent.com/SpartaNeel1010/DocGPT--A-Medical-Chatbot/main/Images/chats.png)


Previous conversation are stored on left side as shown in the Figure. User can navigate
between these conversation. These conversations are stored in MongoDB database and
linked to the userid.
\
\
![App Screenshot](https://raw.githubusercontent.com/SpartaNeel1010/DocGPT--A-Medical-Chatbot/main/Images/previous_conversation.png)

User can add documents to database or create a new database by clicking on create
button as shown in figure.
\
\

![App Screenshot](https://raw.githubusercontent.com/SpartaNeel1010/DocGPT--A-Medical-Chatbot/main/Images/create_database.png)

When user has clicked on the shown button, website is redirected to the create database page.
As shown in the fig user is given two option. In one option user can add documents
to the database or create new database.

![App Screenshot](https://raw.githubusercontent.com/SpartaNeel1010/DocGPT--A-Medical-Chatbot/main/Images/options_database.png)

Fig below shows the page where user can add to the existing database of the DocGPT,
user have to upload the documents in the drag area and have to click on the upload
button. Once the button is clicked all the documents are passed through the pipeline
and stored into the existing DocGPT database

![App Screenshot](https://raw.githubusercontent.com/SpartaNeel1010/DocGPT--A-Medical-Chatbot/main/Images/add_existing.png)

When user clicked on the add new database, page is shown. On this page user have to add name of the database and upload the documents which they want in the new
database. Once these documents are uploaded upload confirmation page is shown and then user is redirected to landing page.

![App Screenshot](https://raw.githubusercontent.com/SpartaNeel1010/DocGPT--A-Medical-Chatbot/main/Images/new_database%20(1).png)


In the login page user can login to the app using userid and password or user can login
using google authentication also. If user is not registered he can register using by clicking
on register here, the user will be redirected to register page.

## Login page
![App Screenshot](https://raw.githubusercontent.com/SpartaNeel1010/DocGPT--A-Medical-Chatbot/main/Images/Login%20(1).png)

## Register page
![App Screenshot](https://raw.githubusercontent.com/SpartaNeel1010/DocGPT--A-Medical-Chatbot/main/Images/register.png)

## Working of the project 
![App Screenshot](https://raw.githubusercontent.com/SpartaNeel1010/DocGPT--A-Medical-Chatbot/main/Images/working.png)

