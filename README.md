# Focus Board

เว็บ To-Do List สไตล์ Notion ที่สร้างด้วย Python และ Streamlit โดยต่อยอดแนวคิดจาก LAB01-LAB08

## ฟีเจอร์

- เพิ่มงานพร้อมหมวดหมู่, priority, deadline และโน้ต
- เปลี่ยนสถานะงานเป็นเสร็จแล้ว/ยังไม่เสร็จ
- แก้ไขและลบงาน
- ค้นหาและกรองตามหมวดหมู่หรือสถานะ
- แสดงสถิติและ progress
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

หมายเหตุ: ระบบไฟล์บน Cloud อาจถูกรีเซ็ตเมื่อแอป restart ดังนั้น `tasks.json` เหมาะกับเดโมหรือโปรเจกต์เรียน หากต้องการใช้งานจริงหลายคนควรเปลี่ยนไปใช้ฐานข้อมูล เช่น SQLite หรือ Supabase
