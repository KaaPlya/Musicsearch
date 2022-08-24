import os
from funcs.download import Descargar
from pyrogram import Client as Music, filters
from pyrogram.types import Message
from pyrogram.errors.exceptions import MessageNotModified
from youtubesearchpython import VideosSearch


text = (
    '__Siz qidirgan qo`shiq biyicha xech narsa topilmadi.'
    ' Iltimos qo`shiqni nomini qaytadan tog`ri yozing.__'
    '\n\nSintaksis: ```/song <qo`shiq nomi>```'
)

descargar = Descargar('downloads/')

@Music.on_message(
    filters.command(['song'],prefixes=['/', '!'])
    & (filters.group | filters.private)
    & ~ filters.edited)
async def song_dl(_, msg: Message):

    if len(msg.command) == 1:
        return await msg.reply(text=text, parse_mode='md')

    r_text = await msg.reply('Qidirilmoqda...')
    url = msg.text.split(None, 1)[1]
    url = extract_the_url(url=url)
    
    if url == 0:return await r_text.edit('Bu qo`shiqni topa olmadim. Boshqa  so`zlar bilan harakat qilib ko`ring...')

    await r_text.edit('Yuklab olinmoqda...')

    ytinfo = descargar.get_song(url)

    if ytinfo == 0:
        await r_text.edit(f'Nimadir xatolik yuz berdi\n\nQaytadan urunib koring... :(')
        return

    try:
        await r_text.edit_text('Yuklanmoqda...')
    except MessageNotModified:
        pass

    await msg.reply_audio(
            audio=f'downloads/{ytinfo.title.replace("/","|")}-{ytinfo.video_id}.mp3', 
            duration=int(ytinfo.length),
            performer=str(ytinfo.author),
            title=f'{str(ytinfo.title)}',
            caption=f"<a href='{url}'>__{ytinfo.title}__</a>\n\n__@Search_mbot__ orqali yuklab olindi"
        )

    await r_text.delete()
    os.remove(f'downloads/{ytinfo.title.replace("/","|")}-{ytinfo.video_id}.mp3')



def extract_the_url(url: str):
    '''youtube URL manzili chiqarilmoqda'''

    v = VideosSearch(url, limit=1)
    v_result = v.result()

    if not v_result['result']:
        return 0
    url = v_result['result'][0]['link']
    return url
