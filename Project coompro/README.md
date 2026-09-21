# Focus Board

เว็บ To-Do List สไตล์ Notion ที่สร้างด้วย Python และ Streamlit โดยต่อยอดแนวคิดจาก LAB01-LAB08

## ฟีเจอร์

- เพิ่มงานพร้อมหมวดหมู่, priority, deadline, เวลา และโน้ต
- เปลี่ยนสถานะงานเป็นเสร็จแล้ว/ยังไม่เสร็จ
- แก้ไขชื่องาน, priority, deadline, เวลา และโน้ต
- ตั้งเวลาแจ้งเตือนล่วงหน้าได้ตั้งแต่ 5 นาทีถึง 1 วัน
- ลบงาน
- ดาวน์โหลดงานเป็นไฟล์ Calendar (`.ics`) พร้อมการแจ้งเตือน
- ค้นหาและกรองตามหมวดหมู่หรือสถานะ
- ตัวเลือก `All` ใช้แสดงทุกหมวดหมู่หรือทุกสถานะโดยไม่กรอง
- แสดงสถิติและ progress
- เรียงงานตามสถานะ, deadline และ priority
- รองรับการใช้งานบนหน้าจอมือถือและธีมมืดของ Streamlit
- ล็อกอินด้วย Google และแยกข้อมูลงานของแต่ละบัญชี
- บันทึกข้อมูลลง `tasks.json`

## รันในเครื่อง

```bash
python3 -m pip install -r requirements.txt
streamlit run app.py
```

จากนั้นเปิด URL ที่ Streamlit แสดงใน Terminal โดยปกติคือ `http://localhost:8501`

## Deploy บน Streamlit Community Cloud

1. สร้าง GitHub repository แล้วอัปโหลด `app.py` และ `requirements.txt`
2. เข้า `https://share.streamlit.io`
3. เลือก repository, branch และไฟล์หลัก `app.py`
4. กด Deploy

หลัง Deploy สำเร็จ Streamlit จะสร้างลิงก์เว็บไซต์ให้โดยอัตโนมัติ

## การตั้งค่า Login

ฟีเจอร์ Login ใช้ Google OAuth โดยต้องใส่ค่าต่อไปนี้ใน Streamlit Cloud ที่เมนู **Settings > Secrets**:

```toml
[auth]
redirect_uri = "https://YOUR-APP-NAME.streamlit.app/oauth2callback"
cookie_secret = "สร้างค่าลับแบบสุ่มที่ยาวและเก็บเป็นความลับ"
client_id = "Google OAuth client ID"
client_secret = "Google OAuth client secret"
server_metadata_url = "https://accounts.google.com/.well-known/openid-configuration"
```

ใน Google Cloud Console ต้องเพิ่ม URL ใน `redirect_uri` เป็น Authorized redirect URI ก่อนใช้งาน

## การตั้งแจ้งเตือน

1. เพิ่มงานและกำหนดวัน เวลา และเวลาแจ้งเตือน
2. กดปุ่ม `Calendar` ในงานที่ต้องการ
3. เปิดไฟล์ `.ics` ที่ดาวน์โหลดด้วยแอป Calendar บน Android, iOS, Windows หรือ macOS
4. กดยืนยันการเพิ่มกิจกรรมใน Calendar

หลังเพิ่มเข้า Calendar แล้ว ระบบของอุปกรณ์จะเป็นผู้แจ้งเตือนตามเวลาที่ตั้งไว้
