import csv

Total = 5
Rank = 3  # 這裡可以改為任意n值

def main(Total, Rank, New):
    # 將新數據添加到CSV文件
    with open('process_times.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([New])
    
    # 從CSV文件讀取最新的Total+1筆數據
    with open('process_times.csv', 'r') as f:
        reader = csv.reader(f)
        data = list(reader)
        latest_data = [int(row[0]) for row in data[-Total-1:]]
    
    print(f"最新{Total+1}筆數據: {latest_data}")

    # 對最新的Total+1筆數據進行排序
    sorted_data = sorted(latest_data)
    print(f"排序後的數據: {sorted_data}")

    # 檢查新數據的排名
    rank = sorted_data.index(int(New))
    if rank < Rank:
        print(f"PASS !! 排名是第 {rank+1}")
    else:
        print(f"FAIL !! 排名是第 {rank+1}")

# 主程序
while True:
    New = input("\n請輸入新的結果 (輸入'quit'退出): ")
    if New.lower() == 'quit':
        break
    try:
        New = int(New)
        # main函數現在將新數據添加到CSV文件,然後從CSV文件讀取最新的數據進行比較。
        main(Total, Rank, New)
    except ValueError:
        print("請輸入有效的整數!")