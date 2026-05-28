from __future__ import annotations

import csv
from io import StringIO


RAW_ELEMENTS = """atomic_number,symbol,name,atomic_mass,period,group,category,class_name
1,H,Hydrogene,1.008,1,1,nonmetal,non-metal
2,He,Helium,4.0026,1,18,noble-gas,gaz-noble
3,Li,Lithium,6.94,2,1,alkali-metal,metal-alcalin
4,Be,Beryllium,9.0122,2,2,alkaline-earth-metal,metal-alcalino-terreux
5,B,Bore,10.81,2,13,metalloid,metalloide
6,C,Carbone,12.011,2,14,nonmetal,non-metal
7,N,Azote,14.007,2,15,nonmetal,non-metal
8,O,Oxygene,15.999,2,16,nonmetal,non-metal
9,F,Fluor,18.998,2,17,halogen,halogene
10,Ne,Neon,20.18,2,18,noble-gas,gaz-noble
11,Na,Sodium,22.99,3,1,alkali-metal,metal-alcalin
12,Mg,Magnesium,24.305,3,2,alkaline-earth-metal,metal-alcalino-terreux
13,Al,Aluminium,26.982,3,13,post-transition-metal,metal-pauvre
14,Si,Silicium,28.085,3,14,metalloid,metalloide
15,P,Phosphore,30.974,3,15,nonmetal,non-metal
16,S,Soufre,32.06,3,16,nonmetal,non-metal
17,Cl,Chlore,35.45,3,17,halogen,halogene
18,Ar,Argon,39.948,3,18,noble-gas,gaz-noble
19,K,Potassium,39.098,4,1,alkali-metal,metal-alcalin
20,Ca,Calcium,40.078,4,2,alkaline-earth-metal,metal-alcalino-terreux
21,Sc,Scandium,44.956,4,3,transition-metal,metal-de-transition
22,Ti,Titane,47.867,4,4,transition-metal,metal-de-transition
23,V,Vanadium,50.942,4,5,transition-metal,metal-de-transition
24,Cr,Chrome,51.996,4,6,transition-metal,metal-lourd
25,Mn,Manganese,54.938,4,7,transition-metal,metal-lourd
26,Fe,Fer,55.845,4,8,transition-metal,metal-lourd
27,Co,Cobalt,58.933,4,9,transition-metal,metal-lourd
28,Ni,Nickel,58.693,4,10,transition-metal,metal-lourd
29,Cu,Cuivre,63.546,4,11,transition-metal,metal-lourd
30,Zn,Zinc,65.38,4,12,transition-metal,metal-lourd
31,Ga,Gallium,69.723,4,13,post-transition-metal,metal-pauvre
32,Ge,Germanium,72.63,4,14,metalloid,metalloide
33,As,Arsenic,74.922,4,15,metalloid,metalloide
34,Se,Selenium,78.971,4,16,nonmetal,non-metal
35,Br,Brome,79.904,4,17,halogen,halogene
36,Kr,Krypton,83.798,4,18,noble-gas,gaz-noble
37,Rb,Rubidium,85.468,5,1,alkali-metal,metal-alcalin
38,Sr,Strontium,87.62,5,2,alkaline-earth-metal,metal-alcalino-terreux
39,Y,Yttrium,88.906,5,3,transition-metal,metal-de-transition
40,Zr,Zirconium,91.224,5,4,transition-metal,metal-de-transition
41,Nb,Niobium,92.906,5,5,transition-metal,metal-lourd
42,Mo,Molybdene,95.95,5,6,transition-metal,metal-lourd
43,Tc,Technetium,98,5,7,transition-metal,metal-lourd
44,Ru,Ruthenium,101.07,5,8,transition-metal,metal-lourd
45,Rh,Rhodium,102.91,5,9,transition-metal,metal-lourd
46,Pd,Palladium,106.42,5,10,transition-metal,metal-lourd
47,Ag,Argent,107.87,5,11,transition-metal,metal-lourd
48,Cd,Cadmium,112.41,5,12,transition-metal,metal-lourd
49,In,Indium,114.82,5,13,post-transition-metal,metal-lourd
50,Sn,Etain,118.71,5,14,post-transition-metal,metal-lourd
51,Sb,Antimoine,121.76,5,15,metalloid,metalloide
52,Te,Tellure,127.6,5,16,metalloid,metalloide
53,I,Iode,126.9,5,17,halogen,halogene
54,Xe,Xenon,131.29,5,18,noble-gas,gaz-noble
55,Cs,Cesium,132.91,6,1,alkali-metal,metal-alcalin
56,Ba,Baryum,137.33,6,2,alkaline-earth-metal,metal-alcalino-terreux
57,La,Lanthane,138.91,6,3,lanthanide,lanthanide
58,Ce,Cerium,140.12,6,,lanthanide,lanthanide
59,Pr,Praseodyme,140.91,6,,lanthanide,lanthanide
60,Nd,Neodyme,144.24,6,,lanthanide,lanthanide
61,Pm,Promethium,145,6,,lanthanide,lanthanide
62,Sm,Samarium,150.36,6,,lanthanide,lanthanide
63,Eu,Europium,151.96,6,,lanthanide,lanthanide
64,Gd,Gadolinium,157.25,6,,lanthanide,lanthanide
65,Tb,Terbium,158.93,6,,lanthanide,lanthanide
66,Dy,Dysprosium,162.5,6,,lanthanide,lanthanide
67,Ho,Holmium,164.93,6,,lanthanide,lanthanide
68,Er,Erbium,167.26,6,,lanthanide,lanthanide
69,Tm,Thulium,168.93,6,,lanthanide,lanthanide
70,Yb,Ytterbium,173.05,6,,lanthanide,lanthanide
71,Lu,Lutecium,174.97,6,3,lanthanide,lanthanide
72,Hf,Hafnium,178.49,6,4,transition-metal,metal-lourd
73,Ta,Tantale,180.95,6,5,transition-metal,metal-lourd
74,W,Tungstene,183.84,6,6,transition-metal,metal-lourd
75,Re,Rhenium,186.21,6,7,transition-metal,metal-lourd
76,Os,Osmium,190.23,6,8,transition-metal,metal-lourd
77,Ir,Iridium,192.22,6,9,transition-metal,metal-lourd
78,Pt,Platine,195.08,6,10,transition-metal,metal-lourd
79,Au,Or,196.97,6,11,transition-metal,metal-lourd
80,Hg,Mercure,200.59,6,12,transition-metal,metal-lourd
81,Tl,Thallium,204.38,6,13,post-transition-metal,metal-lourd
82,Pb,Plomb,207.2,6,14,post-transition-metal,metal-lourd
83,Bi,Bismuth,208.98,6,15,post-transition-metal,metal-lourd
84,Po,Polonium,209,6,16,post-transition-metal,metal-lourd
85,At,Astate,210,6,17,halogen,halogene
86,Rn,Radon,222,6,18,noble-gas,gaz-noble
87,Fr,Francium,223,7,1,alkali-metal,metal-alcalin
88,Ra,Radium,226,7,2,alkaline-earth-metal,metal-alcalino-terreux
89,Ac,Actinium,227,7,3,actinide,actinide
90,Th,Thorium,232.04,7,,actinide,actinide
91,Pa,Protactinium,231.04,7,,actinide,actinide
92,U,Uranium,238.03,7,,actinide,actinide
93,Np,Neptunium,237,7,,actinide,actinide
94,Pu,Plutonium,244,7,,actinide,actinide
95,Am,Americium,243,7,,actinide,actinide
96,Cm,Curium,247,7,,actinide,actinide
97,Bk,Berkelium,247,7,,actinide,actinide
98,Cf,Californium,251,7,,actinide,actinide
99,Es,Einsteinium,252,7,,actinide,actinide
100,Fm,Fermium,257,7,,actinide,actinide
101,Md,Mendelevium,258,7,,actinide,actinide
102,No,Nobelium,259,7,,actinide,actinide
103,Lr,Lawrencium,266,7,3,actinide,actinide
104,Rf,Rutherfordium,267,7,4,transition-metal,metal-lourd
105,Db,Dubnium,268,7,5,transition-metal,metal-lourd
106,Sg,Seaborgium,269,7,6,transition-metal,metal-lourd
107,Bh,Bohrium,270,7,7,transition-metal,metal-lourd
108,Hs,Hassium,277,7,8,transition-metal,metal-lourd
109,Mt,Meitnerium,278,7,9,unknown,inconnue
110,Ds,Darmstadtium,281,7,10,unknown,inconnue
111,Rg,Roentgenium,282,7,11,unknown,inconnue
112,Cn,Copernicium,285,7,12,transition-metal,metal-lourd
113,Nh,Nihonium,286,7,13,unknown,inconnue
114,Fl,Flerovium,289,7,14,unknown,inconnue
115,Mc,Moscovium,290,7,15,unknown,inconnue
116,Lv,Livermorium,293,7,16,unknown,inconnue
117,Ts,Tennessine,294,7,17,unknown,inconnue
118,Og,Oganesson,294,7,18,unknown,inconnue
"""


CLASS_ALIASES = {
    "nonmetal": "non-metal",
    "non-metal": "non-metal",
    "gaz-noble": "gaz-noble",
    "noble-gas": "gaz-noble",
    "metal-alcalin": "metal-alcalin",
    "alkali-metal": "metal-alcalin",
    "metal-alcalino-terreux": "metal-alcalino-terreux",
    "alkaline-earth-metal": "metal-alcalino-terreux",
    "metalloide": "metalloide",
    "metalloid": "metalloide",
    "halogene": "halogene",
    "halogen": "halogene",
    "metal-de-transition": "metal-de-transition",
    "transition-metal": "metal-de-transition",
    "metal-lourd": "metal-lourd",
    "heavy-metal": "metal-lourd",
    "metal-pauvre": "metal-pauvre",
    "post-transition-metal": "metal-pauvre",
    "lanthanide": "lanthanide",
    "actinide": "actinide",
    "inconnue": "inconnue",
    "unknown": "inconnue",
}


def _optional_int(value: str) -> int | None:
    return int(value) if value else None


def load_elements() -> list[dict]:
    reader = csv.DictReader(StringIO(RAW_ELEMENTS))
    elements = []

    for row in reader:
        elements.append(
            {
                "atomicNumber": int(row["atomic_number"]),
                "symbol": row["symbol"],
                "name": row["name"],
                "atomicMass": float(row["atomic_mass"]),
                "period": int(row["period"]),
                "group": _optional_int(row["group"]),
                "category": row["category"],
                "class": row["class_name"],
            }
        )

    return elements


ELEMENTS = load_elements()
