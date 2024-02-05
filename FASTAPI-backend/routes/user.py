from fastapi import APIRouter,HTTPException
from models.user import *
from config.db import conn 
from schemas.user import serializeDict, serializeList
from bson import ObjectId
from datetime import datetime
import re
from bson.regex import Regex

event = APIRouter() 
# from fastapi import status

@event.get('/')
async def find_all_users():
    return serializeList(conn.EventWiz.users.find())

# /////////////////////////////ADMIN///////////////////////////////////////////

# admin login 
@event.post("/adminlogin")
async def admin_login(data:Admin):
    adminform = dict(data)
    # print(adminform)
    adminlist = conn.EventWiz.admin.find({"$and": [{"username":adminform["username"]},{"pwd":adminform["pwd"]}]})
    content = serializeList(adminlist)
    # print(content)
    if (len(content) != 0):
        # print(content)
        # singledict = content[0]
        # print(singledict["applied_org"])
        # singledict["applied_org"] = serializeList(singledict["applied_org"])

        return content
    else:
        return {"error":"Invalid Username Password","success":False}

# fetching all organisations
@event.get("/allorganisations")
async def fetch_all_org():
    return serializeList(conn.EventWiz.organisation.find())

#searching any org by org-name
@event.post("/searchingorgbyname")
async def search_org_byname(data:dict):
    search_query = data["clubname"]
    regex_pattern = re.compile(f"^{re.escape(search_query)}.*", re.IGNORECASE)
    result = conn.EventWiz.organisation.find({"clubname": {"$regex": regex_pattern}})

    result = serializeList(result)
    if result:
        # print(result)
        return result
    else:
        return {"error":"No organisation found","success":False}

#search org member details
@event.post("/adminorgsearchfilter")
async def org_search_filters(data:dict):

    memberlist = data["memberlist"]
    # print(memberlist)
    newdata = data
    del newdata["memberlist"]

    # print(newdata)
    if (newdata["expiry_date"] != ''):
        # data["expiry_date"] = data["expiry_date"].strftime("%Y-%m-%d")
        newdata["expiry_date"] = datetime.strptime(newdata["expiry_date"], "%Y-%m-%d")
    if (newdata["start_date"] != ''):    
        # data["start_date"] = data["start_date"].strftime("%Y-%m-%d")
        newdata["start_date"] = datetime.strptime(newdata["start_date"], "%Y-%m-%d")

    # print(data)
    filtered_data = {}
    for key, value in newdata.items():
        if (value != '' or value != ""):
          filtered_data[key] = value
    print(filtered_data)

    if not filtered_data:
        return {"error": "Empty Filter inputs", "success": False}

    print("inside else")
    result = []
    partial_name = data.get("membername", "")
    regex_pattern = re.compile(f"{re.escape(partial_name)}.*", re.IGNORECASE)

    for memberdict in memberlist:
        if "name" in memberdict and re.match(regex_pattern, memberdict["name"]):
            result.append(memberdict)

    print(result)
    if result:
        return result
    else:
        return {"error": "No such Member found", "success": False}

#admin side org member table filters
@event.post("/adminorgmemberstablefilters")
async def adminside_orgmembertablefilter(filters:dict):
    data = filters["filterdict"]
    filtered_data = {}
    for key, value in data.items():
        if (value != '' or value != ""):
            filtered_data[key] = re.escape(value)
    #print(filtered_data)
    content = []
    if (len(filtered_data) != 0):
        
        regex_patterns = {}
        for key, value in data.items():
            if value:
                regex_patterns[key] = re.compile(f'^{re.escape(value)}', re.IGNORECASE)

        # print (regex_patterns)
        # organisation = conn.EventWiz.organisation.find_one({"_id":ObjectId(orgid)})
        membersList = filters["memberlist"]
        # if membersList:
            # org1 = serializeDict(organisation)
            # membersList = org1["members"]
        if (membersList != []):
            for memberdict in membersList:
                match = all(regex.match(str(memberdict.get(key, ''))) for key, regex in regex_patterns.items())
                if match:
                    content.append(memberdict)
            if content:
                return content
            else:
                return {"error":"No Members","success":False}
        else:
            return {"error":"No Members","success":False}
        # else:
        #     return {"error":"Organisation not found","success":False}
    else:
        
        return {"error":"Please enter data in filter input","success":False,"data_dict":"empty"}
    
    
# admin side loggedin members
@event.post("/loggedinmembers") 
async def loggedin_members(data:dict):

    logginemembers = []
    for singledict in data["data"]:
        if singledict["loggedin"] == True :
            logginemembers.append(singledict)
    if logginemembers:
        # print(logginemembers)
        return logginemembers
    else:
        return {"error":"No loggedin members","success":False}
        # print("no members has loggedin")
    
   
# admin side loggedin members
@event.post("/inactivemembers") 
async def inactive_members(data:dict):

    inactivemembers = []
    for singledict in data["data"]:
        if singledict["loggedin"] == False :
            inactivemembers.append(singledict)
    if inactivemembers:
        # print(logginemembers)
        return inactivemembers
    else:
        return {"error":"No loggedin members","success":False}
        # print("no members has loggedin")

# fetching all users
@event.get("/adminmemberdetails")
async def adminside_allusers():
    result = conn.EventWiz.users.find({})
    result = serializeList(result)
    # print(result)
    if result:
        for i in result:
            if i["expiry_date"]:
                i["expiry_date"] = i["expiry_date"].strftime("%Y-%m-%d")
            if i["start_date"]:
                i["start_date"] = i["start_date"].strftime("%Y-%m-%d")
        return result
    else:
        return {"error":"No Users","success":False}
    
# fetching all new users
@event.get("/fetchingnewusers")
async def adminside_allnewusers():
    newuserslist = []
    result = conn.EventWiz.users.find({})
    result = serializeList(result)
    # print(result)
    if result:
        for i in result:
            if (i["memberid"] == None):
                newuserslist.append(i)
        # print(newuserslist)
        return newuserslist
    else:
        return {"error":"No New Users","success":False}

# searching user by name , start_date/expiry_date
@event.post("/usersearchform")
async def adminside_searchuser(data:dict):
    memberlist = serializeList(conn.EventWiz.users.find({}))
    # print(memberlist)

    # print(newdata)
    if (data["expiry_date"] != ''):
        # data["expiry_date"] = data["expiry_date"].strftime("%Y-%m-%d")
        data["expiry_date"] = datetime.strptime(data["expiry_date"], "%Y-%m-%d")
    if (data["start_date"] != ''):    
        # data["start_date"] = data["start_date"].strftime("%Y-%m-%d")
        data["start_date"] = datetime.strptime(data["start_date"], "%Y-%m-%d")

    # print(data)
    filtered_data = {}
    for key, value in data.items():
        if (value != '' or value != ""):
          filtered_data[key] = value
    print(filtered_data)

    if not filtered_data:
        return {"error": "Empty Filter inputs", "success": False}

    print("inside else")
    result = []
    partial_name = data.get("membername", "")
    regex_pattern = re.compile(f"{re.escape(partial_name)}.*", re.IGNORECASE)

    for memberdict in memberlist:
        if "name" in memberdict and re.match(regex_pattern, memberdict["name"]):
            result.append(memberdict)

    print(result)
    if result:
        return result
    else:
        return {"error": "No such Member found", "success": False}
    
# admin side user section table filters
@event.post("/adminusertablefilters")
async def allusers_tablefilters(data:dict):
    allfiltersdata = data["data"]

    filtered_data = {}
    for key, value in allfiltersdata.items():
        if (value != '' or value != ""):
            filtered_data[key] = re.escape(value)
    print(filtered_data)
            
    content = []
    if (len(filtered_data) != 0):
        
        regex_patterns = {}
        for key, value in filtered_data.items():
            if value:
                regex_patterns[key] = re.compile(f'^{re.escape(value)}.*', re.IGNORECASE)
        print(regex_patterns)
        
        membersList = serializeList(conn.EventWiz.users.find({}))

        print(membersList)
        if membersList:
            
            for memberdict in membersList:
                match = all(regex.match(str(memberdict.get(key, ''))) for key, regex in regex_patterns.items())
                if match:
                   content.append(memberdict)
            print(content)
            if content:
                for i in content:
                    if i["expiry_date"]:
                        i["expiry_date"] = i["expiry_date"].strftime("%Y-%m-%d")
                    if i["start_date"]:
                        i["start_date"] = i["start_date"].strftime("%Y-%m-%d")
                return content
            else:
                return {"error":"No Members","success":False}
   
        else:
            return {"error":"No members","success":False}
    else:
        
        return {"error":"Please enter data in filter input","success":False,"data_dict":"empty"}
    
   
#fetching all appiled organisations
@event.get("/allappliedorg")
async def adminside_allappliedorg():
    appliedlist = serializeList(conn.EventWiz.admin.find())
    # print(appliedlist)
    
    for singledict in appliedlist:
        content = singledict["applied_org"]

    # print(content)
    if (len(content) != 0):
        return serializeList(content)
    else:
        return {"error":"No Applied Organisation","success":False}

# searching by organisation name
@event.post("/searchorgbyname")
async def adminside_searchorgbyname(data:dict):
    # clubname = data["clubname"]
    # print(clubname)
    search_org = data["clubname"]
    regex_pattern = f".*{re.escape(search_org)}.*"
    pipeline = [
        {"$unwind": "$applied_org"},
        {"$match": {"applied_org.clubname": Regex(regex_pattern, "i")}},
    ]
    adminlist = conn.EventWiz.admin.aggregate(pipeline)
    
    content = []

    if adminlist:
        # print(adminlist)
        for admin in adminlist:
            org_dict = admin.get("applied_org", {})
            content.append(org_dict)
        # print(content)
        if content:
            return content
        else:
            return {"error":"Organisation Not Found","success":False}
    else:
        return {"error":"No Admin Data","success":False}

# admin side applied org table filters
@event.post("/appliedorgtablefilters") 
async def adminside_applied_orgtablefilters(data:dict):
    print(data)
    allfiltersdata = data["data"]

    filtered_data = {}
    for key, value in allfiltersdata.items():
        if (value != '' or value != ""):
            filtered_data[key] = re.escape(value)
    # print(filtered_data)
    content = []

    if (len(filtered_data) != 0):
        
        regex_patterns = {}
        for key, value in allfiltersdata.items():
            if value:
                regex_patterns[key] = re.compile(f'^{re.escape(value)}.*', re.IGNORECASE)
        print(regex_patterns)
        
        membersList = serializeList(conn.EventWiz.users.find({}))

        
        appliedlist = serializeList(conn.EventWiz.admin.find({}))
        for singleapplieddict in appliedlist:
            membersList = singleapplieddict["applied_org"]

        if membersList:
            
            for memberdict in membersList:
                match = all(regex.match(str(memberdict.get(key, ''))) for key, regex in regex_patterns.items())
                if match:
                   content.append(memberdict)
            print(content)
            if content:
                return content
            else:
                return {"error":"Organisation not found","success":False}
   
        else:
            return {"error":"No Applied Organisation","success":False}
    else:
        
        return {"error":"Please enter data in filter input","success":False,"data_dict":"empty"}

# accepting org
@event.post("/acceptingorg")
async def adminside_acceptorg(data:dict):
    # print(data["data"])
    acceptedOrg = data["data"]
    result = conn.EventWiz.organisation.insert_one(acceptedOrg)

    adminlist = serializeList(conn.EventWiz.admin.find())

    for singleadmin in adminlist:
        appliedorglist = singleadmin["applied_org"]

        updated_org = [i for i in appliedorglist if i["clubname"] != acceptedOrg["clubname"]]
        # #print("Updated Member list",updated_members)
        content = conn.EventWiz.admin.find_one_and_update({"_id":ObjectId(singleadmin["_id"])},{"$set": {"applied_org":updated_org}})
    if content:
        return True
    else:
        return {"error":"Nothing To Update", "success":False}
    
# rejecting org
@event.post("/rejectingorg")
async def adminside_rejectorg(data:dict):
    # print(data["data"])
    acceptedOrg = data["data"]
    result = conn.EventWiz.rejectedorg.insert_one(acceptedOrg)

    adminlist = serializeList(conn.EventWiz.admin.find())

    for singleadmin in adminlist:
        appliedorglist = singleadmin["applied_org"]

        updated_org = [i for i in appliedorglist if i["clubname"] != acceptedOrg["clubname"]]
        # #print("Updated Member list",updated_members)
        content = conn.EventWiz.admin.find_one_and_update({"_id":ObjectId(singleadmin["_id"])},{"$set": {"applied_org":updated_org}})
    if content:
        return True
    else:
        return {"error":"Nothing To Update", "success":False}
    


# /////////////////////////////////////////////////////////////////////////////

# //////////////////////////////////////USER////////////////////////////////////

# user login
@event.post('/userlogin/')
async def check_user(data:dict):
    if data["clubname"] == "None" or data["clubname"] == "":
        data["clubname"] = None 
    flag=0
    d1= {}
    u1 = conn.EventWiz.users.find_one({"$and": [{"username":data["username"]},{"pwd":data["pwd"]},{"clubname":data["clubname"]}]})
    u3 = conn.EventWiz.organisation.find_one({"clubname":data["clubname"]})
    if u1:
        return serializeDict(u1)
    elif u3:
        user3 = serializeDict(u3)
        #print(user3)
        membersList =  user3["members"]
        for singleDict in membersList:
            if (singleDict["username"] == data["username"]) and (singleDict["pwd"] == data["pwd"]):
                flag =1
                d1 = singleDict
                d1["clubname"] = data["clubname"]
                singleDict["loggedin"] = True       

                print(membersList)
                conn.EventWiz.organisation.find_one_and_update({"clubname":d1["clubname"]},{"$set": {"members":membersList}})

                del d1["loggedin"]
                conn.EventWiz.users.insert_one(d1)

                
                return serializeDict(d1)
        if flag == 0:
            return {"error":"Invalid Username , Password and Clubname","success":False}
    else : 
        return {"error":"Invalid Clubname","success":False}


# user registration 
@event.post('/userregistration/')
async def create_user(user: User):
    d1 = dict(user)
    # print(d1)
    allorg = conn.EventWiz.organisation.find()
    allorg = serializeList(allorg)

    usernameList = []
    for singleorg in allorg:
        memberlist = singleorg["members"]
        for i in memberlist:
            usernameList.append(i["username"])
    allactiveusers = conn.EventWiz.users.find()
    allactiveusers = serializeList(allactiveusers)
    for j in allactiveusers:
        usernameList.append(j["username"])

    uniqueusernameList = list(set(usernameList)) 
    # print(uniqueusernameList)

    if d1["username"] in uniqueusernameList:
        return {"error":"Username already exists","success":False}
    else:
        conn.EventWiz.users.insert_one(dict(user))
        return dict(user)
 

# Get all Post For Users
@event.post("/fetchingallpostforuser/{uname}")
async def fetch_all_post_userside(uname:str):
    result = conn.EventWiz.post.find()
    posts = []
    if (result != []):
        allpost = serializeList(result)
        for i in allpost:
            if len(i["participate"]) !=0:
                for j in i["participate"]:
                    if j["username"] == uname:
                        break
                else:
                    i["event_start_date"] = i["event_start_date"].strftime("%d-%m-%Y")
                    i["event_end_date"] = i["event_end_date"].strftime("%d-%m-%Y")
                    posts.append(i)
            else:
                i["event_start_date"] = i["event_start_date"].strftime("%d-%m-%Y")
                i["event_end_date"] = i["event_end_date"].strftime("%d-%m-%Y")
                posts.append(i)
        return (posts)
    else:
        return {"error":"No post found","success":False}

# Post Filter for user
@event.post("/postfilterforuser")
async def postfilter_user(data : dict):
    query = {}
    print(data)
    and_conditions = []

    for field, value in data.items():
        if field in ["event_start_date", "event_end_date"] and value != "":
            value = datetime.strptime(value, "%Y-%m-%d")
            if field == "event_start_date":
                and_conditions.append({"event_start_date": {"$gte": value}})
            if field == "event_end_date":
                and_conditions.append({"event_start_date": {"$lte": value}})

        if field in ["minprice", "maxprice"] and value != "":
            if field == "minprice":
                and_conditions.append({"ticket_price": {"$gte": float(value)}})
            if field == "maxprice":
                and_conditions.append({"ticket_price": {"$lte": float(value)}})

        if field == "venue_city" and value != "":
            regex_pattern = re.compile(f"^{re.escape(value)}", re.IGNORECASE)
            and_conditions.append({"venue_city": {"$regex": regex_pattern}})
        
        if field == "type" and value!="":
            and_conditions.append({"type":value})
        if field == "clubname" and value!="":
            and_conditions.append({"clubname":value})

    
    if and_conditions:
        query["$and"] = and_conditions

    # Find posts based on the query
    result = conn.EventWiz.post.find(query)

    # Iterate over the result and print each post
    response_list = serializeList(result)
    if response_list:
        lis = []
        d1 = {}
        for singleDict in response_list:
            d1 = singleDict
            d1["event_start_date"] = d1["event_start_date"].strftime("%d-%m-%Y")
            d1["event_end_date"] = d1["event_end_date"].strftime("%d-%m-%Y")
            lis.append(serializeDict(d1))
        return serializeList(lis)
    else:
        return {"error": "No Such Post Available", "success": False}

# User Participate in Event
@event.put("/eventparticipate/{id}")
async def event_participate(id:str,data:dict):
    data["age"] = int(data["age"])
    post = conn.EventWiz.post.find_one({"_id":ObjectId(id)})
    if post:
        p1 = serializeDict(post)["participate"]
        # print(p1)
        p1.append(data)
        conn.EventWiz.post.find_one_and_update({"_id":ObjectId(id)},{"$set": {"participate":p1}})
        return {"data": "Partcipated Successfully"}
    else:
        return {"error": "Event Not Found", "success": False}

# Post Search by User using Title
@event.post("/postsearchbyuser")
async def post_search_user(data : dict):
    result = conn.EventWiz.post.find()
    posts = []
    # print(data)
    regex_pattern = re.compile(f"^{re.escape(data['title'])}.*", re.IGNORECASE)
    # print(re.match(regex_pattern,title))
    
    if (result != []):
        allpost = serializeList(result)
        for i in allpost:
            if re.match(regex_pattern,i["event_title"]):
                if len(i["participate"]) !=0:
                    for j in i["participate"]:
                        if j["username"] == data["uname"]:
                            break
                    else:
                        i["event_start_date"] = i["event_start_date"].strftime("%d-%m-%Y")
                        i["event_end_date"] = i["event_end_date"].strftime("%d-%m-%Y")
                        posts.append(i)
                else:
                    i["event_start_date"] = i["event_start_date"].strftime("%d-%m-%Y")
                    i["event_end_date"] = i["event_end_date"].strftime("%d-%m-%Y")
                    posts.append(i)
        return posts

# Get All Organization for Subscribe
@event.get("/getallorganizatonforuser")
async def getall_organization():
    org = conn.EventWiz.organisation.find()
    if org:
        org1 = serializeList(org)
        return org1
    else:
        return {"error": "Organization Not Found", "success": False}

    
# User Subscribe 
@event.put('/usersubscribe')
async def user_subscribe(user: dict):
    
    appliedmem = user
    
    # print(appliedorg)
    flag =0
    orgdict = serializeDict(conn.EventWiz.organisation.find_one({"clubname":appliedmem["clubname"]}))
    # return orgdict
    if len(orgdict) !=0:
        orgmem = orgdict["members"]
        orgapplied = orgdict["memapplied"]
        if len(orgmem) !=0:
            for i in orgmem:
                if i["username"] == appliedmem["username"]:
                    return {"error":"Username already Exist", "success":False}
            else:
                if len(orgapplied) !=0:
                    for j in orgapplied:
                        if j["username"] == appliedmem["username"] and j["email"] == appliedmem["email"] and j["pnumber"] == appliedmem["pnumber"]:
                            return {"error":"Similar Username,MemberId,Email and Phone Number are already Applied", "success":False}
                    else:
                        orgapplied.append(appliedmem)
                        conn.EventWiz.organisation.update_one({"clubname":appliedmem["clubname"]}, {"$set":  {"memapplied": orgapplied}})
                        return {"data":"Applied For Subscription Successfully.","success":True}
                else:
                    orgapplied.append(appliedmem)
                    conn.EventWiz.organisation.update_one({"clubname":appliedmem["clubname"]}, {"$set":  {"memapplied": orgapplied}})
                    return {"data":"Applied For Subscription Successfully.","success":True}
        else:
            orgapplied.append(appliedmem)
            conn.EventWiz.organisation.update_one({"clubname":appliedmem["clubname"]}, {"$set":  {"memapplied": orgapplied}})
            return {"data":"Applied For Subscription Successfully.","success":True}
    else:
        return {"error":"Organization Not Found", "success":False}

# Get User Participated Events
@event.post("/userparticipated/{uname}")
async def user_participated(uname:str):
    post = conn.EventWiz.post.find()
    allpost=[]
    if post:
        postlist = serializeList(post)
        for singlepost in postlist:
            if len(singlepost)!=0:
                for singlepart in singlepost["participate"]:
                    if singlepart["username"] == uname:
                        singlepost["event_start_date"] = singlepost["event_start_date"].strftime("%d-%m-%Y")
                        singlepost["event_end_date"] = singlepost["event_end_date"].strftime("%d-%m-%Y")
                        allpost.append(singlepost)
        if len(allpost)!=0:
            return allpost
        else:
            return {"error":"You are not Participated in any Event", "success":False}
    else:
        return {"error":"Post Not Found", "success":False}
    
# Get Membership Type using Clubname and Username
@event.post("/filtermemtype")
async def filter_memtype(data : dict):
    org = serializeDict(conn.EventWiz.organisation.find_one({"clubname":data["clubname"]}))
    if len(org) !=0:
        memtype = org["memtype"]
        # print(memtype)
        for singlemember in org["members"]:
            if singlemember["username"] == data["username"]:
                memtype = [item for item in memtype if item["type"] != singlemember["membertype"]]
        return memtype




# //////////////////////////////////////////////////////////////////////////////

# ////////////////////////////////////////ORGANISATION///////////////////////////////////

# fetching all clubname
@event.get("/clubnames/")
async def get_clubnames():
    clubname = []
    cursor = conn.EventWiz.organisation.find({}, {"clubname": 1, "_id": 0})
    for i in serializeList(cursor):
        clubname.append(i["clubname"])
    return clubname

# Get all type of Membership 
@event.get("/allmembershiptype")
async def  all_membershiptype():
    allmemtype =[]
    allorg = conn.EventWiz.organisation.find({})
    if allorg:
        allorg1 = serializeList(allorg)
        for i in allorg1:
            if i["memtype"] != []:
                for j in i["memtype"]:
                    if j["type"] not in allmemtype:
                        allmemtype.append(j["type"])
    return allmemtype

# organisation login
@event.post('/organisationlogin/')
async def check_org(data:dict):
    # #print(data["username"])
    
    d1 = conn.EventWiz.organisation.find_one({"$and": 
    [
        {"username": data["username"]},
        {"pwd": data["pwd"]}
    ]
    })
    # #print(d1["username"],d1["pwd"])
    if d1:
        # #print(d1)
        return serializeDict(d1)
    else:
        return {"error": "No matching user found","success":False}
    

# organisation registration 
@event.post('/organisationregistration')
async def create_org(organisation: dict):

    appliedorg = organisation
    # print(appliedorg)

    allorg = conn.EventWiz.organisation.find()
    allorg = serializeList(allorg)
    orgusernameList = []
    for i in allorg:
        orgusernameList.append(i["username"])

    if  appliedorg["username"] in orgusernameList:
        return {"error":"Username Already Exists", "success":False}
    else:    
        adminlist = serializeList(conn.EventWiz.admin.find())
        # print(adminlist)
        if adminlist:
            for singleadmindict in adminlist:
                appliedlist = singleadmindict["applied_org"]
                for singleorg in appliedlist:
                    if singleorg["clubname"] == appliedorg  ["clubname"]:
                        return {"error":"You Have Already   Applied", "success":False}

                singleadmindict["applied_org"].append(appliedorg)
                conn.EventWiz.admin.update_one({"_id": ObjectId (singleadmindict["_id"])}, {"$set":      {"applied_org": singleadmindict["applied_org"]}})
            return {"message":"Applied Successfully"}
        else:
            return {"error":"No Admin Available",   "success":False}
    

    
    # newadminlist = serializeList(conn.EventWiz.admin.find())
    # print(newadminlist)


# organisation create post
@event.post('/createeventpost/')
async def create_event_post(data : EventPost):
    try:
        # Directly assign datetime.date objects
        data_dict = dict(data)
        if data_dict["type"] == "":
            return {"error":"Select Membership Type","success":False}
        data_dict["event_start_date"] = data_dict["event_start_date"].strftime("%Y-%m-%d")
        data_dict["event_end_date"] = data_dict["event_end_date"].strftime("%Y-%m-%d")
        data_dict["event_start_date"] = datetime.strptime(data_dict["event_start_date"], "%Y-%m-%d")
        data_dict["event_end_date"] = datetime.strptime(data_dict["event_end_date"], "%Y-%m-%d")
        
    except ValueError:
        raise HTTPException(status_code=422, detail="Invalid date format. Use 'yyyy-mm-dd'.")

    # Insert data into the database
    conn.EventWiz.post.insert_one(data_dict)

    return {"message": "Event data successfully submitted"}

# organisation fetch all post details
@event.post("/geteventposts")
async def get_event_posts(data : dict):
    response = conn.EventWiz.post.find({"clubname":data["clubname"]})
    # #print(serializeList(response))
    if response:
        lis = []
        d1= {}
        for singleDict in response:
            d1 = singleDict
            d1["event_start_date"] = d1["event_start_date"].strftime("%d-%m-%Y")
            d1["event_end_date"] = d1["event_end_date"].strftime("%d-%m-%Y")
            # conn.EventWiz.users.insert_one(d1)
            lis.append(serializeDict(d1))
        return serializeList(lis)
        # return serializeList(response)
    else:
        return {"error":"no post found","success":False}
    
# other organisation's fetch all post details
@event.post("/getotherorgeventposts")
async def get_other_org_eventposts(data : dict):
    response = conn.EventWiz.post.find({"clubname": {"$ne": data["clubname"]}})
    # #print(serializeList(response))
    if response:
        lis = []
        d1= {}
        for singleDict in response:
            d1 = singleDict
            d1["event_start_date"] = d1["event_start_date"].strftime("%d-%m-%Y")
            d1["event_end_date"] = d1["event_end_date"].strftime("%d-%m-%Y")
            # conn.EventWiz.users.insert_one(d1)
            lis.append(serializeDict(d1))
        return serializeList(lis)
        # return serializeList(response)
    else:
        return {"error":"no post found","success":False}

# organisation delete post 
@event.delete("/deleteeventposts/{id}")
async def delete_user(id):
    #fetch the details using id
    # if details found execute the delete query
    #always test in swagger first
    #then bind with UI
    response = serializeDict(conn.EventWiz.post.find_one_and_delete({"_id":ObjectId(id)}))
    if response:
        return True
    else:
        return {"error":"no post found","success":False}
    
# organisation filter functionality to fetch post
@event.post("/orgfilters")
async def org_filters(data: dict):
    # Build the query based on the filteredFormData
    cname = data["clubname"]
    filtereddata = data["filteredFormData"]
    query = {}

    and_conditions = [{"clubname":cname}]

    for field, value in filtereddata.items():
        if field in ["event_start_date", "event_end_date"] and value != "":
            value = datetime.strptime(value, "%Y-%m-%d")
            if field == "event_start_date":
                and_conditions.append({"event_start_date": {"$gte": value}})
            if field == "event_end_date":
                and_conditions.append({"event_start_date": {"$lte": value}})

        if field in ["minprice", "maxprice"] and value != "":
            if field == "minprice":
                and_conditions.append({"ticket_price": {"$gte": float(value)}})
            if field == "maxprice":
                and_conditions.append({"ticket_price": {"$lte": float(value)}})

        if field == "venue_city" and value != "":
            regex_pattern = re.compile(f"^{re.escape(value)}", re.IGNORECASE)
            and_conditions.append({"venue_city": {"$regex": regex_pattern}})

    if and_conditions:
        query["$and"] = and_conditions

    # Find posts based on the query
    result = conn.EventWiz.post.find(query)

    # Iterate over the result and print each post
    response_list = serializeList(result)
    if response_list:
        lis = []
        d1 = {}
        for singleDict in response_list:
            d1 = singleDict
            d1["event_start_date"] = d1["event_start_date"].strftime("%d-%m-%Y")
            d1["event_end_date"] = d1["event_end_date"].strftime("%d-%m-%Y")
            lis.append(serializeDict(d1))
        return serializeList(lis)
    else:
        return {"error": "No such Post Available", "success": False}
    
    
# other organisation event post filter functionality to fetch post
@event.post("/otherorgeventpostfilters")
async def other_org_eventpost_filters(data: dict):
    filtereddata = data["filteredFormData"]
    clubname = data["clubname"]
    # Build the query based on the filteredFormData
    query = {"clubname": {"$ne": clubname}}

    for field, value in filtereddata.items():

        if field in ["event_start_date", "event_end_date"] and value != "":
            value = datetime.strptime(value, "%Y-%m-%d")
            #print(value)
            if field == "event_start_date":
                query["event_start_date"] = {"$gte": value}
                #print(query)
            if field == "event_end_date":
                query["event_start_date"] = {"$lte": value}
                #print(query)

        if field in ["minprice", "maxprice"] and value != "":
            if field == "minprice":
                # Convert minprice to float and construct the query
                query["ticket_price"] = {"$gte": float(value)}
                #print(query)
            if field == "maxprice":
                # Convert maxprice to float and construct the query
                query["ticket_price"] = {"$lte": float(value)}
                #print(query)

        if field == "venue_city" and value != "":
            # Construct a case-insensitive regex pattern for venue_city
            regex_pattern = re.compile(f"^{re.escape(value)}", re.IGNORECASE)
            query[field] = {"$regex": regex_pattern}

    # Find posts based on the query
    result = conn.EventWiz.post.find(query)

    # Iterate over the result and print each post
    response_list = serializeList(result)
    if response_list:
        lis = []
        d1= {}
        for singleDict in response_list:
            d1 = singleDict
            d1["event_start_date"] = d1["event_start_date"].strftime("%d-%m-%Y")
            d1["event_end_date"] = d1["event_end_date"].strftime("%d-%m-%Y")
            lis.append(serializeDict(d1))
        return serializeList(lis)
    else:
        return {"error": "Error, please fill the form again", "success": False}
    
# organisation fetch member details 
@event.post("/organizationmemberdetails/")
async def organisation_member_details(data : dict):
    org = conn.EventWiz.organisation.find({"clubname" : data["clubname"]})
    # #print(serializeList(org))
    if org:
        data_dict = serializeList(org)[0]["members"]
        for i in data_dict:
            i["expiry_date"] = i["expiry_date"].strftime("%Y-%m-%d")
            i["start_date"] = i["start_date"].strftime("%Y-%m-%d")
        return data_dict
    else:
        return {"data":"Member doesn't Exist","success":False}

    
#organisation route for fetching  member's membership-type
@event.post("/getmemtype/")
async def get_memtype(data:dict):
    type = []
    cursor = conn.EventWiz.organisation.find({"clubname":data["clubname"]}, {"memtype": 1, "_id": 0})
    # #print(serializeList(cursor))
    d1 = serializeList(cursor)
    # #print(d1[0]["memtype"])
    for i in d1[0]["memtype"]:
        type.append(i["type"])
    return type

# organisation route for adding a member
@event.put("/addorganizationmember/{id}")
async def add_organizaton_member(id:str,member:User):
    data_dict = dict(member)
    org = conn.EventWiz.organisation.find({"_id":ObjectId(id)})

    if org:
        data_dict1 = serializeList(org)[0]["members"]
        for i in data_dict1:
            if (i["username"] == data_dict["username"]):
                return {"data":"Username already Exists","success":False}
            if (i["memberid"] == data_dict["memberid"]):
                return {"data":"Member ID already Exists","success":False}
            
    data_dict["expiry_date"] = data_dict["expiry_date"].strftime("%Y-%m-%d")
    data_dict["expiry_date"] = datetime.strptime(data_dict["expiry_date"], "%Y-%m-%d")
    data_dict["start_date"] = data_dict["start_date"].strftime("%Y-%m-%d")
    data_dict["start_date"] = datetime.strptime(data_dict["start_date"], "%Y-%m-%d")


    if data_dict["membertype"] == "":
        return {"data":"Select Membership Type","success":False}
    d1 = conn.EventWiz.organisation.find_one({"_id":ObjectId(id)})
    if d1:
        # serializeDict(d1)["members"].append(data_dict)
        org1 = serializeDict(d1)
        org1["members"].append(data_dict)
        conn.EventWiz.organisation.find_one_and_update({"_id":ObjectId(id)},{"$set": {"members":org1["members"]}})
        return {"data":"Member Added Successfully","success":True}
    else:
        return {"data":"Invalid Input","success":False}
    

#updating member details
@event.put("/organizationupdatememberdetails/")   
async def update_member_details(data: dict):
    
    organisation = conn.EventWiz.organisation.find_one({"clubname": data["clubname"]})
    if organisation:   
        
        org1 = serializeDict(organisation)
        formdata = data["formData"]
        
        formdata["expiry_date"] = datetime.strptime(formdata["expiry_date"], "%Y-%m-%d")
        formdata["start_date"] = datetime.strptime(formdata["start_date"], "%Y-%m-%d")
        member_id = data["memberId"]
        #print(member_id)
        for memberdict in org1["members"]:
            #print(memberdict["memberid"])
            if memberdict["memberid"] == data["memberId"]:
               
                memberdict.update(data["formData"])
                #print(org1["members"])
                # conn.EventWiz.organisation.replace_one({"_id": org1["_id"]}, org1)
                conn.EventWiz.organisation.find_one_and_update({"_id":ObjectId(org1["_id"])},{"$set": {"members":org1["members"]}})
                # #print(org1["members"])
                return True

        # else:
        #     return {"error": "Member Error", "success": False}
            
        #print(org1)
    else:
        return {"error":"Organisation not found","success": False}
    
    
# deleting a member 
@event.put("/deletemember")
async def delete_member(data : dict):
    org = conn.EventWiz.organisation.find_one({"_id":ObjectId(data['orgid'])})
    if org:
        org1 = serializeDict(org)
        clubname = org1["clubname"]
        org1 = serializeDict(org)["members"]

        for i in org1:
            if i["memberid"] == data["memberid"]:
                i["clubname"] = clubname
                conn.EventWiz.deletemembers.insert_one(i)

        updated_members = [i for i in org1 if i["memberid"] != data["memberid"]]
        # #print("Updated Member list",updated_members)
        conn.EventWiz.organisation.find_one_and_update({"_id":ObjectId(data["orgid"])},{"$set": {"members":updated_members}})
        return {"error":"Member deleted Successfully","success":True}
    else:
        return {"error":"Invalid Input","success":False}
    
# searching a member by name or expiry/start date
@event.post("/orgmemberfilterbyname")
async def fetch_details_bynameordates(data:dict):

    if (data["expiry_date"] != ''):
        # data["expiry_date"] = data["expiry_date"].strftime("%Y-%m-%d")
        data["expiry_date"] = datetime.strptime(data["expiry_date"], "%Y-%m-%d")
    if (data["start_date"] != ''):    
        # data["start_date"] = data["start_date"].strftime("%Y-%m-%d")
        data["start_date"] = datetime.strptime(data["start_date"], "%Y-%m-%d")

    print(data)
    filtered_data = {}
    for key, value in data.items():
        if (value != '' or value != ""):
          filtered_data[key] = value
    
    # return filtered_data 
    print(filtered_data)
    # content = []
    # if (len(filtered_data) != 0):
    #     regex_patterns = {}
    #     for key, value in data.items():
    #         if value:
    #             regex_patterns[key] = re.compile(f'^{re.escape(value)}', re.IGNORECASE)
    organisation = conn.EventWiz.organisation.find_one({"_id":ObjectId(data["cid"])})
    result = []
    if organisation:   
        
        org1 = serializeDict(organisation)
        partial_name = data["membername"]
        regex_pattern = re.compile(f"{re.escape(partial_name)}.*", re.IGNORECASE)
        # #print(org1)
        # member_name = data["membername"]
        # #print(member_name)
        for memberdict in org1["members"]:
            #print(memberdict["name"])
            if "name" in memberdict and re.match(regex_pattern, memberdict["name"]):
                if match_dates(memberdict, data):
                    result.append(memberdict)
                    
        # #print(d1)
        #print(result)
        if (result != []):
        #   print(result)
          for singledict in result:
                singledict["expiry_date"] = singledict["expiry_date"].strftime("%Y-%m-%d")
                singledict["start_date"] = singledict["start_date"].strftime("%Y-%m-%d")
             
          return result
        else:
            return {"error":"Member Not Found","success":False}
    else:
        return {"error":"Organisation Not Found","success":False}

#extended function for searching members by year 
def match_dates(memberdict, data):
    start_date = data.get("start_date")
    expiry_date = data.get("expiry_date")

    if start_date and "start_date" in memberdict:
        if isinstance(memberdict["start_date"], datetime):
            member_start_date = memberdict["start_date"].date()
        else:
            member_start_date = datetime.strptime(memberdict["start_date"]["$date"], "%Y-%m-%dT%H:%M:%S.%fZ").date()
        
        if start_date.year != member_start_date.year:
            return False

    if expiry_date and "expiry_date" in memberdict:
        if isinstance(memberdict["start_date"], datetime):
            member_expiry_date = memberdict["start_date"].date()
        else:
            member_expiry_date = datetime.strptime(memberdict["expiry_date"]["$date"], "%Y-%m-%dT%H:%M:%S.%fZ").date()

        if expiry_date.year != member_expiry_date.year:
            return False

    return True   
# 
#fetching member details for updating
@event.post("/organisationunupdatedmemberdetails")
async def update_member_details(data: dict):
    organisation = conn.EventWiz.organisation.find_one({"_id": ObjectId(data["cid"])})
    
    if not organisation:
        return {"error": "Organization Not Found", "success": False}

    memtype_cursor = conn.EventWiz.organisation.find({"clubname": data["clubname"]}, {"memtype": 1, "_id": 0})
    memtype_cursor = serializeList(memtype_cursor)
    memtypes = []
    for i in memtype_cursor[0]["memtype"]:
        memtypes.append(i["type"])

    result = []
    for memberdict in organisation.get("members", []):
        if memberdict["memberid"] == data["memberid"]:
            result.append(memberdict)
            break  

    if not result:
        return {"error": "Member Not Found", "success": False}

    return {"memtypes": memtypes, "memberDetails": result[0], "success": True}

#fetching organisation event posts by title
@event.post("/organisationeventpostsbytitle")
async def organisation_eventpost_bytitle(data:dict):
    clubname = data["clubname"]
    organisation = conn.EventWiz.organisation.find_one({"clubname": clubname})
    if organisation:
        
        posts = conn.EventWiz.post.find({"clubname": clubname})
        result = []
        if (posts != []):
            partial_name = data["title"]
            regex_pattern = re.compile(f".*{re.escape(partial_name)}.*", re.IGNORECASE)

            for postdict in serializeList(posts):
                # if postdict["event_title"] == data["title"]:
                if "event_title" in postdict and re.match(regex_pattern, postdict["event_title"]):
                    result.append(postdict)
                    break  
            if (result != []):
                return result
            else:
                return {"error":"No post found","success":False}
        else:
            return {"error":"No post found","success":False}
    return {"error":"No organisation found","success":False}

#fetching other organisation's event posts by title
@event.post("/otherorgeventpostsbytitle")
async def otherorg_eventpost_bytitle(data:dict):
    clubname = data["clubname"]
    organisation = conn.EventWiz.organisation.find_one({"clubname": clubname})
    if organisation:
        
        posts = conn.EventWiz.post.find({"clubname": {"$ne": clubname}})
        result = []
        if (posts != []):
            partial_name = data["title"]
            if (partial_name == ""):
                return {"error":"No Title input","success":False}
            else:
                regex_pattern = re.compile(f".*{re.escape(partial_name)}.*", re.IGNORECASE)
    
                for postdict in serializeList(posts):
                    # if postdict["event_title"] == data["title"]:
                    if "event_title" in postdict and re.match(regex_pattern, postdict["event_title"]):
                        result.append(postdict)
                        break  
                if result:
                    return result
                else:
                    return {"error":"No post found","success":False}
        else:
            return {"error":"No post found","success":False}
    return {"error":"No organisation found","success":False}


# organisation's member table filters
@event.post("/organisationmembertablefilters")
async def membertable_filtering(filters:dict):
    data = filters["data"]
    orgid = filters["orgid"]
    
    filtered_data = {}
    for key, value in data.items():
        if (value != '' or value != ""):
            filtered_data[key] = re.escape(value)
    #print(filtered_data)
    content = []
    if (len(filtered_data) != 0):
        
        regex_patterns = {}
        for key, value in data.items():
            if value:
                regex_patterns[key] = re.compile(f'^{re.escape(value)}', re.IGNORECASE)

        print (regex_patterns)
        organisation = conn.EventWiz.organisation.find_one({"_id":ObjectId(orgid)})
        if organisation:
            org1 = serializeDict(organisation)
            membersList = org1["members"]
            if (membersList != []):
                for memberdict in membersList:

                    # match = all(regex.match(str(memberdict.get(key, ''))) for key, regex in regex_patterns.items())
                    match = all(regex.match(str(memberdict.get(key, ''))) for key, regex in regex_patterns.items())
                    if match:
                        #print("Match found:", memberdict)
                        content.append(memberdict)

                if content:
                    for i in content:
                        i["expiry_date"] = i["expiry_date"].strftime("%Y-%m-%d")
                        i["start_date"] = i["start_date"].strftime("%Y-%m-%d")
                    return content
                else:
                    # return content
                    return {"error":"Members not found","success":False}
            else:
                return {"error":"No Members","success":False}
        else:
            return {"error":"Organisation not found","success":False}
    else:
        
        return {"error":"Please enter data in filter input","success":False,"data_dict":"empty"}
        # result = conn.EventWiz.find(query)

# fetching all memberships
@event.post("/organisationgetallmembership")
async def get_all_membership(data : dict):
    membership = conn.EventWiz.organisation.find_one({"clubname":data["clubname"]}, {"memtype": 1, "_id": 0})
    if membership:
        memtype = serializeDict(membership)["memtype"]
        if len(memtype) !=0:
            return memtype
        else:
            return {"error":"No Membership Type Available","success":False}
    else:
        return {"error":"Organization Not Found","success":False}

# org inserting new membership type
@event.put("/addmembership/{clubname}")
async def add_membership(clubname : str,data : dict):
    if type(data["price"]) == str:
        data["price"] = int(data["price"])
    membership = conn.EventWiz.organisation.find_one({"clubname":clubname}, {"memtype": 1, "_id": 0})
    if membership:
        memtype = serializeDict(membership)["memtype"]
        for i in memtype:
            if i["type"] == data["type"]:
                i["price"] = data["price"]
                conn.EventWiz.organisation.find_one_and_update({"clubname":clubname},{"$set": {"memtype":memtype}})
                return {"data":"Membership Updated Successfully","success":True}
        memtype.append(data)
        conn.EventWiz.organisation.find_one_and_update({"clubname":clubname},{"$set": {"memtype":memtype}})
        return {"data":"Membership Added Successfully","success":True}
    else :
        return {"error":"Organization Not Found","success":False}
    
# Get all Membership of Organization by Clubname
@event.post("/getallmembership")
async def get_all_membership(data : dict):
    membership = conn.EventWiz.organisation.find_one({"clubname":data["clubname"]}, {"memtype": 1, "_id": 0})
    if membership:
        memtype = serializeDict(membership)["memtype"]
        if len(memtype) !=0:
            return memtype
        else:
            return {"error":"No Membership Type Available","success":False}
    else:
        return {"error":"Organization Not Found","success":False}

#user side fetch all post
@event.get("/fetchingallpostforuser")
async def fetch_all_post_userside():
    result = conn.EventWiz.post.find()
    if (result != []):  
        return serializeList(result)
    else:
        return {"error":"No post found","success":False}
    
# user side search filter by title for post
@event.post("/usersidesearchtitle")
async def search_by_title(data:dict):
    result = conn.EventWiz.post.find({"event_title":data["title"]})
    if result !=[]:
        return result
    else:
        return {"error":"No post found","success":False}


#sorting user side in org member table
@event.post("/membersortinguserside")
async def member_sorting_userside(data:dict):
    org = conn.EventWiz.organisation.find_one({"clubname" : data["clubname"]})
    if org:
        org1 =  serializeDict(org)["members"]
        if len(org1) != 0:
        # #print(org1)
            if data["value"]:
                sorted_list = sorted(org1, key=lambda x: x[data["col"]])
                for i in sorted_list:
                    i["expiry_date"] = i["expiry_date"].strftime("%Y-%m-%d")
                    i["start_date"] = i["start_date"].strftime("%Y-%m-%d")
                return sorted_list
            else:
                sorted_list = sorted(org1, key=lambda x: x[data["col"]], reverse=True)
                for i in sorted_list:
                    i["expiry_date"] = i["expiry_date"].strftime("%Y-%m-%d")
                    i["start_date"] = i["start_date"].strftime("%Y-%m-%d")
                return sorted_list

    else:
        return {"error":"Organization not Found","success":False}
    

# fetch all the applied users
@event.post("/allappliedusers")
async def adminside_allappliedusers(data:dict):
    clubId = data["clubid"]
    orgData = conn.EventWiz.organisation.find({"_id":ObjectId(clubId)})
    orgData = serializeList(orgData)
    neworgdata = orgData[0]
    # print(orgData[0])
    applied_users = neworgdata["memapplied"]
    # print("-----------------------------")
    # for singleuser in applied_users:
    #     print(singleuser)
    #     print("-----------------------------")

    if (len(applied_users) != 0):
        return applied_users
    else:
        return {"error":"No Applied Organisation","success":False}  

# accepting a user's subscription
@event.post("/acceptingusersubscription")
async def adminside_acceptorg(data:dict):
    # print(data)

    acceptedUser = data["data"]
    givenmemberid = data["memberid"]
    clubid = data["clubid"]

    org = conn.EventWiz.organisation.find({"_id":ObjectId(clubid)})
    org = serializeList(org)[0]

    # print(org)

    memberslists = org["members"]
    orgappliedmemberslist = org["memapplied"]
    # print(memberslists)

    allmemberid = []
    for singlemember in memberslists:
        allmemberid.append(singlemember["memberid"])
    print(allmemberid)

    if (len(allmemberid) !=0):
        if givenmemberid in allmemberid:
            return {"error":"MemberId Already Exists","success":False,"closeform":False}
        else:

            acceptedUser["memberid"] = givenmemberid
            
            usersloggedindata = acceptedUser

            conn.EventWiz.users.insert_one(usersloggedindata)
            

            acceptedUser["loggedin"] = True
            # print(acceptedUser)

            memberslists.append(acceptedUser)

            updated_user = [i for i in orgappliedmemberslist if i["username"] != acceptedUser["username"]]

            # print("Updated Member list",updated_members)

            content = conn.EventWiz.organisation.find_one_and_update({"_id":ObjectId(org["_id"])},{"$set": {"memapplied":updated_user,"members" : memberslists}})


        
            if content:
                return True
            else:
                return {"error":"Nothing To Update", "success":False}
    else:
        acceptedUser["memberid"] = givenmemberid
        
        usersloggedindata = acceptedUser
        conn.EventWiz.users.insert_one(usersloggedindata)
            
        acceptedUser["loggedin"] = True
        # print(acceptedUser)

        memberslists.append(acceptedUser)

        updated_user = [i for i in orgappliedmemberslist if i["username"] != acceptedUser["username"]]

            # print("Updated Member list",updated_members)

        content = conn.EventWiz.organisation.find_one_and_update({"_id":ObjectId(org["_id"])},{"$set": {"memapplied":updated_user,"members" : memberslists}})
        
        if content:
            return True
        else:
            return {"error":"Nothing To Update", "success":False}
      
    
# rejecting subscribing user 
@event.post("/rejectingsubscribinguser")
async def adminside_rejectorg(data:dict):
    # print(data["data"])
    rejectedUser = data["data"]

    conn.EventWiz.rejectedusers.insert_one(rejectedUser)

    orgdata = serializeDict(conn.EventWiz.organisation.find_one({"_id":ObjectId(data["clubid"])}))

    
    orgappliedmemberslist = orgdata["memapplied"]

    updated_user = [i for i in orgappliedmemberslist if i["username"] != rejectedUser["username"]]


    content = conn.EventWiz.organisation.find_one_and_update({"_id":ObjectId(orgdata["_id"])},{"$set": {"memapplied":updated_user}})

    if content:
        return True
    else:
        return {"error":"Nothing To Update", "success":False}


# ///////////////////////////////////////////////////////////////////////////////////