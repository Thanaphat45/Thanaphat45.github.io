# Builds the downloadable one-page resume PDFs (sidebar layout) for TH and EN.
#   python tools/build_resume_pdf.py
import pathlib, subprocess, html
ROOT = pathlib.Path(__file__).resolve().parent.parent
CHROME = r"C:\Program Files\Google\Chrome\Application\chrome.exe"

D = {
 "th": dict(
  name="ธนภัทร อุปพงษ์", sub="THANAPHAT AUPAPHONG", role="Back-end Developer",
  contact_h="ติดต่อ", skills_h="ทักษะ", edu_h="การศึกษา", lang_h="ภาษา",
  profile_h="โปรไฟล์", xp_h="ประสบการณ์ทำงาน", proj_h="ผลงานที่เปิดใช้งานจริง",
  phone="097-338-0410 (โทร / LINE)",
  profile="นักพัฒนา Back-end ที่สร้างระบบและ REST API ด้วย NestJS และ Laravel เน้นความถูกต้องของข้อมูลและการทดสอบอัตโนมัติ มีผลงาน 4 ระบบที่ใช้งานจริง และประสบการณ์ซัพพอร์ตผู้ใช้ 1.5 ปี",
  edu=("ปริญญาตรี เทคโนโลยีสารสนเทศ", "มหาวิทยาลัยราชภัฏบุรีรัมย์", "จบปี 2567"),
  langs=["ไทย — ภาษาแม่", "อังกฤษ — อ่าน/เขียนเชิงเทคนิค"],
  xp=[
   ("Web Developer & IT Support", "The Niya Corporation", "ต.ค. 2569 – ปัจจุบัน",
    ["พัฒนาเว็บไซต์องค์กรทั้งหมดด้วยตนเองตามความต้องการของบริษัท", "ดูแลระบบไอทีภายใน: เครื่องพิมพ์ เครือข่าย และ Microsoft Office"]),
   ("Application Support L1", "Fintechinno", "พ.ค. 2568 – ต.ค. 2569",
    ["แก้ไขปัญหาลูกค้าผ่าน LINE Support และเครื่องมือหลังบ้าน", "ทดสอบ UAT ทุกรอบการอัปเดต พร้อมบันทึกผลการทดสอบ",
     "วิเคราะห์ error ด้วย DevTools และส่ง endpoint/payload ให้ทีมพัฒนา"]),
   ("Web Developer Intern", "Asha Tech Corporation", "ฝึกงาน 3 เดือน",
    ["พัฒนา REST API ด้วย Laravel 11 และฟังก์ชันนำเข้าข้อมูล"]),
  ],
  proj=[
   ("IT Helpdesk", "ระบบแจ้งซ่อมที่ใช้ Claude API คัดแยกและร่างคำตอบ · 26 tests + CI", "NestJS · Angular · PostgreSQL", "it-helpdesk-1bkc.onrender.com"),
   ("ระบบประเมินผู้สูงอายุ (ADL)", "แบบประเมินมาตรฐาน 3 แบบ สิทธิ์ 3 บทบาท · โปรเจกต์จบ", "Laravel · PostgreSQL · Docker", "adl-assessment.onrender.com"),
   ("Clinic Queue API", "ระบบบัตรคิว เลขคิวไม่ซ้ำเมื่อกดพร้อมกัน · 21 tests", "Laravel · PHPUnit · GitHub Actions", "clinic-queue-api-um6b.onrender.com"),
   ("DriveRent", "ระบบเช่ารถพร้อมหน้า Admin และ transaction ฝั่งเซิร์ฟเวอร์", "React · Node.js · PostgreSQL", "driverent-whky.onrender.com"),
  ],
 ),
 "en": dict(
  name="Thanaphat Aupaphong", sub="ธนภัทร อุปพงษ์", role="Back-end Developer",
  contact_h="Contact", skills_h="Skills", edu_h="Education", lang_h="Languages",
  profile_h="Profile", xp_h="Experience", proj_h="Live Projects",
  phone="+66 97 338 0410 (Phone / LINE)",
  profile="Back-end developer building systems and REST APIs with NestJS and Laravel, focused on data integrity and automated testing. Four systems live in production and 1.5 years of hands-on application support.",
  edu=("B.Sc. Information Technology", "Buriram Rajabhat University", "Graduated 2024"),
  langs=["Thai — Native", "English — Technical reading & writing"],
  xp=[
   ("Web Developer & IT Support", "The Niya Corporation", "Oct 2026 – Present",
    ["Built the entire company website independently to business requirements", "Maintain in-house IT: printers, networking and Microsoft Office"]),
   ("Application Support L1", "Fintechinno", "May 2025 – Oct 2026",
    ["Resolved customer issues via LINE Support and internal admin tools", "Performed UAT on every release and documented results",
     "Diagnosed errors with DevTools and escalated endpoints/payloads to developers"]),
   ("Web Developer Intern", "Asha Tech Corporation", "3-month internship",
    ["Developed REST APIs with Laravel 11 and a data import feature"]),
  ],
  proj=[
   ("IT Helpdesk", "AI-assisted ticketing using the Claude API · 26 tests + CI", "NestJS · Angular · PostgreSQL", "it-helpdesk-1bkc.onrender.com"),
   ("Elderly Assessment System (ADL)", "Three standard assessments, three user roles · Capstone", "Laravel · PostgreSQL · Docker", "adl-assessment.onrender.com"),
   ("Clinic Queue API", "Queue ticketing with no duplicates under concurrency · 21 tests", "Laravel · PHPUnit · GitHub Actions", "clinic-queue-api-um6b.onrender.com"),
   ("DriveRent", "Car rental with admin area and server-side transactions", "React · Node.js · PostgreSQL", "driverent-whky.onrender.com"),
  ],
 ),
}
SKILLS = [("Back-end", "NestJS, Laravel, PHP, Node.js, TypeScript, REST API"), ("Database", "PostgreSQL, MySQL, Supabase"),
          ("Front-end", "Angular, React, JavaScript"), ("DevOps", "Docker, GitHub Actions, Render"),
          ("AI", "Claude API, Claude Code"), ("Testing", "PHPUnit, Vitest, UAT")]

def page(L, d):
    e = html.escape
    xp = "".join(f"""<div class="it"><div class="ih"><b>{e(t)}</b><span>{e(w)}</span></div><div class="co">{e(c)}</div>
      <ul>{''.join(f'<li>{e(x)}</li>' for x in bs)}</ul></div>""" for t, c, w, bs in d["xp"])
    pr = "".join(f"""<div class="pj"><b>{e(t)}</b><p>{e(s)}</p><small>{e(st)} · <a href="https://{u}">{u}</a></small></div>""" for t, s, st, u in d["proj"])
    sk = "".join(f"<div class='sk'><h4>{a}</h4><p>{b}</p></div>" for a, b in SKILLS)
    photo = (ROOT / "images/profile.jpg").as_uri()
    return f"""<!doctype html><html lang="{L}"><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+Thai:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
@page {{ size: A4; margin: 0; }}
* {{ box-sizing: border-box; margin: 0; padding: 0; -webkit-print-color-adjust: exact; print-color-adjust: exact; }}
body {{ font-family: Inter, "Noto Sans Thai", sans-serif; color: #1d2433; font-size: 10.6pt; line-height: 1.5; }}
.pg {{ width: 210mm; height: 297mm; display: grid; grid-template-columns: 68mm 1fr; }}
aside {{ background: #1e2a44; color: #dfe6f3; padding: 14mm 8mm 10mm; }}
aside img {{ width: 34mm; height: 34mm; border-radius: 50%; object-fit: cover; display: block; margin: 0 auto 7mm; border: 3px solid #3d5287; }}
aside h3:lang(th) {{ letter-spacing: .02em !important; }} aside h3 {{ font-size: 9pt; letter-spacing: .14em; text-transform: uppercase; color: #9fb4e0; margin: 7mm 0 2.5mm; border-bottom: 1px solid #3d5287; padding-bottom: 1.5mm; }}
aside p, aside li {{ font-size: 9pt; }}
aside a {{ color: #dfe6f3; text-decoration: none; }}
aside .c p {{ margin-bottom: 1.5mm; }} aside .c .em {{ font-size: 8.2pt; }}
.sk {{ margin-bottom: 2.3mm; }} .sk h4 {{ font-size: 8.6pt; color: #fff; font-weight: 600; }} .sk p {{ color: #c3cde0; }}
aside ul {{ list-style: none; }}
main {{ padding: 14mm 12mm 10mm 11mm; }}
h1 {{ font-size: 25pt; line-height: 1.1; color: #1e2a44; font-weight: 700; }}
.sub {{ font-size: 9.5pt; color: #7a8599; letter-spacing: .1em; margin-top: 1mm; }}
.role {{ font-size: 12.5pt; color: #2f5bd2; font-weight: 600; margin-top: 2mm; }}
h2:lang(th) {{ letter-spacing: .02em !important; }} h2 {{ font-size: 10.5pt; letter-spacing: .12em; text-transform: uppercase; color: #1e2a44; margin: 7mm 0 3mm; display: flex; align-items: center; gap: 3mm; }}
h2::after {{ content: ""; flex: 1; height: 1.5px; background: #d6dcea; }}
.lead {{ color: #3b4456; }}
.it {{ margin-bottom: 4mm; }} .ih {{ display: flex; justify-content: space-between; align-items: baseline; }}
.ih b {{ font-size: 11pt; }} .ih span {{ font-size: 8.8pt; color: #7a8599; white-space: nowrap; }}
.co {{ color: #2f5bd2; font-size: 9.5pt; font-weight: 500; }}
ul {{ padding-left: 4.5mm; margin-top: 1mm; }} main li {{ font-size: 9.8pt; color: #3b4456; }}
.pj {{ margin-bottom: 3.2mm; padding-left: 3mm; border-left: 2.5px solid #2f5bd2; }}
.pj b {{ font-size: 10.5pt; }} .pj p {{ font-size: 9.6pt; color: #3b4456; }}
.pj small {{ font-size: 8.4pt; color: #7a8599; }} .pj a {{ color: #2f5bd2; text-decoration: none; }}
</style></head><body><div class="pg">
<aside><img src="{photo}">
<h3>{d['contact_h']}</h3><div class="c"><p>{d['phone']}</p><p class="em"><a href="mailto:thanaphat.aupaphong45@gmail.com">thanaphat.aupaphong45@gmail.com</a></p>
<p><a href="https://github.com/Thanaphat45">github.com/Thanaphat45</a></p><p><a href="https://thanaphat45.github.io">thanaphat45.github.io</a></p></div>
<h3>{d['skills_h']}</h3>{sk}
<h3>{d['edu_h']}</h3><p><b style="color:#fff">{e(d['edu'][0])}</b></p><p>{e(d['edu'][1])}</p><p style="color:#9fb4e0">{e(d['edu'][2])}</p>
</aside>
<main><h1>{d['name']}</h1><div class="sub">{d['sub']}</div><div class="role">{d['role']} · NestJS · Laravel</div>
<h2>{d['profile_h']}</h2><p class="lead">{e(d['profile'])}</p>
<h2>{d['xp_h']}</h2>{xp}
<h2>{d['proj_h']}</h2>{pr}
</main></div></body></html>"""

for L, out in [("th", "Thanaphat-Aupaphong-Resume-TH.pdf"), ("en", "Thanaphat-Aupaphong-Resume-EN.pdf")]:
    src = ROOT / "tools" / f"_resume_{L}.html"
    src.write_text(page(L, D[L]), encoding="utf-8")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer", "--virtual-time-budget=8000",
                    f"--print-to-pdf={ROOT / out}", src.as_uri()], capture_output=True)
    print("built", out)
