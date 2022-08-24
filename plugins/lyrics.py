import os
from config import GENIUS_API
from pyrogram import Client as Music,filters
from pyrogram.types import Message
from lyricsgenius import genius
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong


api = genius.Genius(GENIUS_API,verbose=False)


@Music.on_message(filters.command(['lyrics','lyric'],prefixes=['/','!']) 
    & (filters.group | filters.private) 
    & ~ filters.edited)
async def lyrics(music:Music,msg: Message):

    if len(msg.command) == 1:
        return await msg.reply(
            text='__Iltimos, so`rovni to`gri kiriting...__', 
        )

    r_text = await msg.reply('__Qidirilmoqda...__')
    song_name = msg.text.split(None, 1)[1]

    lyric = api.search_song(song_name)

    if lyric is None:return await r_text.edit('__Siz izlagan qo`shiq matni bo`yicha xech narsa topilmadi...__')

    lyric_title = lyric.title
    lyric_artist = lyric.artist
    lyrics_text = lyric.lyrics

    try:
        await r_text.edit_text(f'__--**{lyric_title}**--__\n__{lyric_artist}\n__\n\n__{lyrics_text}__\n@Search_mbot orqali topildi')

    except MessageTooLong:
        with open(f'downloads/{lyric_title}.txt','w') as f:
            f.write(f'{lyric_title}\n{lyric_artist}\n\n\n{lyrics_text}')

        await r_text.edit_text('__Qo`shiq matni juda uzun. Matn fayli sifatida yuborildi...__')
        await msg.reply_chat_action(
            action='upload_document'
        )
        await msg.reply_document(
            document=f'downloads/{lyric_title}.txt',
            caption=f'\n__--{lyric_title}--__\n__{lyric_artist}__\n\n__@Search_mbot orqali topildi__'
        )

        await r_text.delete()
        
        
        os.remove(f'downloads/{lyric_title}.txt')
