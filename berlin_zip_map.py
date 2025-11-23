# Create a new file or add to district_tagger.py: berlin_zip_map.py

BERLIN_ZIP_MAP = {
    # Mitte
    "10115": "Mitte", "10117": "Mitte", "10119": "Mitte", "10178": "Mitte", "10179": "Mitte",
    "10551": "Tiergarten", "10553": "Tiergarten", "10555": "Tiergarten", "10557": "Tiergarten", "10559": "Tiergarten",
    "13347": "Wedding", "13349": "Wedding", "13351": "Wedding", "13353": "Wedding", "13355": "Wedding", "13357": "Wedding", "13359": "Wedding",
    "10551": "Moabit", # (Shared with Tiergarten, mapping to one is fine for filtering)
    
    # Friedrichshain-Kreuzberg
    "10243": "Friedrichshain", "10245": "Friedrichshain", "10247": "Friedrichshain", "10249": "Friedrichshain",
    "10961": "Kreuzberg", "10963": "Kreuzberg", "10965": "Kreuzberg", "10967": "Kreuzberg", "10969": "Kreuzberg", "10997": "Kreuzberg", "10999": "Kreuzberg",
    
    # Pankow
    "10405": "Prenzlauer Berg", "10407": "Prenzlauer Berg", "10409": "Prenzlauer Berg", "10435": "Prenzlauer Berg", "10437": "Prenzlauer Berg", "10439": "Prenzlauer Berg",
    "13086": "Weissensee", "13088": "Weissensee", "13089": "Weissensee",
    "13187": "Pankow", "13189": "Pankow",
    
    # Charlottenburg-Wilmersdorf
    "10585": "Charlottenburg", "10587": "Charlottenburg", "10589": "Charlottenburg", "10623": "Charlottenburg", "10625": "Charlottenburg", "10627": "Charlottenburg", "10629": "Charlottenburg",
    "10707": "Wilmersdorf", "10709": "Wilmersdorf", "10711": "Wilmersdorf", "10713": "Wilmersdorf", "10715": "Wilmersdorf", "10717": "Wilmersdorf", "10719": "Wilmersdorf",
    "10707": "Halensee", "14193": "Grunewald", "14055": "Westend",

    # Spandau
    "13581": "Spandau", "13583": "Spandau", "13585": "Spandau", "13587": "Spandau", "13589": "Spandau", "13591": "Staaken", "13593": "Staaken", "13595": "Spandau", "13597": "Spandau", "13599": "Haselhorst", "14089": "Kladow",

    # Steglitz-Zehlendorf
    "12157": "Steglitz", "12161": "Steglitz", "12163": "Steglitz", "12165": "Steglitz", "12167": "Steglitz", "12169": "Steglitz",
    "12203": "Lichterfelde", "12205": "Lichterfelde", "12207": "Lichterfelde", "12209": "Lichterfelde",
    "14109": "Wannsee", "14129": "Nikolassee", "14163": "Zehlendorf", "14165": "Zehlendorf", "14167": "Zehlendorf", "14169": "Zehlendorf", "14195": "Dahlem",

    # Tempelhof-Schöneberg
    "10777": "Schöneberg", "10779": "Schöneberg", "10781": "Schöneberg", "10783": "Schöneberg", "10785": "Schöneberg", "10787": "Schöneberg", "10789": "Schöneberg", "10823": "Schöneberg", "10825": "Schöneberg", "10827": "Schöneberg", "10829": "Schöneberg",
    "12159": "Friedenau", "12161": "Friedenau",
    "12099": "Tempelhof", "12101": "Tempelhof", "12103": "Tempelhof", "12105": "Tempelhof", "12107": "Tempelhof", "12109": "Mariendorf",
    "12305": "Lichtenrade", "12307": "Lichtenrade", "12309": "Lichtenrade", 
    "12277": "Marienfelde", "12279": "Marienfelde",

    # Neukölln
    "12043": "Neukölln", "12045": "Neukölln", "12047": "Neukölln", "12049": "Neukölln", "12051": "Neukölln", "12053": "Neukölln", "12055": "Neukölln", "12057": "Neukölln", "12059": "Neukölln",
    "12347": "Britz", "12349": "Britz", "12351": "Buckow", "12353": "Buckow", "12355": "Rudow", "12357": "Rudow", "12359": "Britz",

    # Treptow-Köpenick
    "12435": "Alt-Treptow", "12437": "Plänterwald", "12439": "Niederschöneweide", 
    "12459": "Oberschöneweide", "12487": "Johannisthal", "12489": "Adlershof",
    "12524": "Altglienicke", "12526": "Bohnsdorf", "12527": "Grünau", "12555": "Köpenick", "12557": "Köpenick", "12559": "Müggelheim", "12587": "Friedrichshagen", "12589": "Rahnsdorf",
    
    # Marzahn-Hellersdorf
    "12619": "Kaulsdorf", "12621": "Kaulsdorf", "12623": "Mahlsdorf", "12627": "Hellersdorf", "12629": "Hellersdorf", "12679": "Marzahn", "12681": "Marzahn", "12683": "Biesdorf", "12685": "Marzahn", "12687": "Marzahn", "12689": "Marzahn",

    # Lichtenberg
    "10315": "Friedrichsfelde", "10317": "Lichtenberg", "10318": "Karlshorst", "10319": "Friedrichsfelde", "10365": "Lichtenberg", "10367": "Lichtenberg", "10369": "Fennpfuhl",
    "13051": "Malchow", "13053": "Neu-Hohenschönhausen", "13055": "Alt-Hohenschönhausen", "13057": "Falkenberg", "13059": "Wartenberg",

    # Reinickendorf
    "13403": "Reinickendorf", "13405": "Reinickendorf", "13407": "Reinickendorf", "13409": "Reinickendorf", 
    "13435": "Märkisches Viertel", "13437": "Wittenau", "13439": "Märkisches Viertel", 
    "13465": "Frohnau", "13467": "Hermsdorf", "13469": "Waidmannslust", 
    "13503": "Heiligensee", "13505": "Konradshöhe", "13507": "Tegel", "13509": "Tegel",

    # Additional ZIP codes can be added here as needed
    "13629": "Siemensstadt"
}