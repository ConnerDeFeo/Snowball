from enum import Enum

from document_retrieval.FormType import FormType

type Section = TenQSection | TenKSection

class TenKSection(Enum):
    PART_I_ITEM_1 = "part_i_item_1"
    PART_I_ITEM_1A = "part_i_item_1a"
    PART_I_ITEM_1B = "part_i_item_1b"
    PART_I_ITEM_2 = "part_i_item_2"
    PART_I_ITEM_3 = "part_i_item_3"
    PART_I_ITEM_4 = "part_i_item_4"
    PART_II_ITEM_5 = "part_ii_item_5"
    PART_II_ITEM_6 = "part_ii_item_6"
    PART_II_ITEM_7 = "part_ii_item_7"
    PART_II_ITEM_7A = "part_ii_item_7a"
    PART_II_ITEM_8 = "part_ii_item_8"
    PART_II_ITEM_9 = "part_ii_item_9"
    PART_II_ITEM_9A = "part_ii_item_9a"
    PART_II_ITEM_9B = "part_ii_item_9b"
    PART_III_ITEM_10 = "part_iii_item_10"
    PART_III_ITEM_11 = "part_iii_item_11"
    PART_III_ITEM_12 = "part_iii_item_12"
    PART_III_ITEM_13 = "part_iii_item_13"
    PART_III_ITEM_14 = "part_iii_item_14"
    PART_IV_ITEM_15 = "part_iv_item_15"
    PART_IV_ITEM_16 = "part_iv_item_16"

class TenQSection(Enum):
    PART_I_ITEM_1 = "part_i_item_1"
    PART_I_ITEM_2 = "part_i_item_2"
    PART_I_ITEM_3 = "part_i_item_3"
    PART_I_ITEM_4 = "part_i_item_4"
    PART_II_ITEM_1 = "part_ii_item_1"
    PART_II_ITEM_1A = "part_ii_item_1a"
    PART_II_ITEM_2 = "part_ii_item_2"
    PART_II_ITEM_3 = "part_ii_item_3"
    PART_II_ITEM_4 = "part_ii_item_4"
    PART_II_ITEM_5 = "part_ii_item_5"
    PART_II_ITEM_6 = "part_ii_item_6"

# TenKSection/TenQSection share string values, so the form type decides which
# enum a given section string belongs to.
def section_from_form(form: str, section: str) -> Section:
    if form == FormType.TEN_K.value:
        return TenKSection(section)
    return TenQSection(section)

# Form-qualified key used as the rubric_directions DynamoDB table's location
# SK / META location string, e.g. "10-K#part_i_item_1". Disambiguates
# TenKSection/TenQSection, which otherwise share string values.
def section_location_key(section: Section) -> str:
    form = FormType.TEN_K.value if isinstance(section, TenKSection) else FormType.TEN_Q.value
    return f"{form}#{section.value}"

# Inverse of section_location_key.
def section_from_location_key(key: str) -> Section:
    form, section = key.split("#", 1)
    return section_from_form(form, section)
