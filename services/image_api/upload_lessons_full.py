import os
import base64
from pymongo import MongoClient

# ======================================================
# ⚙️ CẤU HÌNH CHUNG
# ======================================================
# Đường dẫn thư mục ảnh trong frontend
BASE_IMAGE_DIR = r"C:\Users\Precision\SignLanguage-website\Signlanguage-frontend\images"

# Cấu hình MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["SignLanguageDB"]
collection = db["lessons_full"]

# ======================================================
# 🧩 DỮ LIỆU NGUỒN (sử dụng mô tả cũ từ lessonData)
# ======================================================
lessonData = {
    "alphabet": [
        {"id": "lesson-a", "title": "Chữ A", "image": "A-Z/a.png", "description": "Nắm chặt bàn tay, chỉ để ngón cái dựng đứng.", "english": "A", "category": "alphabet"},
        {"id": "lesson-b", "title": "Chữ B", "image": "A-Z/b.png", "description": "Duỗi thẳng 4 ngón tay và khép lại, ngón cái gập vào lòng bàn tay.", "english": "B", "category": "alphabet"},
        {"id": "lesson-c", "title": "Chữ C", "image": "A-Z/c.png", "description": "Uốn cong bàn tay tạo hình chữ C.", "english": "C", "category": "alphabet"},
        {"id": "lesson-d", "title": "Chữ D", "image": "A-Z/d.png", "description": "Ngón trỏ duỗi thẳng, các ngón khác khép lại chạm ngón cái.", "english": "D", "category": "alphabet"},
        {"id": "lesson-e", "title": "Chữ E", "image": "A-Z/e.png", "description": "Tất cả các ngón tay khép lại, chạm vào lòng bàn tay.", "english": "E", "category": "alphabet"},
        {"id": "lesson-f", "title": "Chữ F", "image": "A-Z/f.png", "description": "Ngón trỏ và ngón cái chạm nhau tạo hình tròn, ba ngón còn lại duỗi thẳng.", "english": "F", "category": "alphabet"},
        {"id": "lesson-g", "title": "Chữ G", "image": "A-Z/g.png", "description": "Ngón trỏ và ngón cái duỗi ra, các ngón khác khép lại.", "english": "G", "category": "alphabet"},
        {"id": "lesson-h", "title": "Chữ H", "image": "A-Z/h.png", "description": "Ngón trỏ và ngón giữa duỗi thẳng và song song.", "english": "H", "category": "alphabet"},
        {"id": "lesson-i", "title": "Chữ I", "image": "A-Z/i.png", "description": "Chỉ ngón út duỗi thẳng, các ngón khác khép lại.", "english": "I", "category": "alphabet"},
        {"id": "lesson-j", "title": "Chữ J", "image": "A-Z/j.png", "description": "Tương tự chữ I nhưng có chuyển động cong.", "english": "J", "category": "alphabet"},
        {"id": "lesson-k", "title": "Chữ K", "image": "A-Z/k.png", "description": "Ngón trỏ và ngón giữa duỗi thẳng tạo hình chữ V, ngón cái đặt giữa.", "english": "K", "category": "alphabet"},
        {"id": "lesson-l", "title": "Chữ L", "image": "A-Z/l.png", "description": "Ngón trỏ và ngón cái tạo góc vuông.", "english": "L", "category": "alphabet"},
        {"id": "lesson-m", "title": "Chữ M", "image": "A-Z/m.png", "description": "Ba ngón tay đầu khép lại, ngón cái đặt dưới.", "english": "M", "category": "alphabet"},
        {"id": "lesson-n", "title": "Chữ N", "image": "A-Z/n.png", "description": "Hai ngón tay đầu khép lại, ngón cái đặt dưới.", "english": "N", "category": "alphabet"},
        {"id": "lesson-o", "title": "Chữ O", "image": "A-Z/o.png", "description": "Tất cả các ngón tay tạo hình tròn.", "english": "O", "category": "alphabet"},
        {"id": "lesson-p", "title": "Chữ P", "image": "A-Z/p.png", "description": "Tương tự chữ K nhưng hướng xuống dưới.", "english": "P", "category": "alphabet"},
        {"id": "lesson-q", "title": "Chữ Q", "image": "A-Z/q.png", "description": "Tương tự chữ G nhưng hướng xuống dưới.", "english": "Q", "category": "alphabet"},
        {"id": "lesson-r", "title": "Chữ R", "image": "A-Z/r.png", "description": "Ngón trỏ và ngón giữa chéo nhau.", "english": "R", "category": "alphabet"},
        {"id": "lesson-s", "title": "Chữ S", "image": "A-Z/s.png", "description": "Nắm tay, ngón cái đặt trên các ngón khác.", "english": "S", "category": "alphabet"},
        {"id": "lesson-t", "title": "Chữ T", "image": "A-Z/t.png", "description": "Ngón cái đặt giữa ngón trỏ và ngón giữa.", "english": "T", "category": "alphabet"},
        {"id": "lesson-u", "title": "Chữ U", "image": "A-Z/u.png", "description": "Ngón trỏ và ngón giữa duỗi thẳng và khép lại.", "english": "U", "category": "alphabet"},
        {"id": "lesson-v", "title": "Chữ V", "image": "A-Z/v.png", "description": "Ngón trỏ và ngón giữa duỗi thẳng tách ra tạo hình chữ V.", "english": "V", "category": "alphabet"},
        {"id": "lesson-w", "title": "Chữ W", "image": "A-Z/w.png", "description": "Ba ngón đầu duỗi thẳng tách ra.", "english": "W", "category": "alphabet"},
        {"id": "lesson-x", "title": "Chữ X", "image": "A-Z/x.png", "description": "Ngón trỏ cong như móc câu.", "english": "X", "category": "alphabet"},
        {"id": "lesson-y", "title": "Chữ Y", "image": "A-Z/y.png", "description": "Ngón cái và ngón út duỗi ra, các ngón khác khép lại.", "english": "Y", "category": "alphabet"},
        {"id": "lesson-z", "title": "Chữ Z", "image": "A-Z/z.png", "description": "Ngón trỏ duỗi thẳng và vẽ chữ Z trong không khí.", "english": "Z", "category": "alphabet"}
    ],

    "numbers": [
        {"id": "lesson-1", "title": "Số 1", "image": "1-10/1.png", "description": "Giơ ngón trỏ lên.", "english": "One", "category": "numbers"},
        {"id": "lesson-2", "title": "Số 2", "image": "1-10/2.png", "description": "Giơ ngón trỏ và ngón giữa.", "english": "Two", "category": "numbers"},
        {"id": "lesson-3", "title": "Số 3", "image": "1-10/3.png", "description": "Giơ ngón cái, ngón trỏ và ngón giữa.", "english": "Three", "category": "numbers"},
        {"id": "lesson-4", "title": "Số 4", "image": "1-10/4.png", "description": "Giơ bốn ngón tay, khép ngón cái.", "english": "Four", "category": "numbers"},
        {"id": "lesson-5", "title": "Số 5", "image": "1-10/5.png", "description": "Duỗi thẳng tất cả năm ngón tay.", "english": "Five", "category": "numbers"},
        {"id": "lesson-6", "title": "Số 6", "image": "1-10/6.png", "description": "Khép ngón út, duỗi các ngón khác.", "english": "Six", "category": "numbers"},
        {"id": "lesson-7", "title": "Số 7", "image": "1-10/7.png", "description": "Khép ngón áp út, duỗi các ngón khác.", "english": "Seven", "category": "numbers"},
        {"id": "lesson-8", "title": "Số 8", "image": "1-10/8.png", "description": "Khép ngón giữa, duỗi các ngón khác.", "english": "Eight", "category": "numbers"},
        {"id": "lesson-9", "title": "Số 9", "image": "1-10/9.png", "description": "Khép ngón trỏ, duỗi các ngón khác.", "english": "Nine", "category": "numbers"},
        {"id": "lesson-10", "title": "Số 10", "image": "1-10/10.png", "description": "Nắm tay lại rồi giơ ngón cái lên.", "english": "Ten", "category": "numbers"}
    ],

    "greetings": [
        {"id": "lesson-hello", "title": "Xin Chào", "image": "greeting/hello.png", "description": "Mở rộng bàn tay phải với lòng bàn tay hướng về phía mặt, đưa lên ngang trán và vẫy nhẹ từ trái sang phải.", "english": "Hello", "category": "greetings"},
        {"id": "lesson-myname", "title": "Tên Tôi Là", "image": "greeting/mynameis.png", "description": "Đặt bàn tay phải mở rộng lên ngực với các ngón tay hướng về phía cổ, sau đó chỉ thẳng về phía người đối diện bằng ngón tay trỏ.", "english": "My name is", "category": "greetings"},
        {"id": "lesson-thank", "title": "Cảm Ơn", "image": "greeting/thank.png", "description": "Đặt bàn tay phải mở rộng với lòng bàn tay hướng xuống dưới, chạm nhẹ vào môi rồi đưa thẳng ra phía trước về hướng người đối diện.", "english": "Thank you", "category": "greetings"},
        {"id": "lesson-sorry", "title": "Xin Lỗi", "image": "greeting/sorry.png", "description": "Nắm tay phải thành nắm đấm, đặt lên ngực và xoay theo chuyển động tròn nhẹ nhàng trên vùng tim.", "english": "Please/Sorry", "category": "greetings"},
        {"id": "lesson-yes", "title": "Có", "image": "greeting/yes.png", "description": "Nắm tay phải thành nắm đấm với ngón cái duỗi thẳng hướng lên trên, gật nắm tay lên xuống như động tác gật đầu.", "english": "Yes", "category": "greetings"},
        {"id": "lesson-no", "title": "Không", "image": "greeting/no.png", "description": "Đưa bàn tay phải với ngón tay trỏ và ngón giữa duỗi thẳng, vẫy từ trái sang phải ở trước mặt như động tác lắc đầu.", "english": "No", "category": "greetings"},
        {"id": "lesson-love", "title": "Tôi Yêu Bạn", "image": "greeting/iloveyou.png", "description": "Đưa bàn tay phải lên với ngón cái, ngón trỏ và ngón út duỗi thẳng, ngón giữa và ngón áp út cong xuống, hướng về phía người đối diện.", "english": "I love you", "category": "greetings"},
        {"id": "lesson-help", "title": "Giúp Đỡ", "image": "greeting/help.png", "description": "Nắm tay trái thành nắm đấm với ngón cái duỗi lên trên, đặt bàn tay phải mở rộng dưới nắm tay trái và nâng cả hai tay lên trên.", "english": "Help", "category": "greetings"},
        {"id": "lesson-stop", "title": "Dừng Lại", "image": "greeting/stop.png", "description": "Đưa bàn tay thẳng về phía trước với lòng bàn tay hướng ra ngoài.", "english": "Stop", "category": "greetings"}
    ],

    "people": [
        {"id": "lesson-mother", "title": "Mẹ", "image": "people/mother.png", "description": "Đầu ngón cái tay phải chạm vào phần dưới của cằm (lòng bàn tay mở).", "english": "Mother", "category": "people"},
        {"id": "lesson-father", "title": "Bố", "image": "people/father.png", "description": "Đầu ngón cái tay phải chạm vào trán (lòng bàn tay mở, các ngón xòe ra).", "english": "Father", "category": "people"},
        {"id": "lesson-sister", "title": "Chị/Em gái", "image": "people/sister.png", "description": "Chạm ngón cái của tay phải lên cằm (giống từ girl), sau đó đưa tay ra trước, kết thúc bằng động tác hai tay tạo hình súng và chạm nhau.", "english": "Sister", "category": "people"},
        {"id": "lesson-brother", "title": "Anh/Em trai", "image": "people/brother.png", "description": "Đầu ngón cái tay phải chạm trán (giống từ boy), sau đó hai tay tạo hình súng và chạm nhau như với sister.", "english": "Brother", "category": "people"},
        {"id": "lesson-grandmother", "title": "Bà", "image": "people/grandma.png", "description": "Làm dấu mother nhưng tay di chuyển ra phía trước hai lần.", "english": "Grandmother", "category": "people"},
        {"id": "lesson-grandfather", "title": "Ông", "image": "people/grandpa.png", "description": "Làm dấu father rồi đẩy tay ra phía trước hai lần.", "english": "Grandfather", "category": "people"},
        {"id": "lesson-child-boy", "title": "Bé trai", "image": "people/boy.png", "description": "Dùng tay như đang cầm mũ lưỡi trai (tay đặt ở trán, ngón cái và các ngón mở rộng như đang kẹp và mở).", "english": "Boy", "category": "people"},
        {"id": "lesson-child-girl", "title": "Bé gái", "image": "people/girl.png", "description": "Nắm tay lại, chà nhẹ khớp ngón cái dọc theo cằm (từ tai đến cằm).", "english": "Girl", "category": "people"},
        {"id": "lesson-baby", "title": "Em bé", "image": "people/baby.png", "description": "Đặt hai tay dưới dạng đang bồng trẻ, sau đó nhẹ nhàng đung đưa như đang ru em bé.", "english": "Baby", "category": "people"},
        {"id": "lesson-family", "title": "Gia đình", "image": "people/family.png", "description": "Hai tay tạo hình chữ F, rồi xoay tròn một vòng để kết thúc vị trí hai chữ F sát nhau.", "english": "Family", "category": "people"},
        {"id": "lesson-friend", "title": "Bạn", "image": "people/friend.png", "description": "Móc ngón trỏ tay này vào ngón trỏ tay kia, rồi đổi chiều và móc lại lần nữa.", "english": "Friend", "category": "people"},
        {"id": "lesson-teacher", "title": "Giáo viên", "image": "people/teacher.png", "description": "Đưa hai tay (các ngón khép lại) lên gần trán như đang mở đầu ra, sau đó đưa hai bàn tay xuống hai bên giống như chỉ người.", "english": "Teacher", "category": "people"},
        {"id": "lesson-neighbor", "title": "Hàng xóm", "image": "people/neighbor.png", "description": "Hai bàn tay hướng về nhau như cái bắt tay nhưng không chạm, sau đó nhấn nhẹ một tay vào tay kia.", "english": "Neighbor", "category": "people"},
        {"id": "lesson-woman", "title": "Phụ nữ", "image": "people/woman.png", "description": "Đầu ngón cái tay phải chạm vào cằm, rồi di chuyển xuống chạm nhẹ lên ngực (vùng ngực trên).", "english": "Woman", "category": "people"},
        {"id": "lesson-man", "title": "Đàn ông", "image": "people/man.png", "description": "Đầu ngón cái chạm trán (giống father), sau đó tay mở ra và hạ xuống trước ngực.", "english": "Man", "category": "people"}
    ],

    "emotions": [
        {"id": "lesson-frightened", "title": "Sợ hãi", "image": "feelings/frightened.png", "description": "Đưa hai tay nắm lại trước ngực, sau đó bật mở ra như bị hoảng hốt. Gương mặt hoang mang.", "english": "Frightened", "category": "emotions"},
        {"id": "lesson-happy", "title": "Vui vẻ", "image": "feelings/happy.png", "description": "Dùng lòng bàn tay xoa nhẹ lên ngực theo chuyển động tròn hướng lên, nét mặt tươi sáng.", "english": "Happy", "category": "emotions"},
        {"id": "lesson-sad", "title": "Buồn", "image": "feelings/sad.png", "description": "Mở bàn tay và kéo từ trên mặt xuống, biểu cảm trầm lặng và buồn bã.", "english": "Sad", "category": "emotions"},
        {"id": "lesson-very-good", "title": "Rất tốt", "image": "feelings/very-good.png", "description": "Giơ hai ngón cái lên, nở nụ cười tươi thể hiện sự tích cực.", "english": "Very good", "category": "emotions"},
        {"id": "lesson-angry", "title": "Giận dữ", "image": "feelings/angry.png", "description": "Đưa tay lên phía trước dạng vuốt cong, như cơn giận đang dâng trào. Gương mặt nghiêm lại hoặc cau mày.", "english": "Angry", "category": "emotions"},
        {"id": "lesson-excited", "title": "Hào hứng", "image": "feelings/excited.png", "description": "Đặt hai tay mở gần ngực, ngón giữa chạm nhẹ vào ngực và di chuyển lên xuống luân phiên. Khuôn mặt rạng rỡ.", "english": "Excited", "category": "emotions"},
        {"id": "lesson-love1", "title": "Yêu thương", "image": "feelings/love.png", "description": "Khoanh tay trước ngực như đang ôm người mình thương, kết hợp ánh mắt dịu dàng.", "english": "Love", "category": "emotions"}
    ],

    "colors": [
        {"id": "lesson-green", "title": "Màu lục", "image": "colours/green.png", "description": "Tay hình chữ G lắc nhẹ gần má.", "english": "Green", "category": "colors"},
        {"id": "lesson-blue", "title": "Màu lam", "image": "colours/blue.png", "description": "Tay hình chữ B lắc nhẹ trước vai.", "english": "Blue", "category": "colors"},
        {"id": "lesson-yellow", "title": "Màu vàng", "image": "colours/yellow.png", "description": "Tay chữ Y lắc nhẹ gần cằm.", "english": "Yellow", "category": "colors"},
        {"id": "lesson-red", "title": "Màu đỏ", "image": "colours/red.png", "description": "Ngón trỏ chạm môi rồi hạ xuống.", "english": "Red", "category": "colors"},
        {"id": "lesson-white", "title": "Màu trắng", "image": "colours/white.png", "description": "Mở tay ở ngực, kéo ra rồi khép các ngón.", "english": "White", "category": "colors"},
        {"id": "lesson-black", "title": "Màu đen", "image": "colours/black.png", "description": "Ngón trỏ quét ngang trán.", "english": "Black", "category": "colors"}
    ],

    "places": [
        {"id": "lesson-school", "title": "Trường học", "image": "places/school.png", "description": "Ngón trỏ quét ngang trán.", "english": "School", "category": "places"},
        {"id": "lesson-restaurant", "title": "Nhà hàng", "image": "places/restaurant.png", "description": "_________", "english": "Restaurant", "category": "places"},
        {"id": "lesson-hospital", "title": "Bệnh viện", "image": "places/hospital.png", "description": "_________", "english": "Hospital", "category": "places"},
        {"id": "lesson-hotel", "title": "Khách sạn", "image": "places/hotel.png", "description": "_________", "english": "Hotel", "category": "places"},
        {"id": "lesson-home", "title": "Nhà", "image": "places/home.png", "description": "_________", "english": "Home", "category": "places"}
    ],

    "others": [
        {"id": "lesson-eat", "title": "Ăn", "image": "others/eat.png", "description": "_______", "english": "Eat", "category": "others"},
        {"id": "lesson-drink", "title": "Uống", "image": "others/drink.png", "description": "_______", "english": "Drink", "category": "others"},
        {"id": "lesson-learn", "title": "Học", "image": "others/learn.png", "description": "_______", "english": "Learn", "category": "others"},
        {"id": "lesson-book", "title": "Quyển Sách", "image": "others/book.png", "description": "_______", "english": "Book", "category": "others"},
        {"id": "lesson-water", "title": "Nước", "image": "others/water.png", "description": "_______", "english": "Water", "category": "others"}
    ]
}


# ======================================================
# 🧰 HÀM CHUYỂN ẢNH → BASE64
# ======================================================
def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as img_file:
            encoded = base64.b64encode(img_file.read()).decode("utf-8")
            return f"data:image/png;base64,{encoded}"
    except FileNotFoundError:
        print(f"⚠️ Không tìm thấy ảnh: {image_path}")
        return None

# ======================================================
# 🚀 GHI DỮ LIỆU LÊN MONGODB
# ======================================================
collection.delete_many({})  # Xóa cũ để upload lại sạch
count = 0

for category, lessons in lessonData.items():
    for lesson in lessons:
        image_path = os.path.join(BASE_IMAGE_DIR, lesson["image"])
        encoded_image = encode_image_to_base64(image_path)

        document = {
            "id": lesson["id"],
            "title": lesson["title"],
            "english": lesson["english"],
            "category": category,
            "image": encoded_image,  # ✅ Lưu base64
            "description": f"{lesson['description']} | 📡 Dữ liệu tải từ API thật.",
        }

        collection.insert_one(document)
        print(f"✅ Đã thêm: {lesson['title']} ({category})")
        count += 1

print(f"\n🎉 Hoàn tất! Đã upload {count} bài học lên MongoDB ({db.name}.{collection.name})")
