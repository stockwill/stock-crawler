co_ids = ['1101', '1102', '1216', '1301', '1303', '1326', '1402', '2002', '2105', '2207',
          '2227', '2301', '2303', '2308', '2317', '2327', '2330', '2352', '2357', '2382',
          '2395', '2408', '2409', '2412', '2454', '2474', '2609', '2610', '2633', '2801',
          '2823', '2880', '2881', '2882', '2883', '2884', '2885', '2886', '2887', '2890',
          '2891', '2892', '2912', '3008', '3045', '3711', '4904', '4938', '5871', '5876',
          '5880', '6505', '9904', '9910']


# http://pchome.megatime.com.tw/group/mkt5/cidE002.html
# https://www.cnyes.com/twstock/Etfingredient/0050.html
# https://web.archive.org/web/20100208100742/http://www.twse.com.tw/ch/trading/indices/twco/tai50i.php
# https://www.taiwanindex.com.tw/index/index/TW50
# https://www.twse.com.tw/zh/

def get_co_ids2():
    return ['2330']
    # return ['2801']
    # return co_ids


# See https://www.twse.com.tw/zh/listed/listingProfile
def get_co_ids():
    category_list = [
        {'cat': '金融保險', 'ids': ['2801', '2809', '2812', '2816', '2820', '2823', '2827', '2831', '2832', '2833',
                                '2834', '2836', '2837', '2838', '2845', '2847', '2849', '2850', '2851', '2852', '2854',
                                '2855', '2856', '2867', '2880', '2881', '2882', '2883', '2884', '2885', '2886', '2887',
                                '2888', '2889', '2890', '2891', '2892', '2897', '5854', '5876', '5880', '6004', '6005',
                                '6012', '6024']}
    ]
    for item in category_list:
        for co_id in item['ids']:
            yield co_id


if __name__ == '__main__':
    print(list(get_co_ids()))
