def days_grammar(text):

    if (" "+text.strip())[-2] == '1': #TOFIX: А если text<10?
        return 'дней'
    else:
        return ['дней', 'день', 'дня', 'дня', 'дня', 'дней', 'дней', 'дней', 'дней', 'дней'][int(text.rstrip()[-1])]