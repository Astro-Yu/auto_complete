import redis

# 추후에 redis 데이터베이스 연결할 코드
rd = redis.StrictRedis(host='localhost', port=6379, db=0)

"""문자에서 *표를 제거한다."""
def delete_star(word):
    return word.replace('*', '')

"""
실제 실행할 함수
redis의 자동완성을 위한 데이터베이스의 key가 autocomplete2여야 함.

-----------------------
-args-
search_word = 검색할 단어

-return-
Type : list

-----------------------

ex) 
search_word = "오"
return = ["오란고교 호스트부", "오늘부터 신령님", "오버로드"]

"""
def auto_complete(search_word):
    """ 값이 검색어로 시작하면서 *를 포함한 단어만 필터링한다."""
    def mapper(candidates):
        return candidates.startswith(search_word) and candidates[-1] == "*"

    searchidx = rd.zrank("autocomplete2",search_word)
    result_list = rd.zrange("autocomplete2", start = searchidx, end = searchidx+1000)
    result_str_list = [member.decode('utf-8') for member in result_list]

    results1 = list(filter(mapper,result_str_list))
    result2 = list(map(delete_star,results1))

    return result2
