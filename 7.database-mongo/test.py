# test for mongodb with python
import pymongo
import datetime

db_client = pymongo.MongoClient("mongodb://localhost:27017/")
db_list = db_client.list_database_names()
# dblist = myclient.database_names() # de
if "school" in db_list:
    print("Scholl 数据库已存在！")

db = db_client["school"]

print("插入数据...")


col_grade = db["grade"]
col_grade.drop()

grade_1 = {"name": "Grade One", "updated_at": datetime.datetime.now()}
grade_1_insert = col_grade.insert_one(grade_1)
grade_1_id = grade_1_insert.inserted_id

grade_2 = {"name": "Grade Two", "updated_at": datetime.datetime.now()}
grade_2_insert = col_grade.insert_one(grade_2)
grade_2_id = grade_2_insert.inserted_id

col_grade_two = db["grade_2"]
col_grade_two.insert_one(grade_1)
col_grade_two.insert_one(grade_2)

list_student_1 = [
    {"name": "Tom", "age": 7, "gender": "male", "grade": grade_1_id},
    {"name": "Jack", "age": 8, "gender": "male", "grade": grade_1_id},
    {"name": "Lucy", "age": 7, "gender": "female", "grade": grade_1_id}
]
list_student_2 = [
    {"name": "Lily", "age": 9, "gender": "female", "grade": grade_2_id},
    {"name": "Mike", "age": 8, "gender": "male", "grade": grade_2_id},
    {"name": "Susan", "age": 9, "gender": "female", "grade": grade_2_id}
]
col_student = db["student"]
col_student.drop()

insert_student_1 = col_student.insert_many(list_student_1)
insert_student_2 = col_student.insert_many(list_student_2)

# put student in grade
col_grade.update_one({"_id": grade_1_id}, {"$set": {"students": insert_student_1.inserted_ids}})
col_grade.update_one({"_id": grade_2_id}, {"$set": {"students": insert_student_2.inserted_ids}})


print("查询数据...")

grade_list = col_grade.find()
for x in grade_list:
    print(x)
student_list = col_student.find()
for item in student_list:
    print(item)

student_tom = col_student.find_one({"name": "Tom"})
print("Find Tom: %s" % student_tom)

col_student.update_one({"name": "Tom"}, {"$set": {"age": 9}})
student_tom = col_student.find_one({"name": "Tom"})
print("change Tom's age to 9: %s", student_tom)

print("female increment one !")
col_student.update_many({"gender": "female"}, {'$inc': {"age": 1}})
for item in col_student.find({"gender": "female"}):
    print(item)


# mycol.delete_one(myquery)
# mycol.delete_many(myquery)