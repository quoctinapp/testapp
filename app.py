from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
from gtts import gTTS
import os
from datetime import date
import time as tm
import webbrowser
import requests
from bs4 import BeautifulSoup
import geocoder
from time import strftime
day = date.today()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

def get_location():#vi tri
    g = geocoder.ip('me')
    if g.ok:
        address = g.address
        return address
    else:
        return None
        
def weather():#thoi tiet
    location = get_location() 
    url = f"https://www.google.com/search?q=weather+{location}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")
        weather_element = soup.find("div", class_="BNeawe iBp4i AP7Wnd")
        if weather_element:
            weather_info = weather_element.get_text()
            return weather_info
    return None

@socketio.on('message')        
def handle_message(message):
    response = xu_li(message)
    emit('response', response)

hoa_hoc_la_gi = {
    "Định nghĩa": "Hóa học là một ngành khoa học thuộc lĩnh vực khoa học tự nhiên, nghiên cứu về thành phần, cấu trúc, tính chất, sự biến đổi của các đơn chất, hợp chất và năng lượng đi kèm những quá trình biến đổi đó.",
    "Đối tượng nghiên cứu của hóa học là chất và sự biến đổi của chất.": {
        "Chất": "Tất cả các chất đều được tạo nên từ các nguyên tử của các nguyên tố hóa học. Cấu tạo (thứ tự và cách thức liên kết của các nguyên tử trong phân tử) quyết định đến tính chất vật lý và hóa học của chất.",
        "Sự biến đổi của chất":"Trong tự nhiên và sản xuất hóa học xảy ra sự biến đổi của chất, sự chuyển hóa từ chất này thành chất khác qua các phản ứng hóa học. Các chất phản ứng với nhau theo quy luật nào, ở điều kiện nào,... để tạo ra chất mới.",
    }
}
nguyen_to_hydro = {
    "Tên nguyên tố": "Hydrogen",
    "Kí hiệu": "H",
    "Chu kỳ": "1",
    "Nhóm": "IA",
    "Độ âm điện": "2.20",
    "Phân loại": "Phi kim",
    "Liên kết giữa các phân tử": "Đơn",
    "Hóa trị": "I",
    "Khối lượng nguyên tử": "1.008 amu",
    "Thông tin": {
        "Do ai phát hiện": "Henry Cavendish",
        "Năm phát hiện": "1766",
        "Tồn tại ở tự nhiên dưới dạng": "Khí H2",
        "Chiếm bao nhiêu % khối lượng vỏ Trái Đất": "~75%",
        "Lịch sử phát triển": "Hydrogen được biết đến từ thời cổ đại, nhưng không được công nhận là một nguyên tố cho đến khi Henry Cavendish phát hiện nó vào năm 1766.",
    },   
    "Tính chất vật lí": {
        "Nhiệt độ nóng chảy (độ C)": "-259.16",
        "Nhiệt độ sôi (độ C)": "-252.87",
        "Trạng thái": "Khí",
        "Màu sắc": "Không màu, không mùi, không vị",
    },
    "Tính chất hóa học": {
        "Xu hướng tạo liên kết": "Hydrogen có xu hướng tạo liên kết đơn với các nguyên tố khác. Khi tạo liên kết, hydrogen có thể chia sẻ một electron để hoàn thành lớp vỏ electron của nó. Hoặc trong trường hợp liên kết ion, hydrogen có thể nhường đi một electron để tạo thành ion H⁺.",
        "Cấu trúc nguyên tử": "Cấu trúc nguyên tử của Hydrogen chỉ bao gồm một proton và một electron. Điều này làm cho hydrogen trở thành nguyên tố đơn giản nhất trong bảng tuần hoàn.",
        "Phản ứng hóa học": "Hydrogen tham gia vào nhiều phản ứng hóa học quan trọng. Một trong những phản ứng quan trọng của hydrogen là phản ứng nhiên liệu trong quá trình đốt cháy, khi nó reagieren với oxi để tạo thành nước (H2O). Hydrogen cũng có vai trò trong hình thành các ion trong dung dịch nước như ion H⁺ và ion hidroni (H₃O⁺), đóng vai trò quan trọng trong hóa học axit-baze. Ngoài ra, liên kết hidro, dạng liên kết yếu xảy ra giữa hydrogen và một nguyên tử oxi, nitơ hoặc flor, đóng vai trò quan trọng trong cấu trúc và tính chất của nước và các phân tử hữu cơ khác.",
        "Hydrogen lỏng": "Ở nhiệt độ rất thấp và áp suất cao, hydrogen có thể tồn tại dưới dạng lỏng và có ứng dụng trong công nghiệp và nghiên cứu vật lý.",
    },
    "Tác động trong sinh học": "Hydrogen không có tác động sinh học đáng kể.",
    "Các ứng dụng của hydro trong công nghiệp": {
        "+ Làm nhiên liệu cho động cơ tên lửa và động cơ ô tô thay thế cho xăng.",
        "+ Dùng trong đèn xì oxi-hiđro để hàn cắt kim loại.",
        "+ Là nguyên liệu để sản xuất amoniac NH3, axit clohiđric HCl và nhiều hợp chất hữu cơ.",
        "+ Dùng làm chất khử để điều chế kim loại từ những oxit của chúng.",
        "+ Dùng để bơm vào khinh khí cầu và bóng thám không vì là khí nhẹ nhất.",
        "+ Dùng trong sản xuất hydro proxide, một chất tẩy rửa mạnh và an toàn",
    },
    "Các ứng dụng của hydro trong đời sống": {
        "+ Ứng dụng trong cell nhiên liệu để cung cấp năng lượng cho các thiết bị di động, ô tô điện, máy tính, v.v.",
        "+ Dùng trong sản xuất khí hydro để sử dụng trong việc hàn kim loại, kiểm tra rò rỉ khí, và nhiều ứng dụng công nghiệp khác.",
        "+ Sử dụng trong công nghiệp thực phẩm để làm tăng tính sủi bọt và độ giòn của sản phẩm.",
        "+ Dùng trong ngành công nghiệp luyện kim và chế tạo bán dẫn.",
        "+ Ứng dụng trong ngành y học, chẳng hạn như quá trình hô hấp với oxy hóa và trong một số phản ứng sinh học.",
    },
    
}

def xu_li(you):
        #khai niem hoa hoc
        if "khái niệm" in you.lower() and "hóa học" in you.lower():
            return "\n".join([f"{key}: {value}" if isinstance(value, str) else f"{key}:\n  - " + "\n  - ".join([f"{sub_key}: {sub_value}" for sub_key, sub_value in value.items()]) for key, value in hoa_hoc_la_gi.items()])
        
        #câu hỏi đời sống
        elif "Psychology" in you.lower():
            return "Psychology is the study of the human mind and behavior. It is the study of the mind, how it works, and how it affects behavior."
        elif "day" in you.lower():
            return day.strftime("%d - %m - %Y")
        elif "where" in you.lower():
            return "You are in: " + get_location()
        elif "time" in you.lower():
            return strftime('%H:%M:%S %p')
        elif "weather" in you.lower():
            weather_info = weather()
            location = get_location()
            if weather_info:
                return f"The weather in {location} is: {weather_info}"
        elif "hello" in you.lower():
            return "hello quoc tin"
        elif "good morning" in you.lower():
            return "Good Moring guys"
        elif "good afternoon" in you.lower():
            return "Good Afternoon guys"
        elif "good evening" in you.lower():
            return "Good evening guys"
        elif "good night" in you.lower():
            return "Good night guys and have a beautiful dream"
        elif "do you want to eat something" in you.lower() :
            return "No, I can't. I'm just a computer and I can't eat"
        elif "do you know viet nam" in you.lower():
            return "Yes, I know about Viet Nam. Located in Southeast Asia, Vietnam is a small and beautiful country with a victorious history, profound patriotism, and wonderful landscapes. ..."
        elif "i am too sad " in you.lower():
            return "What's the matter with you?"
        elif "how are you" in you.lower():
            return "I'm fine, thank you. And you?"
        elif "who are you" in you.lower():
            return "My name is Sam. I am a virtual assistant integrated and developed by Ly Tran Quoc Tin, currently studying in class ten A2 of Ly Tu Trong High School for the Gifted. I was created to help people with disabilities live more comfortably."
        elif "how old are you" in you.lower():
            return "I'm 16 years old"
        elif  "goodbye" in you.lower() or "bye bye" in you.lower():
            return "Have a good day!"
        else:
            return "Sorry i don't know what you say"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)