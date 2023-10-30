from multiprocessing import Pool
from common.custom_sort_key import custom_sort_key as cus_sort
import multiprocessing

def parallel_sort(data):
    order_column = data['order_column']
    direction = data['direction']
    subset = data['subset']

    return sorted(subset, key=lambda x: cus_sort(x, order_column), reverse=(direction == 'desc'))

def apply_multiprocessing_sort(user, order_column, order_column_dir):
    # CPU 코어 수를 파악합니다.
    num_cores = multiprocessing.cpu_count()

    # 데이터를 코어 수에 맞게 분할합니다.
    chunk_size = len(user) // num_cores
    chunks = [user[i * chunk_size: (i + 1) * chunk_size] for i in range(num_cores)]
    
    # 각 코어에서 분할된 데이터를 독립적으로 정렬합니다.
    with multiprocessing.Pool(processes=num_cores) as pool:
        sorted_chunks = pool.starmap(parallel_sort, [(chunk, order_column) for chunk in chunks])

    # 정렬된 분할 데이터를 합칩니다.
    user_sorted = []
    for sorted_chunk in sorted_chunks:
        user_sorted.extend(sorted_chunk)

    # 정렬 방향(order_column_dir)이 'desc'일 경우, 결과를 역순으로 반환합니다.
    if order_column_dir == "desc":
        user_sorted = user_sorted[::-1]

    return user_sorted