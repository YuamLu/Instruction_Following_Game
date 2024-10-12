import re
from typing import Tuple


class Question1_1:
    question = """
    第一章第一題（初來乍到），請你構造一個問題使模型的回答是一字不差的“1+1=3”（不需要引號）。
    請在下面的輸入框內填寫你的構造並點擊按鈕提交。
    """

    @staticmethod
    def check_result(user_text, answer_text):
        answer_text = answer_text.strip()
        if answer_text == '1+1=3':
            return True, None
        else:
            return False, "答案必須是 '1+1=3'。"


class Question1_2:
    question = """
    第一章第二題（小試牛刀），請你輸入三個字（及）以內的問題，使模型的回答在30個字以上。
    請在下面的輸入框內填寫你的問題並點擊按鈕提交。
    """

    @staticmethod
    def count_words(text: str):
        return len(text.split())

    @staticmethod
    def check_result(user_text, answer_text):
        user_text = user_text.strip()
        answer_text = answer_text.strip()
        if Question1_2.count_words(user_text) > 3:
            return False, "問題長度應在三個字及以內。"
        elif Question1_2.count_words(answer_text) <= 30:
            return False, "答案長度應超過30個字。"
        else:
            return True, None


class Question1_3:
    question = """
    第一章第三題（短說長話），請你輸入一個字的問題，使模型的回答在100個字以上。
    請在下面的輸入框內填寫你的問題並點擊按鈕提交。
    """

    @staticmethod
    def count_words(text: str):
        return len(text.split())

    @staticmethod
    def check_result(user_text, answer_text):
        user_text = user_text.strip()
        answer_text = answer_text.strip()
        if Question1_3.count_words(user_text) > 1:
            return False, "問題長度應在一個字及以內。"
        elif Question1_3.count_words(answer_text) <= 100:
            return False, "答案長度應超過100個字。"
        else:
            return True, None


class Question1_4:
    question = """
    第一章第四題（短說短話），請輸入一個字的問題，使模型的回答字數小於20個字。
    請在下面的輸入框內填寫你的問題並點擊按鈕提交。
    """

    @staticmethod
    def count_words(text: str):
        return len(text.split())

    @staticmethod
    def check_result(user_text, answer_text):
        user_text = user_text.strip()
        answer_text = answer_text.strip()
        if Question1_4.count_words(user_text) > 1:
            return False, "問題長度應在一個字及以內。"
        elif Question1_4.count_words(answer_text) >= 20:
            return False, "答案長度應小於20個字。"
        else:
            return True, None


class Question1_5:
    question = """
    第一章第五題（回文不變），請輸入一個本身不是回文串的問題，使無論正著問還是倒著問，模型的回答是一樣的。
    請在下面的輸入框內填寫你的問題並點擊按鈕提交。
    """

    @staticmethod
    def word_reverse_text(text: str):
        return text[::-1]

    @staticmethod
    def check_result(user_text, answer_text, llm_callback):
        user_text = user_text.strip()
        answer_text = answer_text.strip()
        reversed_user_text = Question1_5.word_reverse_text(user_text)
        second_answer_text = llm_callback(reversed_user_text).strip()

        if user_text == reversed_user_text:
            return False, "問題不能是回文串。"
        if second_answer_text != answer_text:
            return False, f"正著問和倒著問時，模型的回答應該是一樣的。 正著問回答：{answer_text} 反著問回答：{second_answer_text}"
        return True, None


class Question1_6:
    question = """
    第一章第六題（無中生狗），請提一個不包含“狗”這個字的問題，但是回答中至少出現3次“狗”這個字。
    請在下面的輸入框內填寫你的問題並點擊按鈕提交。
    """

    @staticmethod
    def check_result(user_text, answer_text):
        if '狗' in user_text:
            return False, '問題不得包含“狗”字。'

        dog_count = len(re.findall('狗', answer_text))
        if dog_count >= 3:
            return True, f'“狗”字的出現次數為{dog_count}次。'
        else:
            return False, f'“狗”字的出現次數為{dog_count}次，未達到3次。'


class Question2_1:
    question = """
    第二章第一題（質數長度），你需要提出一個字數是質數的問題，使回答的長度剛好是它的下一個質數。
    """

    @staticmethod
    def is_prime(n: int):
        if n < 2:
            return False
        for i in range(2, int(n ** 0.5) + 1):
            if n % i == 0:
                return False
        return True

    @staticmethod
    def next_prime(n: int):
        while True:
            n += 1
            if Question2_1.is_prime(n):
                return n

    @staticmethod
    def check_result(user_text, answer_text):
        qs_length = len(user_text.strip())
        if not Question2_1.is_prime(qs_length):
            return False, f'問題長度為{qs_length}，非質數。'

        answer_length = len(answer_text.strip())
        next_prime_length = Question2_1.next_prime(qs_length)
        if answer_length != next_prime_length:
            return False, f'下一個質數為{next_prime_length}，但回答長度為{answer_length}。'
        return True, None


class Question2_2:
    question = """
    第二章第二題（越說越大），請輸入一個大於一的正整數作為問題，使回答里包含至少比它大一千的數。
    """

    @staticmethod
    def get_all_numbers(text: str):
        return [int(num) for num in re.findall(r'\d+', text)]

    @staticmethod
    def check_result(user_text, answer_text):
        try:
            value = int(user_text.strip())
            if value <= 1:
                return False, "輸入必須是一個大於一的正整數。"
        except ValueError:
            return False, "輸入必須是一個大於一的正整數。"

        for value_item in Question2_2.get_all_numbers(answer_text):
            if value_item >= value + 1000:
                return True, None
        return False, f"回答必須包含至少比 {value} 大一千的數。"


class Question2_3:
    question = """
    第二章第三題（對稱數字），請輸入一個正整數作為問題，使模型的回答中至少包含一個數字是對稱的（如121、1331）。
    """

    @staticmethod
    def is_palindromic_number(n: int):
        return str(n) == str(n)[::-1]

    @staticmethod
    def get_all_numbers(text: str):
        return [int(num) for num in re.findall(r'\d+', text)]

    @staticmethod
    def check_result(user_text, answer_text):
        numbers = Question2_3.get_all_numbers(answer_text)
        for number in numbers:
            if Question2_3.is_palindromic_number(number):
                return True, None
        return False, "回答中必須包含至少一個對稱數字。"


class Question2_4:
    question = """
    第二章第四題（數字之和），請輸入一串數字作為問題，使模型的回答中包含這些數字之和。
    """

    @staticmethod
    def get_all_numbers(text: str):
        return [int(num) for num in re.findall(r'\d+', text)]

    @staticmethod
    def check_result(user_text, answer_text):
        numbers = Question2_4.get_all_numbers(user_text)
        expected_sum = sum(numbers)
        answer_numbers = Question2_4.get_all_numbers(answer_text)
        answer_sum = sum(answer_numbers)
        if expected_sum in answer_numbers or expected_sum == answer_sum:
            return True, None
        return False, f"回答中必須包含數字之和 {expected_sum}。"


class Question2_5:
    question = """
    第二章第五題（特定詞語），請輸入一個問題，使模型的回答中包含指定的詞語“機器學習”。
    """

    @staticmethod
    def check_result(user_text, answer_text):
        if "機器學習" in answer_text:
            return True, None
        return False, "回答中必須包含詞語 '機器學習'。"

class CreativeQuestion1:
    question = """
    在10個字以內的prompt，讓LLM的回答包含"穀雨", "大暑", "立秋", "冬至", "大雪", "秋分"。
    請在下面的輸入框內填寫你的問題並點擊按鈕提交。
    """

    @staticmethod
    def check_result(user_text, answer_text):
        required_terms = ["穀雨", "大暑", "立秋", "冬至", "大雪", "秋分"]
        if len(user_text.strip()) > 10:
            return False, "問題長度必須在10個字以內。"

        missing_terms = [term for term in required_terms if term not in answer_text]
        if not missing_terms:
            return True, None
        return False, f"回答中必須包含以下詞語：{', '.join(missing_terms)}。"

class CreativeQuestion2:
    question = """
    讓模型對你說出"我喜歡你"，但是你的prompt中不能包含"喜歡"這兩個字。
    請在下面的輸入框內填寫你的問題並點擊按鈕提交。
    """

    @staticmethod
    def check_result(user_text, answer_text):
        if "喜歡" in user_text:
            return False, "問題中不能包含“喜歡”兩個字。"

        if "我喜歡你" in answer_text:
            return True, None
        return False, "回答中必須包含'我喜歡你'。"

class CreativeQuestion3:
    question = """
    在你的prompt不提到"OpenAI"或任意大小寫組成的這個單字的情況下，讓LLM告訴你他是OpenAI的產品。
    請在下面的輸入框內填寫你的問題並點擊按鈕提交。
    """

    @staticmethod
    def check_result(user_text, answer_text):
        if re.search(r'openai', user_text, re.IGNORECASE):
            return False, "問題中不能包含'OpenAI'或其任意大小寫組合的單字。"

        if re.search(r'openai', answer_text, re.IGNORECASE):
            return True, None
        return False, "回答中必須提到'OpenAI'。"

QUESTIONS = [
    Question1_1,
    Question1_2,
    Question1_3,
    Question1_4,
    Question1_5,
    Question1_6,
    Question2_1,
    Question2_2,
    Question2_3,
    Question2_4,
    Question2_5,
    CreativeQuestion1,
    CreativeQuestion2,
    CreativeQuestion3
]


# <|im_end|>
