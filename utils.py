import streamlit as st
import pandas as pd
import geopandas as gpd
import pydeck as pdk
import altair as alt
import folium as fo


# Constants definition

columns_rename = {'code_reg': 'Region Code',
                  'nom_reg': 'Region Name',
                  'code_dep': 'Department Code',
                  'nom_dep': 'Department Name',
                  'nom_com': 'Commune Name',
                  'code_insee': 'INSEE Code',
                  'nbr': 'Entity Number',
                  'inel_hd': 'Ineligible entity',
                  'elig_hd05': '> 0.5 Mbit/s',
                  'elig_hd3': '> 3 Mbit/s',
                  'elig_bhd8': '> 8 Mbit/s',
                  'elig_thd30': '> 30 Mbit/s',
                  'elig_thd100': '> 100 Mbit/s',
                  'elig_thd1g': '> 1 Gbit/s',
                  'elig_ftth': 'Fiber',
                  'elig_coax': 'Cable',
                  'elig_cu': 'DSL',
                  'elig_thdr': 'THD Radio',
                  'elig_4gf': 'Cellular',
                  'elig_hdr': 'HD Radio',
                  'elig_sat': 'Satellite',
                  'year': 'Year',
                  }

columns_description = {'Entity Number': 'Number of entity',
                       'Ineligible entity': 'Number of ineligible entity',
                       '> 0.5 Mbit/s': 'Number of entity eligible to internet speed > 0.5 Mbit/s',
                       '> 3 Mbit/s': 'Number of entity eligible to internet speed > 3 Mbit/s',
                       '> 8 Mbit/s': 'Number of entity eligible to internet speed > 8 Mbit/s',
                       '> 30 Mbit/s': 'Number of entity eligible to internet speed > 30 Mbit/s',
                       '> 100 Mbit/s': 'Number of entity eligible to internet speed > 100 Mbit/s',
                       '> 1 Gbit/s': 'Number of entity eligible to internet speed > 1 Gbit/s',
                       'Fiber': 'Number of entity eligible to fiber',
                       'Cable': 'Number of entity eligible to coaxial cable',
                       'DSL': 'Number of entity eligible to DSL',
                       'THD Radio': 'Number of entity eligible to THD Radio',
                       'Cellular': 'Number of entity eligible to 4G Fixe',
                       'HD Radio': 'Number of entity eligible to HD Radio',
                       'Satellite': 'Number of entity eligible to Satellite',
                       'Year': 'Year of the data',
                       }

techno_description = pd.DataFrame(
    [['Fiber', 2000, '300 Mbit/s', '10 Gbit/s'],
        ['Cable', 1995, '100 Mbit/s', '400 Mbit/s'],
        ['DSL', 1999, '1 Mbit/s', '30 Mbit/s'],
        ['THD Radio', 2008, '30 Mbit/s', '100 Mbit/s'],
        ['Cellular', 2015, '30 Mbit/s', '300 Mbit/s'],
        ['HD Radio', 2000, '0.5 Mbit/s', '30 Mbit/s'],
        ['Satellite', 2000, '2 Mbit/s', '10 Mbit/s']],
    columns=['Technology', 'Year of introduction',
             'Minimum debit', 'Maximum debit']



)

region_list = {
    '1': 'Guadeloupe',
    '2': 'Martinique',
    '3': 'Guyane',
    '4': 'La Réunion',
    '6': 'Mayotte',
    '11': 'Île-de-France',
    '24': 'Centre-Val de Loire',
    '27': 'Bourgogne-Franche-Comté',
    '28': 'Normandie',
    '32': 'Hauts-de-France',
    '44': 'Grand Est',
    '52': 'Pays de la Loire',
    '53': 'Bretagne',
    '75': 'Nouvelle-Aquitaine',
    '76': 'Occitanie',
    '84': 'Auvergne-Rhône-Alpes',
    '93': 'Provence-Alpes-Côte d\'Azur',
    '94': 'Corse'
}

department_list = {
    '01': 'Ain',
    '02': 'Aisne',
    '03': 'Allier',
    '04': 'Alpes-de-Haute-Provence',
    '05': 'Hautes-Alpes',
    '06': 'Alpes-Maritimes',
    '07': 'Ardèche',
    '08': 'Ardennes',
    '09': 'Ariège',
    '10': 'Aube',
    '11': 'Aude',
    '12': 'Aveyron',
    '13': 'Bouches-du-Rhône',
    '14': 'Calvados',
    '15': 'Cantal',
    '16': 'Charente',
    '17': 'Charente-Maritime',
    '18': 'Cher',
    '19': 'Corrèze',
    '21': 'Côte-d\'Or',
    '22': 'Côtes-d\'Armor',
    '23': 'Creuse',
    '24': 'Dordogne',
    '25': 'Doubs',
    '26': 'Drôme',
    '27': 'Eure',
    '28': 'Eure-et-Loir',
    '29': 'Finistère',
    '2A': 'Corse-du-Sud',
    '2B': 'Haute-Corse',
    '30': 'Gard',
    '31': 'Haute-Garonne',
    '32': 'Gers',
    '33': 'Gironde',
    '34': 'Hérault',
    '35': 'Ille-et-Vilaine',
    '36': 'Indre',
    '37': 'Indre-et-Loire',
    '38': 'Isère',
    '39': 'Jura',
    '40': 'Landes',
    '41': 'Loir-et-Cher',
    '42': 'Loire',
    '43': 'Haute-Loire',
    '44': 'Loire-Atlantique',
    '45': 'Loiret',
    '46': 'Lot',
    '47': 'Lot-et-Garonne',
    '48': 'Lozère',
    '49': 'Maine-et-Loire',
    '50': 'Manche',
    '51': 'Marne',
    '52': 'Haute-Marne',
    '53': 'Mayenne',
    '54': 'Meurthe-et-Moselle',
    '55': 'Meuse',
    '56': 'Morbihan',
    '57': 'Moselle',
    '58': 'Nièvre',
    '59': 'Nord',
    '60': 'Oise',
    '61': 'Orne',
    '62': 'Pas-de-Calais',
    '63': 'Puy-de-Dôme',
    '64': 'Pyrénées-Atlantiques',
    '65': 'Hautes-Pyrénées',
    '66': 'Pyrénées-Orientales',
    '67': 'Bas-Rhin',
    '68': 'Haut-Rhin',
    '69': 'Rhône',
    '70': 'Haute-Saône',
    '71': 'Saône-et-Loire',
    '72': 'Sarthe',
    '73': 'Savoie',
    '74': 'Haute-Savoie',
    '75': 'Paris',
    '76': 'Seine-Maritime',
    '77': 'Seine-et-Marne',
    '78': 'Yvelines',
    '79': 'Deux-Sèvres',
    '80': 'Somme',
    '81': 'Tarn',
    '82': 'Tarn-et-Garonne',
    '83': 'Var',
    '84': 'Vaucluse',
    '85': 'Vendée',
    '86': 'Vienne',
    '87': 'Haute-Vienne',
    '88': 'Vosges',
    '89': 'Yonne',
    '90': 'Territoire de Belfort',
    '91': 'Essonne',
    '92': 'Hauts-de-Seine',
    '93': 'Seine-Saint-Denis',
    '94': 'Val-de-Marne',
    '95': 'Val-d\'Oise',
    '971': 'Guadeloupe',
    '972': 'Martinique',
    '973': 'Guyane',
    '974': 'La Réunion',
    '976': 'Mayotte'
}

list_elig = [
    'Ineligible entity', '> 0.5 Mbit/s', '> 3 Mbit/s', '> 8 Mbit/s', '> 30 Mbit/s', '> 100 Mbit/s', '> 1 Gbit/s']

list_techno = [
    'Fiber', 'Cable', 'DSL', 'THD Radio', 'Cellular', 'HD Radio', 'Satellite']

elig_color = {'Ineligible entity': [100, 20, 0],
              '> 0.5 Mbit/s': [242, 45, 32],
              '> 3 Mbit/s': [232, 213, 0],
              '> 8 Mbit/s': [150, 200, 12],
              '> 30 Mbit/s': [20, 245, 12],
              '> 100 Mbit/s': [0, 123, 255],
              '> 1 Gbit/s': [0, 64, 242]}


techno_color = {'Fiber': [0, 64, 242],
                'Cable': [0, 123, 255],
                'DSL': [150, 255, 12],
                'THD Radio': [130, 150, 0],
                'Cellular': [242, 45, 32],
                'HD Radio': [142, 45, 32],
                'Satellite': [239, 107, 0]}

# Function definition


def color_to_hex(color: dict):
    return {k: f'#{v[0]:02x}{v[1]:02x}{v[2]:02x}' for k, v in color.items()}


def color_to_alt(color: dict):
    return alt.Scale(domain=list(color.keys()),
                     range=list(
                         map(lambda x: f'rgb({x[0]}, {x[1]}, {x[2]})', list(color.values())))
                     )


def update_elig(x):
    for i in range(len(list_elig)-1, 0, -1):
        for y in range(1, i):
            x[list_elig[y]] -= x[list_elig[i]]

    return x


def load_data_from_url(zone, times, files, merge_on):
    df = pd.DataFrame()
    for i, file in enumerate(files):
        df_new = pd.DataFrame()
        for time in times:
            df_new = pd.concat([df_new,
                                pd.read_csv(
                                    f"https://files.data.gouv.fr/arcep_donnees/fixe/maconnexioninternet/statistiques/{time}/{zone}/{file}",
                                    sep=';', header=0)], axis=0)
        if i == 0:
            df = df_new
        else:
            # Merge and drop the duplicate column
            df = df.merge(df_new, on=merge_on, suffixes=(
                '', ''))

    df['year'] = pd.to_datetime(
        df['date'], format='%Y-%m-%d').dt.year.astype(int)

    df.drop(['date', 'type'], axis=1, inplace=True)

    return df


def load_geo_from_url(geo_file, columns, simplify_tolerance):
    df = gpd.read_file(geo_file)[columns]
    df['geometry'] = df['geometry'].simplify(tolerance=simplify_tolerance)
    return df


@st.cache_data
def load_data_commune():

    zone = 'commune'
    files = ['commune_debit.csv', 'commune_techno.csv']
    times = ['2020_t3', '2021_t3', '2022_t3', 'last']
    geo_path = "https://osm13.openstreetmap.fr/~cquest/openfla/export/communes-20220101-shp.zip"

    debit = load_data_from_url(zone, times, files, [
        'code_insee', 'nom_com', 'nbr', 'type', 'date', 'code_dep', 'code_reg'])

    geometry = load_geo_from_url(geo_path, ['insee', 'geometry'], 0.001)

    debit = gpd.GeoDataFrame(debit.merge(
        geometry, left_on='code_insee', right_on='insee').drop('insee', axis=1))

    debit.rename(columns=columns_rename, inplace=True)

    debit = debit.apply(update_elig, axis=1)

    return debit


@st.cache_data
def load_data_region():

    zone = 'region'
    files = ['region_debit.csv', 'region_techno.csv']
    times = ['2020_t3', '2021_t3', '2022_t3', 'last']
    geo_path = "https://osm13.openstreetmap.fr/~cquest/openfla/export/regions-20180101-shp.zip"

    df = load_data_from_url(zone, times, files, [
                            'code_reg', 'nom_reg', 'nbr', 'type', 'date'])

    geometry = load_geo_from_url(geo_path, ['code_insee', 'geometry'], 0.05)

    geometry['code_insee'] = geometry['code_insee'].astype(int)

    df = gpd.GeoDataFrame(df.merge(
        geometry, left_on='code_reg', right_on='code_insee').drop('code_insee', axis=1))

    df.rename(columns=columns_rename, inplace=True)

    df = df.apply(update_elig, axis=1)

    return df


@st.cache_data
def load_data_departement():

    zone = 'departement'
    files = ['departement_debit.csv', 'departement_techno.csv']
    times = ['2020_t3', '2021_t3', '2022_t3', 'last']
    geo_path = "https://osm13.openstreetmap.fr/~cquest/openfla/export/departements-20180101-shp.zip"

    df = load_data_from_url(zone, times, files, [
                            'code_dep', 'nom_dep', 'nbr', 'type', 'date', 'code_reg'],)

    geometry = load_geo_from_url(geo_path, ['code_insee', 'geometry'], 0.01)

    df = gpd.GeoDataFrame(df.merge(
        geometry, left_on='code_dep', right_on='code_insee').drop('code_insee', axis=1))

    df.rename(columns=columns_rename, inplace=True)

    df = df.apply(update_elig, axis=1)

    return df


def compute_pdk_map(df, tech_color=None, elevation=10, elevation_scale=1, tooltip=None, latitude=None, longitude=None):
    layer = pdk.Layer(
        'GeoJsonLayer',
        df,
        get_polygon='geometry',
        stroked=True,
        filled=True,
        extruded=True,
        wireframe=True,
        pickable=True,
        auto_highlight=True,
        opacity=0.8,
        get_fill_color=tech_color if tech_color is not None else 'best_tech_color',
        get_elevation=elevation,
        elevation_scale=elevation_scale,
    )

    view_state = pdk.ViewState(
        latitude=latitude if latitude != None else df['geometry'].centroid.y.mean(
        ),
        longitude=longitude if longitude != None else df['geometry'].centroid.x.mean(
        ),
        zoom=1,
        min_zoom=5,
        max_zoom=15,
        pitch=40,
    )

    return pdk.Deck(layers=[layer],
                    initial_view_state=view_state, tooltip=tooltip)


def compute_pdk_column_map(df, columns, radius=100, elevation_scale=1, tooltip=None, latitude=None, longitude=None, zoom=1, color=None):

    df_sum = df.copy()
    df_sum[columns] = df[columns].cumsum(axis=1)
    layer = [
        pdk.Layer(
            'ColumnLayer',
            df_sum,
            get_position=['lon', 'lat'],
            radius=radius - i * radius * 0.05,
            get_elevation=col,
            elevation_scale=elevation_scale,
            pickable=True,
            auto_highlight=True,
            extruded=True,
            coverage=1,
            tooltip=tooltip,
            get_fill_color=color[col] if color is not None else [50, 50, 200]
        ) for i, col in enumerate(columns)
    ]

    view_state = pdk.ViewState(
        latitude=latitude if latitude != None else df['geometry'].centroid.y.mean(
        ),
        longitude=longitude if longitude != None else df['geometry'].centroid.x.mean(
        ),
        zoom=zoom,
        min_zoom=5,
        max_zoom=15,
        pitch=40,
    )

    legend = """
        <style>
            .dot {{
                height: 10px;
                width: 10px;
                border-radius: 50%;
                display: inline-block;
            }}
            {0}
        </style>
        {1}
    """.format(
        ' '.join([f'.{col.replace(" ", "_")} {{background-color: {color_to_hex(color)[col]};}}' for
                  col in columns]),
        ' '.join(
            [f'<span class="dot {col.replace(" ", "_")}"></span> {col} </br>' for col in columns])
    )

    return pdk.Deck(map_style='', layers=layer,
                    initial_view_state=view_state, tooltip=tooltip), legend


def compute_folium_map(df, key,  property, legend_name, bins=None, location=None, zoom_start=6):
    m = fo.Map(location=[df['geometry'].centroid.y.mean(), df['geometry'].centroid.x.mean(
    )] if location is None else location, zoom_start=zoom_start)

    fo.Choropleth(
        geo_data=df,
        data=df,
        columns=[key, property],
        key_on='feature.properties.' + key,
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name=legend_name,
        control=True,
        bins=bins,
    ).add_to(m)

    return m
