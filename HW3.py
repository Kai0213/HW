responses_new = [
    [200, 201],
    [400, 401, 404],
    [500, 502, 503]
]


# 找出最長子列表的長度
max_length = max(len(sublist) for sublist in responses_new)

# 按照要求的順序輸出
for i in range(max_length):
    for sublist in responses_new:
        if i < len(sublist):
            print(sublist[i], end=' ')

print()  