# Focus Board

เว็บ To-Do List สไตล์ Notion ที่สร้างด้วย Python และ Streamlit โดยต่อยอดแนวคิดจาก LAB01-LAB08

## ฟีเจอร์

- เพิ่มงานพร้อมหมวดหมู่, priority, deadline, เวลา และโน้ต
- เปลี่ยนสถานะงานเป็นเสร็จแล้ว/ยังไม่เสร็จ
- แก้ไขชื่องาน, priority, deadline, เวลา และโน้ต
- ลบงาน
- ค้นหาและกรองตามหมวดหมู่หรือสถานะ
- ตัวเลือก `All` ใช้แสดงทุกหมวดหมู่หรือทุกสถานะโดยไม่กรอง
- แสดงสถิติและ progress
- เรียงงานตามสถานะ, deadline และ priority
- รองรับการใช้งานบนหน้าจอมือถือและธีมมืดของ Streamlit
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

หมายเหตุ: แอปนี้ใช้ `tasks.json` เป็นไฟล์บันทึกข้อมูล จึงเหมาะกับการเรียนและการสาธิต ข้อมูลบน Streamlit Community Cloud อาจไม่ถาวรเมื่อแอป Restart หากต้องการใช้งานจริงควรเปลี่ยนไปใช้ฐานข้อมูล เช่น SQLite หรือ Supabase
