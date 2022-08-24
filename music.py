from config import API_ID, API_HASH, BOT_TOKEN, BOT_NAME
from pyrogram import Client, filters, idle
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)

Music = Client(
    session_name=BOT_NAME,
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    plugins=dict(root='plugins')
)


PMTEXT = (
    "Assalomu aleykum Music Search botimizga xush kelibsiz\n"
    "__Men sizga istalgan qo`shig`ingizni topib bera olaman\n "
    "__Botdan tog`ri foydalanish uchun Yordam tugmasini bosing__"
    
)
PMKEYBOARD = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                'Yordam ❓', callback_data='help_callback'),
            InlineKeyboardButton('Haqida ❕', callback_data='about')
        ],
        [
            InlineKeyboardButton(
                'Meni guruhga qoshing 🎊', url='http://t.me/Search_mbot?startgroup=true')  
        ]
    ]
)
HELPTEXT = (
    '**Yordam:**\n\n,Agar qo`shiqni qidirmoqchi bo`lsangiz'
    ' Qo`yidagi buyruqni jo`natishingiz kerak.\n\n'
    '•`/song <q`shiq nomi>`\n\nAgar qoshiq matnini qidirmoqchi bo`lsangiz,'
    ' Qo`yidagi buyruqni jo`nating.\n\n•`/lyrics <qo`shiq nomi>`'
)
ABOUTTEXT = (
    "Assalomu aleykum Music Search bot ga xush kelibsiz\n"
    "Bot sizga izlagan qoshig`ingizni va qo`shiq matnini topib bera oladi:\n"
    "Buning uchun Yordam tugmasini bosib qanday qidirishni korib oling\n"
)


@Music.on_message(
    filters.command(['start', 'help'], ['/', '!'])
    & (filters.private | filters.group)
    & ~ filters.edited
)
async def start_cmd(_, msg: Message):
    ''' /start buyrug'iga javob (shaxsiy yoki guruh) '''

    if msg.chat.type == 'private':
        await msg.reply_sticker(sticker='CAACAgIAAx0CXeethQACBIthRB3WPePSpGljt548kGW3uJ0s3gACkAUAAtJaiAGaVzjS0OoLfh4E')
        await msg.reply(
            text=PMTEXT,
            reply_markup=PMKEYBOARD,
            disable_web_page_preview=True
        )
    else:
        await msg.reply(
            text='Hoy! Men onlaynman. Mendan qanday foydalanish haqida savolingiz bo`lsa, menga xabar bering.',
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text='Start :)',
                           
                            url=f't.me/search_mbot?start=help'
                        )
                    ]
                ]
            )
        )


@Music.on_callback_query()
async def callback_handling(_, query: CallbackQuery):
    ''' Qayta qo'ng'iroq so'rovlariga javob'''

    q_data = query.data
    q_id = query.id

    if q_data == 'menu_1':
        await Music.answer_callback_query(q_id, 'Menyu!')
        await query.message.edit(
            text=PMTEXT,
            reply_markup=PMKEYBOARD,
            disable_web_page_preview=True
        )

    elif q_data == 'help_callback':
        await Music.answer_callback_query(q_id, 'Yordam!')
        await query.message.edit(text=HELPTEXT,
                                 parse_mode='md',
                                 reply_markup=InlineKeyboardMarkup(
                                     [
                                         [
                                             InlineKeyboardButton(
                                                 text="Ortga",
                                                 callback_data='menu_1',
                                             )
                                         ]
                                     ]
                                 ),
                                 )

    elif q_data == 'about':
        await Music.answer_callback_query(q_id, text='Haqida!')
        await query.message.edit(
            text=ABOUTTEXT,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            'Ortga', callback_data='menu_1')
                    ]
                ]
            )
        )




Music.start()
print('Music bot ishga tushdi....')
idle()
print('Music bot toxtadi...')
Music.stop()
