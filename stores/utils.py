# utils.py

def convert_amount_to_words(amount):
    if amount == 0:
        return "Zero"

    ones = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
    teens = ["", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
    tens = ["", "Ten", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
    thousands = ["", "Thousand", "Million", "Billion", "Trillion"]

    def convert_group_of_three(num):
        if num == 0:
            return ""
        elif num < 10:
            return ones[num] + " "
        elif 10 < num < 20:
            return teens[num - 10] + " "
        else:
            return tens[num // 10] + " " + ones[num % 10] + " "

    def convert_to_words_helper(num, place):
        if num == 0:
            return ""
        elif num < 10:
            return ones[num] + " "
        elif num < 100:
            return convert_group_of_three(num)
        else:
            return ones[num // 100] + " Hundred " + convert_group_of_three(num % 100)

    result = ""
    place = 0

    while amount > 0:
        current_group = amount % 1000
        if current_group != 0:
            result = convert_to_words_helper(current_group, place) + thousands[place] + " " + result
        amount //= 1000
        place += 1

    return result.strip()
