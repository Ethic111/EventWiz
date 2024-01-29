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
    result = serializeList(adminlist)
    if result:
        # print(result)
        return result[0]
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
    regex_pattern = re.compile(f"{re.escape(search_query)}.*", re.IGNORECASE)
    result = conn.EventWiz.organisation.find({"clubname": {"$regex": regex_pattern}})

    result = serializeList(result)
    if result:
        # print(result)
        return result
    else:
        return {"error":"No organisation found","success":False}


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
    uname = conn.EventWiz.users.find_one({"$and": 
        [
            {"clubname": None},
            {"username": d1["username"]}
        ]
        },{"username":1,"_id":0})
    #print(serializeDict(uname))
    if uname:
        return {"error":"Username already exists","success":False}
    else:
        conn.EventWiz.users.insert_one(dict(user))
        return dict(user)

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


#all organisations names
@event.get('/allorgnames')
async def fetch_all_organisations_names():
    
    return True


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
@event.post('/organisationregistration/')
async def create_org(organisation: Organisation):
    conn.EventWiz.organisation.insert_one(dict(organisation))
    return serializeList(conn.EventWiz.organisation.find())

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
            # conn.event.user.insert_one(d1)
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
            # conn.event.user.insert_one(d1)
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
async def org_filters(filtereddata: dict):
    # Build the query based on the filteredFormData
    query = {}

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
        regex_pattern = re.compile(f".*{re.escape(partial_name)}.*", re.IGNORECASE)
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
        if isinstance(memberdict["expiry_date"], datetime):
            member_expiry_date = memberdict["expiry_date"].date()
        else:
            member_expiry_date = datetime.strptime(memberdict["expiry_date"]["$date"], "%Y-%m-%dT%H:%M:%S.%fZ").date()

        if expiry_date.year != member_expiry_date.year:
            return False

    return True   

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
                    return content
                    # return {"error":"Members not found","success":False}
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
@event.post("/organisationaddnewmemtype")
async def add_new_membership_type(data : dict):
    formdata = data["formdata"]
    clubId = data["clubID"]
    # print(formdata,clubId)
    addingType = formdata["type"]
    org = conn.EventWiz.organisation.find({"_id":ObjectId(clubId)})
    if org:
        org1 = serializeList(org)
        # print(org1)
        print("hey inside org1")
        memtypelist = org1[0]["memtype"]
        # print(org1["memtype"])
        print(memtypelist)
        for membership in memtypelist:
            if (membership["type"] == formdata["type"]):
                return {"error": "This Membership Type is already present", "success": False}
        
        memtypelist.append({
            "type": formdata["type"],
            "price": formdata["price"]
        })
        
        # print(memtypelist)
        # Update the club document with the modified memtype list
        conn.EventWiz.organisation.update_one({"_id": ObjectId(clubId)}, {"$set": {"memtype": memtypelist}})
        return memtypelist
    else:
        return {"error": "Organisation doesn't exist", "success": False}

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
    
# ///////////////////////////////////////////////////////////////////////////////////