class Region:
    def __init__(self, name: str, code: str, upper_left: tuple[int, int], size: tuple[int, int]):
        self.name = name
        self.code = code
        self.upper_left = upper_left
        self.size = size
        self.lower_right = (self.upper_left[0] + self.size[0], self.upper_left[1] + self.size[1])
    
Region.ALASKA = Region("Alaska", "AL", (10, 10), (20, 10))
Region.NORTH_WEST_TERRITORIES = Region("North West Territories", "NW", (10, 20), (10, 50))
Region.GREENLAND = Region("Greenland", "GR", (10, 90), (30, 20))
Region.ALBERTA = Region("Alberta", "AB", (20, 20), (20, 20))
Region.ONTARIO = Region("Ontario", "ON", (20, 40), (20, 20))
Region.QUEBEC = Region("Quebec", "QB", (30, 60), (10, 20))
Region.WESTERN_UNITED_STATES = Region("Western United States", "WU", (40, 30), (20, 20))
Region.EASTERN_UNITED_STATES = Region("Eastern United States", "EU", (40, 50), (30, 20))
Region.CENTRAL_AMERICA = Region("Central America", "CA", (60, 40), (20, 10))

Region.ICELAND = Region("Iceland", "IC", (10, 120), (10, 10))
Region.SCANDANAVIA = Region("Scandanavia", "SC", (10, 150), (30, 10))
Region.UKRAINE = Region("Ukraine", "UK", (20, 160), (50, 30))
Region.GREAT_BRITIAN = Region("Great Britian", "GB", (30, 120), (10, 20))
Region.NORTHEN_EUROPE = Region("Northen Europe", "NE", (50, 130), (10, 30))
Region.SOUTHERN_EUROPE = Region("Southern Europe", "SE", (60, 130), (20, 30))
Region.WESTERN_EUROPE = Region("Western Europe", "WE", (50, 120), (40, 10))

Region.URAL = Region("Ural", "UR", (20, 190), (40, 10))
Region.SIBERIA = Region("Siberia", "SB", (10, 200), (40, 20))
Region.YAKUTSA = Region("Yakutsa", "YK", (10, 220), (10, 20))
Region.KAMICHATKA = Region("Kamichatka", "KA", (10, 240), (20, 30))
Region.JAPAN = Region("Japan", "JA", (40, 260), (20, 10))
Region.MIDDLE_EAST = Region("Middle East", "ME", (70, 160), (20, 30))
Region.AFGANISTAN = Region("Afganistan", "AF", (60, 190), (20, 10))
Region.CHINA = Region("China", "CN", (50, 200), (30, 40))
Region.MONGOLIA = Region("Mongolia", "MG", (30, 220), (20, 30))
Region.IRKUTSK = Region("Irkutsk", "IR", (20, 220), (10, 20))
Region.INDIA = Region("India", "ID", (80, 190), (30, 20))
Region.SIAM = Region("Siam", "SM", (80, 210), (10, 20))

Region.NORTH_AFRICA = Region("North Africa", "NF", (90, 110), (20, 40))
Region.EGYPT = Region("Egypt", "EG", (90, 150), (10, 20))
Region.EAST_AFRICA = Region("East Africa", "EF", (100, 150), (30, 30))
Region.MADAGASCAR = Region("Madagascar", "MD", (150, 170), (20, 10))
Region.SOUTH_AFRICA = Region("South Africa", "SF", (130, 140), (40, 20))
Region.CONGO = Region("Congo", "CO", (110, 130), (20, 20))

Region.VENEZUELA = Region("Venezuela", "VN", (80, 40), (10, 40))
Region.BRAZIL = Region("Brazil", "BR", (90, 50), (30, 40))
Region.ARGENTINA = Region("Argentina", "AG", (110, 50), (40, 20))
Region.PERU = Region("Peru", "PR", (90, 40), (40, 10))

Region.INDONESIA = Region("Indonesia", "IN", (110, 220), (10, 10))
Region.NEW_GUINEA = Region("New Guinea", "NG", (110, 240), (10, 20))
Region.EASTERN_AUSTRALIA = Region("Eastern Australia", "EA", (130, 250), (30, 20)) # Sports, it's in the game
Region.WESTERN_AUSTRALIA = Region("Western Australia", "WA", (130, 220), (20, 30))

Region.WATER_AL = Region(None, None, (10, 0), (10, 10))
Region.WATER_NW_GR = Region(None, None, (10, 70), (10, 20))
Region.WATER_GR_IC = Region(None, None, (10, 110), (10, 10))
Region.WATER_ON_GR = Region(None, None, (20, 60), (10, 30))
Region.WATER_QB_GR = Region(None, None, (30, 80), (10, 10))
Region.WATER_IC_SC = Region(None, None, (), ())
Region.WATER_IC_GB = Region(None, None, (), ())
Region.WATER_GB_SC = Region(None, None, (), ())
Region.WATER_GB_WE = Region(None, None, (), ())
Region.WATER_GB_NE = Region(None, None, (), ())
Region.WATER_SC_NE = Region(None, None, (), ())
Region.WATER_BR_NF = Region(None, None, (), ())
Region.WATER_SE_NF = Region(None, None, (), ())
Region.WATER_SE_EG = Region(None, None, (), ())
Region.WATER_ME_EF = Region(None, None, (), ())
Region.WATER_EF_MD = Region(None, None, (), ())
Region.WATER_SF_MD = Region(None, None, (), ())
Region.WATER_KA_JA = Region(None, None, (), ())
Region.WATER_MG_JA = Region(None, None, (), ())
Region.WATER_SM_IN = Region(None, None, (), ())
Region.WATER_IN_NG = Region(None, None, (), ())
Region.WATER_IN_WA = Region(None, None, (), ())
Region.WATER_NG_WA = Region(None, None, (), ())
Region.WATER_NG_EA = Region(None, None, (), ())
Region.WATER_KA = Region(None, None, (), (10, 10))

water_routes = [
    Region.WATER_AL,
    Region.WATER_NW_GR,
    Region.WATER_GR_IC,
    Region.WATER_ON_GR,
    Region.WATER_QB_GR,
    Region.WATER_IC_SC,
    Region.WATER_IC_GB,
    Region.WATER_GB_SC,
    Region.WATER_GB_WE,
    Region.WATER_GB_NE,
    Region.WATER_SC_NE,
    Region.WATER_BR_NF,
    Region.WATER_SE_NF,
    Region.WATER_SE_EG,
    Region.WATER_ME_EF,
    Region.WATER_EF_MD,
    Region.WATER_SF_MD,
    Region.WATER_KA_JA,
    Region.WATER_MG_JA,
    Region.WATER_SM_IN,
    Region.WATER_IN_NG,
    Region.WATER_IN_WA,
    Region.WATER_NG_WA,
    Region.WATER_NG_EA,
    Region.WATER_KA,
]

map: dict[Region, list[Region]] = {
    Region.ALASKA: [ Region.NORTH_WEST_TERRITORIES, Region.ALBERTA, Region.KAMICHATKA ],
    Region.NORTH_WEST_TERRITORIES: [ Region.GREENLAND, Region.ONTARIO, Region.ALBERTA, Region.ALASKA ],
    Region.GREENLAND: [ Region.ICELAND, Region.QUEBEC, Region.ONTARIO ]
}

continents = {

}