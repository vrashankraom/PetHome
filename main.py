from flask import Flask,render_template,redirect,url_for,flash
from flask import request, make_response
import mysql.connector as mysql


#To create Pet-Id
import random
import string

app = Flask(__name__)
mydb = mysql.connect(host="localhost",user="root",passwd="vrashank",database="pet_boarding_management")

app.secret_key = "pet-boarding"

@app.route("/")
def home():
    return render_template('index.html')

@app.route("/petowner",methods=["GET","POST"])
def petownerlogin():
    if request.method=="GET":
        return render_template("PetOwner/petowner.html")
    if request.method=="POST":
        id = request.form.get("id")
        cur = mydb.cursor(buffered=True)
        cur.execute("select p_id from pet_details where p_id=%s",[id])
        checkpet=cur.fetchone()
        checkpet=bool(checkpet)
        cur.execute("select pa_id from pet_activity where p_id=%s",[id])
        checkdata=cur.fetchone()
        checkdata=bool(checkdata)
        print(checkpet,checkdata)
        if(checkdata):
            mydb.commit()
            cur.close()
            return redirect(url_for('getmypadetails',id=id))
        if(checkpet and not checkdata):
            flash("Pet-Activity data is not added yet!","info")
            return render_template("PetOwner/petowner.html")
        if(not checkpet):
            flash("Invalid Pet-Id!","info")
            return render_template("PetOwner/petowner.html")

@app.route("/shopowner")
def shopownerlogin():
    return render_template('ShopOwner/shopowner.html')


@app.route("/shopoptions", methods=["GET","POST"])
def validateshop():
    if request.method=="GET":
        cookies = request.cookies
        email = cookies.get("email")
        password = cookies.get("password")
        if (email == "vrashankrao@gmail.com" and password == "vrashank"):
            return render_template("ShopOwner/shopoptions.html")
        else:
            return render_template("index.html")
    if request.method =="POST":
       email=request.form.get("email")
       password=request.form.get("password")
       if(email=="vrashankrao@gmail.com" and password=="vrashank"):
           res = make_response(render_template('ShopOwner/shopoptions.html'),200)
           res.set_cookie(
               "email",
               email
           )
           res.set_cookie(
               "password",
               password
           )
           return res
       else:
           res = make_response(render_template('index.html'), 200)
           res.set_cookie(
               "email",
               email
           )
           res.set_cookie(
               "password",
               password
           )
           return res

    else:
        return render_template("index.html")

@app.route("/addpetowner", methods=["GET","POST"])
def addpetowner():
    cookies = request.cookies
    email = cookies.get("email")
    password = cookies.get("password")
    if request.method == "GET":
        if (email == "vrashankrao@gmail.com" and password == "vrashank"):
            return render_template("ShopOwner/addpetowner.html")
    if request.method == "POST":
        if (email == "vrashankrao@gmail.com" and password == "vrashank"):
            cur = mydb.cursor(buffered=True)
            #cur.execute("CREATE TABLE pet_owner(po_id int(11) primary key,po_name varchar(50) NOT NULL,po_address varchar(150) NOT NULL,po_email varchar(30) NOT NULL);")
            #cur.execute("""CREATE TABLE petowner_phone(po_id int(11) ,po_phone varchar(13), primary key(po_id,po_phone), foreign key(po_id) references pet_owner(po_id));""")

            poid = request.form.get("poid")
            poname = request.form.get("poname")
            poemail = request.form.get("poemail")
            pophone1 = request.form.get("pophone1")
            pophone2 = request.form.get("pophone2")
            poaddress = request.form.get("poaddress")

            cur.execute("Insert into pet_owner(po_id,po_name,po_email,po_address) values(%s,%s,%s,%s)",(poid,poname,poemail,poaddress))
            cur.execute("Insert into petowner_phone(po_id,po_phone) values(%s,%s)",(poid,pophone1))

            if(pophone2!=""):
                cur.execute("Insert into petowner_phone(po_id,po_phone) values(%s,%s)",(poid,pophone2))

            mydb.commit()
            cur.close()

            return render_template("ShopOwner/addpetdetails.html")
    else:
        return render_template("index.html")

@app.route("/addpetdetails", methods=["GET","POST"])
def addpetdetails():
    cookies = request.cookies
    email = cookies.get("email")
    password = cookies.get("password")
    if request.method == "GET":
        if (email == "vrashankrao@gmail.com" and password == "vrashank"):
            return render_template("ShopOwner/addboarddetails.html")
    if request.method == "POST":
        if (email == "vrashankrao@gmail.com" and password == "vrashank"):
            letters = string.ascii_lowercase
            result_str = ''.join(random.choice(letters) for i in range(5))
            cur = mydb.cursor(buffered=True)

            #cur.execute("""CREATE TABLE pet_details (p_id varchar(5) primary key,p_name varchar(30) NOT NULL,p_category varchar(20) NOT NULL,p_breed varchar(20) NOT NULL,p_age int(3) NOT NULL,p_regtime time  not null DEFAULT (current_time()),p_regdate date not null DEFAULT (current_date()),po_id int(11) NOT NULL, foreign key(po_id) references pet_owner(po_id));""")

            pname = request.form.get("pname")
            pcategory = request.form.get("pcategory")
            pbreed = request.form.get("pbreed")
            pyob = request.form.get("pyob")
            cur.execute("select YEAR(CURDATE())")
            year = cur.fetchone()
            page = int(year[0]) - int(pyob)
            cur.execute("select po_id from pet_owner where po_id=(select MAX(po_id) from pet_owner)")
            data=cur.fetchall()
            print("max is ",data)
            cur.execute("Insert into pet_details(p_id,p_name,p_age,p_category,p_breed,po_id) values(%s, %s, %s, %s, %s, %s)",(result_str,pname,page,pcategory,pbreed,data[0][0]))
            mydb.commit()
            cur.close()
            return render_template("ShopOwner/addboarddetails.html")
    else:
        return render_template("index.html")


@app.route("/addpetfood" ,methods=["GET","POST"])
def addpetfood():
    cookies = request.cookies
    email = cookies.get("email")
    password = cookies.get("password")
    if request.method=="GET":
        if (email == "vrashankrao@gmail.com" and password == "vrashank"):
            cur = mydb.cursor(buffered=True)

            #Create a stored procedure
            #cur.execute("""CREATE PROCEDURE GetPacId(IN pacategory varchar(30)) BEGIN select pac_id, pa_type from pet_activitycategory where pa_category = pacategory END""")

            #Call the stored procedure
            cur.callproc('GetPacId',['EATING FOOD'])
            for results in cur.stored_results():
                allfood = results.fetchall()

            mydb.commit()
            cur.close()
            return render_template("ShopOwner/addpetfood.html",allfood=allfood)
    if request.method=="POST":
        if (email == "vrashankrao@gmail.com" and password == "vrashank"):
            cur = mydb.cursor(buffered=True)

            #cur.execute("""CREATE TABLE pet_activitycategory (pac_id int(11) primary key,pa_category varchar(50) NOT NULL,pa_type varchar(50) NOT NULL);""")

            pacategory='EATING FOOD'

            food = request.form.get("food")
            pacid = request.form.get("pacid")
            cur.execute("Insert into pet_activitycategory(pac_id,pa_category,pa_type) values(%s,%s,%s)", (pacid,pacategory,food))

            #call the procedure
            cur.callproc('GetPacId', ['EATING FOOD'])
            for results in cur.stored_results():
                allfood = results.fetchall()
            print(allfood)
            mydb.commit()
            cur.close()
            return render_template("ShopOwner/addpetfood.html",allfood=allfood)
    else:
        return render_template("index.html")

@app.route("/addpetgame" ,methods=["GET","POST"])
def addpetgame():
    cookies = request.cookies
    email = cookies.get("email")
    password = cookies.get("password")
    if request.method=="GET":
        if (email == "vrashankrao@gmail.com" and password == "vrashank"):
            cur = mydb.cursor(buffered=True)

            # call the procedure
            cur.callproc('GetPacId', ['PLAYING GAMES'])
            for results in cur.stored_results():
                allgames = results.fetchall()

            mydb.commit()
            cur.close()
            return render_template("ShopOwner/addpetgame.html",allgames=allgames)
    if request.method=="POST":
        if (email == "vrashankrao@gmail.com" and password == "vrashank"):
            pacategory = 'PLAYING GAMES'
            cur=mydb.cursor(buffered=True)

            game = request.form.get("game")
            pacid = request.form.get("pacid")
            cur.execute("Insert into pet_activitycategory(pac_id,pa_category,pa_type) values(%s,%s,%s)",(pacid, pacategory, game))

            # call the procedure
            cur.callproc('GetPacId', ['PLAYING GAMES'])
            for results in cur.stored_results():
                allgames = results.fetchall()

            mydb.commit()
            cur.close()
            return render_template("ShopOwner/addpetgame.html",allgames=allgames)
    else:
        return render_template("index.html")

@app.route("/addpetgroom" ,methods=["GET","POST"])
def addpetgroom():
    cookies = request.cookies
    email = cookies.get("email")
    password = cookies.get("password")
    if request.method=="GET":
        if (email == "vrashankrao@gmail.com" and password == "vrashank"):
            cur = mydb.cursor(buffered=True)

            # call the procedure
            cur.callproc('GetPacId', ['GROOMING'])
            for results in cur.stored_results():
                allgrooms = results.fetchall()

            mydb.commit()
            cur.close()
            return render_template("ShopOwner/addpetgroom.html",allgrooms=allgrooms)
    if request.method=="POST":
        if (email == "vrashankrao@gmail.com" and password == "vrashank"):
            pacategory = 'GROOMING'
            cur=mydb.cursor(buffered=True)

            groom = request.form.get("groom")
            pacid = request.form.get("pacid")
            cur.execute("Insert into pet_activitycategory(pac_id,pa_category,pa_type) values(%s,%s,%s)",(pacid, pacategory, groom))

            # call the procedure
            cur.callproc('GetPacId', ['GROOMING'])
            for results in cur.stored_results():
                allgrooms = results.fetchall()

            mydb.commit()
            cur.close()
            return render_template("ShopOwner/addpetgroom.html",allgrooms=allgrooms)
    else:
        return render_template("index.html")


@app.route("/addpetboard" ,methods=["GET","POST"])
def addpetboard():
    cookies = request.cookies
    email = cookies.get("email")
    password = cookies.get("password")
    if request.method=="GET":
        if (email == "vrashankrao@gmail.com" and password == "vrashank"):
            return redirect(url_for('givecode'))
    if request.method=="POST":
        if (email == "vrashankrao@gmail.com" and password == "vrashank"):
            cur=mydb.cursor(buffered=True)
            #cur.execute("CREATE TABLE board_details (b_id int(11) primary key,b_basiccost int(11) NOT NULL,b_totalcost int(11) DEFAULT NULL,b_nailcutcount int(11) DEFAULT 0,b_haircutcount int(11) DEFAULT 0,b_bathcount int(11) DEFAULT 0,b_foodcount int(11) NOT NULL,b_foodpref varchar(100) DEFAULT NULL,b_fromdate date NOT NULL,b_nodays int(11) DEFAULT NULL,b_tilldate date NOT NULL,p_id varchar(5) NOT NULL,b_healthcond varchar(100) DEFAULT NULL, foreign key(p_id) references pet_details(p_id));")

            bid = request.form.get("bid")
            basiccost = request.form.get("basiccost")
            boardfromdate = request.form.get("boardfromdate")
            boardtilldate = request.form.get("boardtilldate")
            petfoodpref = request.form.get("petfoodpref")
            pethealthcond = request.form.get("pethealthcond")
            bnailcutcount = request.form.get("bnailcutcount")
            bhaircutcount = request.form.get("bhaircutcount")
            bbathcount = request.form.get("bbathcount")
            bfoodcount = request.form.get("bfoodcount")

            # Code to reverse date
            fromdate = boardfromdate
            tilldate = boardtilldate

            # Code to Get No. of Days
            cur.execute("SELECT DATEDIFF(%s, %s)", (tilldate, fromdate))
            days = cur.fetchone()

            cur.execute("select p_id from pet_details order by p_regdate DESC,p_regtime DESC limit 1")
            data = cur.fetchone()
            print(bbathcount,bfoodcount,days,data)
            # Calculate the Total Cost of Pet-Board
            totalcost = int(days[0])*int(basiccost) + (50 * int(bnailcutcount[0])) + (100 * int(bhaircutcount[0])) + int(days[0])*(50 * int(bfoodcount[0])) + (30 * int(bbathcount[0]))

            #Add a Trigger

            #cur.execute("create trigger calculate_total_cost before insert on board_details for each row set new.b_totalcost = new.b_totalcost + new.b_totalcost * 0.18")

            #Insert details into board_details
            cur.execute("Insert into board_details(b_id,b_basiccost,b_totalcost,b_foodpref,b_nodays,b_fromdate,b_tilldate,b_healthcond,p_id,b_nailcutcount,b_haircutcount,b_bathcount,b_foodcount) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(bid,basiccost,totalcost,petfoodpref,days[0],fromdate,tilldate,pethealthcond,data[0],bnailcutcount,bhaircutcount,bbathcount,bfoodcount))

            mydb.commit()
            cur.close()
            return redirect(url_for('givecode'))
    else:
        return render_template("index.html")

#Code to give the Pet-id
@app.route("/givecode")
def givecode():
    cookies = request.cookies
    email = cookies.get("email")
    password = cookies.get("password")
    if(email == "vrashankrao@gmail.com" and password == "vrashank"):
        cur = mydb.cursor(buffered=True)
        cur.execute("select p_id from board_details order by b_id DESC limit 1")
        code = cur.fetchone()
        cur.execute("select b_id from board_details order by b_id DESC limit 1")
        data = cur.fetchone()
        print(data)
        # Get Count of activities
        cur.execute("select b_nailcutcount from board_details where b_id=%s", data)
        nailcutcount = cur.fetchone()
        cur.execute("select b_haircutcount from board_details where b_id=%s", data)
        haircutcount = cur.fetchone()
        cur.execute("select b_foodcount from board_details where b_id=%s", data)
        foodcount = cur.fetchone()
        cur.execute("select b_bathcount from board_details where b_id=%s", data)
        bathcount = cur.fetchone()


        #Get the No. of Days of Boarding
        cur.execute("select b_nodays from board_details where b_id=%s",data)
        days = cur.fetchone()

        #Get the Single dayBasic Cost of Boarding
        cur.execute("select b_basiccost from board_details where b_id=%s", data)
        basiccost = cur.fetchone()

        #Get the Total days Basic Cost of Boarding
        totalbasiccost = basiccost[0]*days[0]

        #Get Total Boarding Cost
        cur.execute("select b_totalcost from board_details where b_id=%s", data)
        totalcost = cur.fetchone()
        print(days[0])
        print(foodcount[0])

        #Get individual activity cost
        food=50*days[0]*foodcount[0]
        haircut=100*haircutcount[0]
        nailcut=50*nailcutcount[0]
        bath=30*bathcount[0]

        #Get Total Number of Meals
        totalfoodcount=days[0]*foodcount[0]

        mydb.commit()
        cur.close()
        return render_template("ShopOwner/givecode.html", Code=code[0],FoodCount=totalfoodcount,FoodCost=food,HairCutCount=haircutcount[0],HairCutCost=haircut,NailCutCount=nailcutcount[0],NailCutCost=nailcut,BathCount=bathcount[0],BathCost=bath,TotalCost=totalcost[0],days=days[0],singleday=basiccost[0],basiccost=totalbasiccost)
    else:
        return render_template("index.html")

@app.route("/getpetdetails")
def getpetdetails():
    cookies = request.cookies
    email = cookies.get("email")
    password = cookies.get("password")
    if request.method=="GET":
        if (email == "vrashankrao@gmail.com" and password == "vrashank"):
            cur = mydb.cursor(buffered=True)
            cur.execute("select p_id,p_name,p_category,DATE_FORMAT(p_regdate,'%d/%m/%Y'),po_name from pet_details,pet_owner where pet_details.po_id=pet_owner.po_id order by pet_details.po_id")
            data = cur.fetchall()
            cur.execute("select p_id from pet_details order by po_id")
            id = cur.fetchall()
            print(id)
            mydb.commit()
            cur.close()
            return render_template("ShopOwner/getpetdetails.html",data=data,id = id)
        else:
            return render_template("index.html")


@app.route("/addactivity/<id>",methods=["GET","POST"])
def addactivity(id):
    cookies = request.cookies
    email = cookies.get("email")
    password = cookies.get("password")
    if request.method=="GET":
        if (email == "vrashankrao@gmail.com" and password == "vrashank"):
            cur = mydb.cursor(buffered=True)
            # Get all Activities
            cur.execute("select pa_type from pet_activitycategory where pa_category='EATING FOOD'")
            food=cur.fetchall()
            cur.execute("select pa_type from pet_activitycategory where pa_category='GROOMING'")
            groom=cur.fetchall()
            cur.execute("select pa_type from pet_activitycategory where pa_category='PLAYING GAMES'")
            game=cur.fetchall()
            activities = food+groom+game
            mydb.commit()
            cur.close()
            return render_template("ShopOwner/addactivity.html",id=id,activities=activities)
    if request.method=="POST":
        if (email == "vrashankrao@gmail.com" and password == "vrashank"):
            cur = mydb.cursor(buffered=True)

            #cur.execute("""CREATE TABLE pet_activity (pa_id int(11) primary key,pac_id int(11) NOT NULL,pa_duration int(11) NOT NULL,pa_time time DEFAULT (current_time()),pa_date date DEFAULT (current_date()),p_health varchar(100) NOT NULL,p_id varchar(5),foreign key(p_id) references pet_details(p_id),foreign key(pac_id) references pet_activitycategory(pac_id));""")

            #Get all Activities
            cur.execute("select pa_type from pet_activitycategory where pa_category='EATING FOOD'")
            food = cur.fetchall()
            cur.execute("select pa_type from pet_activitycategory where pa_category='GROOMING'")
            groom = cur.fetchall()
            cur.execute("select pa_type from pet_activitycategory where pa_category='PLAYING GAMES'")
            game = cur.fetchall()
            activities = food + groom + game

            #Get details from form

            paid = request.form.get("paid")
            activitycategory = request.form.get("activitycategory")
            pactivity = request.form.get("pactivity")
            duration = request.form.get("duration")
            health = request.form.get("health")
            print(activitycategory,pactivity,duration,health)

            #Get the pac_id from pet_activitycategory
            cur.execute("select pac_id from pet_activitycategory where pa_category=%s and pa_type=%s",(activitycategory,pactivity))
            pacid=cur.fetchall()
            print(pacid)

            #Add all details
            cur.execute("insert into pet_activity(pa_id,p_id,pa_duration,pac_id,p_health) values(%s,%s,%s,%s,%s)",(paid,id,duration,pacid[0][0],health))
            mydb.commit()
            cur.close()
            return render_template("ShopOwner/addactivity.html",id=id,activities=activities)
    else:
        return render_template("index.html")

#Route to get Pet-Activity details for Pet-Owner
@app.route("/getmypadetails/<id>")
def getmypadetails(id):
    if request.method=="GET":
        cur = mydb.cursor(buffered=True)

        #Get all pet_activities
        cur.execute("select pa_date,DAYNAME(pa_date),pa_time,pa_category,pa_type,pa_duration,p_health from pet_activity,pet_activitycategory where pet_activity.pac_id=pet_activitycategory.pac_id and p_id=%s",[id])
        data=cur.fetchall()
        mydb.commit()
        cur.close()
        return render_template("PetOwner/getmypadetails.html",data=data)
    else:
        return render_template("index.html")

#Route to Get every details
@app.route("/getalldetails")
def getalldetails():
    cookies = request.cookies
    email = cookies.get("email")
    password = cookies.get("password")
    if request.method=="GET":
        if (email == "vrashankrao@gmail.com" and password == "vrashank"):
            cur = mydb.cursor(buffered=True)
            cur.execute("select p_id,p_name,p_category,DATE_FORMAT(p_regdate,'%d/%m/%Y'),po_name from pet_details,pet_owner where pet_details.po_id=pet_owner.po_id order by pet_details.po_id")
            data = cur.fetchall()
            cur.execute("select p_id from pet_details order by po_id")
            id = cur.fetchall()
            mydb.commit()
            cur.close()
            return render_template("ShopOwner/getalldetails.html",data=data,id = id)
        else:
            return render_template("index.html")


@app.route("/getboarddetails/<id>")
def getboarddetails(id):
    cookies = request.cookies
    email = cookies.get("email")
    password = cookies.get("password")
    if (email == "vrashankrao@gmail.com" and password == "vrashank"):
        cur = mydb.cursor(buffered=True)

        # Get all details
        cur.execute("select p_id,p_regdate,p_name,p_category,p_breed,p_age from pet_details where pet_details.p_id=%s",[id])
        petdata = cur.fetchall()
        cur.execute("select b_fromdate,b_tilldate,b_basiccost,b_totalcost,b_healthcond,b_foodpref from board_details where board_details.p_id=%s",[id])
        boarddata = cur.fetchall()
        cur.execute("select b_nailcutcount,b_haircutcount,b_bathcount,b_foodcount from board_details where board_details.p_id=%s",[id])
        countdata = cur.fetchall()
        cur.execute("select po_name,po_email,po_address from pet_owner where po_id = (select po_id from pet_details where pet_details.p_id=%s)",[id])
        petownerdata = cur.fetchall()
        cur.execute("select po_phone from petowner_phone where po_id=(select po_id from pet_details where pet_details.p_id=%s)",[id])
        phone = cur.fetchall()
        count=len(phone)
        print(phone)
        mydb.commit()
        cur.close()
        return render_template("ShopOwner/getboarddetails.html",petdata=petdata,boarddata=boarddata,petownerdata=petownerdata,phone=phone,countdata=countdata,count=count,id=id)
    else:
        return render_template("index.html")

#Route to Get Pet-Owner details to add a new pet
@app.route("/getallpetowners")
def getallpetowners():
    cookies = request.cookies
    email = cookies.get("email")
    password = cookies.get("password")
    if request.method=="GET":
        if (email == "vrashankrao@gmail.com" and password == "vrashank"):
            cur = mydb.cursor(buffered=True)
            cur.execute("select po_id,po_name,po_email from pet_owner order by po_id")
            data = cur.fetchall()
            mydb.commit()
            cur.close()
            return render_template("ShopOwner/getallpetowners.html",data=data)
        else:
            return render_template("index.html")

#Route to add a new pet of Existing Pet-Owner
@app.route("/addpetonly/<id>", methods=["GET","POST"])
def addpetonly(id):
    print("id is",id)
    cookies = request.cookies
    email = cookies.get("email")
    password = cookies.get("password")
    if request.method == "GET":
        if (email == "vrashankrao@gmail.com" and password == "vrashank"):
            return render_template("ShopOwner/addpetonly.html",id=id)
    if request.method == "POST":
        if (email == "vrashankrao@gmail.com" and password == "vrashank"):
            letters = string.ascii_lowercase
            result_str = ''.join(random.choice(letters) for i in range(5))
            cur = mydb.cursor(buffered=True)
            pname = request.form.get("pname")
            pcategory = request.form.get("pcategory")
            pbreed = request.form.get("pbreed")
            pyob = request.form.get("pyob")
            cur.execute("select YEAR(CURDATE())")
            year = cur.fetchone()
            page = int(year[0]) - int(pyob)
            cur.execute("Insert into pet_details(p_id,p_name,p_age,p_category,p_breed,po_id) values(%s, %s, %s, %s, %s, %s)", (result_str,pname,page,pcategory,pbreed,id))
            mydb.commit()
            cur.close()
            return render_template("ShopOwner/addboarddetails.html",id=id)
    else:
        return render_template("index.html")

#Route to delete a Pet-Food
@app.route("/deletepetfood/<id>", methods=["GET","POST"])
def deletepetfood(id):
    cookies = request.cookies
    email = cookies.get("email")
    password = cookies.get("password")
    if request.method == "POST":
        if (email == "vrashankrao@gmail.com" and password == "vrashank"):

            #Delete the Pet-Food
            cur = mydb.cursor(buffered=True)
            cur.execute("delete from pet_activitycategory where pac_id=%s",[id])
            mydb.commit()
            cur.close()
            return redirect('/addpetfood')
    else:
        return render_template("index.html")

#Route to Delete a Pet-Game
@app.route("/deletepetgame/<id>", methods=["GET","POST"])
def deletepetgame(id):
    cookies = request.cookies
    email = cookies.get("email")
    password = cookies.get("password")
    if request.method == "POST":
        if (email == "vrashankrao@gmail.com" and password == "vrashank"):

            #Delete the Pet-Game
            cur = mydb.cursor(buffered=True)
            cur.execute("delete from pet_activitycategory where pac_id=%s",[id])
            mydb.commit()
            cur.close()
            return redirect('/addpetgame')
    else:
        return render_template("index.html")

#Route to Delete a Pet-Groom
@app.route("/deletepetgroom/<id>", methods=["GET","POST"])
def deletepetgroom(id):
    cookies = request.cookies
    email = cookies.get("email")
    password = cookies.get("password")
    if request.method == "POST":
        if (email == "vrashankrao@gmail.com" and password == "vrashank"):

            #Delete the Pet-Groom
            cur = mydb.cursor(buffered=True)
            cur.execute("delete from pet_activitycategory where pac_id=%s",[id])
            mydb.commit()
            cur.close()
            return redirect('/addpetgroom')
    else:
        return render_template("index.html")

#Route to get a Pet-Owner
@app.route("/getapetowner")
def getapetowner():
    cookies = request.cookies
    email = cookies.get("email")
    password = cookies.get("password")
    if request.method=="GET":
        if (email == "vrashankrao@gmail.com" and password == "vrashank"):
            cur = mydb.cursor(buffered=True)
            cur.execute("select po_id,po_name,po_email from pet_owner order by po_id")
            data = cur.fetchall()
            mydb.commit()
            cur.close()
            return render_template("ShopOwner/getapetowner.html",data=data)
        else:
            return render_template("index.html")


#Route to get pets for board only
@app.route("/getallthepets", methods=["GET","POST"])
def getallthepets():
    cookies = request.cookies
    email = cookies.get("email")
    password = cookies.get("password")
    if request.method == "GET":
        if (email == "vrashankrao@gmail.com" and password == "vrashank"):
            cur = mydb.cursor(buffered=True)
            cur.execute("select p_id,p_name,p_category,DATE_FORMAT(p_regdate,'%d/%m/%Y'),po_name from pet_details,pet_owner where pet_details.po_id=pet_owner.po_id order by pet_details.po_id")
            data = cur.fetchall()
            cur.execute("select p_id from pet_details order by po_id")
            id = cur.fetchall()
            mydb.commit()
            cur.close()
            return render_template("ShopOwner/getallthepets.html", data=data, id=id)

# Route to add a Boarding-Details of an Existing-Pet
@app.route("/addboardonly/<id>", methods=["GET", "POST"])
def addboardonly(id):
    cookies = request.cookies
    email = cookies.get("email")
    password = cookies.get("password")
    if request.method == "GET":
        if (email == "vrashankrao@gmail.com" and password == "vrashank"):
            return render_template("ShopOwner/addboardonly.html",id=id)
    if request.method == "POST":
        if (email == "vrashankrao@gmail.com" and password == "vrashank"):
            cur = mydb.cursor(buffered=True)

            bid = request.form.get("bid")
            basiccost = request.form.get("basiccost")
            boardfromdate = request.form.get("boardfromdate")
            boardtilldate = request.form.get("boardtilldate")
            petfoodpref = request.form.get("petfoodpref")
            pethealthcond = request.form.get("pethealthcond")
            bnailcutcount = request.form.get("bnailcutcount")
            bhaircutcount = request.form.get("bhaircutcount")
            bbathcount = request.form.get("bbathcount")
            bfoodcount = request.form.get("bfoodcount")

            # Code to reverse date
            fromdate = boardfromdate
            tilldate = boardtilldate

            # Code to Get No. of Days
            cur.execute("SELECT DATEDIFF(%s, %s)", (tilldate, fromdate))
            days = cur.fetchone()

            # Calculate the Total Cost of Pet-Board
            totalcost = int(days[0]) * int(basiccost) + (50 * int(bnailcutcount[0])) + (100 * int(bhaircutcount[0])) + int(days[0]) * (50 * int(bfoodcount[0])) + (30 * int(bbathcount[0]))

            # Insert details into board_details
            cur.execute("Insert into board_details(b_id,b_basiccost,b_totalcost,b_foodpref,b_nodays,b_fromdate,b_tilldate,b_healthcond,p_id,b_nailcutcount,b_haircutcount,b_bathcount,b_foodcount) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(bid, basiccost, totalcost, petfoodpref, days[0], fromdate, tilldate, pethealthcond, id,bnailcutcount, bhaircutcount, bbathcount, bfoodcount))

            mydb.commit()
            cur.close()
            return redirect('/givecode')
    else:
        return render_template("index.html")


#Route to update a Pet-Owner
@app.route("/updatepetowner/<id>", methods=["GET","POST"])
def updatepetowner(id):
    print("id is",id)
    cookies = request.cookies
    email = cookies.get("email")
    password = cookies.get("password")
    if request.method == "GET":
        if (email == "vrashankrao@gmail.com" and password == "vrashank"):
            cur = mydb.cursor(buffered=True)
            cur.execute("select po_name,po_email,po_address from pet_owner where po_id=%s",[id])
            data = cur.fetchall()
            cur.execute("select po_phone from petowner_phone where po_id=%s",[id])
            phone = cur.fetchone()
            print(data[0])
            mydb.commit()
            cur.close()
            return render_template("ShopOwner/updatepetowner.html",data=data[0],phone=phone[0],id=id)
    if request.method == "POST":
        if (email == "vrashankrao@gmail.com" and password == "vrashank"):
            cur = mydb.cursor(buffered=True)

            poname = request.form.get("poname")
            pophone = request.form.get("pophone")
            poemail = request.form.get("poemail")
            poaddress = request.form.get("poaddress")
            print(poname,pophone)
            #Update if there is any changes
            if(poname!=""):
                cur.execute("update pet_owner set po_name=%s where po_id=%s",(poname,id))
            if(pophone!= ""):
                cur.execute(" update petowner_phone set po_phone=%s where po_id=%s limit 1",(pophone, id))
            if(poemail != ""):
                cur.execute("update pet_owner set po_email=%s where po_id=%s",(poemail, id))
            if(poaddress!= ""):
                cur.execute("update pet_owner set po_address=%s where po_id=%s",(poaddress, id))
            mydb.commit()
            cur.close()
            return redirect(request.url)
    else:
        return render_template("index.html")

app.run(debug=True)