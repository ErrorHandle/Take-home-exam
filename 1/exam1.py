import pandas as pd
import re
import sys


#
#   讀取csv檔，並移除不要的欄位
#
def read_csv_files(csv_file):
    df = pd.read_csv('./data/{}'.format(csv_file))
    #移除 The villages and towns urban district transaction sign ...
    df.drop([0], inplace=True)
    return df
#
#   合併資料，並 reset index
#
def concat_df():
    df_a = read_csv_files('a_lvr_land_a.csv')
    df_b = read_csv_files('b_lvr_land_a.csv')
    df_e = read_csv_files('e_lvr_land_a.csv')
    df_f = read_csv_files('f_lvr_land_a.csv')
    df_h = read_csv_files('h_lvr_land_a.csv')
    #處理合併後的 index
    try:
        df_all = pd.concat([df_a, df_b, df_e, df_f, df_h]).reset_index(drop=True)
        print('concat csv files successfully.')
        print(df_all)
        return df_all
    except:
        print('concat csv fail!')
#
#  將樓層數繁體中文轉成數字，方便篩選資料
#
def floor_to_int(df):
    dict = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10}
    #遇到空值填0
    df_all = df.fillna(0)
    for index, floors in enumerate(df_all['總樓層數']):
        if floors != 0:
            num = 0
            #中文數字長度為3 ex.二十二
            if len(floors[:-1]) == 3:
                num = dict[floors[0]] * 10 + dict[floors[-2]]
                # df_all[index] = num
            #中文數字長度為2 ex.二十 or 十一
            elif len(floors[:-1]) == 2:
                #非十的倍數
                if floors[0] != '十':
                    num = dict[floors[0]] * 10
                #十的倍數
                else:
                    num = 10 + dict[floors[-2]]
                # df_all[index] = num
            #中文個位數轉int ex.十
            elif len(floors[:-1]) == 1:
                num = dict[floors[-2]]
            df_all['總樓層數'][index] = num
    return df_all

def filter_a(data, save_path):
    #總樓層數中文轉int
    data = floor_to_int(data)
    #篩選條件
    mask1 = data['主要用途'] == '住家用'
    mask2 = data['建物型態'] == '住宅大樓(11層含以上有電梯)'
    mask3 = data['總樓層數'] >= 13
    try:
        filter = data[(mask1 & mask2 & mask3)]
        filter.reset_index(drop=True).to_csv(save_path)
        print('filter_a successfully!\nsave path:{}'.format(save_path))
    except:
        print('filter_a fail!')

def filter_b(data, save_path):
    total = data.index[-1] + 1
    sum_price = data['總價元'].astype('int').sum()
    sum_parking_space = 0
    sum_parking_space_price = 0

    #取得交易筆棟數欄位資料
    for value in data['交易筆棟數']:
        #土地3建物1車位0 取最後一位數字
        parking_space = int(value[-1])
        sum_parking_space += parking_space

    for price in data['車位總價元']:
        #str to int
        price = int(price)
        sum_parking_space_price += price


    average_house_price = sum_price // total
    average_parking_space_price = sum_parking_space_price // sum_parking_space
    print('總件數:{} 總價:{} 平均價:{}'.format(total, sum_price, average_house_price))
    print('總車位數:{} 總車位價錢:{} 平均車位價錢:{}'.format(sum_parking_space, sum_parking_space_price, average_parking_space_price))

    filter_b = {
        '總件數': total,
        '總車位數': sum_parking_space,
        '平均總價元': average_house_price,
        '平均車位總價元': average_parking_space_price
    }
    filter_b = pd.DataFrame(filter_b, index=[0])
    filter_b.to_csv(save_path)

def main():
    filter_a_save_path = './output/filter_a.csv'
    filter_b_save_path = './output/filter_b.csv'

    df = concat_df()

    # filter_a(df, filter_a_save_path)
    # filter_b(df, filter_b_save_path)

if __name__ == "__main__":
    main()
