# Graphics
from auth import API_KEY, API_SECRET, CLOUD_NAME
from config import URL_COUNTRIES
import requests
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm, colors
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
from datetime import datetime
import cloudinary
from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

cloudinary.config(
    cloud_name=CLOUD_NAME,
    api_key=API_KEY,
    api_secret=API_SECRET
)

matplotlib.use('Agg')

# COUNTRIES WITH NO ISO INFO IN THE API
EXCEPTIONS = {
    'S. Korea': 'KOR',
    'UK': 'GBR',
    'Iran': 'IRN',
    'Czechia': 'CZE',
    'UAE': 'ARE',
    'North Macedonia': 'MKD',
    'Moldova': 'MDA',
    'Palestine': 'PSE',
    'DRC': 'COD',
    'Tanzania': 'TZA',
    'Eswatini': 'SWZ',
    'Cabo Verde': 'CAF',
    'Syria': 'SYR',
    'USA': 'USA'
}


def get_data(criteria):
    resp = requests.get(URL_COUNTRIES)
    paises = {}
    maxima = 0
    for item in resp.json():
        nombre = item['countryInfo']['iso3']
        # countries with no iso data
        if nombre == 'NO DATA' and item['country'] in EXCEPTIONS:
            nombre = EXCEPTIONS[item['country']]

        paises[nombre] = item[criteria]
        # update max number as of the criteria
        if paises[nombre] > maxima:
            maxima = paises[nombre]

    return paises, maxima


def crear_imagen(criteria='cases', filename='mapa.jpg'):
    paises, maxima = get_data(criteria)
    # LogNorm for normalizing values
    norm = colors.LogNorm(1, maxima)
    now = datetime.now().strftime("%d-%m-%y %I:%M%p")
    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())

    # make the map global rather than have it zoom in to
    # the extents of any plotted data
    ax.set_global()
    ax.set_title('Última actualización: %s' % now)

    ax.add_feature(cfeature.BORDERS, linestyle='-')
    ax.add_feature(cfeature.COASTLINE, linestyle='-')
    ax.add_feature(cfeature.OCEAN, facecolor='white')

    # colormap
    cmap = cm.get_cmap('OrRd')
    # get countries info
    shpfilename = shpreader.natural_earth(resolution='110m',
                                          category='cultural',
                                          name='admin_0_countries')

    # plot countries
    reader = shpreader.Reader(shpfilename)
    countries = reader.records()
    for country in countries:
        nombre = country.attributes['ISO_A3']
        if nombre in paises:
            # decide color based in the number of the criteria
            color = cmap(norm(paises[nombre]))
            ax.add_geometries(country.geometry, ccrs.PlateCarree(),
                              facecolor=color,
                              label=country.attributes['ADM0_A3'])

    plt.savefig(filename)
    cloudinary.uploader.upload(file=open(filename, 'rb'), public_id=filename, overwrite=True)
    print(cloudinary.api.resource(filename)['url'])
