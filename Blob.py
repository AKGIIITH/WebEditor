import pymysql
import pymysql.cursors

DB= pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="Images"
)

cursor = DB.cursor()

UserId= "Ayush"
image_metadata= "This is a test image"

Filepath="/Images/back.jpg"
cursor.execute("CREATE TABLE IF NOT EXISTS Images (ImageId INTEGER(45) AUTO_INCREMENT PRIMARY KEY NOT NULL, UserId VARCHAR(255) NOT NULL, images LONGBLOB NOT NULL), image_metadata VARCHAR(255))")

def InsertImage(UserId, Filepath, image_metadata):
    with open(Filepath,"rb") as file:
        BinaryData= file.read()
        cursor.execute("INSERT INTO Images (UserId, images, image_metadata) VALUES (%s, %s, %s)", (UserId, BinaryData, image_metadata))
        DB.commit()
        print("Image inserted successfully")

def RetrieveImage(UserId,ImageId):
    cursor.execute("SELECT images FROM Images WHERE UserId=%s ImageId=%s", (UserId,ImageId))
    image= cursor.fetchone()
    with open("retrieved_image.jpg","wb") as file:
        file.write(image[0])
        print("Image retrieved successfully")

InsertImage(UserId, Filepath, image_metadata)
RetrieveImage(UserId, 1)