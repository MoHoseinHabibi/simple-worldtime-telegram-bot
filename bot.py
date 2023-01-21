import logging
from telegram import Update
from telegram.ext import ApplicationBuilder
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, filters
import config
from pytz import country_timezones, timezone
from datetime import datetime

country_code = {'افغانستان': 'AF', 'انتیاگو': 'AG', 'آرژانتين': 'AG', 'استرالیا': 'AU', 'بحرین': 'BH', 'بنگلادش': 'BD', 'بلژیک': 'BE', 'بولیوی': 'BO', 'برزیل': 'BR', 'بلغارستان': 'BG', 'بورکینا': 'BF', 'کامبوج': 'KH', 'کامرون': 'CM', 'کانادا': 'CA', 'افریقا': 'ZA', 'چاد': 'TD', 'شیلی': 'CL', 'چین': 'CN', 'کلمبیا': 'CO', 'کنگو': 'CG', 'کاستا': 'CR', 'کوبا': 'CU', 'دانمارک': 'DK', 'دومینیکن': 'DO', 'اکوادور': 'EC', 'گینه': 'GN', 'اتیوپی': 'ET', 'فیجی': 'FJ', 'فرانسه': 'FR', 'گابن': 'GA', 'گرجستان': 'GE', 'آلمان': 'DE', 'گواتمالا': 'GT', 'گینه بیسائو': 'GW', 'هندوراس': 'HN', 'ایسلند': 'IS', 'هند': 'IN', 'اندونزی': 'ID', 'ایران': 'IR', 'عراق': 'IQ', 'ایرلند': 'IE', 'اسرائیل': 'IL', 'ایتالیا': 'IT', 'جامائیکا': 'JM', 'ژاپن': 'JP', 'قزاقزستان': 'KZ', 'کنیا': 'KE', 'لائوس': 'LA', 'لبنان': 'LB', 'لیبری': 'LR', 'لیبی': 'LY', 'ماداگاسکار': 'MG', 'مالزی': 'MY', 'مالی': 'ML', 'مکزیک': 'MX', 'مولداوی': 'MD', 'موزامبیک': 'MZ', 'میانمار': 'MM', 'نامبیا': 'NA', 'نپال': 'NP', 'نیکاراگوئه': 'NE', 'نیجر': 'NE', 'نیجریه': 'NG', 'نروژ': 'NO', 'عمان': 'OM', 'پاکستان': 'PK', 'پالائو': 'PW', 'پاناما': 'PA', 'پاراگوئه': 'PY', 'پرو': 'PE', 'فلیپین': 'PH', 'لهستان': 'PL', 'پرتغال': 'PT', 'رومانی': 'RO', 'عربستان سعودی': 'SA', 'سنگال': 'SN', 'صربستان': 'RS', 'سیرالئون': 'SL', 'اسلو': 'SI', 'سومالی': 'SO', 'اسپانیا': 'ES', 'سریلانکا': 'LK', 'سوئد': 'SE', 'سوئیس سوییس': 'SZ', 'تانزانیا': 'TZ', 'تایلند': 'TH', 'ترکیه': 'TR', 'اکراین': 'UA', 'ایالات متحده عربی': 'AE', 'انگلستان': 'GB', 'امریکا': 'US', 'اروگوئه': 'UY', 'ازبکستان': 'UZ', 'ون': 'VU', 'ونزوئلا': 'VE', 'یمن': 'YE', 'زئیر': 'ZR'}

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    message = 'به ربات خوش آمدید.\n برای دریافت ساعت کشور ها میتوانید نام کشور مورد نظر را ارسال کنید. '
    await update.message.reply_text(message, quote=True)

def country_time(country_name: str) -> tuple[tuple[str, datetime]]:
    tzs = country_timezones[country_code[country_name]]
    result = tuple()
    for tz in tzs:
        result += ((tz, datetime.now().astimezone(timezone(tz))),)
    return result

async def search_timezone(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_chat_action('typing')
    timezones_time = country_time(update.message.text)
    message = f'ساعت کشور {update.message.text}\n'
    for i in timezones_time:
        message += f'{i[0]} : {i[1].strftime("%H:%M:%S")}\n'
    await update.message.reply_text(message, quote=True)

def main() -> None:
    application = ApplicationBuilder().token(config.TOKEN).build()

    application.add_handler(CommandHandler('start', start_command))
    application.add_handler(MessageHandler(filters.TEXT, search_timezone))
    application.run_polling()

if __name__ == '__main__':
    main()
