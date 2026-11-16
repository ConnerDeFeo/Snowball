from enum import Enum

class FormType(Enum):
    TEN_K = "10-K"
    TEN_Q = "10-Q"
    PROXY = "DEF 14A"
    EIGHT_K = "8-K"
    FORM_4 = "4"
    SC_13D = "SC 13D"
    SCHEDULE_13D = "SCHEDULE 13D"


INSIDER_FORMS = [FormType.FORM_4, FormType.SC_13D, FormType.SCHEDULE_13D]
