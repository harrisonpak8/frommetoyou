from flask import current_app as app, flash
import datetime


class PReview:
    def __init__(self, uid, pid, rating, time_purchased):
        self.uid = uid
        self.pid = pid
        self.rating = rating
        self.time_purchased = time_purchased
        
    @staticmethod
    def getUserProductReviews(uid):
        rows = app.db.execute('''
SELECT uid, pid, name, rating, review, u.link AS link
FROM Products u, P_Reviews p
WHERE uid = :uid AND pid = id
ORDER BY time_purchased DESC
''',
                              uid=uid)
        return rows
    
    @staticmethod
    def getAProductReviews(pid):
        rows = app.db.execute('''
    SELECT CONCAT(firstname, ' ', lastname) AS name, rating, review, uid
    FROM Users u, P_Reviews p
    WHERE uid = id AND pid = :pid
    ORDER BY time_purchased DESC
''',
                              pid=pid)
        return rows    

    @staticmethod
    def numberOfReview(pid):
        rows = app.db.execute('''
    SELECT COUNT(*)
    FROM P_Reviews
    WHERE pid = :pid
''',
                              pid=pid)
        return int(rows[0][0]) 
    
    @staticmethod
    def updateProductReview(uid, pid, rating, review, link):
        rows = app.db.execute('''
UPDATE P_Reviews
SET rating = :rating, review = :review, link = :link
WHERE uid = :uid and pid = :pid
''',
                              uid=uid, pid = pid, rating = rating, review = review, link = link)
        return None
    
    @staticmethod
    def createProductReview(uid, pid, rating, review, link):
        currentdate = datetime.datetime.now()
        try:
            rows = app.db.execute('''
INSERT INTO P_Reviews(uid, pid, rating, review, link, time_purchased)
VALUES(:uid, :pid, :rating, :review, :link, :time_purchased)
''',
                              uid=uid, pid = pid, rating = rating, time_purchased = currentdate, review = review, link = link)
            return None   
    
        except Exception as e:
            print(str(e))
            return None 

    @staticmethod
    def reviewexist(uid, pid):
        rows = app.db.execute("""
SELECT uid, pid
FROM P_Reviews
WHERE pid = :pid and uid = :uid
""",
                              uid = uid, pid = pid)
        return len(rows) > 0

    @staticmethod
    def deletereview(uid, pid):
        rows = app.db.execute("""
DELETE FROM P_Reviews
WHERE uid = :uid and pid = :pid
""",
                              uid = uid, pid = pid)
        return None
    
    @staticmethod
    def getAverage(pid):
        rows = app.db.execute('''
SELECT AVG(rating)
FROM P_Reviews
WHERE pid = :pid
''',
                              pid=pid)
        if rows[0][0] is None:
            return 0
        else:
            return int(rows[0][0])
    

    @staticmethod
    def numberOfReviewOne(pid):
        rows = app.db.execute('''
    SELECT COUNT(*)
    FROM P_Reviews
    WHERE pid = :pid AND rating = 1
''',
                              pid=pid)
        return int(rows[0][0]) 
    
    @staticmethod
    def numberOfReviewTwo(pid):
        rows = app.db.execute('''
    SELECT COUNT(*)
    FROM P_Reviews
    WHERE pid = :pid AND rating = 2
''',
                              pid=pid)
        return int(rows[0][0]) 
    
    @staticmethod
    def numberOfReviewThree(pid):
        rows = app.db.execute('''
    SELECT COUNT(*)
    FROM P_Reviews
    WHERE pid = :pid AND rating = 3
''',
                              pid=pid)
        return int(rows[0][0]) 
    
    @staticmethod
    def numberOfReviewFour(pid):
        rows = app.db.execute('''
    SELECT COUNT(*)
    FROM P_Reviews
    WHERE pid = :pid AND rating = 4
''',
                              pid=pid)
        return int(rows[0][0]) 
    
    @staticmethod
    def numberOfReviewFive(pid):
        rows = app.db.execute('''
    SELECT COUNT(*)
    FROM P_Reviews
    WHERE pid = :pid AND rating = 5
''',
                              pid=pid)
        return int(rows[0][0]) 
    
    @staticmethod
    def orderExist(uid, pid):
        rows = app.db.execute('''
    SELECT uid, pid
    FROM Orders
    WHERE pid = :pid AND uid = :uid
''',
                              pid=pid, uid = uid)
        return len(rows) > 0
    
    @staticmethod
    def getAPReviewLinks(pid):
        rows = app.db.execute('''
    SELECT link, CONCAT(firstname, ' ', lastname) AS name
    FROM Users u, P_Reviews p
    WHERE uid = id AND pid = :pid
''',
                              pid=pid)
        return rows  
    
    #########################################
    #User Queries
    #######################################
    
    @staticmethod
    def getAverageU(uid):
        rows = app.db.execute('''
    SELECT AVG(rating)
    FROM P_Reviews
    WHERE uid = :uid
    ''',
                              uid=uid)
        if rows[0][0] is None:
            return 0
        else:
            return int(rows[0][0])
    
    @staticmethod
    def numberOfReviewU(uid):
        rows = app.db.execute('''
    SELECT COUNT(*)
    FROM P_Reviews
    WHERE uid = :uid
''',
                              uid=uid)
        if rows[0][0] is None:
            return 0
        else:
            return int(rows[0][0]) 
    
    @staticmethod
    def numberOfReviewOneU(uid):
        rows = app.db.execute('''
    SELECT COUNT(*)
    FROM P_Reviews
    WHERE uid = :uid AND rating = 1
''',
                              uid=uid)
        if rows[0][0] is None:
            return 0
        else:
            return int(rows[0][0]) 
    
    @staticmethod
    def numberOfReviewTwoU(uid):
        rows = app.db.execute('''
    SELECT COUNT(*)
    FROM P_Reviews
    WHERE uid = :uid AND rating = 2
''',
                              uid=uid)
        if rows[0][0] is None:
            return 0
        else:
            return int(rows[0][0]) 
    
    @staticmethod
    def numberOfReviewThreeU(uid):
        rows = app.db.execute('''
    SELECT COUNT(*)
    FROM P_Reviews
    WHERE uid = :uid AND rating = 3
''',
                              uid=uid)
        if rows[0][0] is None:
            return 0
        else:
            return int(rows[0][0]) 
    
    @staticmethod
    def numberOfReviewFourU(uid):
        rows = app.db.execute('''
    SELECT COUNT(*)
    FROM P_Reviews
    WHERE uid = :uid AND rating = 4
''',
                              uid=uid)
        if rows[0][0] is None:
            return 0
        else:
            return int(rows[0][0]) 
    
    @staticmethod
    def numberOfReviewFiveU(uid):
        rows = app.db.execute('''
    SELECT COUNT(*)
    FROM P_Reviews
    WHERE uid = :uid AND rating = 5
''',
                              uid=uid)
        if rows[0][0] is None:
            return 0
        else:
            return int(rows[0][0])
    ##############################################################
    #Seller Queries
    ############################################################
    
    @staticmethod
    def getAverageS(sid):
        rows = app.db.execute('''
    SELECT AVG(rating)
    FROM S_Reviews
    WHERE sid = :sid
    ''',
                              sid=sid)
        if rows[0][0] is None:
            return 0
        else:
            return int(rows[0][0])
    
    @staticmethod
    def numberOfReviewS(sid):
        rows = app.db.execute('''
    SELECT COUNT(*)
    FROM S_Reviews
    WHERE sid = :sid
''',
                              sid=sid)
        if rows[0][0] is None:
            return 0
        else:
            return int(rows[0][0])
    
    @staticmethod
    def numberOfReviewOneS(sid):
        rows = app.db.execute('''
    SELECT COUNT(*)
    FROM S_Reviews
    WHERE sid = :sid AND rating = 1
''',
                              sid=sid)
        if rows[0][0] is None:
            return 0
        else:
            return int(rows[0][0]) 
    
    @staticmethod
    def numberOfReviewTwoS(sid):
        rows = app.db.execute('''
    SELECT COUNT(*)
    FROM S_Reviews
    WHERE sid = :sid AND rating = 2
''',
                              sid=sid)
        if rows[0][0] is None:
            return 0
        else:
            return int(rows[0][0])
    
    @staticmethod
    def numberOfReviewThreeS(sid):
        rows = app.db.execute('''
    SELECT COUNT(*)
    FROM S_Reviews
    WHERE sid = :sid AND rating = 3
''',
                              sid=sid)
        if rows[0][0] is None:
            return 0
        else:
            return int(rows[0][0])
    
    @staticmethod
    def numberOfReviewFourS(sid):
        rows = app.db.execute('''
    SELECT COUNT(*)
    FROM S_Reviews
    WHERE sid = :sid AND rating = 4
''',
                              sid=sid)
        if rows[0][0] is None:
            return 0
        else:
            return int(rows[0][0])
    
    @staticmethod
    def numberOfReviewFiveS(sid):
        rows = app.db.execute('''
    SELECT COUNT(*)
    FROM S_Reviews
    WHERE sid = :sid AND rating = 5
''',
                              sid=sid)
        if rows[0][0] is None:
            return 0
        else:
            return int(rows[0][0])
    
    @staticmethod
    def getSellerProductReviews(sid):
        rows = app.db.execute('''
SELECT CONCAT(firstname, ' ', lastname) AS name, rating, review, uid
FROM Users u, S_Reviews s
WHERE sid = :sid AND uid = id
ORDER BY time_purchased DESC
''',
                              sid=sid)
        return rows
    
    @staticmethod
    def updateSellerReview(uid, sid, rating, review):
        rows = app.db.execute('''
UPDATE S_Reviews
SET rating = :rating, review = :review
WHERE sid = :sid and uid = :uid
''',
                              uid=uid, sid = sid, rating = rating, review = review)
        return None    
    
    @staticmethod
    def deleteSellerReview(uid, sid):
        rows = app.db.execute("""
DELETE FROM S_Reviews
WHERE uid = :uid and sid = :sid
""",
                              uid = uid, sid = sid)
        return None
    
    @staticmethod
    def createSellerReview(uid, sid, rating, review):
        currentdate = datetime.datetime.now()
        rows = app.db.execute('''
INSERT INTO S_Reviews(uid, sid, rating, review, time_purchased)
VALUES(:uid, :sid, :rating, :review, :time_purchased)
''',
                              uid=uid, sid = sid, rating = rating, time_purchased = currentdate, review = review)
        return None 
    
    @staticmethod
    def sellerReviewexist(uid, sid):
        rows = app.db.execute("""
SELECT uid, sid
FROM S_Reviews
WHERE sid = :sid and uid = :uid
""",
                              uid = uid, sid = sid)
        return len(rows) > 0
    
    @staticmethod
    def sellerOrderExist(uid, sid):
        rows = app.db.execute('''
    SELECT uid, sid
    FROM Orders
    WHERE sid = :sid AND uid = :uid
''',
                              sid=sid, uid = uid)
        return len(rows) > 0
    
###########################################################################
# Messaging
##########################################################################
    
    @staticmethod
    def getUserConvo(uid):
        rows = app.db.execute('''
    SELECT uid, sid, cid, CONCAT(firstname, ' ', lastname) AS othername
    FROM Conversations c, Users u
    WHERE uid = :uid AND sid = id
''',
                              uid = uid)
        if rows is None:
            return 0
        else:
            return rows  
    
    @staticmethod
    def getSellerConvo(sid):
        rows = app.db.execute('''
    SELECT uid, sid, cid, CONCAT(firstname, ' ', lastname) AS othername
    FROM Conversations c, Users u
    WHERE sid = :sid AND uid = id
''',
                              sid = sid)
        if rows is None:
            return 0
        else:
            return rows  
    
    @staticmethod
    def createConversations(sid, uid, cid):
            rows = app.db.execute("""
INSERT INTO Conversations(uid, sid, cid)
VALUES(:uid, :sid, :cid)
""",
                                  uid = uid, sid = sid, cid = cid)
            return None
        
    @staticmethod
    def maxcid(uid, sid):
            row1 = int(app.db.execute("""
SELECT MAX(cid)
FROM Conversations
""", uid=uid, sid = sid)[0][0] + 1)
            return row1
        
    @staticmethod
    def getMessages(cid):
        rows = app.db.execute('''
    SELECT CONCAT(firstname, ' ', lastname) AS name, message, time_sent
    FROM Messages c, Users u
    WHERE cid = :cid AND c.id = u.id
    ORDER BY time_sent ASC
''',
                              cid = cid)
        if rows is None:
            return 0
        else:
            return rows 
        
    @staticmethod
    def addMessage(cid, id, message):
        currentdate = datetime.datetime.now()
        rows = app.db.execute('''
INSERT INTO Messages(cid, id, message, time_sent)
VALUES(:cid, :id, :message, :time_sent)
''',
                              time_sent = currentdate, cid = cid, id = id, message = message)
        return None 
    
    @staticmethod
    def convoExist(id, uid):
        rows = app.db.execute('''
    SELECT cid
    FROM Conversations
    WHERE uid = :uid AND sid = :sid
''',
                              sid = id, uid = uid)
        
        return len(rows) > 0