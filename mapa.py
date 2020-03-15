# Graphics
import requests
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
from datetime import datetime

matplotlib.use('Agg')

URL_COUNTRIES = 'https://corona.lmao.ninja/countries/'


# TODO Usar escala LogNorm

def scale(casos):
    if casos < 100:
        return 0.2
    if casos < 200:
        return 0.3
    if casos < 400:
        return 0.4
    elif casos < 500:
        return 0.5
    elif casos < 1000:
        return 0.6
    elif casos < 5000:
        return 0.7
    elif casos < 10000:
        return 0.8
    elif casos < 15000:
        return 0.85
    else:
        return 0.9


def scale_muertes(muertes):
    if muertes == 0:
        return 0
    if muertes < 10:
        return 0.2
    if muertes < 20:
        return 0.3
    if muertes < 40:
        return 0.4
    elif muertes < 50:
        return 0.5
    elif muertes < 100:
        return 0.6
    elif muertes < 500:
        return 0.7
    elif muertes < 1000:
        return 0.8
    elif muertes < 1500:
        return 0.85
    else:
        return 0.9


def crear_imagen(criteria='cases', filename='mapa.png'):
    resp = requests.get(URL_COUNTRIES)
    paises = {}
    for item in resp.json():
        nombre = item['country']
        if criteria != 'cases':
            paises[nombre] = scale_muertes(item[criteria])
        else:
            paises[nombre] = scale(item[criteria])

    now = datetime.now().strftime("%d-%m-%y %I:%M%p")

    fig = plt.figure(figsize=(10, 5))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson())

    # make the map global rather than have it zoom in to
    # the extents of any plotted data
    ax.set_global()
    ax.set_title('Última actualización: %s' % now)

    # ax.stock_img()
    ax.add_feature(cfeature.BORDERS, linestyle='-')
    ax.add_feature(cfeature.COASTLINE, linestyle='-')
    ax.add_feature(cfeature.OCEAN, facecolor='white')

    shpfilename = shpreader.natural_earth(resolution='110m',
                                          category='cultural',
                                          name='admin_0_countries')

    cmap = cm.get_cmap('OrRd')

    reader = shpreader.Reader(shpfilename)
    countries = reader.records()
    for country in countries:
        nombre = country.attributes['ADMIN']
        nom2 = country.attributes['NAME_SV']
        if nombre in paises or nom2 in paises:
            if nombre in paises:
                color = cmap(paises[nombre])
            else:
                color = cmap(paises[nom2])

            ax.add_geometries(country.geometry, ccrs.PlateCarree(),
                              facecolor=color,
                              label=country.attributes['ADM0_A3'])

    plt.savefig(filename)
