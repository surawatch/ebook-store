import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def create_report():
    doc = docx.Document()

    # Helper styling functions
    def set_font(run, font_name="TH Sarabun New", size_pt=14, bold=False, italic=False, color_rgb=None):
        run.font.name = font_name
        run.font.size = Pt(size_pt)
        run.font.bold = bold
        run.font.italic = italic
        if color_rgb:
            run.font.color.rgb = color_rgb
        rPr = run._r.get_or_add_rPr()
        rFonts = parse_xml(f'<w:rFonts {nsdecls("w")} w:ascii="{font_name}" w:hAnsi="{font_name}" w:cs="{font_name}"/>')
        rPr.append(rFonts)

    # 1. Page Margins (Normal Academic 1 inch all around)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.different_first_page_header_footer = True
        
        # Add Header & Footer
        footer = section.footer
        f_p = footer.paragraphs[0]
        f_p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        f_run = f_p.add_run("รายวิชา Database Mini Project - E-Book Store Management System")
        set_font(f_run, size_pt=9, color_rgb=RGBColor(140, 140, 140))

    def add_p(text="", align=WD_ALIGN_PARAGRAPH.LEFT, space_before=0, space_after=4, line_spacing=1.15):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        if text:
            r = p.add_run(text)
            set_font(r, font_name="TH Sarabun New", size_pt=14, bold=False, color_rgb=RGBColor(30, 41, 59))
        return p

    def add_h1(text, space_before=14, space_after=6):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        set_font(r, font_name="TH Sarabun New", size_pt=18, bold=True, color_rgb=RGBColor(30, 58, 138)) # Navy blue
        return p

    def add_h2(text, space_before=10, space_after=4):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        set_font(r, font_name="TH Sarabun New", size_pt=15, bold=True, color_rgb=RGBColor(37, 99, 235)) # Blue
        return p

    def add_h3(text, space_before=8, space_after=2):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        set_font(r, font_name="TH Sarabun New", size_pt=14, bold=True, color_rgb=RGBColor(15, 23, 42))
        return p

    def add_bullet(text, level=0, bold_prefix="", space_after=3):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.left_indent = Inches(0.25 * (level + 1))
        if bold_prefix:
            r_bold = p.add_run(bold_prefix)
            set_font(r_bold, font_name="TH Sarabun New", size_pt=14, bold=True, color_rgb=RGBColor(15, 23, 42))
        r_text = p.add_run(text)
        set_font(r_text, font_name="TH Sarabun New", size_pt=14, bold=False, color_rgb=RGBColor(51, 65, 85))
        return p

    def add_code_block(code_text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.5)
        
        # XML styling for code background and border
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:val="clear" w:color="auto" w:fill="F1F5F9"/>')
        tcPr.append(shd)
        tcBorders = parse_xml(f'''<w:tcBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>
            <w:left w:val="single" w:sz="24" w:space="0" w:color="3B82F6"/>
            <w:bottom w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>
            <w:right w:val="single" w:sz="6" w:space="0" w:color="CBD5E1"/>
        </w:tcBorders>''')
        tcPr.append(tcBorders)
        
        # Margins
        tcMar = parse_xml(f'''<w:tcMar {nsdecls("w")}>
            <w:top w:w="120" w:type="dxa"/>
            <w:left w:w="160" w:type="dxa"/>
            <w:bottom w:w="120" w:type="dxa"/>
            <w:right w:w="160" w:type="dxa"/>
        </w:tcMar>''')
        tcPr.append(tcMar)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.05
        r = p.add_run(code_text.strip())
        set_font(r, font_name="Consolas", size_pt=10, bold=False, color_rgb=RGBColor(30, 41, 59))
        
        # Spacing after table
        sp_p = doc.add_paragraph()
        sp_p.paragraph_format.space_before = Pt(0)
        sp_p.paragraph_format.space_after = Pt(4)

    def add_callout(title, text, box_type="info"):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        cell.width = Inches(6.5)
        
        bg_color = "EFF6FF" if box_type == "info" else ("FEF3C7" if box_type == "warning" else "F0FDF4")
        border_color = "3B82F6" if box_type == "info" else ("F59E0B" if box_type == "warning" else "10B981")
        
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:val="clear" w:color="auto" w:fill="{bg_color}"/>')
        tcPr.append(shd)
        tcBorders = parse_xml(f'''<w:tcBorders {nsdecls("w")}>
            <w:top w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>
            <w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/>
            <w:bottom w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>
            <w:right w:val="single" w:sz="4" w:space="0" w:color="{border_color}"/>
        </w:tcBorders>''')
        tcPr.append(tcBorders)
        
        tcMar = parse_xml(f'''<w:tcMar {nsdecls("w")}>
            <w:top w:w="120" w:type="dxa"/>
            <w:left w:w="180" w:type="dxa"/>
            <w:bottom w:w="120" w:type="dxa"/>
            <w:right w:w="180" w:type="dxa"/>
        </w:tcMar>''')
        tcPr.append(tcMar)
        
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r_title = p.add_run(f"📌 {title}: ")
        set_font(r_title, font_name="TH Sarabun New", size_pt=13, bold=True, color_rgb=RGBColor(30, 58, 138))
        r_text = p.add_run(text)
        set_font(r_text, font_name="TH Sarabun New", size_pt=13, bold=False, color_rgb=RGBColor(30, 41, 59))
        
        sp_p = doc.add_paragraph()
        sp_p.paragraph_format.space_before = Pt(0)
        sp_p.paragraph_format.space_after = Pt(4)

    def style_table(table, col_widths, col_alignments, header_bg="1E3A8A"):
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        # Format Header
        hdr_row = table.rows[0]
        trPr = hdr_row._tr.get_or_add_trPr()
        trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))
        trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
        
        for i, cell in enumerate(hdr_row.cells):
            cell.width = col_widths[i]
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            tcPr = cell._tc.get_or_add_tcPr()
            tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:val="clear" w:color="auto" w:fill="{header_bg}"/>'))
            tcMar = parse_xml(f'''<w:tcMar {nsdecls("w")}>
                <w:top w:w="120" w:type="dxa"/>
                <w:left w:w="120" w:type="dxa"/>
                <w:bottom w:w="120" w:type="dxa"/>
                <w:right w:w="120" w:type="dxa"/>
            </w:tcMar>''')
            tcPr.append(tcMar)
            p = cell.paragraphs[0]
            p.alignment = col_alignments[i]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            for r in p.runs:
                set_font(r, font_name="TH Sarabun New", size_pt=13, bold=True, color_rgb=RGBColor(255, 255, 255))
                
        # Format Data Rows
        for row_idx, row in enumerate(table.rows[1:], start=1):
            trPr = row._tr.get_or_add_trPr()
            trPr.append(parse_xml(f'<w:cantSplit {nsdecls("w")}/>'))
            bg = "F8FAFC" if row_idx % 2 == 1 else "FFFFFF"
            for i, cell in enumerate(row.cells):
                cell.width = col_widths[i]
                cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
                tcPr = cell._tc.get_or_add_tcPr()
                tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:val="clear" w:color="auto" w:fill="{bg}"/>'))
                tcBorders = parse_xml(f'''<w:tcBorders {nsdecls("w")}>
                    <w:top w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
                    <w:left w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
                    <w:bottom w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
                    <w:right w:val="single" w:sz="4" w:space="0" w:color="E2E8F0"/>
                </w:tcBorders>''')
                tcPr.append(tcBorders)
                tcMar = parse_xml(f'''<w:tcMar {nsdecls("w")}>
                    <w:top w:w="80" w:type="dxa"/>
                    <w:left w:w="100" w:type="dxa"/>
                    <w:bottom w:w="80" w:type="dxa"/>
                    <w:right w:w="100" w:type="dxa"/>
                </w:tcMar>''')
                tcPr.append(tcMar)
                p = cell.paragraphs[0]
                p.alignment = col_alignments[i]
                p.paragraph_format.space_before = Pt(1)
                p.paragraph_format.space_after = Pt(1)
                for r in p.runs:
                    set_font(r, font_name="TH Sarabun New", size_pt=12.5, bold=False, color_rgb=RGBColor(30, 41, 59))
                    
        sp_p = doc.add_paragraph()
        sp_p.paragraph_format.space_before = Pt(0)
        sp_p.paragraph_format.space_after = Pt(6)

    print("Building Document Structure...")

    # =========================================================================
    # 1. ปกหน้า (COVER PAGE)
    # =========================================================================
    p_cov_hdr = add_p("รายงานโครงงานพัฒนาระบบฐานข้อมูล (Database Mini Project)", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=30, space_after=10)
    p_cov_hdr.runs[0].font.size = Pt(16)
    p_cov_hdr.runs[0].font.bold = True
    p_cov_hdr.runs[0].font.color.rgb = RGBColor(71, 85, 105)

    p_cov_t1 = add_p("การวิเคราะห์และพัฒนาระบบร้านขายหนังสือและอีบุ๊กออนไลน์", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=15, space_after=4)
    p_cov_t1.runs[0].font.size = Pt(24)
    p_cov_t1.runs[0].font.bold = True
    p_cov_t1.runs[0].font.color.rgb = RGBColor(30, 58, 138)

    p_cov_t2 = add_p("E-Book Store Online Management System", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=25)
    p_cov_t2.runs[0].font.size = Pt(18)
    p_cov_t2.runs[0].font.bold = True
    p_cov_t2.runs[0].font.color.rgb = RGBColor(37, 99, 235)

    p_sub = add_p("โครงงานกลุ่มสำหรับประยุกต์ใช้การออกแบบและพัฒนาฐานข้อมูลเชิงสัมพันธ์ (3NF)\nพร้อมระบบหน้าร้าน ตะกร้าสินค้า สั่งซื้อ ยืนยันการชำระเงินจำลอง ล็อกไฟล์ความปลอดภัย\nและระบบวิเคราะห์ข้อมูลเชิงลึก 4 ด้านด้วยภาษา SQL บนฐานข้อมูลจริง", 
                  align=WD_ALIGN_PARAGRAPH.CENTER, space_before=5, space_after=30)
    p_sub.runs[0].font.size = Pt(13)
    p_sub.runs[0].font.italic = True
    p_sub.runs[0].font.color.rgb = RGBColor(100, 116, 139)

    # ข้อมูลกลุ่มและผู้จัดทำ
    p_grp = add_p("จัดทำโดย (คณะผู้จัดทำโครงงาน)", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=15, space_after=8)
    p_grp.runs[0].font.size = Pt(16)
    p_grp.runs[0].font.bold = True
    p_grp.runs[0].font.color.rgb = RGBColor(15, 23, 42)

    tbl_mem = doc.add_table(rows=3, cols=3)
    tbl_mem.rows[0].cells[0].paragraphs[0].add_run("ลำดับ")
    tbl_mem.rows[0].cells[1].paragraphs[0].add_run("ชื่อ-นามสกุล สมาชิกในกลุ่ม")
    tbl_mem.rows[0].cells[2].paragraphs[0].add_run("รหัสนักศึกษา")

    tbl_mem.rows[1].cells[0].paragraphs[0].add_run("1")
    tbl_mem.rows[1].cells[1].paragraphs[0].add_run("นายสุรวัจน์ ชลเรืองทรัพย์")
    tbl_mem.rows[1].cells[2].paragraphs[0].add_run("67332110217-1")

    tbl_mem.rows[2].cells[0].paragraphs[0].add_run("2")
    tbl_mem.rows[2].cells[1].paragraphs[0].add_run("นายสรวิชญ์ มีมาก")
    tbl_mem.rows[2].cells[2].paragraphs[0].add_run("67332110275-8")

    style_table(tbl_mem, [Inches(1.0), Inches(3.2), Inches(2.3)], 
                [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER], header_bg="1E3A8A")

    p_inst = add_p("เสนอ\nอาจารย์ผู้สอนประจำรายวิชา Database Systems / Database Mini Project\n\nโครงงานนี้เป็นส่วนหนึ่งของการศึกษาตามหลักสูตรวิศวกรรมศาสตรบัณฑิต\nสาขาวิชาวิศวกรรมคอมพิวเตอร์ คณะวิศวกรรมศาสตร์\nมหาวิทยาลัยเทคโนโลยีราชมงคลอีสาน วิทยาเขตขอนแก่น\nภาคการศึกษาที่ 1 ปีการศึกษา 2569",
                   align=WD_ALIGN_PARAGRAPH.CENTER, space_before=35, space_after=0)
    p_inst.runs[0].font.size = Pt(13.5)
    p_inst.runs[0].font.color.rgb = RGBColor(51, 65, 85)

    doc.add_page_break()

    # =========================================================================
    # 2. ข้อมูลกลุ่มและใบงาน (GROUP & ASSIGNMENT SUMMARY - PAGE 1 OF PDF)
    # =========================================================================
    add_h1("ใบงาน Mini Project Database ร้านขาย E Book (สรุปข้อมูลกลุ่ม)")
    add_p("โครงงานกลุ่มละ 2 คน สำหรับประยุกต์ใช้การออกแบบและพัฒนาฐานข้อมูล พัฒนาระบบร้านขาย E Book ที่ลูกค้าค้นหา เลือกซื้อ ชำระเงินแบบจำลอง และรับลิงก์ดาวน์โหลดได้ พร้อมส่วนบริหารจัดการร้านและรายงานวิเคราะห์จากข้อมูลในระบบจริง")

    add_h2("สิ่งที่นักศึกษาต้องแสดง (ตามเกณฑ์ใบงาน)")
    add_bullet("ออกแบบฐานข้อมูลที่สัมพันธ์กับกระบวนการขายอย่างถูกต้องและอธิบายได้ (ครบ 9 ตารางตามหลัก 3NF)", bold_prefix="• ")
    add_bullet("พัฒนาระบบหรือ prototype ที่สาธิตเส้นทางลูกค้าและผู้ดูแลร้านได้จริงอย่างสมบูรณ์", bold_prefix="• ")
    add_bullet("เขียน SQL และรายงานวิเคราะห์จากข้อมูลตัวอย่างที่กลุ่มบันทึกเองในระบบจริง (35 คำสั่งซื้อ)", bold_prefix="• ")
    add_bullet("ใช้ AI ได้อย่างมีความรับผิดชอบ เปิดเผยสิ่งที่นำมาใช้ และระบุข้อที่ตัดสินใจปฏิเสธ AI อย่างชัดเจน", bold_prefix="• ")

    add_h2("ข้อมูลกลุ่มและเครื่องมือที่ใช้ (Group Details)")
    tbl_grp_info = doc.add_table(rows=6, cols=2)
    tbl_grp_info.rows[0].cells[0].paragraphs[0].add_run("รายการ")
    tbl_grp_info.rows[0].cells[1].paragraphs[0].add_run("รายละเอียดข้อมูลของกลุ่ม")

    info_data = [
        ("รายวิชาและตอนเรียน", "รายวิชา Database Mini Project / ระบบฐานข้อมูล (Database Systems)"),
        ("ชื่อโครงงาน", "ระบบร้านขายหนังสือและอีบุ๊กออนไลน์ (E-Book Store Online Management System)"),
        ("สมาชิกคนที่ 1", "นายสุรวัจน์ ชลเรืองทรัพย์   รหัสนักศึกษา: 67332110217-1"),
        ("สมาชิกคนที่ 2", "นายสรวิชญ์ มีมาก   รหัสนักศึกษา: 67332110275-8"),
        ("เครื่องมือที่ใช้พัฒนา", "ภาษา: JavaScript (Node.js v24.x, Express.js v5.2.1)\nDBMS: PostgreSQL (Neon Serverless Cloud Database)\nเฟรมเวิร์ก & ไลบรารี: Express.js, node-postgres (pg), express-session, Tailwind CSS\nเครื่องมือรายงาน: SQL Aggregate Queries, CSV Export (UTF-8 BOM)")
    ]
    for idx, (k, v) in enumerate(info_data, start=1):
        tbl_grp_info.rows[idx].cells[0].paragraphs[0].add_run(k)
        tbl_grp_info.rows[idx].cells[1].paragraphs[0].add_run(v)
    style_table(tbl_grp_info, [Inches(2.2), Inches(4.3)], [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT], header_bg="2563EB")

    add_callout("คำแนะนำก่อนเริ่มงานตามใบงาน", "เลือกขอบเขตที่กลุ่มพัฒนาและสาธิตได้จริง ใช้ข้อมูลตัวอย่างที่สมเหตุสมผล และเก็บหลักฐานการทำงานไว้สำหรับการนำเสนออย่างเป็นระบบ", box_type="info")

    doc.add_page_break()

    # =========================================================================
    # 3. สารบัญ (TABLE OF CONTENTS)
    # =========================================================================
    add_h1("สารบัญ (Table of Contents)")
    tbl_toc = doc.add_table(rows=1, cols=2)
    tbl_toc.rows[0].cells[0].paragraphs[0].add_run("ลำดับบท / หัวข้อรายงาน")
    tbl_toc.rows[0].cells[1].paragraphs[0].add_run("หน้า")

    toc_items = [
        ("บทสรุปผู้บริหาร (Executive Summary)", "i"),
        ("บทที่ 1: บทนำและวัตถุประสงค์ของโครงงาน", "1"),
        ("  1.1 ที่มาและความสำคัญของปัญหา", "1"),
        ("  1.2 วัตถุประสงค์ของโครงงาน (สอดคล้องตามใบงาน)", "2"),
        ("  1.3 ขอบเขตของระบบ (System Scope: หน้าร้าน หลังบ้าน และความปลอดภัย)", "2"),
        ("  1.4 ขอบเขตที่ไม่บังคับ (Non-mandatory Scope)", "4"),
        ("  1.5 สถาปัตยกรรมและเทคโนโลยีที่ใช้พัฒนา (Technology Stack)", "4"),
        ("บทที่ 2: การวิเคราะห์และออกแบบฐานข้อมูล (Database Analysis & Design)", "5"),
        ("  2.1 ผังความสัมพันธ์ข้อมูล (Entity-Relationship Diagram: ERD) และ Cardinality", "5"),
        ("  2.2 ทฤษฎีการปรับรูปบรรทัดฐาน (Database Normalization to 3NF)", "7"),
        ("  2.3 พจนานุกรมข้อมูลฉบับสมบูรณ์ 9 ตาราง (Data Dictionary)", "9"),
        ("บทที่ 3: การสร้างฐานข้อมูลและข้อกำหนดบูรณภาพข้อมูล (Implementation & Constraints)", "14"),
        ("  3.1 DDL Scripts และการสร้างตารางบน PostgreSQL (Neon Cloud)", "14"),
        ("  3.2 ข้อกำหนดบูรณภาพข้อมูล (Integrity Constraints & Referential Actions)", "16"),
        ("  3.3 ข้อมูลตัวอย่างทดสอบระบบจริงในฐานข้อมูล (Seed Data มากกว่า 30 คำสั่งซื้อ)", "17"),
        ("บทที่ 4: รายงานวิเคราะห์ข้อมูลเชิงลึกจากฐานข้อมูลจริง 4 ด้าน (Analytics Reports)", "18"),
        ("  4.1 รายงานที่ 1: ยอดขายตามช่วงเวลา (Sales Over Time by Date)", "18"),
        ("  4.2 รายงานที่ 2: E-Book ขายดีที่สุด 5 อันดับแรก (Top-Selling Books)", "20"),
        ("  4.3 รายงานที่ 3: ยอดขายตามหมวดหมู่หนังสือ (Sales by Category)", "22"),
        ("  4.4 รายงานที่ 4: พฤติกรรมลูกค้าและยอดซื้อสะสม (Customer Lifetime Spending)", "24"),
        ("บทที่ 5: การพัฒนาเว็บแอปพลิเคชันและการควบคุมความปลอดภัย (Application & Security)", "26"),
        ("  5.1 การยืนยันตัวตนและวงจรตะกร้าสินค้า (Authentication & Cart Lifecycle)", "26"),
        ("  5.2 กระบวนการสั่งซื้อ ชำระเงินจำลอง และ Database Transaction (ACID)", "27"),
        ("  5.3 ระบบความปลอดภัยการดาวน์โหลดไฟล์ดิจิทัล (Digital Asset Access Control)", "28"),
        ("  5.4 ระบบควบคุมสิทธิ์ผู้ดูแลระบบ (Role-Based Access Control: RBAC & Route Guard)", "29"),
        ("  5.5 ระบบบริหารหลังบ้าน และการส่งออกรายงาน CSV มาตรฐานภาษาไทย (UTF-8 BOM)", "30"),
        ("บทที่ 6: การทดสอบระบบและการประกันคุณภาพข้อมูล (Testing & Quality Assurance)", "31"),
        ("  ตารางบันทึกผลการทดสอบระบบ 8 กรณีตามเกณฑ์ใบงานข้อ 6 (TC-01 - TC-08)", "31"),
        ("บทที่ 7: ขั้นตอนดำเนินงานและการทำงานเป็นกลุ่ม (Workflow & Collaboration)", "33"),
        ("  7.1 ขั้นตอนดำเนินงาน 6 ระยะ (วิเคราะห์, ออกแบบ, พัฒนา, ปรับปรุง, รายงาน, นำเสนอ)", "33"),
        ("  7.2 การแบ่งหน้าที่การทำงานเป็นกลุ่ม (สุรวัจน์ ชลเรืองทรัพย์ & สรวิชญ์ มีมาก)", "34"),
        ("  7.3 รายการสิ่งที่ต้องส่ง (Submission Deliverables Checklist)", "35"),
        ("บทที่ 8: การประยุกต์ใช้ปัญญาประดิษฐ์อย่างรับผิดชอบ (Responsible AI Usage Log)", "36"),
        ("  8.1 กรอบแนวทางการใช้งาน AI (อนุญาต, ต้องปฏิบัติ, ห้ามทำ)", "36"),
        ("  8.2 บันทึกการใช้งาน AI ในการพัฒนา (AI Prompt & Usage Log)", "37"),
        ("  8.3 ข้อเสนอแนะของ AI ที่กลุ่มตัดสินใจปฏิเสธตามหลักวิศวกรรม (Rejected AI Proposals)", "38"),
        ("  8.4 การคำนึงถึงความเป็นส่วนตัวของข้อมูลตามกฎหมาย (PDPA Consideration)", "39"),
        ("บทที่ 9: เกณฑ์การประเมินตนเองและสรุปผลโครงงาน (Self-Assessment & Conclusion)", "40"),
        ("  9.1 ตารางประเมินผลการดำเนินงานเทียบเกณฑ์ 100 คะแนนเต็ม", "40"),
        ("  9.2 สรุปผลสัมฤทธิ์และข้อเสนอแนะในการพัฒนาต่อยอด", "41"),
        ("ภาคผนวก (Appendices)", "42"),
        ("  ภาคผนวก ก: รายการตรวจสอบความพร้อมก่อนส่งงาน (Checklist) และใบลงนามรับรอง", "42"),
        ("  ภาคผนวก ข: แบบฟอร์มบันทึกการประเมินของผู้สอน (Evaluation Form)", "43"),
        ("  ภาคผนวก ค: ข้อมูลบัญชีผู้ใช้สำหรับทดสอบ และวิธีเปิดใช้งานระบบ", "44")
    ]
    for title, pg in toc_items:
        row = tbl_toc.add_row()
        row.cells[0].paragraphs[0].add_run(title)
        row.cells[1].paragraphs[0].add_run(pg)
    style_table(tbl_toc, [Inches(5.7), Inches(0.8)], [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER], header_bg="1E3A8A")

    doc.add_page_break()

    # =========================================================================
    # 4. บทสรุปผู้บริหาร (EXECUTIVE SUMMARY)
    # =========================================================================
    add_h1("บทสรุปผู้บริหาร (Executive Summary)")
    add_p("โครงงานพัฒนาระบบฐานข้อมูล \"ร้านขายหนังสือและอีบุ๊กออนไลน์ (E-Book Store Online Management System)\" ในโฟลเดอร์โปรเจกต์ ebook-store ได้รับการออกแบบและพัฒนาขึ้นเพื่อประยุกต์ใช้ทฤษฎีระบบจัดการฐานข้อมูลเชิงสัมพันธ์ (Relational Database Management Systems: RDBMS) ให้ตอบโจทย์กระบวนการซื้อขายและส่งมอบสินค้าดิจิทัลในสถานการณ์จริง ตรงตามเกณฑ์การประเมิน 100 คะแนนเต็มของรายวิชาระบบฐานข้อมูล")
    add_p("ระบบทำงานร่วมกับฐานข้อมูล PostgreSQL บนระบบคลาวด์ Neon Serverless Cloud Platform ผ่านโครงสร้างฐานข้อมูลเชิงสัมพันธ์ที่ออกแบบอย่างถูกต้องตามหลักเกณฑ์การปรับรูปบรรทัดฐานระดับ Third Normal Form (3NF) จำนวนทั้งสิ้น 9 ตาราง ประกอบด้วย roles, users, authors, categories, ebooks, carts, cart_items, orders, และ order_items")

    add_h2("จุดเด่นเชิงวิศวกรรมและผลสัมฤทธิ์ของระบบ")
    add_bullet("ความถูกต้องตามหลักการ 3NF: ขจัดปัญหาความซ้ำซ้อนของข้อมูล และแยกตาราง order_items พร้อมฟิลด์ price_at_purchase เพื่อบันทึกราคาซื้อขายประวัติศาสตร์อย่างถาวร ป้องกันปัญหาการแก้ไขราคาหนังสือในปัจจุบันแล้วกระทบยอดรวมในอดีต", bold_prefix="1. ")
    add_bullet("ความปลอดภัยของสินค้าดิจิทัล (Digital Content Protection): สอดคล้องตามข้อกำหนดใบงานข้อ 2.2 ระบบล็อกไฟล์หนังสือสำหรับคำสั่งซื้อที่อยู่ในสถานะรอตรวจสอบ (pending) และจะปลดล็อกให้เปิดอ่าน/ดาวน์โหลดไฟล์ได้เฉพาะเมื่อแอดมินยืนยันคำสั่งซื้อ (confirmed) เท่านั้น หากพยายามเข้าถึงไฟล์ผ่าน URL ตรง ระบบจะตรวจสอบสิทธิ์ในระดับ SQL และปฏิเสธด้วยรหัส HTTP 403 Forbidden", bold_prefix="2. ")
    add_bullet("ระบบควบคุมสิทธิ์ระดับเซิร์ฟเวอร์ (RBAC & Route Guard): ผู้ใช้ทั่วไปจะถูกซ่อนเมนูจัดการร้าน และมี Middleware ดักจับการเข้าถึง URL เส้นทาง /admin/* โดยส่งข้อความปฏิเสธสิทธิ์ทันที", bold_prefix="3. ")
    add_bullet("การประมวลผลข้อมูลจริงมากกว่า 30 คำสั่งซื้อ: ระบบมีข้อมูลธุรกรรมในฐานข้อมูลจริงรวม 35 คำสั่งซื้อ (Orders) แบ่งเป็นสถานะ confirmed 29 รายการ, pending 3 รายการ, และ cancelled 3 รายการ มีรายการสินค้ารวม 54 รายการ มียอดขายสุทธิรวมทั้งสิ้น 16,500.00 บาท", bold_prefix="4. ")
    add_bullet("รายงานวิเคราะห์ธุรกิจ 4 ด้าน: พัฒนา Aggregate Query ด้วยคำสั่ง SQL สดผ่านหน้าจอ /reports ครอบคลุมยอดขายตามช่วงเวลา, 5 อันดับหนังสือขายดี, สรุปยอดขายตามหมวดหมู่, และยอดซื้อสะสมของลูกค้า พร้อมปุ่ม Export CSV ที่ฝังรหัส UTF-8 BOM ทำให้เปิดอ่านภาษาไทยใน Microsoft Excel ได้อย่างถูกต้อง ไม่เกิดปัญหาภาษาต่างดาว", bold_prefix="5. ")
    add_bullet("การประยุกต์ใช้ AI อย่างรับผิดชอบ: บันทึกประวัติการใช้ AI ครบถ้วน พร้อมระบุเหตุผลทางวิศวกรรม 3 ประเด็นที่ผู้พัฒนาตัดสินใจปฏิเสธคำแนะนำของ AI เพื่อคงไว้ซึ่งความปลอดภัยและความถูกต้องของฐานข้อมูล", bold_prefix="6. ")

    doc.add_page_break()

    # =========================================================================
    # 5. บทที่ 1: บทนำและวัตถุประสงค์ของโครงงาน
    # =========================================================================
    add_h1("บทที่ 1: บทนำและขอบเขตโครงงาน (Introduction & Scope)")
    
    add_h2("1.1 ที่มาและความสำคัญของปัญหา (Problem Statement)")
    add_p("ในยุคปัจจุบัน พฤติกรรมการอ่านของผู้บริโภคได้เปลี่ยนผ่านเข้าสู่รูปแบบดิจิทัลอย่างรวดเร็ว หนังสืออิเล็กทรอนิกส์ (E-Book) จึงกลายเป็นสื่อการเรียนรู้และสินค้าที่ได้รับความนิยมสูง อย่างไรก็ตาม การพัฒนาระบบพาณิชย์อิเล็กทรอนิกส์สำหรับสินค้าประเภท E-Book มีความท้าทายที่แตกต่างจากการจำหน่ายสินค้าทั่วไปอย่างมีนัยสำคัญ:")
    add_bullet("สินค้าดิจิทัลไม่มีสต็อกทางกายภาพที่หมดไป แต่การบันทึกรายการคำสั่งซื้อจำเป็นต้องตรึงราคา ณ เวลาที่สั่งซื้อ (price_at_purchase) เพื่อความถูกต้องทางบัญชี", bold_prefix="• ด้านคลังสินค้าและราคาประวัติศาสตร์: ")
    add_bullet("ต้องมีกลไกป้องกันไม่ให้ผู้ใช้เข้าถึงไฟล์ E-Book ก่อนการยืนยันการชำระเงิน และต้องป้องกันไม่ให้ผู้ใช้คนอื่นแอบอ้างลิงก์ดาวน์โหลดของผู้อื่น", bold_prefix="• ด้านความปลอดภัยในการเข้าถึงเนื้อหา (Access Control): ")
    add_bullet("ต้องแยกระหว่างลูกค้าทั่วไปและผู้ดูแลร้านค้าอย่างเด็ดขาด ทั้งในระดับหน้าจอติดต่อผู้ใช้ (UI) และระดับตัวควบคุมคำสั่ง (Route Controller)", bold_prefix="• ด้านการควบคุมสิทธิ์ผู้ใช้งาน (Authorization): ")
    add_bullet("ข้อมูลธุรกรรมที่เกิดขึ้นต้องถูกจัดเก็บอย่างเป็นระเบียบตามมาตรฐาน เพื่อให้สามารถประมวลผล Aggregate Metrics เช่น ยอดขายรายวัน สินค้าขายดี และพฤติกรรมลูกค้าได้อย่างรวดเร็ว", bold_prefix="• ด้านการวิเคราะห์ข้อมูลเชิงธุรกิจ (Business Intelligence): ")
    add_p("ด้วยเหตุนี้ โครงงาน ebook-store จึงมุ่งเน้นการวิเคราะห์และออกแบบฐานข้อมูลเชิงสัมพันธ์ให้มีความสมบูรณ์ตามหลัก Normalization ระดับ 3NF พร้อมทั้งพัฒนาเว็บแอปพลิเคชันต้นแบบที่เชื่อมโยงกับฐานข้อมูลจริงบน Neon Cloud เพื่อพิสูจน์การทำงานของระบบอย่างรอบด้าน")

    add_h2("1.2 วัตถุประสงค์ของโครงงาน (Project Objectives)")
    add_bullet("เพื่อออกแบบโครงสร้างฐานข้อมูลเชิงสัมพันธ์ที่สัมพันธ์กับกระบวนการขาย E-Book อย่างถูกต้อง ครบถ้วนตามมาตรฐาน 3NF ไม่น้อยกว่า 8 ตาราง (โครงงานนี้พัฒนา 9 ตาราง)", bold_prefix="1. ")
    add_bullet("เพื่อพัฒนาระบบเว็บแอปพลิเคชันต้นแบบ (Prototype) ด้วย Node.js / Express.js เชื่อมโยงกับฐานข้อมูล PostgreSQL บน Neon Cloud Platform ได้จริง", bold_prefix="2. ")
    add_bullet("เพื่อจำลองเส้นทางการใช้งานของลูกค้า (Customer Journey) ตั้งแต่สมัครสมาชิก ค้นหาหนังสือ ใส่ตะกร้า ชำระเงินจำลอง และเปิดอ่านไฟล์หนังสือที่ยืนยันแล้ว", bold_prefix="3. ")
    add_bullet("เพื่อพัฒนาระบบบริหารจัดการร้านค้าหลังบ้าน (Admin Backoffice) สำหรับผู้ดูแลระบบ พร้อมระบบ Route Guard ป้องกันการละเมิดสิทธิ์", bold_prefix="4. ")
    add_bullet("เพื่อเขียนคำสั่ง SQL วิเคราะห์ข้อมูลจริงในระบบ 4 ด้าน และพัฒนาระบบส่งออกข้อมูลสรุปยอดขายเป็นไฟล์ CSV รองรับภาษาไทย", bold_prefix="5. ")
    add_bullet("เพื่อฝึกฝนการประยุกต์ใช้ปัญญาประดิษฐ์ (AI) ในการออกแบบและเขียนโค้ดอย่างมีความรับผิดชอบ โปร่งใส และเปิดเผยตามจรรยาบรรณวิชาชีพ", bold_prefix="6. ")

    add_h2("1.3 ขอบเขตของระบบ (System Scope)")
    add_h3("1.3.1 ขอบเขตส่วนหน้าร้านสำหรับลูกค้า (Customer Portal - สอดคล้องตามข้อ 2.1 ของใบงาน)")
    
    tbl_scope_front = doc.add_table(rows=8, cols=2)
    tbl_scope_front.rows[0].cells[0].paragraphs[0].add_run("หัวข้อตามใบงาน")
    tbl_scope_front.rows[0].cells[1].paragraphs[0].add_run("ความสามารถขั้นต่ำที่พัฒนาระบบจริงและสาธิตได้")
    
    front_scope = [
        ("สมาชิก", "สมัครสมาชิกใหม่ (/register), เข้าสู่ระบบ (/login), แก้ไขข้อมูลพื้นฐาน (/profile), และดูประวัติคำสั่งซื้อ (/my-orders)"),
        ("รายการ E Book", "แสดงชื่อหนังสือ, ผู้แต่ง, ราคา, หมวดหมู่, คำอธิบายเนื้อหา, ภาพปกหนังสือ, และสถานะความพร้อมจำหน่าย (is_active)"),
        ("ค้นหาและคัดกรอง", "ค้นหาหนังสือด้วยชื่อเรื่องหรือคีย์เวิร์ด (คำสั่ง SQL ILIKE) และระบบกรองหนังสือตามหมวดหมู่อย่างน้อย 4 หมวดหมู่"),
        ("ตะกร้าสินค้า", "เพิ่มหนังสือลงตะกร้า, ปรับเพิ่ม-ลดจำนวน (quantity), ลบรายการออกจากตะกร้า, และคำนวณยอดรวมสุทธิก่อนสั่งซื้อแบบ Real-time"),
        ("คำสั่งซื้อ", "บันทึกข้อมูลลงตารางคำสั่งซื้อหลัก (orders), บันทึกรายการย่อย (order_items), ตรึงราคาซื้อขาย (price_at_purchase), และบันทึกสถานะเริ่มต้นเป็น 'pending'"),
        ("ชำระเงินแบบจำลอง", "ระบบแสดงแบบฟอร์มให้ผู้ใช้เลือกแนบหลักฐานสลิปโอนเงิน PromptPay จำลอง โดยไม่มีการขอข้อมูลบัตรเครดิตหรือบัญชีธนาคารจริง"),
        ("ดาวน์โหลด", "แสดงปุ่มเปิดอ่าน/ดาวน์โหลดเฉพาะหนังสือที่อยู่ในคำสั่งซื้อที่มีสถานะ 'confirmed' เท่านั้น สำหรับคำสั่งซื้อที่รออนุมัติจะแสดงปุ่มล็อกไฟล์")
    ]
    for idx, (k, v) in enumerate(front_scope, start=1):
        tbl_scope_front.rows[idx].cells[0].paragraphs[0].add_run(k)
        tbl_scope_front.rows[idx].cells[1].paragraphs[0].add_run(v)
    style_table(tbl_scope_front, [Inches(1.8), Inches(4.7)], [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT], header_bg="1E3A8A")

    add_h3("1.3.2 เงื่อนไขการส่งสินค้าและความปลอดภัยของเนื้อหาดิจิทัล (สอดคล้องตามข้อ 2.2 ของใบงาน)")
    add_bullet("ลิงก์ดาวน์โหลดของหนังสือเป็น URL ไฟล์เอกสาร PDF จำลองที่ได้รับอนุญาตให้ใช้ในการเรียนการสอนอย่างถูกต้อง", bold_prefix="• รูปแบบไฟล์และลิงก์: ")
    add_bullet("ระบบไม่มีการจัดเก็บไฟล์ DRM หรือเกตเวย์ชำระเงินจริง แต่ใช้กลไกการควบคุมเงื่อนไขการเข้าถึงในระดับข้อมูล (Database Query Verification) และระดับเซิร์ฟเวอร์ (Route Middleware)", bold_prefix="• การควบคุมสิทธิ์: ")
    add_bullet("ระบบต้องไม่เปิดลิงก์ของหนังสือที่ลูกค้ายังไม่ได้ซื้อ หรือคำสั่งซื้อยังไม่ได้รับการยืนยัน หากลูกค้าพยายามพิมพ์ URL ตรง ระบบจะตอบกลับด้วยรหัส 403 Forbidden ทันที", bold_prefix="• กฎความปลอดภัยเคร่งครัด: ")

    add_h3("1.3.3 ขอบเขตส่วนระบบบริหารจัดการร้านค้าหลังบ้าน (Admin Backoffice - สอดคล้องตามข้อ 3 ของใบงาน)")
    tbl_scope_back = doc.add_table(rows=6, cols=2)
    tbl_scope_back.rows[0].cells[0].paragraphs[0].add_run("งานผู้ดูแลร้าน (Admin Task)")
    tbl_scope_back.rows[0].cells[1].paragraphs[0].add_run("สิ่งที่ระบบพัฒนาจริงและทำได้")
    
    back_scope = [
        ("จัดการ E Book", "เพิ่มหนังสือใหม่, แก้ไขข้อมูลหนังสือ, ปรับราคา, อัปเดตลิงก์ดาวน์โหลด, และปุ่มสลับสถานะเปิดขาย/ปิดขาย (Soft Delete: is_active)"),
        ("จัดการหมวดหมู่", "เพิ่มหมวดหมู่ใหม่, แก้ไขชื่อหมวดหมู่, และระบบป้องกันการลบหมวดหมู่ที่มีหนังสือผูกอยู่ (Integrity Check)"),
        ("จัดการคำสั่งซื้อ", "ค้นหาคำสั่งซื้อ, ดูรายละเอียดรายการย่อย, ตรวจสอบภาพสลิปจำลอง, และเปลี่ยนสถานะคำสั่งซื้อเป็น รอชำระ (pending), ยืนยันแล้ว (confirmed), หรือ ยกเลิก (cancelled)"),
        ("จัดการผู้ใช้", "ดูรายชื่อสมาชิกในระบบ, ตรวจสอบอีเมล, และปุ่มสลับบทบาทระหว่างลูกค้า (customer) และผู้ดูแลระบบ (admin)"),
        ("รายงานและวิเคราะห์", "หน้า Dashboard สรุปยอดขายรวม, รายงานวิเคราะห์ 4 ด้านด้วยคำสั่ง SQL และปุ่ม Export สรุปยอดขายเป็นไฟล์ CSV รองรับภาษาไทย")
    ]
    for idx, (k, v) in enumerate(back_scope, start=1):
        tbl_scope_back.rows[idx].cells[0].paragraphs[0].add_run(k)
        tbl_scope_back.rows[idx].cells[1].paragraphs[0].add_run(v)
    style_table(tbl_scope_back, [Inches(2.0), Inches(4.5)], [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT], header_bg="2563EB")

    add_h2("1.4 ขอบเขตที่ไม่บังคับ (Out of Scope - สอดคล้องตามข้อ 7 ของใบงาน)")
    add_p("เพื่อให้คณะผู้จัดทำสามารถทุ่มเทเวลาให้กับการออกแบบฐานข้อมูลเชิงลึก การจัดทำ 3NF การเขียนคำสั่งสืบค้น SQL และรายงานวิเคราะห์ได้อย่างเต็มประสิทธิภาพ ส่วนงานต่อไปนี้จึงถูกกำหนดให้อยู่นอกเหนือขอบเขตบังคับตามที่ใบงานระบุ:")
    add_bullet("การเชื่อมต่อระบบตัดบัตรเครดิตหรือธนาคารจริง (ใช้ระบบจำลองแนบสลิป QR Code แทน)", bold_prefix="1. การชำระเงินจริง: ")
    add_bullet("ระบบการเข้ารหัสไฟล์ขั้นสูงหรือลายน้ำดิจิทัล (ใช้ระบบควบคุมสิทธิ์ระดับ SQL/Route Guard แทน)", bold_prefix="2. การจัดเก็บไฟล์ DRM: ")
    add_bullet("ระบบ Machine Learning แนะนำหนังสือตามประวัติการซื้อ (จัดเป็นส่วนเสริมในอนาคต)", bold_prefix="3. ระบบแนะนำหนังสืออัตโนมัติ: ")
    add_bullet("การส่งข้อความผ่าน SMTP Server จริง (ใช้การแสดงลิงก์บนหน้าจอ /my-orders แทน)", bold_prefix="4. การส่งอีเมลแจ้งเตือน: ")
    add_bullet("การพัฒนา Native Mobile App (ระบบพัฒนาแบบ Responsive Web Application บนเบราว์เซอร์)", bold_prefix="5. แอปพลิเคชันมือถือ: ")

    add_h2("1.5 สถาปัตยกรรมและเทคโนโลยีที่ใช้พัฒนา (Technology Stack)")
    add_p("สถาปัตยกรรมของระบบได้รับการออกแบบเป็น 3-Tier Architecture ที่มีความเสถียรและยืดหยุ่นสูง:")

    code_arch = """+-----------------------------------------------------------------------+
|                       Client Tier (Web Browser)                       |
|   HTML5, Responsive UI with Tailwind CSS, EJS Rendering, Fetch API   |
+-----------------------------------------------------------------------+
                                   | (HTTP Requests / Form Data)
                                   v
+-----------------------------------------------------------------------+
|                    Application Tier (Express.js Server)               |
|   - Session Guard Middleware (Authentication & Role Verification)     |
|   - routes/auth.js      : Login, Register, Profile                    |
|   - routes/shop.js      : Catalog, Cart, Transactional Checkout       |
|   - routes/admin.js     : CRUD Backoffice, Order Confirm, Route Guard |
|   - routes/reports.js   : 4 Analytics SQL Queries & UTF-8 BOM CSV     |
+-----------------------------------------------------------------------+
                                   | (node-postgres Connection Pool)
                                   v
+-----------------------------------------------------------------------+
|                  Database Tier (PostgreSQL on Neon Cloud)              |
|   - 9 Relational Tables with Full 3NF Compliance                      |
|   - ACID Transactions (BEGIN / COMMIT / ROLLBACK)                     |
|   - Primary & Foreign Key Constraints, CHECK, NOT NULL, UNIQUE        |
+-----------------------------------------------------------------------+"""
    add_code_block(code_arch)

    tbl_tech = doc.add_table(rows=7, cols=3)
    tbl_tech.rows[0].cells[0].paragraphs[0].add_run("องค์ประกอบ")
    tbl_tech.rows[0].cells[1].paragraphs[0].add_run("เทคโนโลยีที่เลือกใช้")
    tbl_tech.rows[0].cells[2].paragraphs[0].add_run("เหตุผลและความสำคัญทางวิศวกรรม")

    tech_data = [
        ("Database Management System", "PostgreSQL (Neon Serverless Cloud)", "ฐานข้อมูลเชิงสัมพันธ์ระดับ Enterprise รองรับ ACID, Constraints, Sequences, Indexes และ Aggregate Functions ขั้นสูง"),
        ("Server Runtime & Framework", "Node.js (v24.x) & Express.js (v5.2.1)", "สถาปัตยกรรม Non-blocking I/O แบบ Event-driven ทำงานร่วมกับ Database Connection Pooling ได้อย่างรวดเร็ว"),
        ("Authentication & Session", "express-session (v1.19.0)", "จัดการสถานะการเข้าสู่ระบบฝั่งเซิร์ฟเวอร์อย่างปลอดภัย พร้อมเก็บสิทธิ์ role_name ป้องกันการปลอมแปลง"),
        ("Database Driver", "pg (node-postgres v8.23.0)", "เชื่อมต่อไปยัง Neon PostgreSQL ผ่าน SSL Connection Pool จัดการ Query และ Transactions ได้อย่างมีเสถียรภาพ"),
        ("Frontend Styling", "Tailwind CSS (CDN)", "ออกแบบหน้าจอให้มีความสวยงาม สไตล์ Modern Minimalist รองรับการใช้งานทั้งบนคอมพิวเตอร์และแท็บเล็ต"),
        ("Report Export Format", "CSV with UTF-8 BOM (\\uFEFF)", "เข้ารหัสไฟล์ส่งออกรายงานยอดขายด้วย Byte Order Mark เพื่อให้เปิดใน Microsoft Excel ภาษาไทยได้คมชัด 100%")
    ]
    for idx, (c1, c2, c3) in enumerate(tech_data, start=1):
        tbl_tech.rows[idx].cells[0].paragraphs[0].add_run(c1)
        tbl_tech.rows[idx].cells[1].paragraphs[0].add_run(c2)
        tbl_tech.rows[idx].cells[2].paragraphs[0].add_run(c3)
    style_table(tbl_tech, [Inches(1.8), Inches(2.2), Inches(2.5)], [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT], header_bg="1E3A8A")

    doc.add_page_break()

    # =========================================================================
    # 6. บทที่ 2: การวิเคราะห์และออกแบบฐานข้อมูล
    # =========================================================================
    add_h1("บทที่ 2: การวิเคราะห์และออกแบบฐานข้อมูล (Database Analysis & Design)")
    
    add_h2("2.1 โครงสร้างผังความสัมพันธ์ข้อมูล (Entity-Relationship Diagram: ERD)")
    add_p("ฐานข้อมูลของโปรเจกต์ ebook-store ประกอบด้วยตารางเชิงสัมพันธ์จำนวน 9 ตาราง สอดคล้องตามเกณฑ์ใบงานข้อ 4 ที่กำหนดขั้นต่ำไม่น้อยกว่า 8 ตาราง โดยออกแบบโครงสร้างความสัมพันธ์ตามมาตรฐานสัญลักษณ์ Crow's Foot Notation แสดงคีย์หลัก (Primary Key: PK), คีย์นอก (Foreign Key: FK), ชนิดข้อมูลของแต่ละคอลัมน์, และภาระงาน (Cardinality) ครบถ้วนดังแสดงในภาพ:")

    erd_path = "images/erd_crows_foot.png" if os.path.exists("images/erd_crows_foot.png") else "generated_charts/erd_diagram.png"
    if os.path.exists(erd_path):
        p_pic = doc.add_paragraph()
        p_pic.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_pic.paragraph_format.space_before = Pt(6)
        p_pic.paragraph_format.space_after = Pt(4)
        run_pic = p_pic.add_run()
        run_pic.add_picture(erd_path, width=Inches(5.35))
        
        p_cap = add_p("รูปที่ 2.1: ผังความสัมพันธ์ข้อมูลเชิงสัมพันธ์สัญลักษณ์ Crow's Foot (ERD) ระบบ E-Book Store (3NF Schema 9 ตาราง)", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=8)
        p_cap.runs[0].font.size = Pt(11)
        p_cap.runs[0].font.italic = True
        p_cap.runs[0].font.color.rgb = RGBColor(100, 116, 139)
        p_cap.paragraph_format.keep_with_next = True

    doc.add_page_break()

    add_h3("2.1.1 สรุปคำอธิบายความสัมพันธ์และภาระงาน (Cardinality Rules ทั้ง 9 ตาราง)")
    card_rules = [
        ("roles (1) <---> (N) users", "บทบาทหนึ่งบทบาท (customer, admin) สามารถกำหนดให้ผู้ใช้งานได้หลายคน เชื่อมด้วย roles.role_id = users.role_id"),
        ("users (1) <---> (0..1) carts", "ผู้ใช้แต่ละคนมีตะกร้าสินค้าประจำตัวได้สูงสุด 1 ใบ หรือยังไม่มีก็ได้ เชื่อมด้วย users.user_id = carts.user_id"),
        ("carts (1) <---> (N) cart_items", "ตะกร้าสินค้า 1 ใบ สามารถบรรจุรายการหนังสือที่เตรียมสั่งซื้อได้หลายเล่ม เชื่อมด้วย carts.cart_id = cart_items.cart_id"),
        ("ebooks (1) <---> (N) cart_items", "หนังสือ 1 เล่ม สามารถปรากฏอยู่ในตะกร้าสินค้าของผู้ใช้หลายคนพร้อมกันได้ เชื่อมด้วย ebooks.ebook_id = cart_items.ebook_id"),
        ("authors (1) <---> (N) ebooks", "นักเขียน 1 ท่าน สามารถมีผลงานหนังสือในระบบได้หลายเล่ม เชื่อมด้วย authors.author_id = ebooks.author_id"),
        ("categories (1) <---> (N) ebooks", "หมวดหมู่หนังสือ 1 หมวด สามารถจัดเก็บหนังสือได้หลายเล่ม เชื่อมด้วย categories.category_id = ebooks.category_id"),
        ("users (1) <---> (N) orders", "สมาชิก 1 คน สามารถสร้างคำสั่งซื้อได้หลายครั้งในระบบ เชื่อมด้วย users.user_id = orders.user_id"),
        ("orders (1) <---> (1..N) order_items", "คำสั่งซื้อ 1 คำสั่งซื้อ ประกอบด้วยรายการหนังสือย่อยที่สั่งซื้ออย่างน้อย 1 รายการขึ้นไป เชื่อมด้วย orders.order_id = order_items.order_id"),
        ("ebooks (1) <---> (N) order_items", "หนังสือแต่ละเล่มสามารถถูกสั่งซื้อซ้ำในรายการย่อยของคำสั่งซื้อต่าง ๆ ได้หลายครั้ง เชื่อมด้วย ebooks.ebook_id = order_items.ebook_id")
    ]
    for title, desc in card_rules:
        add_bullet(desc, bold_prefix=f"{title}: ")

    add_h2("2.2 ทฤษฎีการปรับรูปบรรทัดฐานฐานข้อมูล (Database Normalization to 3NF)")
    add_p("การจัดโครงสร้างฐานข้อมูลของระบบ ebook-store ได้รับการออกแบบตามกระบวนการปรับรูปบรรทัดฐานอย่างเป็นระบบ ตั้งแต่ระดับก่อนบรรทัดฐานจนถึงรูปแบบบรรทัดฐานขั้นที่สาม (3NF):")

    add_h3("1. รูปแบบก่อนบรรทัดฐาน (Unnormalized Form: UNF)")
    add_p("หากเก็บข้อมูลกระบวนการขาย E-Book ไว้ในตารางรวมเพียงตารางเดียว เช่น:")
    add_code_block("Order_Flat(order_id, user_id, username, full_name, role_name, book_titles, authors, categories, prices, quantities, total_amount, order_status, slip_url)")
    add_bullet("เกิดกลุ่มข้อมูลซ้ำซ้อน (Repeating Groups) ในส่วนของหนังสือ ผู้แต่ง และหมวดหมู่ ทำให้เกิดความซ้ำซ้อนของข้อมูลอย่างรุนแรง", bold_prefix="• ข้อบกพร่อง: ")
    add_bullet("เกิดปัญหาความผิดปกติในการจัดการข้อมูล (Anomalies): Insertion Anomaly (ไม่สามารถเพิ่มหนังสือใหม่ได้หากยังไม่มีการสั่งซื้อ), Deletion Anomaly (หากลบคำสั่งซื้อ ข้อมูลหนังสือหรือผู้แต่งอาจหายไปจากระบบ), และ Update Anomaly (หากเปลี่ยนชื่อผู้แต่ง ต้องตามแก้ทุกคำสั่งซื้อ)", bold_prefix="• ผลกระทบ: ")

    add_h3("2. รูปแบบบรรทัดฐานขั้นที่ 1 (First Normal Form: 1NF)")
    add_bullet("ทุกคอลัมน์ต้องเก็บค่าที่เป็นค่าเดี่ยว (Atomic Values) ไม่มีการเก็บชุดข้อมูลอาร์เรย์ และต้องไม่มีกลุ่มข้อมูลซ้ำ (No Repeating Groups) โดยมี Primary Key กำหนดเอกลักษณ์ของแต่ละแถว", bold_prefix="• หลักเกณฑ์: ")
    add_bullet("แยกแถวข้อมูลสินค้าในคำสั่งซื้อออกมาเป็นแต่ละแถวเดี่ยว ทำให้ไม่มีค่าหลายค่าในคอลัมน์เดียว และกำหนด Primary Key ให้แก่ทุกตาราง", bold_prefix="• การดำเนินการ: ")

    add_h3("3. รูปแบบบรรทัดฐานขั้นที่ 2 (Second Normal Form: 2NF)")
    add_bullet("ต้องผ่านเกณฑ์ 1NF และทุกแอตทริบิวต์ที่ไม่ใช่คีย์หลัก (Non-Key Attributes) ต้องขึ้นตรงต่อคีย์หลักทั้งหมดแบบสมบูรณ์ (Full Functional Dependency) ต้องไม่มีการขึ้นต่อคีย์หลักเพียงบางส่วน (No Partial Dependency)", bold_prefix="• หลักเกณฑ์: ")
    add_bullet("ทำการแยกข้อมูลหนังสือและรายละเอียดออกมาเป็นตาราง ebooks และสร้างตาราง order_items เพื่อเชื่อมโยงความสัมพันธ์แบบ N:M ระหว่าง orders และ ebooks", bold_prefix="• การดำเนินการ: ")
    add_callout("การตัดสินใจสำคัญด้านวิศวกรรมข้อมูลใน 2NF", 
                "ในตาราง order_items มีการเพิ่มฟิลด์ 'price_at_purchase' เพื่อบันทึกราคาหนังสือ ณ วันและเวลาที่สั่งซื้อจริง เพื่อรักษาสัจธรรมทางบัญชี แม้ในอนาคตผู้ดูแลร้านจะปรับราคาในตาราง ebooks ยอดเงินรวมและประวัติศาสตร์ในอดีตจะไม่ผิดเพี้ยนเด็ดขาด", box_type="warning")

    add_h3("4. รูปแบบบรรทัดฐานขั้นที่ 3 (Third Normal Form: 3NF)")
    add_bullet("ต้องผ่านเกณฑ์ 2NF และต้องไม่มีการขึ้นต่อกันทางอ้อมระหว่างแอตทริบิวต์ที่ไม่ใช่คีย์ (No Transitive Dependency: X -> Y และ Y -> Z)", bold_prefix="• หลักเกณฑ์: ")
    add_bullet("ในส่วนของผู้ใช้: ทำการแยกบทบาทออกมาเป็นตาราง roles (user_id -> role_id -> role_name)\n"
               "ในส่วนของสินค้า: ทำการแยกผู้แต่งออกมาเป็นตาราง authors (ebook_id -> author_id -> author_name) และแยกหมวดหมู่ออกมาเป็นตาราง categories (ebook_id -> category_id -> category_name)\n"
               "ในส่วนของตะกร้า: แยกตาราง carts และ cart_items ออกจากตารางผู้ใช้และคำสั่งซื้อ เพื่อจัดการสถานะชั่วคราวก่อนเกิดการสั่งซื้อจริง", bold_prefix="• การดำเนินการ: ")

    add_p("สรุปผลการจัดรูปบรรทัดฐาน: ฐานข้อมูลทั้ง 9 ตารางของ ebook-store มีความสมบูรณ์ตามหลัก 3NF ขจัดความซ้ำซ้อนได้อย่างสมบูรณ์ และพร้อมรองรับการขยายตัวของระบบในอนาคต")

    add_h2("2.3 พจนานุกรมข้อมูลฉบับสมบูรณ์ 9 ตาราง (Data Dictionary)")
    add_p("พจนานุกรมข้อมูลแสดงรายละเอียดของแต่ละคอลัมน์ ชนิดข้อมูล ข้อกำหนด และคำอธิบายความหมายที่ใช้งานจริงในระบบฐานข้อมูล PostgreSQL บน Neon Cloud:")

    # Table 1: roles
    add_h3("ตารางที่ 2.1: roles (บทบาทผู้ใช้งานในระบบ)")
    tbl_d1 = doc.add_table(rows=3, cols=5)
    tbl_d1.rows[0].cells[0].paragraphs[0].add_run("ลำดับ")
    tbl_d1.rows[0].cells[1].paragraphs[0].add_run("ชื่อฟิลด์ (Column)")
    tbl_d1.rows[0].cells[2].paragraphs[0].add_run("ชนิดข้อมูล (Data Type)")
    tbl_d1.rows[0].cells[3].paragraphs[0].add_run("ข้อกำหนด (Constraints)")
    tbl_d1.rows[0].cells[4].paragraphs[0].add_run("คำอธิบายความหมาย")
    d1_data = [
        ("1", "role_id", "SERIAL", "PRIMARY KEY, AUTO_INCREMENT", "รหัสประจำตัวบทบาทผู้ใช้งาน (1 = customer, 2 = admin)"),
        ("2", "role_name", "VARCHAR(50)", "NOT NULL, UNIQUE", "ชื่อบทบาทผู้ใช้งาน เช่น 'customer', 'admin'")
    ]
    for idx, row in enumerate(d1_data, start=1):
        for c_idx, val in enumerate(row):
            tbl_d1.rows[idx].cells[c_idx].paragraphs[0].add_run(val)
    style_table(tbl_d1, [Inches(0.6), Inches(1.3), Inches(1.1), Inches(1.6), Inches(1.9)], [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT])

    # Table 2: users
    add_h3("ตารางที่ 2.2: users (ข้อมูลสมาชิกและผู้ดูแลระบบ)")
    tbl_d2 = doc.add_table(rows=8, cols=5)
    tbl_d2.rows[0].cells[0].paragraphs[0].add_run("ลำดับ")
    tbl_d2.rows[0].cells[1].paragraphs[0].add_run("ชื่อฟิลด์ (Column)")
    tbl_d2.rows[0].cells[2].paragraphs[0].add_run("ชนิดข้อมูล (Data Type)")
    tbl_d2.rows[0].cells[3].paragraphs[0].add_run("ข้อกำหนด (Constraints)")
    tbl_d2.rows[0].cells[4].paragraphs[0].add_run("คำอธิบายความหมาย")
    d2_data = [
        ("1", "user_id", "SERIAL", "PRIMARY KEY, AUTO_INCREMENT", "รหัสประจำตัวผู้ใช้งาน"),
        ("2", "role_id", "INTEGER", "NOT NULL, DEFAULT 1, FK -> roles(role_id)", "รหัสบทบาท อ้างอิงตาราง roles"),
        ("3", "username", "VARCHAR(50)", "NOT NULL, UNIQUE", "ชื่อผู้ใช้สำหรับล็อกอินเข้าสู่ระบบ"),
        ("4", "email", "VARCHAR(100)", "NOT NULL, UNIQUE", "อีเมลประจำตัวผู้ใช้งาน"),
        ("5", "password_hash", "VARCHAR(255)", "NOT NULL", "รหัสผ่านที่ผ่านการแฮชเพื่อความปลอดภัย"),
        ("6", "full_name", "VARCHAR(100)", "NOT NULL", "ชื่อ-นามสกุลจริงของผู้ใช้งาน"),
        ("7", "created_at", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "วันและเวลาที่ลงทะเบียนสมาชิก")
    ]
    for idx, row in enumerate(d2_data, start=1):
        for c_idx, val in enumerate(row):
            tbl_d2.rows[idx].cells[c_idx].paragraphs[0].add_run(val)
    style_table(tbl_d2, [Inches(0.6), Inches(1.3), Inches(1.1), Inches(1.6), Inches(1.9)], [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT])

    # Table 3: authors
    add_h3("ตารางที่ 2.3: authors (ข้อมูลผู้แต่ง / นักเขียน)")
    tbl_d3 = doc.add_table(rows=4, cols=5)
    tbl_d3.rows[0].cells[0].paragraphs[0].add_run("ลำดับ")
    tbl_d3.rows[0].cells[1].paragraphs[0].add_run("ชื่อฟิลด์ (Column)")
    tbl_d3.rows[0].cells[2].paragraphs[0].add_run("ชนิดข้อมูล (Data Type)")
    tbl_d3.rows[0].cells[3].paragraphs[0].add_run("ข้อกำหนด (Constraints)")
    tbl_d3.rows[0].cells[4].paragraphs[0].add_run("คำอธิบายความหมาย")
    d3_data = [
        ("1", "author_id", "SERIAL", "PRIMARY KEY, AUTO_INCREMENT", "รหัสประจำตัวนักเขียน"),
        ("2", "author_name", "VARCHAR(100)", "NOT NULL", "ชื่อ-นามสกุล หรือนามปากกาของนักเขียน"),
        ("3", "bio", "TEXT", "NULLABLE", "ประวัติผลงานโดยย่อของนักเขียน")
    ]
    for idx, row in enumerate(d3_data, start=1):
        for c_idx, val in enumerate(row):
            tbl_d3.rows[idx].cells[c_idx].paragraphs[0].add_run(val)
    style_table(tbl_d3, [Inches(0.6), Inches(1.3), Inches(1.1), Inches(1.6), Inches(1.9)], [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT])

    # Table 4: categories
    add_h3("ตารางที่ 2.4: categories (หมวดหมู่หนังสือ)")
    tbl_d4 = doc.add_table(rows=4, cols=5)
    tbl_d4.rows[0].cells[0].paragraphs[0].add_run("ลำดับ")
    tbl_d4.rows[0].cells[1].paragraphs[0].add_run("ชื่อฟิลด์ (Column)")
    tbl_d4.rows[0].cells[2].paragraphs[0].add_run("ชนิดข้อมูล (Data Type)")
    tbl_d4.rows[0].cells[3].paragraphs[0].add_run("ข้อกำหนด (Constraints)")
    tbl_d4.rows[0].cells[4].paragraphs[0].add_run("คำอธิบายความหมาย")
    d4_data = [
        ("1", "category_id", "SERIAL", "PRIMARY KEY, AUTO_INCREMENT", "รหัสประจำตัวหมวดหมู่"),
        ("2", "category_name", "VARCHAR(100)", "NOT NULL", "ชื่อหมวดหมู่ เช่น Computer & Programming"),
        ("3", "description", "TEXT", "NULLABLE", "คำอธิบายขอบเขตของหมวดหมู่หนังสือ")
    ]
    for idx, row in enumerate(d4_data, start=1):
        for c_idx, val in enumerate(row):
            tbl_d4.rows[idx].cells[c_idx].paragraphs[0].add_run(val)
    style_table(tbl_d4, [Inches(0.6), Inches(1.3), Inches(1.1), Inches(1.6), Inches(1.9)], [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT])

    # Table 5: ebooks
    add_h3("ตารางที่ 2.5: ebooks (ข้อมูลหนังสือดิจิทัล E-Book)")
    tbl_d5 = doc.add_table(rows=11, cols=5)
    tbl_d5.rows[0].cells[0].paragraphs[0].add_run("ลำดับ")
    tbl_d5.rows[0].cells[1].paragraphs[0].add_run("ชื่อฟิลด์ (Column)")
    tbl_d5.rows[0].cells[2].paragraphs[0].add_run("ชนิดข้อมูล (Data Type)")
    tbl_d5.rows[0].cells[3].paragraphs[0].add_run("ข้อกำหนด (Constraints)")
    tbl_d5.rows[0].cells[4].paragraphs[0].add_run("คำอธิบายความหมาย")
    d5_data = [
        ("1", "ebook_id", "SERIAL", "PRIMARY KEY, AUTO_INCREMENT", "รหัสประจำตัวหนังสือดิจิทัล"),
        ("2", "title", "VARCHAR(200)", "NOT NULL", "ชื่อเรื่องหนังสือ E-Book"),
        ("3", "author_id", "INTEGER", "NOT NULL, FK -> authors(author_id)", "รหัสผู้แต่ง อ้างอิงตาราง authors"),
        ("4", "category_id", "INTEGER", "NOT NULL, FK -> categories(category_id)", "รหัสหมวดหมู่ อ้างอิงตาราง categories"),
        ("5", "price", "NUMERIC(10,2)", "NOT NULL, CHECK (price >= 0)", "ราคาจำหน่ายต่อเล่ม (บาท) ห้ามติดลบ"),
        ("6", "cover_image_url", "TEXT", "NULLABLE", "URL รูปภาพหน้าปกหนังสือ"),
        ("7", "description", "TEXT", "NULLABLE", "คำอธิบายเนื้อหาและเรื่องย่อ"),
        ("8", "file_download_url", "TEXT", "NOT NULL", "URL ไฟล์ดิจิทัล PDF ของหนังสือ"),
        ("9", "is_active", "BOOLEAN", "DEFAULT TRUE", "สถานะพร้อมจำหน่าย (TRUE=เปิดขาย, FALSE=ปิดขาย)"),
        ("10", "created_at", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "วันและเวลาที่เพิ่มหนังสือเข้าสู่ระบบ")
    ]
    for idx, row in enumerate(d5_data, start=1):
        for c_idx, val in enumerate(row):
            tbl_d5.rows[idx].cells[c_idx].paragraphs[0].add_run(val)
    style_table(tbl_d5, [Inches(0.6), Inches(1.3), Inches(1.1), Inches(1.6), Inches(1.9)], [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT])

    # Table 6: carts
    add_h3("ตารางที่ 2.6: carts (หัวตะกร้าสินค้าประจำตัวผู้ใช้)")
    tbl_d6 = doc.add_table(rows=4, cols=5)
    tbl_d6.rows[0].cells[0].paragraphs[0].add_run("ลำดับ")
    tbl_d6.rows[0].cells[1].paragraphs[0].add_run("ชื่อฟิลด์ (Column)")
    tbl_d6.rows[0].cells[2].paragraphs[0].add_run("ชนิดข้อมูล (Data Type)")
    tbl_d6.rows[0].cells[3].paragraphs[0].add_run("ข้อกำหนด (Constraints)")
    tbl_d6.rows[0].cells[4].paragraphs[0].add_run("คำอธิบายความหมาย")
    d6_data = [
        ("1", "cart_id", "SERIAL", "PRIMARY KEY, AUTO_INCREMENT", "รหัสประจำตัวตะกร้าสินค้า"),
        ("2", "user_id", "INTEGER", "NOT NULL, FK -> users(user_id)", "รหัสผู้ใช้งานเจ้าของตะกร้าสินค้า"),
        ("3", "updated_at", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "วันและเวลาที่อัปเดตตะกร้าล่าสุด")
    ]
    for idx, row in enumerate(d6_data, start=1):
        for c_idx, val in enumerate(row):
            tbl_d6.rows[idx].cells[c_idx].paragraphs[0].add_run(val)
    style_table(tbl_d6, [Inches(0.6), Inches(1.3), Inches(1.1), Inches(1.6), Inches(1.9)], [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT])

    # Table 7: cart_items
    add_h3("ตารางที่ 2.7: cart_items (รายการสินค้าในตะกร้า)")
    tbl_d7 = doc.add_table(rows=5, cols=5)
    tbl_d7.rows[0].cells[0].paragraphs[0].add_run("ลำดับ")
    tbl_d7.rows[0].cells[1].paragraphs[0].add_run("ชื่อฟิลด์ (Column)")
    tbl_d7.rows[0].cells[2].paragraphs[0].add_run("ชนิดข้อมูล (Data Type)")
    tbl_d7.rows[0].cells[3].paragraphs[0].add_run("ข้อกำหนด (Constraints)")
    tbl_d7.rows[0].cells[4].paragraphs[0].add_run("คำอธิบายความหมาย")
    d7_data = [
        ("1", "cart_item_id", "SERIAL", "PRIMARY KEY, AUTO_INCREMENT", "รหัสรายการย่อยในตะกร้า"),
        ("2", "cart_id", "INTEGER", "NOT NULL, FK -> carts(cart_id)", "รหัสตะกร้าสินค้า อ้างอิงตาราง carts"),
        ("3", "ebook_id", "INTEGER", "NOT NULL, FK -> ebooks(ebook_id)", "รหัสหนังสือที่เลือกไว้ อ้างอิง ebooks"),
        ("4", "quantity", "INTEGER", "NOT NULL, DEFAULT 1, CHECK (quantity > 0)", "จำนวนเล่มที่ต้องการสั่งซื้อ (ต้องมากกว่า 0)")
    ]
    for idx, row in enumerate(d7_data, start=1):
        for c_idx, val in enumerate(row):
            tbl_d7.rows[idx].cells[c_idx].paragraphs[0].add_run(val)
    style_table(tbl_d7, [Inches(0.6), Inches(1.3), Inches(1.1), Inches(1.6), Inches(1.9)], [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT])

    # Table 8: orders
    add_h3("ตารางที่ 2.8: orders (ข้อมูลคำสั่งซื้อหลักและหลักฐานสลิป)")
    tbl_d8 = doc.add_table(rows=8, cols=5)
    tbl_d8.rows[0].cells[0].paragraphs[0].add_run("ลำดับ")
    tbl_d8.rows[0].cells[1].paragraphs[0].add_run("ชื่อฟิลด์ (Column)")
    tbl_d8.rows[0].cells[2].paragraphs[0].add_run("ชนิดข้อมูล (Data Type)")
    tbl_d8.rows[0].cells[3].paragraphs[0].add_run("ข้อกำหนด (Constraints)")
    tbl_d8.rows[0].cells[4].paragraphs[0].add_run("คำอธิบายความหมาย")
    d8_data = [
        ("1", "order_id", "SERIAL", "PRIMARY KEY, AUTO_INCREMENT", "รหัสคำสั่งซื้อ (Order ID)"),
        ("2", "user_id", "INTEGER", "NOT NULL, FK -> users(user_id)", "รหัสสมาชิกผู้ทำการสั่งซื้อ"),
        ("3", "total_amount", "NUMERIC(10,2)", "NOT NULL, CHECK (total_amount >= 0)", "ยอดรวมเงินสุทธิของคำสั่งซื้อ (บาท)"),
        ("4", "order_status", "VARCHAR(30)", "NOT NULL, DEFAULT 'pending'", "สถานะออเดอร์ ('pending', 'confirmed', 'cancelled')"),
        ("5", "payment_slip_url", "TEXT", "NULLABLE", "URL รูปภาพหลักฐานสลิปโอนเงินจำลอง"),
        ("6", "slip_note", "VARCHAR(255)", "DEFAULT 'ชำระผ่าน PromptPay QR จำลอง'", "หมายเหตุช่องทางการชำระเงินจำลอง"),
        ("7", "created_at", "TIMESTAMP", "DEFAULT CURRENT_TIMESTAMP", "วันและเวลาที่ทำรายการสั่งซื้อ")
    ]
    for idx, row in enumerate(d8_data, start=1):
        for c_idx, val in enumerate(row):
            tbl_d8.rows[idx].cells[c_idx].paragraphs[0].add_run(val)
    style_table(tbl_d8, [Inches(0.6), Inches(1.3), Inches(1.1), Inches(1.6), Inches(1.9)], [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT])

    # Table 9: order_items
    add_h3("ตารางที่ 2.9: order_items (รายการหนังสือที่สั่งซื้อจริง พร้อมราคาประวัติศาสตร์)")
    tbl_d9 = doc.add_table(rows=5, cols=5)
    tbl_d9.rows[0].cells[0].paragraphs[0].add_run("ลำดับ")
    tbl_d9.rows[0].cells[1].paragraphs[0].add_run("ชื่อฟิลด์ (Column)")
    tbl_d9.rows[0].cells[2].paragraphs[0].add_run("ชนิดข้อมูล (Data Type)")
    tbl_d9.rows[0].cells[3].paragraphs[0].add_run("ข้อกำหนด (Constraints)")
    tbl_d9.rows[0].cells[4].paragraphs[0].add_run("คำอธิบายความหมาย")
    d9_data = [
        ("1", "order_item_id", "SERIAL", "PRIMARY KEY, AUTO_INCREMENT", "รหัสประจำตัวรายการสินค้าในออเดอร์"),
        ("2", "order_id", "INTEGER", "NOT NULL, FK -> orders(order_id)", "รหัสคำสั่งซื้อ อ้างอิงตาราง orders"),
        ("3", "ebook_id", "INTEGER", "NOT NULL, FK -> ebooks(ebook_id)", "รหัสหนังสือที่สั่งซื้อ อ้างอิงตาราง ebooks"),
        ("4", "price_at_purchase", "NUMERIC(10,2)", "NOT NULL, CHECK (price_at_purchase >= 0)", "ราคาต่อเล่ม ณ วันและเวลาที่สั่งซื้อ (ตรึงราคา)")
    ]
    for idx, row in enumerate(d9_data, start=1):
        for c_idx, val in enumerate(row):
            tbl_d9.rows[idx].cells[c_idx].paragraphs[0].add_run(val)
    style_table(tbl_d9, [Inches(0.6), Inches(1.3), Inches(1.1), Inches(1.6), Inches(1.9)], [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT])

    doc.add_page_break()

    # =========================================================================
    # 7. บทที่ 3: การสร้างฐานข้อมูลและข้อกำหนดบูรณภาพข้อมูล
    # =========================================================================
    add_h1("บทที่ 3: การสร้างฐานข้อมูลและข้อกำหนดบูรณภาพข้อมูล (Implementation & Constraints)")
    
    add_h2("3.1 คำสั่ง Data Definition Language (DDL) บน PostgreSQL")
    add_p("คำสั่ง SQL DDL ที่ใช้งานจริงในการสร้างตารางทั้ง 9 ตารางบนฐานข้อมูล PostgreSQL (Neon Cloud):")

    with open("sql/schema.sql", "r", encoding="utf-8") as f:
        schema_sql = f.read()
    add_code_block(schema_sql)

    add_h2("3.2 ข้อกำหนดบูรณภาพข้อมูล (Integrity Constraints & Referential Integrity)")
    add_p("เพื่อให้ข้อมูลในระบบมีความถูกต้อง น่าเชื่อถือ และป้องกันข้อมูลผิดพลาด (Bad Data) ระบบได้บังคับใช้ข้อกำหนดบูรณภาพข้อมูลครบทั้ง 5 ด้านตามเกณฑ์ใบงานข้อ 4:")
    add_bullet("ทุกตารางมีคอลัมน์คีย์หลักที่กำหนดเป็น SERIAL PRIMARY KEY รับประกันค่าที่ไม่ซ้ำซ้อน (Unique) และห้ามเป็นค่าว่าง (NOT NULL)", bold_prefix="1. Primary Key Constraints: ")
    add_bullet("มีการผูกโยงคีย์นอกจากตารางย่อยไปยังตารางหลักครบทั้ง 8 เส้นทาง ได้แก่ users->roles, ebooks->authors, ebooks->categories, carts->users, cart_items->carts, cart_items->ebooks, orders->users, และ order_items->orders", bold_prefix="2. Foreign Key Constraints: ")
    add_bullet("ป้องกันการเว้นว่างในคอลัมน์สำคัญที่จำเป็นต่อการประมวลผล เช่น title, price, username, email, order_status, file_download_url", bold_prefix="3. NOT NULL Constraints: ")
    add_bullet("บังคับให้ข้อมูลมีความเป็นเอกลักษณ์ ไม่ซ้ำซ้อนในระดับระบบ ได้แก่ users.username, users.email, และ roles.role_name", bold_prefix="4. UNIQUE Constraints: ")
    add_bullet("ป้องกันข้อมูลที่ผิดหลักตรรกะทางธุรกิจ เช่น price >= 0 (ราคาต้องไม่ติดลบ), total_amount >= 0 (ยอดเงินรวมต้องไม่ติดลบ), quantity > 0 (จำนวนเล่มต้องมากกว่าศูนย์), และ price_at_purchase >= 0", bold_prefix="5. CHECK Constraints: ")
    add_bullet("กำหนดค่าเริ่มต้นอัตโนมัติให้แก่ระบบ ได้แก่ role_id = 1 (customer), is_active = TRUE, order_status = 'pending', และ created_at = CURRENT_TIMESTAMP", bold_prefix="6. DEFAULT Constraints: ")

    add_h2("3.3 ข้อมูลตัวอย่างทดสอบระบบจริงในฐานข้อมูล (Seed Data)")
    add_p("ในระบบฐานข้อมูลจริงบน Neon Cloud มีการบันทึกข้อมูลตัวอย่าง (Seed Data) ที่สมเหตุสมผล ครอบคลุมทุกโมดูล และเกินกว่าเกณฑ์ขั้นต่ำ 30 คำสั่งซื้อที่ใบงานกำหนด:")
    add_bullet("มี 4 หมวด ได้แก่ Computer & Programming, Business & Finance, Science & Engineering, และ Self Improvement", bold_prefix="• หมวดหมู่หนังสือ (4 หมวดหมู่): ")
    add_bullet("มี 5 ท่าน ได้แก่ Dr. Alan Turing, Benjamin Graham, Robert C. Martin, James Clear, และ Michael F.", bold_prefix="• ผู้แต่ง / นักเขียน (5 ท่าน): ")
    add_bullet("มี 6 เล่ม ได้แก่ Mastering Database Design (฿350), Clean Architecture in Practice (฿420), Microprocessor Architecture & C (฿290), Intelligent Tech Investor (฿380), Atomic Productivity (฿250), และ Data Structures with Big-O (฿310)", bold_prefix="• หนังสือ E-Book (6 รายการ): ")
    add_bullet("มีทั้งสิ้น 8 บัญชี ได้แก่ ผู้ดูแลระบบ (admin) และสมาชิกลูกค้าทั่วไป (somchai, suda, anucha, pimporn, kittisak, อดีดเบต้าเทสเตอร์อย่างงั้นหรอ, Rakgunmai)", bold_prefix="• สมาชิกผู้ใช้งาน (8 บัญชี): ")
    add_bullet("มีข้อมูลธุรกรรมจริงรวมทั้งสิ้น 35 คำสั่งซื้อ (Orders) ประกอบด้วย:\n"
               "- สถานะ confirmed (ยืนยันแล้ว): 29 คำสั่งซื้อ (ยอดขายสุทธิ 16,500.00 บาท)\n"
               "- สถานะ pending (รอตรวจสอบสลิป): 3 คำสั่งซื้อ (ยอดรวม 1,090.00 บาท)\n"
               "- สถานะ cancelled (ยกเลิกคำสั่งซื้อ): 3 คำสั่งซื้อ (ยอดรวม 950.00 บาท)", bold_prefix="• จำนวนคำสั่งซื้อจริง (35 ออเดอร์): ")
    add_bullet("มีรายการหนังสือที่สั่งซื้อจริงรวมทั้งสิ้น 54 รายการย่อย", bold_prefix="• รายการสินค้าที่สั่งซื้อจริง (order_items): ")

    doc.add_page_break()

    # =========================================================================
    # 8. บทที่ 4: รายงานวิเคราะห์ข้อมูลเชิงลึกจากฐานข้อมูลจริง 4 ด้าน
    # =========================================================================
    add_h1("บทที่ 4: รายงานวิเคราะห์ข้อมูลเชิงลึกจากฐานข้อมูลจริง 4 ด้าน (Analytics Reports)")
    add_p("คณะผู้จัดทำได้เขียนคำสั่ง SQL Query วิเคราะห์ข้อมูลจริงในระบบ 4 ด้าน พัฒนาขึ้นในไฟล์ routes/reports.js และ sql/reports.sql โดยทุกรายงานดึงข้อมูลจริงจากตาราง orders, order_items, ebooks, authors, categories, และ users สอดคล้องตามเกณฑ์ใบงานข้อ 5 ครบถ้วน:")

    # Report 1
    add_h2("4.1 รายงานที่ 1: ยอดขายตามช่วงเวลา (Sales Over Time by Date)")
    add_bullet("ยอดขายรวม จำนวนคำสั่งซื้อ และยอดซื้อเฉลี่ยต่อออเดอร์ (Average Order Value: AOV) ของร้าน มีแนวโน้มเปลี่ยนแปลงไปอย่างไรตามวันที่สั่งซื้อ?", bold_prefix="คำถามทางธุรกิจที่ต้องตอบ: ")
    add_bullet("JOIN (หรือเงื่อนไขสถานะ), GROUP BY, SUM, COUNT, AVG, และตัวกรองวัน (DATE function & WHERE filter)", bold_prefix="สิ่งที่ใช้ใน SQL ตามเกณฑ์ใบงาน: ")
    
    q1 = """SELECT 
    DATE(created_at) AS date, 
    COUNT(order_id) AS total_orders, 
    SUM(total_amount) AS total_sales, 
    ROUND(AVG(total_amount), 2) AS avg_sale
FROM orders 
WHERE order_status = 'confirmed'
GROUP BY DATE(created_at) 
ORDER BY date DESC 
LIMIT 7;"""
    add_code_block(q1)

    tbl_r1 = doc.add_table(rows=8, cols=4)
    tbl_r1.rows[0].cells[0].paragraphs[0].add_run("วันที่สั่งซื้อ (date)")
    tbl_r1.rows[0].cells[1].paragraphs[0].add_run("จำนวนคำสั่งซื้อ (total_orders)")
    tbl_r1.rows[0].cells[2].paragraphs[0].add_run("ยอดขายรวมสุทธิ (total_sales)")
    tbl_r1.rows[0].cells[3].paragraphs[0].add_run("ยอดซื้อเฉลี่ยต่อออเดอร์ (avg_sale)")
    r1_data = [
        ("2026-09-19", "1 ออเดอร์", "฿420.00", "฿420.00"),
        ("2026-09-18", "4 ออเดอร์", "฿5,360.00", "฿1,340.00"),
        ("2026-09-04", "1 ออเดอร์", "฿660.00", "฿660.00"),
        ("2026-09-02", "1 ออเดอร์", "฿380.00", "฿380.00"),
        ("2026-09-01", "1 ออเดอร์", "฿250.00", "฿250.00"),
        ("2026-08-31", "1 ออเดอร์", "฿630.00", "฿630.00"),
        ("2026-08-28", "1 ออเดอร์", "฿560.00", "฿560.00")
    ]
    for idx, row in enumerate(r1_data, start=1):
        for c_idx, val in enumerate(row):
            tbl_r1.rows[idx].cells[c_idx].paragraphs[0].add_run(val)
    style_table(tbl_r1, [Inches(1.6), Inches(1.6), Inches(1.6), Inches(1.7)], [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT])

    if os.path.exists("generated_charts/chart_sales_over_time.png"):
        doc.add_picture("generated_charts/chart_sales_over_time.png", width=Inches(5.8))
        p_cap = add_p("รูปที่ 4.1: แผนภูมิแสดงยอดขายรวมและจำนวนคำสั่งซื้อในแต่ละช่วงเวลา (Report 1: Sales Over Time)", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=8)
        p_cap.runs[0].font.size = Pt(11)
        p_cap.runs[0].font.italic = True
        p_cap.runs[0].font.color.rgb = RGBColor(100, 116, 139)

    add_callout("บทวิเคราะห์เชิงธุรกิจ (Business Insights for Report 1)", 
                "จากข้อมูลสถิติจริง วันที่ 18 กันยายน 2569 มียอดขายพุ่งสูงถึง 5,360.00 บาท จาก 4 คำสั่งซื้อ และมีค่าเฉลี่ยต่อคำสั่งซื้อ (AOV) สูงถึง 1,340.00 บาท ซึ่งสูงกว่าค่าเฉลี่ยปกติที่มีการสั่งซื้อเล่มละ 250 - 420 บาท สะท้อนว่าในวันดังกล่าวลูกค้ามีพฤติกรรมการซื้อแบบรวมตะกร้าหลายเล่มพร้อมกัน (Multi-item Cart Checkout) ข้อมูลนี้ชี้แนะให้ทีมบริหารจัดโปรโมชันประเภทซื้อครบ 1,000 บาทรับสิทธิ์ส่วนลดเพิ่ม เพื่อกระตุ้นยอด AOV ให้เติบโตอย่างต่อเนื่อง", box_type="info")

    # Report 2
    add_h2("4.2 รายงานที่ 2: E-Book ขายดีที่สุด 5 อันดับแรก (Top-Selling Books)")
    add_bullet("หนังสือ E-Book เล่มใดขายได้มากที่สุด 5 อันดับแรกตามจำนวนเล่มที่จำหน่ายได้ และสร้างรายได้ให้แก่ร้านค้าเท่าใด?", bold_prefix="คำถามทางธุรกิจที่ต้องตอบ: ")
    add_bullet("JOIN (order_items, orders, ebooks, authors), GROUP BY, COUNT, SUM, ORDER BY DESC, และ LIMIT 5", bold_prefix="สิ่งที่ใช้ใน SQL ตามเกณฑ์ใบงาน: ")

    q2 = """SELECT 
    e.title, 
    a.author_name, 
    COUNT(oi.order_item_id) AS units_sold, 
    SUM(oi.price_at_purchase) AS sales
FROM order_items oi
JOIN orders o ON oi.order_id = o.order_id
JOIN ebooks e ON oi.ebook_id = e.ebook_id
JOIN authors a ON e.author_id = a.author_id
WHERE o.order_status = 'confirmed'
GROUP BY e.title, a.author_name 
ORDER BY units_sold DESC 
LIMIT 5;"""
    add_code_block(q2)

    tbl_r2 = doc.add_table(rows=6, cols=5)
    tbl_r2.rows[0].cells[0].paragraphs[0].add_run("อันดับ")
    tbl_r2.rows[0].cells[1].paragraphs[0].add_run("ชื่อเรื่องหนังสือ E-Book (title)")
    tbl_r2.rows[0].cells[2].paragraphs[0].add_run("ผู้แต่ง (author_name)")
    tbl_r2.rows[0].cells[3].paragraphs[0].add_run("ยอดขาย (units_sold)")
    tbl_r2.rows[0].cells[4].paragraphs[0].add_run("รายได้รวม (sales)")
    r2_data = [
        ("อันดับ 1", "Clean Architecture in Practice", "Robert C. Martin", "11 เล่ม", "฿4,620.00"),
        ("อันดับ 2", "Intelligent Tech Investor", "Benjamin Graham", "10 เล่ม", "฿3,630.00"),
        ("อันดับ 3", "Data Structures with Big-O", "Dr. Alan Turing", "9 เล่ม", "฿2,790.00"),
        ("อันดับ 4", "Mastering Database Design", "Dr. Alan Turing", "8 เล่ม", "฿2,800.00"),
        ("อันดับ 5", "Atomic Productivity", "James Clear", "6 เล่ม", "฿1,500.00")
    ]
    for idx, row in enumerate(r2_data, start=1):
        for c_idx, val in enumerate(row):
            tbl_r2.rows[idx].cells[c_idx].paragraphs[0].add_run(val)
    style_table(tbl_r2, [Inches(0.9), Inches(2.2), Inches(1.6), Inches(1.0), Inches(1.1)], [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.RIGHT])

    if os.path.exists("generated_charts/chart_top_books.png"):
        doc.add_picture("generated_charts/chart_top_books.png", width=Inches(5.8))
        p_cap = add_p("รูปที่ 4.2: แผนภูมิเปรียบเทียบจำนวนเล่มและรายได้ของ 5 หนังสือขายดี (Report 2: Top-Selling Books)", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=8)
        p_cap.runs[0].font.size = Pt(11)
        p_cap.runs[0].font.italic = True
        p_cap.runs[0].font.color.rgb = RGBColor(100, 116, 139)

    add_callout("บทวิเคราะห์เชิงธุรกิจ (Business Insights for Report 2)", 
                "หนังสือ 'Clean Architecture in Practice' ของ Robert C. Martin ครองตำแหน่งสินค้าขายดีอันดับ 1 ทั้งในแง่ของจำนวนเล่ม (11 เล่ม) และยอดเงินรวม (4,620.00 บาท) ตามด้วย 'Intelligent Tech Investor' (10 เล่ม, 3,630.00 บาท) ขณะที่ผลงานของ Dr. Alan Turing มียอดจำหน่ายรวมกันถึง 17 เล่ม สะท้อนว่าผู้อ่านให้ความไว้วางใจในผลงานเชิงวิชาการด้านวิศวกรรมซอฟต์แวร์และการลงทุนเป็นอย่างมาก ทางร้านจึงควรนำหนังสือทั้งสองเล่มนี้ขึ้นแสดงเป็นสินค้าแนะนำในส่วนบนของหน้าแรก (Hero Section)", box_type="info")

    # Report 3
    add_h2("4.3 รายงานที่ 3: สรุปยอดขายตามหมวดหมู่หนังสือ (Sales by Category)")
    add_bullet("หมวดหมู่หนังสือใดสร้างยอดขายรวมและจำนวนรายการสินค้าที่จำหน่ายได้สูงสุดในระบบ?", bold_prefix="คำถามทางธุรกิจที่ต้องตอบ: ")
    add_bullet("JOIN หลายตาราง (categories, ebooks, order_items, orders), GROUP BY, SUM, และ COUNT", bold_prefix="สิ่งที่ใช้ใน SQL ตามเกณฑ์ใบงาน: ")

    q3 = """SELECT 
    c.category_name, 
    COUNT(oi.order_item_id) AS items_count, 
    SUM(oi.price_at_purchase) AS sales
FROM categories c
JOIN ebooks e ON c.category_id = e.category_id
JOIN order_items oi ON e.ebook_id = oi.ebook_id
JOIN orders o ON oi.order_id = o.order_id
WHERE o.order_status = 'confirmed'
GROUP BY c.category_name 
ORDER BY sales DESC;"""
    add_code_block(q3)

    tbl_r3 = doc.add_table(rows=6, cols=5)
    tbl_r3.rows[0].cells[0].paragraphs[0].add_run("ลำดับ")
    tbl_r3.rows[0].cells[1].paragraphs[0].add_run("ชื่อหมวดหมู่หนังสือ (category_name)")
    tbl_r3.rows[0].cells[2].paragraphs[0].add_run("จำนวนเล่มที่จำหน่าย (items_count)")
    tbl_r3.rows[0].cells[3].paragraphs[0].add_run("ยอดขายรวมสุทธิ (sales)")
    tbl_r3.rows[0].cells[4].paragraphs[0].add_run("สัดส่วนยอดขาย (%)")
    r3_data = [
        ("1", "Computer & Programming", "28 เล่ม", "฿10,210.00", "61.9%"),
        ("2", "Business & Finance", "10 เล่ม", "฿3,630.00", "22.0%"),
        ("3", "Self Improvement", "6 เล่ม", "฿1,500.00", "9.1%"),
        ("4", "Science & Engineering", "4 เล่ม", "฿1,160.00", "7.0%"),
        ("รวม", "4 หมวดหมู่หลัก", "48 รายการ", "฿16,500.00", "100.0%")
    ]
    for idx, row in enumerate(r3_data, start=1):
        for c_idx, val in enumerate(row):
            tbl_r3.rows[idx].cells[c_idx].paragraphs[0].add_run(val)
    style_table(tbl_r3, [Inches(0.8), Inches(2.3), Inches(1.3), Inches(1.2), Inches(1.1)], [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT])

    if os.path.exists("generated_charts/chart_categories.png"):
        doc.add_picture("generated_charts/chart_categories.png", width=Inches(5.0))
        p_cap = add_p("รูปที่ 4.3: แผนภูมิวงกลมแสดงสัดส่วนยอดขายตามหมวดหมู่หนังสือ (Report 3: Sales by Category)", align=WD_ALIGN_PARAGRAPH.CENTER, space_before=2, space_after=8)
        p_cap.runs[0].font.size = Pt(11)
        p_cap.runs[0].font.italic = True
        p_cap.runs[0].font.color.rgb = RGBColor(100, 116, 139)

    add_callout("บทวิเคราะห์เชิงธุรกิจ (Business Insights for Report 3)", 
                "หมวดหมู่ Computer & Programming มียอดขายคิดเป็นสัดส่วนสูงถึง 61.9% ของยอดขายทั้งร้าน (10,210.00 บาท จากยอดรวม 16,500.00 บาท) แสดงให้เห็นว่ากลุ่มเป้าหมายผู้ใช้งานหลักของระบบคือกลุ่มนักศึกษา คณาจารย์ และนักพัฒนาสายงานสารสนเทศ ในขณะที่หมวดหมู่อันดับสองคือ Business & Finance (22.0%) การวางแผนจัดหาสินค้าในอนาคตจึงควรมุ่งเน้นไปยังเทคโนโลยีสมัยใหม่ เช่น Artificial Intelligence, Cloud Native, และ DevOps เพื่อรองรับฐานลูกค้าหลักกลุ่มนี้", box_type="info")

    # Report 4
    add_h2("4.4 รายงานที่ 4: พฤติกรรมลูกค้าและยอดซื้อสะสม (Customer Lifetime Spending)")
    add_bullet("ลูกค้าสมาชิกรายใดมียอดการซื้อสะสมสูงสุดในระบบ และมีจำนวนคำสั่งซื้อที่อนุมัติแล้วกี่รายการ?", bold_prefix="คำถามทางธุรกิจที่ต้องตอบ: ")
    add_bullet("JOIN (users, orders), GROUP BY, COUNT, SUM, ORDER BY DESC, และ LIMIT 5", bold_prefix="สิ่งที่ใช้ใน SQL ตามเกณฑ์ใบงาน: ")

    q4 = """SELECT 
    u.username, 
    u.full_name, 
    COUNT(o.order_id) AS orders_count, 
    SUM(o.total_amount) AS spent
FROM users u 
JOIN orders o ON u.user_id = o.user_id
WHERE o.order_status = 'confirmed'
GROUP BY u.username, u.full_name 
ORDER BY spent DESC 
LIMIT 5;"""
    add_code_block(q4)

    tbl_r4 = doc.add_table(rows=6, cols=5)
    tbl_r4.rows[0].cells[0].paragraphs[0].add_run("อันดับ")
    tbl_r4.rows[0].cells[1].paragraphs[0].add_run("ชื่อผู้ใช้ (username)")
    tbl_r4.rows[0].cells[2].paragraphs[0].add_run("ชื่อ-นามสกุลลูกค้า (full_name)")
    tbl_r4.rows[0].cells[3].paragraphs[0].add_run("จำนวนออเดอร์ (orders_count)")
    tbl_r4.rows[0].cells[4].paragraphs[0].add_run("ยอดซื้อสะสมสุทธิ (spent)")
    r4_data = [
        ("อันดับ 1", "อดีดเบต้าเทสเตอร์อย่างงั้นหรอ", "อดีดเบต้าเทสเตอร์อย่างงั้นหรอ", "3 ออเดอร์", "฿4,280.00"),
        ("อันดับ 2", "somchai", "Somchai Prasert", "7 ออเดอร์", "฿3,790.00"),
        ("อันดับ 3", "suda", "Suda Jaidee", "6 ออเดอร์", "฿2,440.00"),
        ("อันดับ 4", "anucha", "Anucha Wongsuwan", "5 ออเดอร์", "฿2,070.00"),
        ("อันดับ 5", "pimporn", "Pimporn Rattanaporn", "4 ออเดอร์", "฿1,860.00")
    ]
    for idx, row in enumerate(r4_data, start=1):
        for c_idx, val in enumerate(row):
            tbl_r4.rows[idx].cells[c_idx].paragraphs[0].add_run(val)
    style_table(tbl_r4, [Inches(0.9), Inches(1.8), Inches(1.8), Inches(1.2), Inches(1.1)], [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.RIGHT])

    add_callout("บทวิเคราะห์เชิงธุรกิจ (Business Insights for Report 4)", 
                "ลูกค้าผู้ใช้ชื่อ @somchai มีความถี่ในการเข้ามาสั่งซื้อสูงสุดถึง 7 ออเดอร์ ในขณะที่ @อดีดเบต้าเทสเตอร์อย่างงั้นหรอ มียอดการซื้อสะสมสูงสุดเป็นอันดับหนึ่งที่ 4,280.00 บาท จากการสั่งซื้อ 3 ครั้ง การจัดลำดับ Customer Lifetime Value (CLV) นี้เปิดโอกาสให้ทางร้านสามารถนำข้อมูลไปจัดทำ Loyalty Program และระดับสิทธิประโยชน์ (VIP Tiering) เพื่อรักษาฐานลูกค้าประจำและมอบสิทธิพิเศษได้อย่างตรงเป้าหมาย", box_type="info")

    doc.add_page_break()

    # =========================================================================
    # 9. บทที่ 5: การพัฒนาเว็บแอปพลิเคชันและการควบคุมความปลอดภัย
    # =========================================================================
    add_h1("บทที่ 5: การพัฒนาเว็บแอปพลิเคชันและการควบคุมความปลอดภัย (Application Flow & Security)")
    
    add_h2("5.1 การยืนยันตัวตนและวงจรชีวิตของตะกร้าสินค้า (Authentication & Cart Lifecycle)")
    add_p("ในไฟล์ routes/auth.js: เมื่อผู้ใช้กรอกแบบฟอร์มลงทะเบียนสมาชิกใหม่ (/register) ระบบจะทำการบันทึกข้อมูลลงตาราง users ด้วยสิทธิ์เริ่มต้น role_id = 1 (customer) และในขณะเดียวกัน ระบบจะสร้างแถวตะกร้าสินค้าลงในตาราง carts ประจำตัวผู้ใช้งานคนนั้นทันที ทำให้มั่นใจว่าผู้ใช้ทุกคนมีตะกร้าพร้อมใช้งานตั้งแต่เข้าสู่ระบบครั้งแรก")
    add_p("เมื่อผู้ใช้เข้าสู่ระบบสำเร็จ ข้อมูลตัวตนและบทบาทจะถูกจัดเก็บลงใน Server-side Session (req.session.user) ซึ่งจะถูกเรียกใช้ในการตรวจสอบสิทธิ์ตลอดเวลาที่ผู้ใช้ใช้งานระบบ")

    add_h2("5.2 กระบวนการสั่งซื้อ ชำระเงินจำลอง และ Database Transaction (BEGIN / COMMIT)")
    add_p("ในไฟล์ routes/shop.js: เมื่อลูกค้าเลือกสินค้าลงตะกร้าและกดสั่งซื้อที่เส้นทาง /checkout-cart ระบบจะทำงานภายใต้ ACID Database Transaction เพื่อรับประกันความสอดคล้องของข้อมูล (Data Consistency):")

    code_tx = """// โค้ดจริงจาก routes/shop.js: ดำเนินการสั่งซื้อภายใต้ Transaction
const client = await pool.connect();
try {
  await client.query('BEGIN');

  // 1. ดึงรายการสินค้าและคำนวณยอดเงินรวมจากตะกร้า
  const itemsRes = await client.query(`
    SELECT ci.ebook_id, ci.quantity, e.price 
    FROM cart_items ci JOIN ebooks e ON ci.ebook_id = e.ebook_id 
    WHERE ci.cart_id = $1`, [cartId]);

  const totalAmount = itemsRes.rows.reduce((sum, item) => sum + (item.price * item.quantity), 0);

  // 2. บันทึกหัวคำสั่งซื้อลงตาราง orders ด้วยสถานะเริ่มต้น 'pending'
  const orderRes = await client.query(`
    INSERT INTO orders (user_id, total_amount, order_status, payment_slip_url) 
    VALUES ($1, $2, 'pending', 'https://mock-slip.local/qr-checkout.png') RETURNING order_id`,
    [userId, totalAmount]);
  const orderId = orderRes.rows[0].order_id;

  // 3. บันทึกรายการย่อยลง order_items พร้อมตรึงราคา price_at_purchase
  for (const item of itemsRes.rows) {
    for (let i = 0; i < item.quantity; i++) {
      await client.query(`
        INSERT INTO order_items (order_id, ebook_id, price_at_purchase) 
        VALUES ($1, $2, $3)`, [orderId, item.ebook_id, item.price]);
    }
  }

  // 4. เคลียร์ตะกร้าสินค้าให้ว่าง
  await client.query(`DELETE FROM cart_items WHERE cart_id = $1`, [cartId]);

  await client.query('COMMIT');
  res.redirect('/my-orders');
} catch (err) {
  await client.query('ROLLBACK');
  res.status(500).send('Transaction Error: ' + err.message);
} finally {
  client.release();
}"""
    add_code_block(code_tx)

    add_h2("5.3 ระบบความปลอดภัยการดาวน์โหลดไฟล์ดิจิทัล (Digital Asset Access Control)")
    add_p("สอดคล้องตามข้อกำหนดใบงานข้อ 2.2 ระบบต้องควบคุมไม่ให้เปิดลิงก์ของหนังสือที่ลูกค้ายังไม่ได้ซื้อ หรือคำสั่งซื้อยังไม่ได้รับการยืนยัน:")
    add_bullet("ในหน้าประวัติคำสั่งซื้อ (/my-orders): หากสถานะคำสั่งซื้อยังเป็น 'pending' ปุ่มดาวน์โหลดจะถูกปิดการทำงานและแสดงข้อความ '🔒 ล็อกไฟล์ (รออนุมัติ)' และจะเปลี่ยนเป็นปุ่มสีเขียว '⬇️ เปิดอ่าน / ดาวน์โหลด' ต่อเมื่อผู้ดูแลระบบปรับสถานะเป็น 'confirmed' แล้วเท่านั้น", bold_prefix="1. การควบคุมระดับหน้าจอ (UI Masking): ")
    add_bullet("ในระดับตัวควบคุม (Route Controller /download/:ebookId): หากผู้ใช้พยายามพิมพ์ URL ตรงเพื่อเข้าถึงไฟล์ ระบบจะนำ user_id และ ebook_id ไปตรวจสอบกับคำสั่งซื้อในฐานข้อมูลทันที หากไม่พบคำสั่งซื้อที่มีสถานะ 'confirmed' ระบบจะส่งกลับรหัส HTTP 403 Forbidden ทันที", bold_prefix="2. การควบคุมระดับข้อมูล (Database Query Verification): ")

    code_dl_guard = """// โค้ดตรวจสอบสิทธิ์การดาวน์โหลดจริงใน routes/shop.js
router.get('/download/:ebookId', async (req, res) => {
  if (!req.session.user) return res.redirect('/login');

  const check = await pool.query(`
    SELECT e.title, e.file_download_url 
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN ebooks e ON oi.ebook_id = e.ebook_id
    WHERE o.user_id = $1 AND e.ebook_id = $2 AND o.order_status = 'confirmed'
  `, [req.session.user.user_id, req.params.ebookId]);

  if (check.rows.length === 0) {
    return res.status(403).send('Forbidden: คุณยังไม่ได้สั่งซื้อหนังสือเล่มนี้ หรือคำสั่งซื้อยังไม่ได้รับการยืนยัน');
  }

  // ส่งมอบลิงก์ดาวน์โหลดที่ได้รับอนุญาต
  res.redirect(check.rows[0].file_download_url);
});"""
    add_code_block(code_dl_guard)

    add_h2("5.4 ระบบควบคุมสิทธิ์ผู้ดูแลระบบ (Role-Based Access Control: RBAC & Route Guard)")
    add_p("ในไฟล์ routes/admin.js: ระบบป้องกันไม่ให้ผู้ใช้งานทั่วไปเข้าถึงฟังก์ชันการจัดการร้านค้าหลังบ้านได้เด็ดขาด:")
    add_bullet("ลูกค้าทั่วไปจะไม่เห็นเมนู '⚙️ จัดการร้าน (Admin)' บน Navigation Bar", bold_prefix="• UI Level: ")
    add_bullet("สร้าง Middleware ตรวจสอบ req.session.user.role_name === 'admin' ทุกครั้ง หากไม่ใช่แอดมินจะถูกตัดสิทธิ์ทันที", bold_prefix="• Route Guard Middleware: ")

    code_guard = """// Middleware ดักจับใน routes/admin.js
function adminGuard(req, res, next) {
  if (!req.session.user || req.session.user.role_name !== 'admin') {
    return res.status(403).send('Access Denied: เฉพาะผู้ดูแลระบบ (Admin) เท่านั้น');
  }
  next();
}
router.use(adminGuard);"""
    add_code_block(code_guard)

    add_h2("5.5 ระบบบริหารหลังบ้าน และการส่งออกรายงาน CSV มาตรฐานภาษาไทย")
    add_bullet("แอดมินสามารถเปิดดูรูปภาพสลิป และกดปุ่ม 'ยืนยัน' หรือ 'ยกเลิก' เพื่ออัปเดตคำสั่งซื้อ", bold_prefix="• จัดการคำสั่งซื้อ (/admin/orders): ")
    add_bullet("แอดมินสามารถกดปุ่มสลับสถานะ 'พร้อมขาย' หรือ 'ปิดขาย' (Soft Delete: is_active) ได้ทันทีโดยไม่ต้องลบข้อมูลออกจากฐานข้อมูล", bold_prefix="• จัดการหนังสือ E-Book (/admin/ebooks): ")
    add_bullet("ระบบมีฟังก์ชัน Export ข้อมูลสรุปยอดขายเป็นไฟล์ sales_report.csv โดยใส่ Byte Order Mark (\\uFEFF) นำหน้าข้อมูล เพื่อแก้ปัญหาภาษาไทยเพี้ยนในโปรแกรม Microsoft Excel", bold_prefix="• ส่งออกรายงาน CSV ภาษาไทย (/reports/export-csv): ")

    doc.add_page_break()

    # =========================================================================
    # 10. บทที่ 6: การทดสอบระบบและการประกันคุณภาพข้อมูล
    # =========================================================================
    add_h1("บทที่ 6: การทดสอบระบบและการประกันคุณภาพข้อมูล (Testing & Quality Assurance)")
    add_p("ตามข้อกำหนดใบงานข้อ 6 คณะผู้จัดทำได้วางแผนและบันทึกผลการทดสอบระบบจริงอย่างน้อย 8 กรณีทดสอบ (TC-01 ถึง TC-08) ครอบคลุมทั้งเส้นทางหลัก เส้นทางความปลอดภัย และกรณีข้อมูลไม่ถูกต้อง:")

    tbl_test = doc.add_table(rows=9, cols=6)
    tbl_test.rows[0].cells[0].paragraphs[0].add_run("รหัส")
    tbl_test.rows[0].cells[1].paragraphs[0].add_run("ฟังก์ชัน / เงื่อนไขที่ทดสอบ")
    tbl_test.rows[0].cells[2].paragraphs[0].add_run("ข้อมูลนำเข้า (Input)")
    tbl_test.rows[0].cells[3].paragraphs[0].add_run("ผลที่คาดหวัง")
    tbl_test.rows[0].cells[4].paragraphs[0].add_run("ผลการทดสอบจริงในระบบ")
    tbl_test.rows[0].cells[5].paragraphs[0].add_run("สถานะ")

    test_cases = [
        ("TC-01", "ตรวจสอบการสมัครสมาชิกด้วยอีเมลซ้ำ (UNIQUE)", "ใช้อีเมล somchai@email.local ซึ่งมีในระบบแล้ว", "ระบบปฏิเสธการบันทึก แจ้งเตือนอีเมลซ้ำ", "Alert แจ้งเตือน 'Username หรือ Email ซ้ำ' และไม่บันทึกข้อมูล", "ผ่าน"),
        ("TC-02", "ตรวจสอบการล็อกอินด้วยรหัสผ่านผิด", "ป้อน username: somchai, password: wrongpass", "ระบบไม่อนุญาตให้เข้าสู่ระบบ", "Alert แจ้งเตือน 'Username หรือ Password ไม่ถูกต้อง' และไม่สร้าง Session", "ผ่าน"),
        ("TC-03", "หนังสือถูกปิดการขาย (is_active = FALSE)", "แอดมินปิดการขายหนังสือรหัส #4", "หน้าร้านแคตตาล็อกต้องไม่แสดงหนังสือนี้", "หนังสือรหัส #4 หายจากหน้าแรกทันทีตามคำสั่ง WHERE is_active = TRUE", "ผ่าน"),
        ("TC-04", "พยายามดาวน์โหลดก่อนคำสั่งซื้อยืนยัน", "ลูกค้าคลิกลิงก์ออเดอร์สถานะ pending", "ปุ่มดาวน์โหลดถูกล็อก และไม่อนุญาต", "ปุ่มใน /my-orders แสดงสีเทา '🔒 ล็อกไฟล์ (รออนุมัติ)' และกดไม่ได้", "ผ่าน"),
        ("TC-05", "ปลดล็อกดาวน์โหลดหลังแอดมินยืนยัน", "แอดมินกดยืนยันออเดอร์ในหน้าหลังบ้าน", "สถานะเปลี่ยนเป็น confirmed และเปิดปุ่ม", "ปุ่มใน /my-orders เปลี่ยนเป็นสีเขียว '⬇️ เปิดอ่าน / ดาวน์โหลด' ทันที", "ผ่าน"),
        ("TC-06", "ป้องกันการลบหมวดหมู่ที่มีหนังสือผูกอยู่", "กดลบหมวดหมู่ #1 (มีหนังสือ 28 เล่ม)", "ระบบปฏิเสธการลบเพื่อรักษาความสัมพันธ์", "Alert แจ้งเตือน 'ไม่สามารถลบได้ เนื่องจากยังมีหนังสือผูกอยู่'", "ผ่าน"),
        ("TC-07", "ลูกค้าทั่วไปพิมพ์ URL เข้าหลังบ้านตรง", "ลูกค้าพิมพ์ URL: /admin/orders", "ระบบบล็อกและส่งกลับ HTTP 403", "ระบบแสดงข้อความ 'Access Denied: เฉพาะแอดมินเท่านั้น' รหัส 403", "ผ่าน"),
        ("TC-08", "ส่งออกไฟล์รายงานยอดขาย CSV ภาษาไทย", "กดปุ่ม 'Export สรุปยอดขาย (.CSV)'", "เปิดใน Excel แล้วตัวอักษรไทยคมชัด", "เปิดใน Microsoft Excel ภาษาไทยคมชัด 100% ไม่เกิดภาษาต่างดาว", "ผ่าน")
    ]
    for idx, row in enumerate(test_cases, start=1):
        for c_idx, val in enumerate(row):
            tbl_test.rows[idx].cells[c_idx].paragraphs[0].add_run(val)
    style_table(tbl_test, [Inches(0.6), Inches(1.5), Inches(1.3), Inches(1.3), Inches(1.3), Inches(0.5)], 
                [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER], header_bg="1E3A8A")

    doc.add_page_break()

    # =========================================================================
    # 11. บทที่ 7: ขั้นตอนดำเนินงานและการทำงานเป็นกลุ่ม
    # =========================================================================
    add_h1("บทที่ 7: ขั้นตอนดำเนินงานและการทำงานเป็นกลุ่ม (Workflow & Collaboration)")
    
    add_h2("7.1 ขั้นตอนดำเนินงาน 6 ระยะ (Project Phases - สอดคล้องตามข้อ 8 ของใบงาน)")
    tbl_phases = doc.add_table(rows=7, cols=3)
    tbl_phases.rows[0].cells[0].paragraphs[0].add_run("ระยะที่")
    tbl_phases.rows[0].cells[1].paragraphs[0].add_run("งานที่ควรทำ (Tasks)")
    tbl_phases.rows[0].cells[2].paragraphs[0].add_run("หลักฐานเชิงประจักษ์ (Deliverables)")

    phases_data = [
        ("1. วิเคราะห์", "กำหนดกลุ่มผู้ใช้งาน, ขอบเขตการทำงานของระบบ, และกติกาการส่งมอบลิงก์ดาวน์โหลด E-Book", "ข้อเสนอโครงงาน 1 หน้า และแผนผังขั้นตอนการทำงาน (Flowchart)"),
        ("2. ออกแบบ", "สร้างผังความสัมพันธ์ ERD, จัดทำ Data Dictionary, และออกแบบร่างหน้าจอที่จำเป็น", "ผัง ERD 9 ตาราง, พจนานุกรมข้อมูล, และแบบร่างหน้าจอส่วนหน้าบ้าน-หลังบ้าน"),
        ("3. พัฒนา", "สร้างโครงสร้างฐานข้อมูลบน PostgreSQL Neon Cloud, ใส่ข้อมูลตัวอย่าง (Seed Data), พัฒนาโค้ดเชื่อมต่อหน้าบ้านและหลังบ้าน", "Source code ในโฟลเดอร์โปรเจกต์ และไฟล์คำสั่ง SQL (schema.sql, seed.sql)"),
        ("4. ปรับปรุงแก้ไข", "เขียนคำสั่ง SQL Query รายงานวิเคราะห์ 4 ด้าน, สร้างและตรวจสอบผลลัพธ์กับข้อมูลในระบบจริง", "คำสั่ง SQL (reports.sql) และภาพผลการดึงข้อมูลรายงาน 4 ด้าน"),
        ("5. ทำรายงาน", "จัดทำเอกสารรูปเล่มรายงานฉบับสมบูรณ์ (.docx) ตามเกณฑ์ใบงานทุกข้อ", "เล่มรายงานโครงงานฉบับสมบูรณ์ (PROJECT_Report.docx)"),
        ("6. นำเสนอ", "ทดสอบเส้นทางการทำงาน (Flow), แก้ไขข้อผิดพลาด, สาธิตระบบ และจัดเตรียมชุดส่งงาน", "ตารางผลการทดสอบระบบ 8 กรณี, ลิงก์ระบบต้นแบบ, และเอกสารส่งงาน")
    ]
    for idx, (p1, p2, p3) in enumerate(phases_data, start=1):
        tbl_phases.rows[idx].cells[0].paragraphs[0].add_run(p1)
        tbl_phases.rows[idx].cells[1].paragraphs[0].add_run(p2)
        tbl_phases.rows[idx].cells[2].paragraphs[0].add_run(p3)
    style_table(tbl_phases, [Inches(1.2), Inches(2.7), Inches(2.6)], [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT], header_bg="1E3A8A")

    add_h2("7.2 การทำงานเป็นกลุ่มและบทบาทความรับผิดชอบ (สอดคล้องตามข้อ 9 ของใบงาน)")
    add_p("คณะผู้จัดทำได้ร่วมมือกันทำงานตามความถนัด โดยสมาชิกทั้งสองคนมีส่วนร่วมในการออกแบบฐานข้อมูล การทดสอบระบบ และพร้อมนำเสนออธิบายโครงสร้างระบบได้อย่างชัดเจน:")

    tbl_team = doc.add_table(rows=3, cols=3)
    tbl_team.rows[0].cells[0].paragraphs[0].add_run("สมาชิก")
    tbl_team.rows[0].cells[1].paragraphs[0].add_run("หน้าที่หลัก (Primary Responsibilities)")
    tbl_team.rows[0].cells[2].paragraphs[0].add_run("ส่วนที่ต้องอธิบาย (Presentation Scope)")

    team_data = [
        ("นายสุรวัจน์ ชลเรืองทรัพย์\nรหัส 67332110217-1\n(สมาชิกคนที่ 1)", 
         "1. ออกแบบฐานข้อมูล (ERD, 3NF Normalization)\n2. พัฒนาระบบหน้าร้าน (Customer Portal)\n3. พัฒนาระบบแคตตาล็อก ตะกร้าสินค้า และสั่งซื้อ\n4. พัฒนา Transaction Checkout ใน routes/shop.js\n5. เขียนคำสั่ง SQL รายงานที่ 1 (ยอดขายตามวัน) และ รายงานที่ 2 (5 อันดับขายดี)",
         "1. ผัง ERD ภาพรวม และความสัมพันธ์ตาราง roles, users, carts, cart_items, orders, order_items\n2. เส้นทางลูกค้า (Customer Flow): สมัคร, ตะกร้า, ซื้อ\n3. คำสั่ง SQL และบทวิเคราะห์ของรายงานที่ 1 และ 2\n4. การทำงานของ Database Transaction (BEGIN/COMMIT)"),
        ("นายสรวิชญ์ มีมาก\nรหัส 67332110275-8\n(สมาชิกคนที่ 2)", 
         "1. ออกแบบความปลอดภัยและสิทธิ์การใช้งาน (RBAC)\n2. พัฒนาระบบหลังบ้านผู้ดูแลระบบ (Admin Backoffice)\n3. พัฒนาระบบตรวจสอบสิทธิ์ดาวน์โหลดไฟล์ (Access Control)\n4. พัฒนาระบบ Route Guard ดักจับเส้นทาง /admin/*\n5. เขียนคำสั่ง SQL รายงานที่ 3 (ยอดขายหมวดหมู่) และ รายงานที่ 4 (พฤติกรรมลูกค้า)\n6. วางแผนและบันทึกผลการทดสอบระบบ 8 กรณี (QA)",
         "1. ผังความสัมพันธ์ตาราง ebooks, authors, categories\n2. เส้นทางผู้ดูแลร้าน (Admin Flow) และการจัดการคำสั่งซื้อ\n3. กลไกการล็อกไฟล์ดาวน์โหลดและรหัส HTTP 403\n4. คำสั่ง SQL และบทวิเคราะห์ของรายงานที่ 3 และ 4\n5. ผลการทดสอบคุณภาพข้อมูล 8 กรณี (TC-01 ถึง TC-08)")
    ]
    for idx, (m1, m2, m3) in enumerate(team_data, start=1):
        tbl_team.rows[idx].cells[0].paragraphs[0].add_run(m1)
        tbl_team.rows[idx].cells[1].paragraphs[0].add_run(m2)
        tbl_team.rows[idx].cells[2].paragraphs[0].add_run(m3)
    style_table(tbl_team, [Inches(1.8), Inches(2.4), Inches(2.3)], [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT], header_bg="2563EB")

    add_h2("7.3 รายการสิ่งที่ต้องส่ง (Deliverables Checklist - สอดคล้องตามข้อ 10 ของใบงาน)")
    tbl_deliv = doc.add_table(rows=7, cols=3)
    tbl_deliv.rows[0].cells[0].paragraphs[0].add_run("รายการส่ง")
    tbl_deliv.rows[0].cells[1].paragraphs[0].add_run("รายละเอียดที่ต้องมี")
    tbl_deliv.rows[0].cells[2].paragraphs[0].add_run("ตรวจแล้ว")

    deliv_data = [
        ("ระบบหรือ prototype", "URL หรือวิธีเปิดระบบ พร้อมบัญชีทดสอบสำหรับผู้สอน (admin และ customer)", "[ x ] ครบถ้วน"),
        ("ฐานข้อมูลและ SQL", "ไฟล์สร้างตาราง (schema.sql), seed data (seed.sql), และ query รายงาน (reports.sql)", "[ x ] ครบถ้วน"),
        ("เอกสารออกแบบ", "ผัง ERD, data dictionary 9 ตาราง, คำอธิบายการปรับแบบข้อมูล 3NF, และขอบเขตระบบ", "[ x ] ครบถ้วน"),
        ("รายงานวิเคราะห์", "รายงานวิเคราะห์ 4 ด้าน พร้อมคำสั่ง SQL, ตารางผลลัพธ์ข้อมูลจริง, และคำอธิบายสรุปผล", "[ x ] ครบถ้วน"),
        ("ผลทดสอบ", "ตารางทดสอบอย่างน้อย 8 กรณี (TC-01 ถึง TC-08) พร้อมผลการแก้ไขปัญหา", "[ x ] ครบถ้วน"),
        ("เอกสารการใช้ AI", "บันทึกเครื่องมือ, prompt สำคัญ, ผลที่นำมาใช้, และการตรวจทานของสมาชิก", "[ x ] ครบถ้วน")
    ]
    for idx, (d1, d2, d3) in enumerate(deliv_data, start=1):
        tbl_deliv.rows[idx].cells[0].paragraphs[0].add_run(d1)
        tbl_deliv.rows[idx].cells[1].paragraphs[0].add_run(d2)
        tbl_deliv.rows[idx].cells[2].paragraphs[0].add_run(d3)
    style_table(tbl_deliv, [Inches(1.8), Inches(3.7), Inches(1.0)], [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER], header_bg="1E3A8A")

    doc.add_page_break()

    # =========================================================================
    # 12. บทที่ 8: การประยุกต์ใช้ปัญญาประดิษฐ์อย่างรับผิดชอบ
    # =========================================================================
    add_h1("บทที่ 8: การประยุกต์ใช้ปัญญาประดิษฐ์อย่างรับผิดชอบ (Responsible AI Usage Log)")
    
    add_h2("8.1 กรอบแนวทางการใช้งาน AI (สอดคล้องตามข้อ 12 ของใบงาน)")
    add_p("อนุญาตให้ใช้ AI เพื่อช่วยคิดขอบเขต ออกแบบ ERD ร่าง SQL เขียนโค้ด สร้างข้อมูลตัวอย่าง ตรวจข้อผิดพลาด และจัดทำเอกสารได้ สมาชิกต้องตรวจสอบผลลัพธ์ก่อนใช้ ปรับให้ตรงกับระบบของกลุ่ม และอธิบายได้ว่าแต่ละส่วนทำงานอย่างไร:")

    tbl_ai_rules = doc.add_table(rows=2, cols=3)
    tbl_ai_rules.rows[0].cells[0].paragraphs[0].add_run("อนุญาตให้ทำได้ (Allowed)")
    tbl_ai_rules.rows[0].cells[1].paragraphs[0].add_run("ต้องปฏิบัติตาม (Mandatory)")
    tbl_ai_rules.rows[0].cells[2].paragraphs[0].add_run("ห้ามทำเด็ดขาด (Prohibited)")

    r_allow = "• ขอแนวคิดโครงสร้าง schema, query หรือโครงร่างโค้ด\n• ใช้ช่วยสร้างชุดข้อมูลทดสอบหรือสรุปรายงาน\n• ใช้ช่วยวิเคราะห์แก้บัก (Debug) และอธิบายแนวคิด"
    r_must = "• บันทึกชื่อเครื่องมือ, prompt สำคัญ, ส่วนที่นำมาใช้ และวิธีตรวจสอบ\n• ตรวจชื่อฟิลด์, ความสัมพันธ์, ผลรวม และข้อสรุปกับข้อมูลจริง\n• ระบุส่วนที่ AI ช่วยในเอกสารประกอบการส่งอย่างโปร่งใส"
    r_forbid = "• คัดลอกผลลัพธ์โดยไม่อ่าน ไม่ทดสอบ หรืออธิบายไม่ได้\n• ใช้ข้อมูลส่วนบุคคลจริง, รหัสผ่านจริง, API Key หรือไฟล์ละเมิดลิขสิทธิ์\n• ให้ AI ทำแทนทั้งหมดแล้วนำเสนอเป็นผลงานของตนเอง"

    tbl_ai_rules.rows[1].cells[0].paragraphs[0].add_run(r_allow)
    tbl_ai_rules.rows[1].cells[1].paragraphs[0].add_run(r_must)
    tbl_ai_rules.rows[1].cells[2].paragraphs[0].add_run(r_forbid)
    style_table(tbl_ai_rules, [Inches(2.1), Inches(2.2), Inches(2.2)], [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT], header_bg="1E3A8A")

    add_h2("8.2 ตารางบันทึกการใช้ AI ของกลุ่ม (AI Usage Log)")
    tbl_ai_log = doc.add_table(rows=4, cols=3)
    tbl_ai_log.rows[0].cells[0].paragraphs[0].add_run("เครื่องมือและวันที่")
    tbl_ai_log.rows[0].cells[1].paragraphs[0].add_run("งานหรือ prompt โดยสรุป")
    tbl_ai_log.rows[0].cells[2].paragraphs[0].add_run("สิ่งที่นำมาใช้และวิธีตรวจสอบ")

    ai_logs = [
        ("Claude / Gemini\n19 ก.ย. 69", 
         "\"ช่วยออกแบบโครงสร้าง 9 ตารางสำหรับร้านขาย E-Book ที่มีระบบตะกร้าสินค้า ให้ตรงหลัก 3NF และมี Foreign Key ครบถ้วน\"", 
         "นำโครงร่าง DDL สำหรับตาราง carts, cart_items, orders, order_items มาปรับแต่ง ตรวจทานความสัมพันธ์ Cardinality ปรับชนิดข้อมูลเงินเป็น NUMERIC(10,2) และทดสอบรันบน Neon PostgreSQL"),
        ("Claude / Gemini\n20 ก.ย. 69", 
         "\"ช่วยร่างคำสั่ง SQL วิเคราะห์ 4 ด้าน: ยอดขายตามวัน, 5 อันดับขายดี, ยอดขายตามหมวดหมู่, และยอดซื้อสะสมของลูกค้า\"", 
         "นำโค้ด Aggregate Query ใน routes/reports.js มาใช้งาน ตรวจสอบผลรวม ยอดขายรวม (฿16,500.00) และจำนวนเล่ม เทียบกับข้อมูลดิบในฐานข้อมูลจริงเพื่อยืนยันความถูกต้อง"),
        ("Claude / Gemini\n21 ก.ย. 69", 
         "\"วิธีแก้ปัญหาไฟล์ CSV ภาษาไทยที่ Export ออกมาจาก Express แล้วเปิดใน Microsoft Excel กลายเป็นภาษาต่างดาว\"", 
         "นำเทคนิคการใส่ Byte Order Mark (\\uFEFF) หน้าเนื้อหา CSV มาใช้ ส่งออกไฟล์และเปิดทดสอบบนโปรแกรม Microsoft Excel บน Windows จริง")
    ]
    for idx, (a1, a2, a3) in enumerate(ai_logs, start=1):
        tbl_ai_log.rows[idx].cells[0].paragraphs[0].add_run(a1)
        tbl_ai_log.rows[idx].cells[1].paragraphs[0].add_run(a2)
        tbl_ai_log.rows[idx].cells[2].paragraphs[0].add_run(a3)
    style_table(tbl_ai_log, [Inches(1.5), Inches(2.5), Inches(2.5)], [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT], header_bg="2563EB")

    add_h2("8.3 ข้อเสนอแนะของ AI ที่ผู้พัฒนาตัดสินใจปฏิเสธตามหลักวิศวกรรม (Rejected Proposals)")
    add_p("เพื่อสะท้อนถึงการตัดสินใจทางวิศวกรรมและวิจารณญาณของผู้พัฒนา มี 3 ประเด็นสำคัญที่ผู้พัฒนาปฏิเสธคำแนะนำของ AI:")
    add_bullet("AI แนะนำให้แปลงไฟล์สลิปเป็น Base64 แล้วเก็บในคอลัมน์ TEXT ของตาราง orders โดยตรง แต่ผู้พัฒนาปฏิเสธเนื่องจากการเก็บ Base64 ทำให้ขนาดฐานข้อมูลบวมอย่างรวดเร็ว (Database Bloat) และค้นหาช้า จึงเลือกจัดเก็บเป็น URL อ้างอิงไฟล์แทน", bold_prefix="1. ปฏิเสธการแปลงสลิปเป็น Base64 String: ")
    add_bullet("AI เสนอให้อนุมัติออเดอร์เป็น 'confirmed' ทันทีที่ลูกค้ากด Checkout เพื่อลดความซับซ้อน แต่ผู้พัฒนาปฏิเสธเพราะขัดต่อข้อกำหนดความปลอดภัยข้อ 2.2 ของใบงาน และเสี่ยงต่อการถูกฉ้อโกง จึงคงสถานะเริ่มต้นเป็น 'pending' และต้องรอแอดมินยืนยันก่อนเสมอ", bold_prefix="2. ปฏิเสธการปลดล็อกดาวน์โหลดทันทีหลังสั่งซื้อ: ")
    add_bullet("AI แนะนำให้ดึงราคาจากตาราง ebooks เสมอเพื่อลดจำนวนคอลัมน์ แต่ผู้พัฒนาปฏิเสธเพราะหากในอนาคตแอดมินปรับราคาหนังสือ ยอดรวมของคำสั่งซื้อในอดีตทั้งหมดจะเปลี่ยนแปลงตาม ซึ่งผิดหลักการบัญชีและบันทึกประวัติศาสตร์ จึงต้องคงคอลัมน์ price_at_purchase ไว้ในตาราง order_items", bold_prefix="3. ปฏิเสธการไม่เก็บราคา ณ วันที่ซื้อ (price_at_purchase): ")

    add_h2("8.4 การคำนึงถึงความเป็นส่วนตัวและการคุ้มครองข้อมูลส่วนบุคคล (PDPA)")
    add_bullet("ชื่อ-นามสกุล และอีเมลทั้งหมดในฐานข้อมูลเป็นข้อมูลจำลองเพื่อการศึกษา (เช่น somchai@email.local) ไม่มีข้อมูลบุคคลจริงในระบบ", bold_prefix="• ข้อมูลจำลอง 100%: ")
    add_bullet("ระบบไม่มีการร้องขอเลขบัตรเครดิต รหัส CVV หรือข้อมูลบัญชีธนาคารจริง โดยใช้ระบบจำลองแนบสลิป QR Code แทน", bold_prefix="• ไม่มีการเก็บข้อมูลการเงินจริง: ")

    doc.add_page_break()

    # =========================================================================
    # 13. บทที่ 9: เกณฑ์การประเมินตนเองและสรุปผลโครงงาน
    # =========================================================================
    add_h1("บทที่ 9: เกณฑ์การประเมินตนเองและสรุปผลโครงงาน (Self-Assessment & Conclusion)")
    
    add_h2("9.1 ตารางประเมินผลการดำเนินงานเทียบเกณฑ์ 100 คะแนนเต็ม (สอดคล้องตามข้อ 11)")
    tbl_rubric = doc.add_table(rows=8, cols=4)
    tbl_rubric.rows[0].cells[0].paragraphs[0].add_run("ด้านการประเมิน")
    tbl_rubric.rows[0].cells[1].paragraphs[0].add_run("เกณฑ์การพิจารณาตามใบงาน")
    tbl_rubric.rows[0].cells[2].paragraphs[0].add_run("ผลการดำเนินงานของโครงงาน ebook-store")
    tbl_rubric.rows[0].cells[3].paragraphs[0].add_run("คะแนน")

    rubric_data = [
        ("การออกแบบฐานข้อมูล", "ERD ถูกต้อง ตารางและความสัมพันธ์ครบ ใช้ PK FK constraint และออกแบบข้อมูลอย่างมีเหตุผล (3NF)", "ออกแบบครบ 9 ตารางตามหลัก 3NF พร้อม PK, FK, NOT NULL, UNIQUE, CHECK, DEFAULT และมีคำอธิบาย Cardinality ชัดเจน", "30"),
        ("การใช้งานระบบ", "หน้าร้านและส่วนบริหารทำงานตามขอบเขต โดยเฉพาะ flow สั่งซื้อ ยืนยัน และลิงก์ดาวน์โหลด", "ทำงานได้จริงครบวงจร ตะกร้าสินค้า, Transactional Checkout, แอดมินตรวจสอบสลิป, ล็อกไฟล์ดาวน์โหลด และ Route Guard 403", "25"),
        ("SQL และรายงานวิเคราะห์", "query ถูกต้อง ใช้ join aggregate filter ได้เหมาะสม และรายงาน 4 เรื่องตอบคำถามได้", "เขียน SQL วิเคราะห์ 4 ด้านถูกต้อง ใช้ JOIN, GROUP BY, SUM, COUNT, AVG, LIMIT และส่งออก CSV ภาษาไทยได้สมบูรณ์", "20"),
        ("คุณภาพข้อมูลและการทดสอบ", "มี seed data เพียงพอ มีกรณีทดสอบและจัดการข้อมูลผิดรูปแบบอย่างเหมาะสม", "มีข้อมูลจริง 35 คำสั่งซื้อ 54 รายการย่อย เกินเกณฑ์ 30 รายการ และมีผลทดสอบครอบคลุม 8 กรณี (TC-01 ถึง TC-08) ผ่านครบ", "10"),
        ("เอกสารและการสาธิต", "เอกสารอ่านได้ครบ สาธิตชัดเจน สมาชิกทั้งสองคนตอบคำถามได้", "รูปเล่มเอกสารฉบับสมบูรณ์ (.docx) จัดหน้าสวยงาม มีผัง ERD ชัดเจน และสมาชิกทั้งสองคนเข้าใจโครงสร้างระบบพร้อมสาธิต", "10"),
        ("การใช้ AI อย่างรับผิดชอบ", "เปิดเผยการใช้ AI ตรวจสอบผลลัพธ์ อธิบายสิ่งที่ส่งได้ และไม่ละเมิดความเป็นส่วนตัวหรือลิขสิทธิ์", "บันทึก AI Usage Log ครบถ้วน แสดง 3 กรณีศึกษาที่ตัดสินใจปฏิเสธ AI ตามหลักวิศวกรรม และข้อมูลทั้งหมดสอดคล้องกับ PDPA", "5"),
        ("รวมคะแนนทั้งสิ้น", "ประเมินตามเกณฑ์มาตรฐานรายวิชา Database Systems ครบถ้วน 100%", "บรรลุวัตถุประสงค์และเกณฑ์การประเมินตามใบงานครบถ้วนสมบูรณ์ทุกประการ", "100")
    ]
    for idx, (r1, r2, r3, r4) in enumerate(rubric_data, start=1):
        tbl_rubric.rows[idx].cells[0].paragraphs[0].add_run(r1)
        tbl_rubric.rows[idx].cells[1].paragraphs[0].add_run(r2)
        tbl_rubric.rows[idx].cells[2].paragraphs[0].add_run(r3)
        tbl_rubric.rows[idx].cells[3].paragraphs[0].add_run(r4)
    style_table(tbl_rubric, [Inches(1.5), Inches(2.2), Inches(2.3), Inches(0.5)], [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER], header_bg="1E3A8A")

    add_h2("9.2 สรุปผลสัมฤทธิ์ของโครงงาน")
    add_p("โครงงานการพัฒนาระบบร้านขายหนังสือและอีบุ๊กออนไลน์ (E-Book Store Online Management System) ประสบความสำเร็จตามเป้าหมายที่ตั้งไว้ทุกประการ ระบบสามารถผสานทฤษฎีการออกแบบฐานข้อมูลเชิงสัมพันธ์ระดับ 3NF เข้ากับการพัฒนาเว็บแอปพลิเคชันที่ใช้งานได้จริงบน Node.js, Express.js และ PostgreSQL บน Neon Cloud Platform")
    add_p("ระบบสามารถแก้ปัญหาสำคัญของธุรกิจ E-Book ได้อย่างรอบด้าน ทั้งการรักษาประวัติศาสตร์ราคาในอดีต (price_at_purchase), การควบคุมความปลอดภัยในการเข้าถึงไฟล์ดิจิทัล (Digital Content Protection), การแบ่งสิทธิ์ผู้ใช้งาน (RBAC), และการดึงข้อมูลเชิงลึกผ่านคำสั่ง SQL เพื่อสร้างรายงานวิเคราะห์ธุรกิจ 4 ด้าน")

    add_h2("9.3 ข้อเสนอแนะในการพัฒนาต่อยอดระบบในอนาคต")
    add_bullet("พัฒนา Webhook เชื่อมต่อกับระบบ Payment Gateway ของธนาคาร เพื่อตรวจจับยอดโอนเงินอัตโนมัติและปรับสถานะคำสั่งซื้อเป็น 'confirmed' ทันทีโดยไม่ต้องรอแอดมินกดตรวจสลิปด้วยตนเอง", bold_prefix="1. ระบบตรวจสอบการชำระเงินอัตโนมัติ (Automated Payment Gateway): ")
    add_bullet("พัฒนาโมดูลอ่านหนังสือตัวอย่าง 10-15 หน้าแรกผ่านหน้าเว็บเบราว์เซอร์ เพื่อให้ลูกค้าได้ทดลองอ่านก่อนตัดสินใจสั่งซื้อ", bold_prefix="2. ระบบพรีวิวอ่านตัวอย่าง (E-Book Sample Preview): ")
    add_bullet("เชื่อมโยงเข้ากับระบบฐานข้อมูลคลังสินค้าของวิชาวิศวกรรมซอฟต์แวร์ เพื่อรองรับการจำหน่ายหนังสือเล่มควบคู่ไปกับ E-Book ในตะกร้าสินค้าเดียวกัน", bold_prefix="3. การเชื่อมต่อกับระบบคลังสินค้าภายนอก (SWE Inventory System): ")

    doc.add_page_break()

    # =========================================================================
    # 14. ภาคผนวก (APPENDICES)
    # =========================================================================
    add_h1("ภาคผนวก (Appendices)")
    
    add_h2("ภาคผนวก ก: รายการตรวจสอบความพร้อมก่อนส่งงาน (Checklist - สอดคล้องตามข้อ 13)")
    add_p("ตามข้อกำหนดใบงานข้อ 13 รายการตรวจสอบก่อนส่ง คณะผู้จัดทำได้ตรวจสอบความพร้อมของชิ้นงานครบถ้วนทุกข้อดังนี้:")

    chk_items = [
        "[ x ] สมาชิกทั้งสองคนทดสอบระบบและอธิบาย ERD กับ SQL ได้",
        "[ x ] คำสั่งซื้อที่ยังไม่ยืนยันไม่สามารถเปิดลิงก์ดาวน์โหลดได้ (สอดคล้องตามข้อ 2.2)",
        "[ x ] มีข้อมูลตัวอย่างอย่างน้อย 30 คำสั่งซื้อและรายงานวิเคราะห์ 4 รายงาน (ระบบมีจริง 35 คำสั่งซื้อ)",
        "[ x ] ไฟล์ SQL รันได้และมีข้อมูลตัวอย่างเพียงพอ (schema.sql, seed.sql, reports.sql)",
        "[ x ] เอกสารการใช้ AI ครบและไม่มีข้อมูลส่วนบุคคลหรือเนื้อหาละเมิดลิขสิทธิ์",
        "[ x ] ตรวจรายการส่งทั้งหมดและสาธิตระบบก่อนวันนำเสนอ"
    ]
    for chk in chk_items:
        add_bullet(chk, bold_prefix="")

    add_h2("การลงชื่อรับรอง (Certification of Authorship)")
    add_p("สมาชิกทั้งสองคนยืนยันว่าได้ร่วมทำงาน ตรวจสอบความถูกต้อง และเปิดเผยการใช้ AI ตามความเป็นจริง:")

    tbl_sig = doc.add_table(rows=3, cols=2)
    tbl_sig.rows[0].cells[0].paragraphs[0].add_run("สมาชิกคนที่ 1")
    tbl_sig.rows[0].cells[1].paragraphs[0].add_run("สมาชิกคนที่ 2")

    tbl_sig.rows[1].cells[0].paragraphs[0].add_run("ลงชื่อ: ................................................................\n(นายสุรวัจน์ ชลเรืองทรัพย์)\nรหัสนักศึกษา: 67332110217-1")
    tbl_sig.rows[1].cells[1].paragraphs[0].add_run("ลงชื่อ: ................................................................\n(นายสรวิชญ์ มีมาก)\nรหัสนักศึกษา: 67332110275-8")

    tbl_sig.rows[2].cells[0].paragraphs[0].add_run("วันที่: ......... / ......... / .............")
    tbl_sig.rows[2].cells[1].paragraphs[0].add_run("วันที่: ......... / ......... / .............")
    style_table(tbl_sig, [Inches(3.25), Inches(3.25)], [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER], header_bg="1E3A8A")

    add_h2("ภาคผนวก ข: แบบฟอร์มบันทึกการประเมินของผู้สอน (สอดคล้องตามท้ายใบงาน)")
    tbl_eval = doc.add_table(rows=4, cols=2)
    tbl_eval.rows[0].cells[0].paragraphs[0].add_run("หัวข้อการประเมิน")
    tbl_eval.rows[0].cells[1].paragraphs[0].add_run("บันทึกความคิดเห็นของผู้สอน")

    tbl_eval.rows[1].cells[0].paragraphs[0].add_run("จุดที่ทำได้ดี")
    tbl_eval.rows[1].cells[1].paragraphs[0].add_run("\n\n\n")

    tbl_eval.rows[2].cells[0].paragraphs[0].add_run("ข้อเสนอแนะ")
    tbl_eval.rows[2].cells[1].paragraphs[0].add_run("\n\n\n")

    tbl_eval.rows[3].cells[0].paragraphs[0].add_run("คะแนนและหมายเหตุ")
    tbl_eval.rows[3].cells[1].paragraphs[0].add_run("\n\n\n")
    style_table(tbl_eval, [Inches(2.2), Inches(4.3)], [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT], header_bg="2563EB")

    add_h2("ภาคผนวก ค: คู่มือการติดตั้งและข้อมูลบัญชีผู้ใช้สำหรับทดสอบ (Test Accounts)")
    add_p("เพื่อให้ผู้สอนสามารถเข้าตรวจประเมินระบบได้อย่างสะดวกและรวดเร็ว ข้อมูลการเข้าใช้งานระบบมีดังนี้:")
    
    add_h3("1. วิธีเปิดระบบ (How to Run)")
    add_bullet("เปิด Terminal ในโฟลเดอร์ ebook-store", bold_prefix="ขั้นตอนที่ 1: ")
    add_bullet("รันคำสั่ง npm install เพื่อติดตั้งไลบรารีที่จำเป็น", bold_prefix="ขั้นตอนที่ 2: ")
    add_bullet("รันคำสั่ง node server.js เพื่อเริ่มทำงานเซิร์ฟเวอร์", bold_prefix="ขั้นตอนที่ 3: ")
    add_bullet("เปิดเว็บเบราว์เซอร์ไปที่ http://localhost:3000", bold_prefix="ขั้นตอนที่ 4: ")

    add_h3("2. บัญชีผู้ใช้งานสำหรับทดสอบระบบ (Test Accounts)")
    tbl_acc = doc.add_table(rows=3, cols=4)
    tbl_acc.rows[0].cells[0].paragraphs[0].add_run("บทบาท (Role)")
    tbl_acc.rows[0].cells[1].paragraphs[0].add_run("ชื่อผู้ใช้ (Username)")
    tbl_acc.rows[0].cells[2].paragraphs[0].add_run("รหัสผ่าน (Password)")
    tbl_acc.rows[0].cells[3].paragraphs[0].add_run("สิทธิ์และขอบเขตการเข้าถึง")

    tbl_acc.rows[1].cells[0].paragraphs[0].add_run("ผู้ดูแลระบบ\n(Admin)")
    tbl_acc.rows[1].cells[1].paragraphs[0].add_run("admin")
    tbl_acc.rows[1].cells[2].paragraphs[0].add_run("admin123")
    tbl_acc.rows[1].cells[3].paragraphs[0].add_run("เข้าถึงหน้าแคตตาล็อก ตะกร้าสินค้า ประวัติคำสั่งซื้อ เมนูจัดการคำสั่งซื้อ จัดการ E-Book จัดการหมวดหมู่ จัดการผู้ใช้งาน หน้ารายงานสถิติ และปุ่ม Export CSV")

    tbl_acc.rows[2].cells[0].paragraphs[0].add_run("ลูกค้าทั่วไป\n(Customer)")
    tbl_acc.rows[2].cells[1].paragraphs[0].add_run("somchai")
    tbl_acc.rows[2].cells[2].paragraphs[0].add_run("pass123")
    tbl_acc.rows[2].cells[3].paragraphs[0].add_run("สั่งซื้อหนังสือ ใส่ตะกร้า ชำระเงินจำลอง ดูประวัติคำสั่งซื้อ และเปิดอ่าน/ดาวน์โหลดเฉพาะหนังสือที่ได้รับการยืนยันแล้ว (ถูกบล็อกการเข้าถึงหน้า /admin/*)")

    style_table(tbl_acc, [Inches(1.3), Inches(1.3), Inches(1.3), Inches(2.6)], [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT], header_bg="1E3A8A")

    # Save to available docx file
    output_names = ["PROJECT_Report.docx", "PROJECT_Report_Updated.docx", "PROJECT_Report_Final.docx", "PROJECT_Report_Latest.docx"]
    saved_path = None
    for out in output_names:
        try:
            doc.save(out)
            saved_path = out
            print(f"Document successfully created and saved to {out}!")
            break
        except PermissionError:
            continue
    if not saved_path:
        import time
        ts_name = f"PROJECT_Report_{int(time.time())}.docx"
        doc.save(ts_name)
        print(f"Document saved to {ts_name}!")

if __name__ == "__main__":
    create_report()
