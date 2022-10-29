import math
import csv
import pandas as pd

ratings = pd.read_csv('data/ratings.csv')
# print (ratings.head(20))
movies = pd.read_csv('data/movies.csv')
# print(movies.head(5))
data = pd.merge(movies, ratings, on='movieId')
# print(data.head(5))
data[['userId', 'rating', 'movieId', 'title']].sort_values('userId').to_csv('data/data.csv', index=False)

file = open("data/data.csv", 'r', encoding='UTF-8')
data = {}
# 用字典存储数据
for line in file.readlines():
    line = line.strip().split(',')
    if not line[0] in data.keys():
        data[line[0]] = {line[2]: line[1]}
    else:
        data[line[0]][line[2]] = line[1]


# 找不同用户共同评论过的电影，计算距离
def distance_calculation(user1, user2):
    user1_data = data[user1]
    user2_data = data[user2]
    distance = 0
    for key in user1_data.keys():
        if key in user2_data.keys():
            distance += pow(float(user1_data[key]) - float(user2_data[key]), 2)

    return 1 / (1 + math.sqrt(distance))


# 计算用户相似度
def similarity(userID):
    res = []
    for userid in data.keys():
        # 排除自己
        if not userid == userID:
            similar = distance_calculation(userID, userid)
            res.append((userid, similar))
    res.sort(key=lambda val: val[1])
    return res[:4]


# 参照相似度最高的用户进行推荐
def recommend(user):
    users = similarity(user)[0][0]
    items = data[users]
    recommendations = []
    for item in items.keys():
        if item not in data[user].keys():
            recommendations.append((item, items[item]))
    recommendations.sort(key=lambda val: val[1], reverse=True)  # 按照评分排序
    for j in range(len(recommendations)):
        if recommendations[j][1] < recommendations[0][1]:  # 筛选出评分最高的项目
            break
    return recommendations[:int(math.sqrt(j))]  # 开平方削减数量（也可以不这么干，就是条目有点多）


with open('result/movie.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['USERID', 'MOVIEID'])
    for i in range(len(data) - 1):
        Recommendations = recommend(str(i + 1))
        print('userID:' + str(i + 1))
        for m in Recommendations:
            writer.writerow([i + 1, m[0]])
f.close()
print('finished')
