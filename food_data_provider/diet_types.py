from enum import Enum


class DietType(Enum):
    GLUTEN_FREE = "glutenfree"
    KETOGENIC = "ketogenic"
    LACTO_VEGETARIAN = "lactovegetarian"
    OVO_VEGETARIAN = "ovovegetarian"
    VEGAN = "vegan"
    PESCETARIAN = "pescetarian"
    PALEO = "paleo"
    PRIMAL = "primal"
    LOW_FODMAP = "lowfodmap"
    WHOLE30 = "whole30"