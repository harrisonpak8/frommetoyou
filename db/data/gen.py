from werkzeug.security import generate_password_hash
import csv
from faker import Faker
import random
from faker.providers import internet, misc, lorem, date_time, profile
from werkzeug.security import generate_password_hash

num_users = 1000
num_products = 2000
num_purchases = 2500
num_inventory = 2000

Faker.seed(0)
fake = Faker()


def get_csv_writer(f):
    return csv.writer(f, dialect='unix')

def gen_data(num):
    with open('Users.csv', 'w') as f1, open('Seller.csv', 'w') as f2, open('Products.csv', 'w') as f3,open('Inventory.csv', 'w') as f4, open('Carts.csv', 'w') as f5, open('Orders.csv', 'w') as f6, open('P_Reviews.csv', 'w') as f7, open('S_Reviews.csv', 'w') as f8:
        writer1 = get_csv_writer(f1)
        writer2 = get_csv_writer(f2)
        writer3 = get_csv_writer(f3)
        writer4 = get_csv_writer(f4)
        writer5 = get_csv_writer(f5)
        writer6 = get_csv_writer(f6)
        writer7 = get_csv_writer(f7)
        writer8 = get_csv_writer(f8)

        ##available user ids
        user_ids = []

        ##users table
        for uid in range(num):
            user_ids.append(uid)
            
            profile = fake.profile()
            email = fake.unique.email()
            plain_password = 'password1!'
            password = generate_password_hash(plain_password)
            name_components = profile['name'].split(' ')
            firstname = name_components[0]
            lastname = name_components[-1]
            address = profile['address']
            balance = 0
            writer1.writerow([uid, email, password, firstname, lastname, address, balance])
        print('users generated')

        ##sellers table
        seller_ids = user_ids[:]
        for sid in seller_ids:
            balance = quantity = fake.pyint(min_value = 0, max_value = 500)
            writer2.writerow([sid, balance])
        print('sellers generated')

        ###products, inventory, carts, orders, p_reviews, s_reviews
        cats = ["accessories", "books", "clothes", "decor", "electronics", "food", "games", "shoes"]
        links = ["https://images.pexels.com/photos/12026054/pexels-photo-12026054.jpeg?auto=compress&cs=tinysrgb&w=600", "https://images.unsplash.com/photo-1544947950-fa07a98d237f?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MTF8fGJvb2t8ZW58MHx8MHx8&auto=format&fit=crop&w=700&q=60", "https://images.unsplash.com/photo-1583743814966-8936f5b7be1a?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8NXx8c2hpcnR8ZW58MHx8MHx8&auto=format&fit=crop&w=700&q=60", "https://images.unsplash.com/photo-1584589167171-541ce45f1eea?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8NHx8ZGVjb3J8ZW58MHx8MHx8&auto=format&fit=crop&w=700&q=60", "https://images.unsplash.com/photo-1537963447914-dbc04b81de27?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MTZ8fGdhbWV8ZW58MHx8MHx8&auto=format&fit=crop&w=700&q=60", "https://images.unsplash.com/photo-1621939514649-280e2ee25f60?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8OHx8Y2VyZWFsJTIwYm94fGVufDB8fDB8fA%3D%3D&auto=format&fit=crop&w=700&q=60", "https://images.unsplash.com/photo-1640461470346-c8b56497850a?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8MTR8fGJvYXJkJTIwZ2FtZXxlbnwwfHwwfHw%3D&auto=format&fit=crop&w=700&q=60", "https://images.unsplash.com/photo-1549298916-b41d501d3772?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxzZWFyY2h8NHx8c2hvZXN8ZW58MHx8MHx8&auto=format&fit=crop&w=700&q=60"]
        reviewlinks = ["https://www.shutterstock.com/image-photo/unhappy-man-frustrated-by-wrong-600w-2051406776.jpg", "https://shutterstock.com/image-photo/oh-dear-what-confused-shocked-600w-1845313102.jpg", "https://news.artnet.com/app/news-upload/2016/05/sculpture-shattered-portuga-large.jpg", "https://www.shutterstock.com/image-photo/unhappy-young-caucasian-woman-look-600w-1896027958.jpg", "https://www.shutterstock.com/image-photo/home-delivery-confused-young-man-600w-1934788400.jpg", "https://www.shutterstock.com/image-photo/young-man-surprised-opening-box-600w-1337933900.jpg"]
        
        for pid in range(num):
            ##products
            idx = fake.pyint(min_value = 0, max_value = 7)
            sid = pid
            productname = fake.sentence(nb_words=3)[:-1]
            descr = fake.sentence(nb_words=40)[:-1]
            cat = cats[idx]
            price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            link = links[idx]
            available = fake.random_element(elements=('true', 'false'))
            writer3.writerow([pid, sid, productname, descr, cat, price, link, available])

            ##inventory
            quantity = fake.pyint(min_value = 0, max_value = 200)
            writer4.writerow([sid, pid, productname, quantity])

            ##carts
            buyer_uid = fake.random_int(min=0, max=num-1)
            cart_quantity = fake.random_int(min=1, max=10)
            unit_price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            writer5.writerow([buyer_uid, pid, sid, productname, quantity, unit_price])

            ##orders
            oid = pid
            time_purchased = fake.date_time()
            ff = fake.random_element(elements=('true', 'false'))
            writer6.writerow([oid, buyer_uid, pid, sid, cart_quantity, unit_price, time_purchased, ff])

            ##p_reviews
            idx2 = fake.pyint(min_value = 0, max_value = 5)
            reviewlink = reviewlinks[idx2]
            
            rating = fake.random_int(min=1, max=5)
            review = fake.sentence(nb_words=20)[:-1]
            writer7.writerow([buyer_uid, pid, rating, review, reviewlink, time_purchased])

            #s_reviews
            rating = fake.random_int(min=1, max=5)
            review = fake.sentence(nb_words=20)[:-1]
            writer8.writerow([buyer_uid, sid, rating, review, time_purchased])
    print('remaining tables created')
    return


""" def gen_carts(num_carts):
    with open('Carts.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Carts...', end=' ', flush = True)
        for cart in range(num_carts):
            if cart % 100 == 0:
                print(f'{cart}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            pid = fake.random_int(min=0, max=num_products-1)
            sid = fake.random_int(min=0, max=1999)
            productname = fake.sentence(nb_words=4)[:-1]
            quantity = fake.random_int(min=1, max=10)
            unit_price = f'{str(fake.random_int(max=500))}.{fake.random_int(max=99):02}'
            writer.writerow([uid, pid, sid, productname, quantity, unit_price])
        print(f'{num_carts} generated')
    return

def gen_review(num_review):
    with open('P_Reviews.csv', 'w') as f:
        writer = get_csv_writer(f)
        print('Review...', end=' ', flush = True)
        for review in range(num_review):
            if review % 100 == 0:
                print(f'{review}', end=' ', flush=True)
            uid = fake.random_int(min=0, max=num_users-1)
            sid = fake.random_int(min=0, max=num_products-1)
            rating = fake.random_int(min=1, max=5)
            time_purchased = fake.date_time()
            writer.writerow([uid, sid, rating, time_purchased])
        print(f'{num_review} generated')
    return
 """
 
def gen_convo(num):
    with open('Conversations.csv', 'w') as f1, open('Messages.csv', 'w') as f2:
        writer1 = get_csv_writer(f1)
        writer2 = get_csv_writer(f2)
        
        for cid in range(num):
            ##products
            sid = fake.pyint(min_value = 0, max_value = 2000)
            writer1.writerow([cid, sid, cid])    
            
            for message in range(10):
                user = fake.pyint(min_value = 0, max_value = 1)
                
                if(user == 0):
                    id = sid
                else:
                    id = cid
                    
                message = fake.sentence(nb_words=20)[:-1]
                time = fake.date_time()
                writer2.writerow([cid, id, message, time])    
            

#gen_data(2000)
gen_convo(2000)
#gen_carts(num_carts)            
#gen_review(1000)


