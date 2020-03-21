import sys, traceback

import cloudinary
import os
import logging
import requests
import telegram
from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineQueryResultPhoto
from uuid import uuid4
from mapa import crear_imagen
from datetime import datetime, timedelta

URL_ALL = 'https://corona.lmao.ninja/all'
URL_COUNTRIES = 'https://corona.lmao.ninja/countries/'

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def consulta(pais='Colombia'):
    return requests.get(URL_COUNTRIES + pais).json()


def total():
    resp = requests.get(URL_ALL)
    if resp.status_code != 200:
        return resp.status_code, '', ''

    cases = resp.json()['cases']
    deaths = resp.json()['deaths']
    recovered = resp.json()['recovered']
    return 'A nivel mundial, hasta el momento, se tienen las siguientes cifras:' \
           '\nCasos: {}.\nMuertos: {}.\nRecuperados: {}.'.format(cases, deaths, recovered)


def casos():
    return 'El total de casos de Coronavirus en Colombia es {}.'.format(consulta()['cases'])


def casos_hoy():
    return 'El total de casos de Coronavirus confirmados hoy en Colombia es {}.'.format(consulta()['todayCases'])


def recuperados():
    return 'El total de pacientes recuperados del Coronavirus en Colombia es {}.'.format(consulta()['recovered'])


def muertos():
    return 'El total de muertos por Coronavirus en Colombia es {}.'.format(consulta()['deaths'])


def start(update, context):
    update.message.reply_text(
        'Bienvenido a este bot que le brinda información sobre los casos de enfermos, '
        'muertos y recuperados de el Coronavirus en Colombia. :-)')


def mapa(update, context):
    chat_id = update.message.chat.id
    FILE = "mapa.jpg"
    # TODO verificar si el archivo existe
    fecha = os.path.getmtime(FILE)
    diff = datetime.fromtimestamp(fecha) - datetime.now()
    delta = timedelta(hours=120)
    if diff > delta:
        crear_imagen()

    context.bot.send_photo(chat_id, open(FILE, 'rb'))


def muertes(update, context):
    chat_id = update.message.chat.id
    FILE = "muertes.jpg"
    # TODO verificar si el archivo existe
    fecha = os.path.getmtime(FILE)
    diff = datetime.fromtimestamp(fecha) - datetime.now()
    delta = timedelta(minutes=10)
    if diff > delta:
        crear_imagen(criteria='deaths', filename=FILE)

    context.bot.send_photo(chat_id, open(FILE, 'rb'))


def url_from_name(filename):
    return cloudinary.api.resource(filename)['url']


def inline_query(update, context):

    results = [
        InlineQueryResultArticle(
            id=uuid4(),
            title="Mundo",
            thumb_url="https://upload.wikimedia.org/wikipedia/commons/thumb/e/ef/Erioll_world_2.svg/1024px-Erioll_world_2.svg.png",
            thumb_width="32",
            thumb_height="32",
            input_message_content=InputTextMessageContent(total())),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Casos",
            input_message_content=InputTextMessageContent(casos())),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Muertos",
            input_message_content=InputTextMessageContent(muertos())),
        InlineQueryResultArticle(
            id=uuid4(),
            title="Recuperados",
            input_message_content=InputTextMessageContent(recuperados())),
        InlineQueryResultPhoto(
            id=uuid4(),
            title="Mapa de Casos",
            caption="Mapa de Casos",
            description="Mapa de Casos",
            photo_url=url_from_name('mapa.jpg'),
            thumb_url='https://res.cloudinary.com/dlyc7rdxt/image/upload/ar_1:1,b_rgb:262c35,bo_5px_solid_rgb:ff0000,c_fill,g_auto,r_max,t_media_lib_thumb,w_100/v1584293147/coronavirus_w28z7e.jpg'),
        InlineQueryResultPhoto(
            id=uuid4(),
            title="Mapa de Muertes",
            caption="Mapa de Muertes",
            description="Mapa de Muertes",
            photo_url=url_from_name('muertes.jpg'),
            thumb_url='https://res.cloudinary.com/dlyc7rdxt/image/upload/ar_1:1,b_rgb:262c35,bo_5px_solid_rgb:ff0000,c_fill,g_auto,r_max,t_media_lib_thumb,w_100/v1584293147/coronavirus_w28z7e.jpg'),
    ]
    update.inline_query.answer(results)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)