import logging
import requests
from telegram import InlineQueryResultArticle, InputTextMessageContent
from uuid import uuid4

URL_ALL = 'https://corona.lmao.ninja/all'
URL_COUNTRIES = 'https://corona.lmao.ninja/countries/'

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)


def consulta(pais='Colombia'):
    resp = requests.get(URL_COUNTRIES)
    for item in resp.json():
        if item['country'] == pais:
            return item


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
    ]

    update.inline_query.answer(results)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)