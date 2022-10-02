import os
import textwrap

from PIL import Image, ImageDraw, ImageFont

from django.conf import settings


MAIN_FONT = os.path.join(settings.BASE_DIR, 'users/fonts/main.ttf')

BIG_FONT = ImageFont.truetype(MAIN_FONT, size=20, encoding='UTF-8')
SMALL_FONT = ImageFont.truetype(MAIN_FONT, size=16, encoding='UTF-8')
VERY_SMALL_FONT = ImageFont.truetype(MAIN_FONT, size=12, encoding='UTF-8')


def draw_cv(photo, name, profession, experience, about, file_name):
    new_file_name = f'{file_name.split("/")[1][:-4]}.jpg'
    path_to_save = settings.MEDIA_ROOT + '/cvs/' + new_file_name

    cv = Image.new('RGB', (650, 250), color='white')
    photo = Image.open(photo)
    photo = photo.resize((250, 250))

    cv.paste(photo)
    cvdraw = ImageDraw.Draw(cv)

    about_text = textwrap.fill(f'Описание {about}', width=50)

    cvdraw.text((255, 20), text=name,
                font=BIG_FONT, align='center', fill='black'
                )
    cvdraw.text((255, 60), text=f'Профессия - {profession}',
                font=SMALL_FONT, fill='black'
                )
    cvdraw.text((255, 80), text=f'Опыт работы - {experience}',
                font=SMALL_FONT, fill='black'
                )
    cvdraw.text((255, 120), text=about_text,
                font=VERY_SMALL_FONT, fill='black'
                )
    cv.save(path_to_save)
    return path_to_save
