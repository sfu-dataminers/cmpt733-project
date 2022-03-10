import pandas as pd


if __name__ == '__main__':
    list = [
        'Aeromexico',
        'AirAsia',
        'AirArabia',
        'AirChina',
        'AirCanada',
        'AirFrance',
        'AirComplaints',
        'AirFrance',
        'AirlineDispute',
        'AirMauritius',
        'AirTransat',
        'AlaskaAir',
        'AllegiantAir',
        'AmericanAir',
        'AustrianAirlines',
        'Avianca',
        'CathayPacific',
        'CathayPacificAirways',
        'Citilink',
        'Delta',
        'EnvoyAir',
        'Etihad',
        'evaair',
        'Finnair',
        'FlyAirNZ',
        'FlyFrontier',
        'FronterAirlines',
        'GarudaIndonesia',
        'HawaiianAirlines',
        'IndiGo',
        'JapanAirlines',
        'JetBlue',
        'KLM',
        'KuwaitAirways',
        'LATAMAirlines',
        'Lufthansa',
        'Qantas',
        'QatarAirways',
        'PhilippineAirlines',
        'RoyalAirMaroc',
        'Saudia',
        'SingaporeAir',
        'Southwestair',
        'SpiceJet',
        'SpritAirlines',
        'RoyalAirMaroc_',
        'SouthwestAir',
        'TurkishAirlines',
        'UnitedAirlines',
        'VriginAtlantic',
        'VriginAustralia',
        'Vistara',
        'WestJet',
        ]

    list = [i.lower() for i in list]
    df = pd.read_csv('data/clean_data.csv')
    df['username'] = df['username'].str.lower()
    bool_val = ~df.username.isin(list)
    df = df[bool_val]
    df.to_csv('data/filtered_data.csv')
