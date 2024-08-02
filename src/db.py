from pymongo import MongoClient
def get_all_chats(user_id,convo_id):
    try: 
        client=MongoClient('mongodb://localhost:27017')
        collection = client.conversations_db.conversations
        convos=collection.find({'user_id':user_id})[0]['conversations']
        title=""
        out_chats=[]
        for convo in convos:
            if convo['id']==convo_id:
                title=convo['title']
                chats=convo['chats']
                for chat in chats:
                    temp=[]
                    temp.append(chat['Human'].replace("\n","<br>"))
                    temp.append(chat['Bot'].replace("\n","<br>"))
                    out_chats.append(temp)

                
                return out_chats

        
    except Exception as e:
        print(e)

def add_chat(user_id,convo_id,chat):
    try: 
        client=MongoClient('mongodb://localhost:27017')
        collection = client.conversations_db.conversations
        convos=collection.find({'user_id':user_id})[0]['conversations']
        for i in range(len(convos)):
            if convos[i]['id']==convo_id:
                data={'Human':chat[0],'Bot':chat[1]}
                convos[i]['chats'].append(data)
                collection.update_one(
                    {"user_id": user_id, "conversations.id": convo_id},
                    {"$set": {"conversations.$.chats": convos[i]['chats']}}
                )
    except Exception as e:
        print(e)
def get_databases(user_id):
    client=MongoClient('mongodb://localhost:27017')
    collection = client.conversations_db.user_vectordbs
    databases=collection.find_one({'user_id':user_id})['databases']
    return databases


def add_conversation(user_id,convo_id,chats):
    try:
        client=MongoClient('mongodb://localhost:27017')
        collection = client.conversations_db.conversations
        user=collection.find_one({'user_id':user_id})

        new_conversation={
            "id":convo_id,
            "title":chats[0][:50],
            "chats": [
                {
                "Human":chats[0],
                'Bot':chats[1] 
                }
            ]
            
             
        }
        
        user['conversations'].append(new_conversation)
        collection.update_one({"user_id": user_id}, {"$set": {"conversations": user['conversations']}})

        
    except Exception as e:
        print(e)
    


def add_user(user_id):
    try:
        client=MongoClient('mongodb://localhost:27017')
        collection = client.conversations_db.conversations
        new_user={
            "user_id":user_id,
            "conversations":[]
        }
        collection.insert_one(new_user)
        add_database(user_id)
    except Exception as e:
        print(e)
def add_database(user_id):
    try:
        client=MongoClient('mongodb://localhost:27017')
        collection = client.conversations_db.user_vectordbs
        new_user={
            "user_id":user_id,
            "databases":['medical-data']
        }
        collection.insert_one(new_user)
    
    except Exception as e:
        print(e)


def get_latest_convoid(user_id):
    try: 
        client=MongoClient('mongodb://localhost:27017')
        collection = client.conversations_db.conversations
        convos=collection.find({'user_id':user_id})[0]['conversations']
        ans=0
        for convo in convos:
            ans=convo['id']
        return ans
            

                
                

    except Exception as e:
        print(e)


def get_all_conversations(user_id):
    try:
        out_convos=[]
        client=MongoClient('mongodb://localhost:27017')
        collection = client.conversations_db.conversations
        convos=collection.find({'user_id':user_id})[0]['conversations']
        for convo in convos:
            temp={}
            temp['id']=convo['id']
            temp['title']=convo['title']
            out_convos.append(temp)
        return out_convos
    except Exception as e:
        print(e)

def get_chat_history(user_id,convo_id):
    try: 
        client=MongoClient('mongodb://localhost:27017')
        collection = client.conversations_db.conversations
        convos=collection.find({'user_id':user_id})[0]['conversations']
        chat_history=""
        for convo in convos:
            if convo['id']==convo_id:
                chats=convo['chats']
                for chat in chats:
                    chat_history+=("Human: "+ chat['Human']+"\n")
                    chat_history+=("AI: " +chat['Bot']+"\n")
                
                return chat_history
        return chat_history

        
    except Exception as e:
        print(e)





# store_chat("neel1010",1,['jai hind','jai jai garvi gujarat'])
# add_conversation("neel1010",2,chats=['jai hind','jai jai garvi gujarat'])

# data={
#         "user_id": "neel1010",
#         "conversations": [
#             {
#             "id":1,
#             "title":"Hello",

#             "chats": [
#                 {
#                 "Human":"Hello how are you?",
#                 'Bot':"Bas, majama tame kem?"
#                 },
#                 {
#                 "Human":"Hello how are you?",
#                 'Bot':"Bas, majama tame kem?"
#                 }
                
#             ]
#             }
            
#         ]
#         }
        # collection.insert_one(data)