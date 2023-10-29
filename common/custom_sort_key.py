def custom_sort_key(item, order_column):
    # item에서 order_column 값을 가져오기
    if "__" in order_column:
        parts = order_column.split("__")
        fk_field = parts[0]
        related_field = parts[1]
        
        related_obj = getattr(item, fk_field)
        if related_obj:
            value = getattr(related_obj, related_field, "")
            if isinstance(value, str):  # 문자열인 경우에만 strip 메서드를 호출
                value = value.strip()
        else:
            value = ""
    else:
        value = getattr(item, order_column, "")
        if isinstance(value, str):  # 문자열인 경우에만 strip 메서드를 호출
            value = value.strip()
    
    if not value:
        return (3, )  # 정의되지 않은 값은 가장 마지막에 위치

    if isinstance(value, str):  # value가 문자열일 경우에만 소문자 변환 적용
        value = value.lower()
        first_char = value[0] if value else ''
    else:
        first_char = str(value)[0] if value else ''
    
    # 한글 처리
    if '가' <= first_char <= '힣':
        cho = ['ㄱ', 'ㄲ', 'ㄴ', 'ㄷ', 'ㄸ', 'ㄹ', 'ㅁ', 'ㅂ', 'ㅃ', 'ㅅ', 'ㅆ', 'ㅇ', 'ㅈ', 'ㅉ', 'ㅊ', 'ㅋ', 'ㅌ', 'ㅍ', 'ㅎ']
        jung = ['ㅏ', 'ㅐ', 'ㅑ', 'ㅒ', 'ㅓ', 'ㅔ', 'ㅕ', 'ㅖ', 'ㅗ', 'ㅘ', 'ㅙ', 'ㅚ', 'ㅛ', 'ㅜ', 'ㅝ', 'ㅞ', 'ㅟ', 'ㅠ', 'ㅡ', 'ㅢ', 'ㅣ']
        
        cho_index = next((i for i, c in enumerate(cho) if first_char.startswith(c)), len(cho))
        jung_index = next((i for i, c in enumerate(jung) if first_char.startswith(c)), len(jung))
        
        return (0, cho_index, jung_index, value)
    
    # 영어 처리
    elif 'a' <= first_char <= 'z':
        return (1, value)  # 전체 value를 사용하여 정렬
    
    # 숫자 처리
    elif '0' <= first_char <= '9':
        return (2, first_char)
    
    # 그 외 처리
    else:
        return (3, first_char)