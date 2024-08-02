from dotenv import load_dotenv
import google.oauth2
from src.helper import *
from flask import render_template,redirect,jsonify,request,Flask,url_for,session,abort
from src.prompt import template
from src.db import *
from requests import get
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from src.create import *
import PyPDF2
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
import os,pathlib,requests
import oauth2


load_dotenv()
embedding_model=get_embedding_model()
dbname="medical-data"
db=get_indexed_data(embedding_model,dbname)
llm=get_llm()
chain,memory=get_chain_and_memory(llm,template)


app=Flask(__name__)
app.secret_key = 'thisisasecretkey'

client = MongoClient('mongodb://localhost:27017/')
users_collection = client.conversations_db.users

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = "your_ID"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)

def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper




class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

    @staticmethod
    def get(user_id):
        user_data = users_collection.find_one({"_id": user_id})
        if user_data:
            return User(user_id)
        return None

    @staticmethod
    def create(user_id, password):
        hashed_password = generate_password_hash(password)
        users_collection.insert_one({"_id": user_id, "password": hashed_password})
        add_user(user_id)
        return User(user_id)

    def check_password(self, password):
        user_data = users_collection.find_one({"_id": self.id})
        if user_data:
            return check_password_hash(user_data['password'], password)
        return False

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/convo/<int:id>",methods=['POST','GET'] )
@login_required
def update(id):
    user_id=current_user.id
    convo_id=id
    databases=get_databases(user_id)
    if request.method=='POST':
        query=request.form['inp_text']
        chat_history=get_chat_history(user_id,convo_id)
        
        print(chat_history)
        
        temp_chat=chat_history.replace("Human:","")
        temp_chat=temp_chat.replace("AI:","")
        search=temp_chat + " \n" + query
        db = Pinecone.from_existing_index(dbname, embedding_model)
        ans=db.similarity_search(search,k=3)
        context=""
        for i in ans:
            context+=f"Document: {i.page_content} \n \n"

        response = chain({"input_documents": ans,"query":query,"context": context,'chat_history':chat_history})
        # response={}
        # response['output_text']=get_response(query)
        # memory.save_context({'query': f'{query}'}, {'output': f"{response['output_text']}!"})

        add_chat(user_id,convo_id,chat=[query,response['output_text']])

        chats=get_all_chats(user_id,convo_id)
        convos= get_all_conversations(user_id)
        action=f"convo/{convo_id}"
        return render_template('index.html',chats=chats,convos=convos[::-1],action=action,databases=databases,current_db=dbname)
    
    
    convos=get_all_conversations(user_id)
    chats= get_all_chats(user_id,convo_id)
    action=f"convo/{convo_id}"
    return render_template('index.html',chats=chats,convos=convos[::-1],action=action,user_id=user_id,databases=databases,current_db=dbname)


@app.route("/logout",methods=['POST','GET'] )
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect("/")


@app.route("/new",methods=['POST','GET'] )
@login_required
def clear_memory():
    memory.clear()
    return redirect("/")

@app.route("/login",methods=['POST',"GET"])
def login():
    if request.method == 'POST':
        user_id = request.form['user_id']
        print(user_id)
        password = request.form['pass']
        print(password)
        user = User.get(user_id)
        print(user)
        if user and user.check_password(password):
            login_user(user)
            return redirect("/")
        else:
            errorText= "Invalid username or password. Please try again."
            return render_template('login.html',errorText=errorText)
    return render_template('login.html',errorText="")

@app.route("/register",methods=['POST',"GET"])
def register():
    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['pass']
        repass= request.form['repass']
        if(password != repass):
            errorText= "Both password fields do not match"
            return render_template('register.html',errorText=errorText)
        elif User.get(user_id):
            errorText= "User already exists. Please choose a different username. "
            return render_template('register.html',errorText=errorText)
        else:
            User.create(user_id, password)
            return redirect('/login')
        
    return render_template('register.html',errorText="")


@app.route("/google_login")
def google_login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )
    email = id_info.get("email")
    session["email"] = email
    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    user_id=email.split('@')[0]
    if User.get(user_id):
        user = User.get(user_id)
        print(user)
        login_user(user)
        return redirect("/")
    else:
        User.create(user_id, "")
        user = User.get(user_id)
        print(user)
        login_user(user)
        return redirect('/')



@app.route("/",methods= ['POST','GET'])
def generate():
    if not current_user.is_authenticated:
         return redirect("/login")
    
    user_id=current_user.id
    print(user_id)
    databases=get_databases(user_id)
    print(databases)
    current_convo_id=get_latest_convoid(user_id)
    # print(current_convo_id)
    if request.method=='POST':
        query=request.form['inp_text'] 
        # print(query)
        chat_history=memory.load_memory_variables({})['chat_history']
        
        temp_chat=chat_history.replace("Human:","")
        temp_chat=temp_chat.replace("AI:","")

        search=temp_chat + " \n" + query
        db = Pinecone.from_existing_index(dbname, embedding_model)
        print(dbname)
        ans=db.similarity_search(search,k=3)
        print(ans)
        context=""
        for i in ans:
            context+=f"Document: {i.page_content} \n \n"

        response = chain({"input_documents": ans,"query":query,"context": context,'chat_history':chat_history})
        # response={}
        # response['output_text']=get_response(query)
        # memory.save_context({'query': f'{query}'}, {'output': f"{response['output_text']}!"})

        chat_history=memory.load_memory_variables({})['chat_history']
        chats= generate_chats(chat_history)

        if len(chats)==1:
            current_convo_id+=1
            add_conversation(user_id,current_convo_id,chats=[query,response['output_text']])
            convos=get_all_conversations(user_id)
        else:
            
            add_chat(user_id,current_convo_id,chat=[query,response['output_text']])

        chats=get_all_chats(user_id,current_convo_id)
        convos= get_all_conversations(user_id)
        return render_template('index.html',chats=chats,convos=convos[::-1],action="",user_id=user_id,databases=databases,current_db=dbname)
    
    chat_history=memory.load_memory_variables({})['chat_history']
    chats= generate_chats(chat_history)
    convos=get_all_conversations(user_id)
    return   render_template('index.html',chats=chats,convos=convos[::-1],action="",user_id=user_id,databases=databases,current_db=dbname)

@app.route("/create")
@login_required
def create():
    if not current_user.is_authenticated:
         return redirect("/login")
    
    user_id=current_user.id
    return render_template('create.html',user_id=user_id)

def read_pdf(pdf_file): 
    from PyPDF2 import PdfReader
    pdf_reader = PdfReader(pdf_file)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

@app.route("/adddata",methods=['GET','POST'])
@login_required
def adddata():
    if not current_user.is_authenticated:
         return redirect("/login")
    
    if request.method == 'POST':
        import PyPDF2
        uploaded_files = request.files.getlist('files')
        pdf_contents =""
        for file in uploaded_files:
            pdf_text = read_pdf(file)
            pdf_contents += pdf_text
                
        try:
            add_data_to_vectordb(pdf_contents,"medical-data")
            data="Successfully added your data to the DocGPT vector database"
            return render_template('updatesuccess.html',data=data)
        except Exception as e:
            return e

    user_id=current_user.id
    return render_template('adddata.html',user_id=user_id)
 

@app.route("/owndata",methods=['GET','POST'])
@login_required
def owndata():
    if not current_user.is_authenticated:
         return redirect("/login")
    user_id=current_user.id
    if request.method == 'POST':
        uploaded_files = request.files.getlist('files')
        dbname=request.form['dbname']
        print(dbname)
        print(uploaded_files)
        pdf_contents =""
        for file in uploaded_files:
            pdf_text = read_pdf(file)
            pdf_contents += pdf_text
                
        try:
            create_index(dbname,user_id)
            add_data_to_vectordb(pdf_contents,dbname)
            data=f"Successfully created {dbname} vectordb and added your data to it."
            return render_template('updatesuccess.html',data=data)
        except Exception as e:
            print(e)
            return e.__str__()
    
    user_id=current_user.id
    return render_template('owndata.html',user_id=user_id)

@app.route("/database/<string:name>")
@login_required
def change_dbname(name):
    global dbname
    dbname=name
    return redirect("/new")
if __name__=="__main__":
    app.run(debug=True)