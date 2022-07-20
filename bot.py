from main import names_list, card_list, expireations_list
from main import phone_codes, city_state_list, strt_ending, password_list
import requests
import random
import string
import threading

# scam link: https://serviceid-amazon.lnk.to/verify


# setting up input generators
def pick_random(arr):
    result = random.choice(arr)
    return result

def ssn():
    lst1 = ""
    lst2 = ""
    lst3 = ""
    for x in range(0, 9):
        if x < 3:
            lst1 += (str(random.randint(0, 9)))
        elif x < 5:
            lst2 += (str(random.randint(0, 9)))
        else: lst3 += (str(random.randint(0, 9)))

    social_security_num = f'{lst1}-{lst2}-{lst3} '

    return social_security_num

def phone_num():
    front = str(phone_codes[random.randint(0,205)])
    back = ""
    for x in range(0, 6):
        back += str(random.randint(0, 9))
    pn = front + back
    return pn

def email_gen(person):
    name = person[0] + person[-1][0]
    front = f'{name}+{"".join(random.choice(string.digits)for i in range(0,1))}'
    email = f'{front}@gmail.com'
    return email

def password_gen():
    pasw = pick_random(password_list)
    extra = "".join(random.choice(string.digits) for i in range(0,random.randint(0,3)))
    password = f'{pasw}{extra}'
    return password

def dob():
    front = random.randint(1,12)
    mid = random.randint(1,28)
    back = random.randint(1976, 2001)
    if front < 10:
        front = "0" + str(front)
    else: front = str(front)
    if mid < 10: mid = "0" + str(mid)
    else: mid = str(mid)
    dob = f'{front}/{mid}/{back}'
    return dob

def zipcode():
    zc = ""
    for x in range(0, 4):
        zc += str(random.randint(0, 9))
    return(zc)

def address():
    address = ""
    for x in range(0, 3): address += str(random.randint(1, 9))
    return address


# setting up trolling functions
def card_data_troll(req_url, person):
    card = pick_random(card_list)
    exp = pick_random(expireations_list)
    noc = f'{person[0]} {person[1]}'
    cn = card[0]
    ccv = card[1]
    acid = ""
    cem = exp[0]
    cey = exp[1]

    requests.post(req_url, allow_redirects=False, data={
        "noc": noc,
        "cn": cn,
        "acid": "",
        "cem": cem,
        "cey": cey,
        "3d": ccv,
        "submit": "Submit"
    })

def personal_info_troll(req_url, person, pn):
    street1 = pick_random(names_list)
    street = street1[0]
    ending = pick_random(strt_ending)
    location = pick_random(city_state_list)
    city = location[0]
    state = location[-1]
    house_num = address()
    requests.post(url=req_url, allow_redirects=False, data={
        "country": "US",
        "fullname": f'{person[0]} {person[1]}',
        "phone": pn,
        "address": f'{house_num} {street} {ending}',
        "address2": "",
        "city": city,
        "state": state,
        "zipcode": zipcode(),
        "dob": dob(),
        "ssn": ssn(),
        "submit": "Submit"
    })

def amazon_troll(req_url, password):
    requests.post(url=req_url, allow_redirects=False, data={
        "password": password,
        "submit": "Submit"
    })

def user_troll(req_url, pn, email):
    prob = random.randint(0, 15)
    if prob == 14: user = email
    else: user = pn
    
    requests.post(url=req_url, allow_redirects=False, data={
        "email": user,
        "submit": "Submit"
    })


# defining variables

# the total amount of trolls executed == multiplier*thread_amount
multiplier = range(1, 21)
thread_amount = 80

# I ruined abunch of this scammers documents he might ↓↓change↓↓ this part of the url
#  https://int-service-amzn-account.4nmn.com/THIS PART RIGHT HERE/submission@...
ru_phone_em = "https://int-service-amzn-account.4nmn.com/32ceeb2d816a9bde658c30b13c10f1b7/submission@login"
ru_amazon = "https://int-service-amzn-account.4nmn.com/32ceeb2d816a9bde658c30b13c10f1b7/submission@continue"
ru_person = "https://int-service-amzn-account.4nmn.com/32ceeb2d816a9bde658c30b13c10f1b7/submission@billing"
ru_card = "https://int-service-amzn-account.4nmn.com/32ceeb2d816a9bde658c30b13c10f1b7/submission@card"

# function that will send the sets of data all
# together in one go
def troll():
    for x in multiplier:
        # card info
        person = pick_random(names_list)
        pn = phone_num()
        password = password_gen()
        email = email_gen(person=person)
        user_troll(req_url=ru_phone_em, email=email, pn=pn)
        amazon_troll(req_url=ru_amazon, password=password)
        personal_info_troll(req_url=ru_person, person=person, pn=pn)
        print(x)


# threading to speed up proccess
threads = []

for i in range(thread_amount):
    t = threading.Thread(target=troll)
    t.daemon = True
    threads.append(t)

for i in range(thread_amount):
    threads[i].start()

for i in range(thread_amount):
    threads[i].join()