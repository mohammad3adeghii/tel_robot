import telebot
import cv2 as cv
import os
from rembg import remove
from fpdf import FPDF
from pytube import YouTube
from MukeshAPI import api
import random
from flask import Flask

app = Flask(__name__)

API_TOKEN = "7502187198:AAFqt-hOzuVH4mIxdc5_DDeLRPf6wrHA7X0"
bot = telebot.TeleBot(API_TOKEN)
pdf = FPDF()
# Start Sections

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "سلام! من خودآگاه هستم، یک ربات هوش مصنوعی همه‌کاره که می‌توانم به شما در انجام انواع کارها کمک کنم. از حذف نویز عکس، ترجمه‌ی متن، حذف بکگراند،تبدیل متن به عکس! هر سوالی دارید یا هر کمکی می‌خواهید، کافی است به من پیام دهید. آماده‌ام تا در هر زمان و هر مکان به شما کمک کنم! 🌟برای شروع، فقط بگویید چه کاری از من می‌خواهید. ")

# End Section
# Start Help Sections
@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, "برای استفاده از امکانات ربات دستورات زیر را بفرستید.\n start - شروع ربات\nhelp - راهنمای استفاده از ربات\ncontact_us - ارتباط با ما\nreduce_noise - حذف نویز عکس\nremove_bg - حذف بکگراند\ntext2pdf - تبدیل متن به pdf\nimage2text - تبدیل عکس به متن\ndownload_youtube - دانلود ویدیو از یوتیوب\ndirect_auto_insta - دایرکت خودکار اینستاگرام\ndownload_insta_post - دانلود پست اینستاگرام\nimage_generator - تولید تصاویر\nvirtual_glass_and_clouth — عینک و پیراهن مجازی\nsms_bomber - اس ام اس بمبر\nface_swap - تغییر چهره")

# Start Contact-us Section
@bot.message_handler(commands=['contact_us'])
def contact_us_handler(message):
    bot.reply_to(message, "برای ارتباط با پشتیبان ربات با آیدی زیر در ارتباط باشید@sadeghi_code")

# Start Reduce Noise
@bot.message_handler(commands=['reduce_noise'])
def redce_noise(message):
    bot.reply_to(message, "لطفا یک عکس را بفرستید تا بدون نویز برات ارسال بشه")
    bot.register_next_step_handler(message=message, callback=reduce)

def enhance(image_path):
    image = cv.imread(image_path)

    reduce_noise = cv.bilateralFilter(image, 9, 75, 75)

    output_path = "dnoise.jpg"
    cv.imwrite(output_path, reduce_noise)

    return output_path
def reduce(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with open("after_denoise.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.send_message(message.chat.id, "عکس در حال حذف نویز می باشد. لطفا کمی صبر کنید")
    processed_image_path = enhance("after_denoise.jpg")
    
    file_size = os.path.getsize(processed_image_path)
    file_size_kb = file_size / 1024

    bot.send_message(message.chat.id, "نویز عکس با موفقیت حذف شد\nعکس درحال ارسال به تلگرام می باشد")
    with open(processed_image_path, 'rb') as photo:
        bot.send_photo(message.chat.id, photo, f"size: {file_size_kb} KB")
    bot.send_message(message.chat.id, "عکس بدون نویز آپلود شد!")

# Start Removebg section
@bot.message_handler(commands=['remove_bg'])
def removes(message):
    bot.reply_to(message, "لطفا یک عکس را بفرستید تا بدون پس زمینش برات ارسال بشه")
    bot.register_next_step_handler(message=message, callback=removebg)

def removebg(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    with open("remove_background.png", 'wb') as new_file:
        new_file.write(downloaded_file)

    bot.send_message(message.chat.id, "عکس در حال حذف پس زمینه می باشد. لطفا کمی صبر کنید")

    # Remove background
    with open("remove_background.png", "rb") as input_file:
        output = remove(input_file.read())
    
    processed_image_path = "removedbg.png"
    with open(processed_image_path, "wb") as output_file:
        output_file.write(output)
    
    file_size = os.path.getsize(processed_image_path)
    file_size_kb = file_size / 1024

    bot.send_message(message.chat.id, "پس زمینه عکس با موفقیت حذف شد\nعکس درحال ارسال به تلگرام می باشد")
    with open(processed_image_path, 'rb') as photo:
        bot.send_document(message.chat.id, photo, f"size: {file_size_kb} KB")
    bot.send_message(message.chat.id, "عکس بدون پس زمینه آپلود شد!")

# Start text2pdf section
@bot.message_handler(commands=['text2pdf'])
def pdfs1(message):
    bot.reply_to(message, "لطفا یک متن را بفرستید تا پی دی افش برات ارسال بشه")
    bot.register_next_step_handler(message=message, callback=text2pdf)

def text2pdf(message):
    text = message.text
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    bot.send_message(message.chat.id, "متن درحال تبدیل است. لطفا کمی صبر کنید")
    
    pdf.multi_cell(0, 10, text)
    file_names = "out.pdf"
    pdf.output(file_names)

    bot.send_message(message.chat.id, "متن با موفقیت به pdf تبدیل شد")
    with open(file_names, 'rb') as pdfs:
        bot.send_document(message.chat.id, pdfs)
    bot.send_message(message.chat.id, "فایل pdf تو تلگرام آپلود شد")


# Start text2pdf section
@bot.message_handler(commands=['download_youtube'])
def yt_download(message):
    bot.reply_to(message, "برای دانلود ویدیو از یوتیوب لینک ویدیو را وارد نمایید")
    bot.register_next_step_handler(message=message, callback=youtube)

def get_video(video_path, chatID):
    try:
        yt = YouTube(video_path)
        bot.send_message(chatID, f"Title: {yt.title}")

        stream = yt.streams.get_highest_resolution()
        
        bot.send_message(chatID, "ویدیوی یوتیوب در صف دانلود قرار گرفته است لطفا کمی صبر کنید")

    
        stream.download(output_path=".", filename="yt_video.mp4")

        with open("yt_video.mp4", 'wb') as vid:
            vid.write("yt_writed.mp4")

        bot.send_message(chatID, "ویدیوی یوتیوب با موفقیت دانلود شد")
        return "yt_video.mp4"
    except Exception as e:
        bot.send_message(chatID, f"مشکلی در دانلود ویدیو رخ داد: {str(e)}")
        return None
    
def youtube(message):
    video_path = message.text

    vid_yt = get_video(video_path, message.chat.id)

    with open(vid_yt, 'rb') as vid:
        bot.send_document(message.chat.id, vid)
    bot.send_message(message.chat.id, "ویدیو با موفقیت فرستاده شد")

    os.remove("yt_video.mp4")



# Start image-generator section
@bot.message_handler(commands=['image_generator'])
def img_generator(message):
    bot.reply_to(message, "لطفا متن مورد نظرتون رو برای تولید تصویر بنویسید")
    bot.register_next_step_handler(message=message, callback=generatorai)


def generatorai(message):
    text = message.text
    response = api.ai_image(text)

    bot.send_message(message.chat.id, "تصویر درحال ساخت می باشد. لطفا کمی صبر کنید")
    
    bot.send_message(message.chat.id, "عکس با موفقیت به ساخته شد")
    with open(f"image-{random.randint(1000,10000)}", 'wb') as f:
        f.write(response)
        bot.send_document(message.chat.id, f)
    bot.send_message(message.chat.id, "عکس تو تلگرام آپلود شد")


bot.polling()

if __name__ == '__main__':
    app.run(debug=True)