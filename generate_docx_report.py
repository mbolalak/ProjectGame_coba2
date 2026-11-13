import os
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, fill_hex):
    """Sets background color of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Sets cell padding (in twips: 20 twips = 1 pt)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''
        <w:tcMar {nsdecls("w")}>
            <w:top w:w="{top}" w:type="dxa"/>
            <w:bottom w:w="{bottom}" w:type="dxa"/>
            <w:left w:w="{left}" w:type="dxa"/>
            <w:right w:w="{right}" w:type="dxa"/>
        </w:tcMar>
    ''')
    tcPr.append(tcMar)

def set_table_borders(table, color="CCCCCC", sz="4", val="single"):
    """Applies neat borders to a table."""
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideV w:val="none"/>
            <w:left w:val="none"/>
            <w:right w:val="none"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)

def add_callout(doc, text, title="Catatan Arsitektur:"):
    """Adds a stylish callout box."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F0F4F8")
    set_cell_margins(cell, top=120, bottom=120, left=200, right=160)
    
    # Left border thick accent
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:left w:val="single" w:sz="24" w:space="0" w:color="1F4E79"/>
            <w:top w:val="none"/>
            <w:right w:val="none"/>
            <w:bottom w:val="none"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    run_t = p.add_run(f"{title} ")
    run_t.bold = True
    run_t.font.name = "Segoe UI"
    run_t.font.size = Pt(9.5)
    run_t.font.color.rgb = RGBColor(0x1F, 0x4E, 0x79)
    
    run_b = p.add_run(text)
    run_b.font.name = "Segoe UI"
    run_b.font.size = Pt(9.5)
    run_b.font.color.rgb = RGBColor(0x33, 0x33, 0x33)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_code_block(doc, code_str):
    """Adds a monospaced code snippet box."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F8F9FA")
    set_cell_margins(cell, top=100, bottom=100, left=160, right=140)
    
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:left w:val="single" w:sz="6" w:space="0" w:color="D0D5DD"/>
            <w:top w:val="single" w:sz="6" w:space="0" w:color="D0D5DD"/>
            <w:right w:val="single" w:sz="6" w:space="0" w:color="D0D5DD"/>
            <w:bottom w:val="single" w:sz="6" w:space="0" w:color="D0D5DD"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(code_str.strip())
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(0x24, 0x29, 0x2F)
    
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def build_report():
    doc = Document()
    
    # Page setup - A4 with 1 inch margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.27)  # A4 width
        section.page_height = Inches(11.69) # A4 height

    # Color Palette definitions
    NAVY = RGBColor(0x1F, 0x4E, 0x79)
    STEEL_BLUE = RGBColor(0x2E, 0x75, 0xB6)
    DARK_TEXT = RGBColor(0x26, 0x26, 0x26)
    MUTED_TEXT = RGBColor(0x59, 0x59, 0x59)
    
    # Configure Normal Style
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Segoe UI'
    normal_style.font.size = Pt(10)
    normal_style.font.color.rgb = DARK_TEXT

    # ==========================================================
    # 1. HEADER & COVER SECTION
    # ==========================================================
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(0)
    title_p.paragraph_format.space_after = Pt(4)
    run_title = title_p.add_run("Laporan Analisis System & Script Project CoinCollector")
    run_title.font.name = "Segoe UI"
    run_title.font.size = Pt(22)
    run_title.font.bold = True
    run_title.font.color.rgb = NAVY

    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_before = Pt(0)
    sub_p.paragraph_format.space_after = Pt(14)
    run_sub = sub_p.add_run("Dokumentasi Komprehensif Arsitektur Skrip C#, Pola Desain OOP, Integrasi Unity 6, & Pemetaan Objek Scene")
    run_sub.font.name = "Segoe UI"
    run_sub.font.size = Pt(11.5)
    run_sub.font.italic = True
    run_sub.font.color.rgb = MUTED_TEXT

    # Meta Info Table
    meta_tbl = doc.add_table(rows=4, cols=2)
    meta_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(meta_tbl, color="E0E0E0", sz="4")
    
    meta_data = [
        ("Nama Proyek", "CoinCollector_HananVictor (PTS Pemrograman Game Dev)"),
        ("Game Engine / Pipeline", "Unity 6 (6000.5.3f1) — Universal Render Pipeline (URP 2D)"),
        ("Target Platform & Build", "Standalone Windows (x86_64)"),
        ("Tanggal Dokumentasi", "November 2026")
    ]
    
    for i, (k, v) in enumerate(meta_data):
        row = meta_tbl.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.2)
        c1.width = Inches(4.3)
        set_cell_background(c0, "F4F6F9")
        set_cell_margins(c0, top=60, bottom=60, left=100, right=100)
        set_cell_margins(c1, top=60, bottom=60, left=100, right=100)
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_before = Pt(1)
        p0.paragraph_format.space_after = Pt(1)
        r0 = p0.add_run(k)
        r0.bold = True
        r0.font.size = Pt(9.5)
        r0.font.color.rgb = NAVY
        
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_before = Pt(1)
        p1.paragraph_format.space_after = Pt(1)
        r1 = p1.add_run(v)
        r1.font.size = Pt(9.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # ==========================================================
    # 2. RINGKASAN EKSEKUTIF ARSITEKTUR
    # ==========================================================
    h1 = doc.add_paragraph()
    h1.paragraph_format.space_before = Pt(14)
    h1.paragraph_format.space_after = Pt(6)
    r_h1 = h1.add_run("1. Ringkasan Eksekutif & Arsitektur Sistem")
    r_h1.font.name = "Segoe UI"
    r_h1.font.size = Pt(15)
    r_h1.font.bold = True
    r_h1.font.color.rgb = NAVY

    p_intro = doc.add_paragraph(
        "Proyek CoinCollector dibangun menggunakan arsitektur modular berbasis fitur (feature-driven) "
        "pada platform Unity 6 URP 2D. Arsitektur proyek mengombinasikan paradigma Object-Oriented Programming (OOP), "
        "pola desain Singleton, State Machine (FSM), Observer Pattern melalui Events & Delegates C#, "
        "serta arsitektur data-driven berbasis ScriptableObject untuk manajemen item inventaris."
    )
    p_intro.paragraph_format.line_spacing = 1.15
    p_intro.paragraph_format.space_after = Pt(6)

    add_callout(
        doc,
        "Seluruh skrip C# pada proyek telah diorganisir ke dalam sub-folder modular di bawah 'Assets/Scripts/': "
        "Core, Player, Enemies, dan Inventory (dengan sub-folder ScriptableObjects), serta folder khusus Events/ dan Editor/. "
        "Struktur ini menjamin integritas GUID, isolasi fitur, kemudahan kolaborasi tim, dan skalabilitas jangka panjang.",
        "Highlight Struktur Proyek:"
    )

    # Core Pillars Table
    pillars = [
        ("Core & Game Management", "GameManager mengelola alur menang/kalah, penghitungan koin, jumlah musuh aktif, sinkronisasi UI, dan restart scene."),
        ("Player Controller & Combat", "PlayerMovement menangani input gerak berbasis fisika Rigidbody2D, animator speed parameter, attack hitbox overlap, serta koleksi koin. PlayerHealth mengelola dual-layer Health & auto-regen Shield."),
        ("AI Enemy & Combat FSM", "State Machine (IDLE, PATROL, CHASE, ATTACK) di Enemy.cs berpadu dengan pergerakan fisika aktif dan tabrakan damage di EnemyAI.cs serta pelaporan eliminasi di EnemyHealth.cs."),
        ("Inventory & ScriptableObject", "InventoryManager mengatur pembukaan tas, time-freeze, slot stacking otomatis (maks 99), dan seleksi item. ItemDetails (ScriptableObject) memisahkan definisi data aset dari logika monobehaviour."),
        ("Event & Delegate Decoupling", "Implementasi Publisher-Subscriber menggunakan PemancarEvent (static event Action) dan PenerimaEvent (subscribe OnEnable / unsubscribe OnDisable) untuk mereduksi tight coupling.")
    ]

    p_tbl = doc.add_table(rows=len(pillars) + 1, cols=2)
    p_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(p_tbl, color="D0D5DD", sz="4")

    # Header
    hdr_cells = p_tbl.rows[0].cells
    hdr_cells[0].width = Inches(2.2)
    hdr_cells[1].width = Inches(4.3)
    set_cell_background(hdr_cells[0], "1F4E79")
    set_cell_background(hdr_cells[1], "1F4E79")
    set_cell_margins(hdr_cells[0], top=80, bottom=80, left=100, right=100)
    set_cell_margins(hdr_cells[1], top=80, bottom=80, left=100, right=100)
    
    r0 = hdr_cells[0].paragraphs[0].add_run("Pilar Sistem")
    r0.bold = True
    r0.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)
    r1 = hdr_cells[1].paragraphs[0].add_run("Deskripsi & Peran Arsitektur")
    r1.bold = True
    r1.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for idx, (p_name, p_desc) in enumerate(pillars):
        row = p_tbl.rows[idx + 1]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.2)
        c1.width = Inches(4.3)
        if idx % 2 == 1:
            set_cell_background(c0, "F8FAFC")
            set_cell_background(c1, "F8FAFC")
        set_cell_margins(c0, top=70, bottom=70, left=100, right=100)
        set_cell_margins(c1, top=70, bottom=70, left=100, right=100)
        
        pr0 = c0.paragraphs[0]
        pr0.paragraph_format.line_spacing = 1.15
        run0 = pr0.add_run(p_name)
        run0.bold = True
        run0.font.size = Pt(9.5)
        run0.font.color.rgb = NAVY
        
        pr1 = c1.paragraphs[0]
        pr1.paragraph_format.line_spacing = 1.15
        run1 = pr1.add_run(p_desc)
        run1.font.size = Pt(9.0)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # ==========================================================
    # 3. TABEL STRUKTUR SCRIPT & FOLDER LENGKAP
    # ==========================================================
    h2 = doc.add_paragraph()
    h2.paragraph_format.space_before = Pt(14)
    h2.paragraph_format.space_after = Pt(6)
    r_h2 = h2.add_run("2. Inventarisasi & Struktur Folder Skrip Proyek")
    r_h2.font.name = "Segoe UI"
    r_h2.font.size = Pt(15)
    r_h2.font.bold = True
    r_h2.font.color.rgb = NAVY

    p_struct = doc.add_paragraph(
        "Tabel berikut merangkum seluruh skrip C# pada proyek, lokasi path direktori, Unity GUID (dari file .cs.meta), "
        "kategori fungsional, dan status keterikatan objek di scene / prefab."
    )
    p_struct.paragraph_format.line_spacing = 1.15
    p_struct.paragraph_format.space_after = Pt(6)

    scripts_master = [
        # (No, Nama File, Kategori, Relative Path, GUID, Status / Attachment)
        ("1", "GameManager.cs", "Core", "Assets/Scripts/Core/", "0e2f44b6a4f2bd04ea894c340eea6ca9", "Aktif: GO 'GameManager'"),
        ("2", "StateZombie.cs", "Core", "Assets/Scripts/Core/", "fe15019a5e3c98d419a8cfdc679f54a1", "Enum Type (Dipakai Enemy.cs)"),
        ("3", "PlayerMovement.cs", "Player", "Assets/Scripts/Player/", "52f1270fa8ccdd5449fbb5ac975682d5", "Aktif: GO 'Player'"),
        ("4", "PlayerHealth.cs", "Player", "Assets/Scripts/Player/", "536bf28dc387ae9409c77a49d14708ee", "Aktif: GO 'Player'"),
        ("5", "Enemy.cs", "Enemies", "Assets/Scripts/Enemies/", "0a7c7b099fe999c49bdc942c96ccf610", "Aktif: GO 'Orc'"),
        ("6", "EnemyAI.cs", "Enemies", "Assets/Scripts/Enemies/", "66af829c1a9a88a40b543b90c0bf6c4e", "Aktif: 4 GO Orc Varian"),
        ("7", "EnemyHealth.cs", "Enemies", "Assets/Scripts/Enemies/", "6c8f8e1d6c61563498e59b97e1fd713b", "Aktif: 4 GO Orc Varian"),
        ("8", "IDamageable.cs", "Enemies", "Assets/Scripts/Enemies/", "6168124a0e2f0714c94fb87ae0401ea8", "Interface (Diimplementasi Enemy)"),
        ("9", "InventoryManager.cs", "Inventory", "Assets/Scripts/Inventory/", "0e5901c77e4349a438911a30c9ad8afd", "Aktif: GO 'InventoryManager'"),
        ("10", "ItemDetailsPanel.cs", "Inventory", "Assets/Scripts/Inventory/", "438b63dbe7e63ff4b9d866b7f64c6c8b", "Aktif: GO 'itemDescription'"),
        ("11", "WorldItem.cs", "Inventory", "Assets/Scripts/Inventory/", "6962d7bcbc9c0454aba6d056b8887467", "Aktif: GO 'Potion 1_0'"),
        ("12", "GrabableItem.cs", "Inventory", "Assets/Scripts/Inventory/", "5c443c571bf13a445b283ee293cbdb95", "Interface (Diimplementasi WorldItem)"),
        ("13", "ItemDetails.cs", "Inventory (SO)", "Assets/Scripts/Inventory/ScriptableObjects/", "89a9f1aa238cd814daad3f6f4a332486", "ScriptableObject (3 File .asset)"),
        ("14", "ItemSlot.cs", "Inventory (SO)", "Assets/Scripts/Inventory/ScriptableObjects/", "eea08762a2cbaef478991f41a9cccbec", "Aktif: 6 GO 'Item (0..5)'"),
        ("15", "BelajarDelegate.cs", "Events", "Assets/Events/", "89efa9a36339f5842bb4dfa8be57ed56", "Aktif: GO 'GameManager'"),
        ("16", "PemancarEvent.cs", "Events", "Assets/Events/", "3222feba45e600749a452a1e379ad988", "Aktif: GO 'PemancarEvent_GO'"),
        ("17", "PenerimaEvent.cs", "Events", "Assets/Events/", "16c1cdb7a2c73af4380a75684824ec15", "Aktif: GO 'Player'"),
        ("18", "DungeonMapBuilder.cs", "Editor Tool", "Assets/Editor/", "f8b5f05d7354b62449e982ae0503c5b4", "Editor Window (Tools Menu)"),
        ("19", "blyatman.cs", "Trash (Dead Code)", "Assets/Scripts/Trash/", "3cb291d69436a84459f261508f69009d", "TIDAK TERPASANG (Diisolasi)")
    ]

    t_all = doc.add_table(rows=len(scripts_master) + 1, cols=6)
    t_all.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_all, color="D0D5DD", sz="4")

    headers = ["No", "Nama Skrip", "Kategori", "Direktori Folder", "Unity GUID", "Status Penggunaan"]
    col_widths = [Inches(0.4), Inches(1.5), Inches(0.9), Inches(1.8), Inches(1.0), Inches(1.3)]

    for idx, h_text in enumerate(headers):
        c = t_all.rows[0].cells[idx]
        c.width = col_widths[idx]
        set_cell_background(c, "1F4E79")
        set_cell_margins(c, top=70, bottom=70, left=60, right=60)
        p = c.paragraphs[0]
        run = p.add_run(h_text)
        run.bold = True
        run.font.size = Pt(8.5)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for r_idx, row_data in enumerate(scripts_master):
        row = t_all.rows[r_idx + 1]
        bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        if row_data[2] == "Trash (Dead Code)":
            bg = "FFF5F5"
            
        for c_idx, val in enumerate(row_data):
            c = row.cells[c_idx]
            c.width = col_widths[c_idx]
            set_cell_background(c, bg)
            set_cell_margins(c, top=50, bottom=50, left=60, right=60)
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.05
            
            run = p.add_run(val)
            run.font.size = Pt(8.0)
            if c_idx == 1:
                run.bold = True
                run.font.color.rgb = NAVY
            elif c_idx == 4:
                run.font.name = "Consolas"
                run.font.size = Pt(7.0)
            elif c_idx == 5 and "TIDAK" in val:
                run.font.color.rgb = RGBColor(0xC0, 0x00, 0x00)
                run.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # ==========================================================
    # 4. DETAIL ANALISIS PER FITUR & ENTITAS
    # ==========================================================
    h3 = doc.add_paragraph()
    h3.paragraph_format.space_before = Pt(14)
    h3.paragraph_format.space_after = Pt(6)
    r_h3 = h3.add_run("3. Detail Analisis Fungsional, Logika, & Keterikatan Tiap Skrip")
    r_h3.font.name = "Segoe UI"
    r_h3.font.size = Pt(15)
    r_h3.font.bold = True
    r_h3.font.color.rgb = NAVY

    sections_detail = [
        {
            "category": "3.1 Fitur Core & Game Management",
            "desc": "Mengatur logika makro permainan, status menang/kalah, penghitungan objek koleksi, dan enum state machine.",
            "scripts": [
                {
                    "name": "GameManager.cs",
                    "path": "Assets/Scripts/Core/GameManager.cs",
                    "guid": "0e2f44b6a4f2bd04ea894c340eea6ca9",
                    "attached": "GameObject 'GameManager' pada scene MainScene.unity",
                    "summary": "Singleton pengatur siklus hidup game, skor, kondisi menang (seluruh musuh tereliminasi), kondisi kalah (pemain mati), dan sistem restart.",
                    "logic": [
                        "Pola Singleton: Menggunakan properti publik static 'Instance' dengan auto-destroy pada duplikat di Awake().",
                        "Inisialisasi Dinamis: Start() mendeteksi jumlah koin di scene via GameObject.FindGameObjectsWithTag('Coin') dan menghitung musuh aktif via HitungTotalMusuh().",
                        "Evaluasi Kemenangan: MusuhKalah(EnemyHealth) memantau sisa objek EnemyHealth aktif menggunakan Object.FindObjectsByType<EnemyHealth>(). Menang terpicu jika sisa musuh bernilai 0 atau musuhTerkalahkan mencapai totalMusuh.",
                        "Evaluasi Kekalahan: PlayerKalah() dipanggil langsung dari PlayerHealth saat nyawa pemain habis. Mengaktifkan teks status dan panel kalah.",
                        "Koleksi Koin: AmbilKoin() menambah skor lokal, memperbarui teks UI, serta mengalirkan penambahan item ke InventoryManager.Instance.AddItem(coinData).",
                        "Fallback UI OnGUI: Menyediakan GUI native darurat jika panel Canvas UI belum ditautkan pada Inspector, menampilkan banner kemenangan/kekalahan dan tombol restart."
                    ],
                    "code_snippet": "public static GameManager Instance { get; private set; }\npublic void MusuhKalah(EnemyHealth musuh) {\n    musuhTerkalahkan++;\n    EnemyHealth[] remaining = Object.FindObjectsByType<EnemyHealth>(FindObjectsInactive.Exclude);\n    int activeCount = remaining.Count(e => e != null && e != musuh && e.gameObject.activeInHierarchy);\n    if (activeCount <= 0) Menang();\n}"
                },
                {
                    "name": "StateZombie.cs",
                    "path": "Assets/Scripts/Core/StateZombie.cs",
                    "guid": "fe15019a5e3c98d419a8cfdc679f54a1",
                    "attached": "Tipe Data Enum — Digunakan pada variabel state di Enemy.cs",
                    "summary": "Mendefinisikan 4 status dasar Finite State Machine (FSM) musuh.",
                    "logic": [
                        "IDLE: Status diam / siaga saat target belum terdeteksi.",
                        "PATROL: Status berkeliling area saat pemain berada di luar jarak deteksi aman.",
                        "CHASE: Status aktif mengejar pemain ketika jarak Euclidean lebih kecil atau sama dengan jarakDeteksi (default 6 unit).",
                        "ATTACK: Status melancarkan serangan jarak dekat ketika pemain berada dalam jarakSerang (default 1.5 unit)."
                    ],
                    "code_snippet": "public enum StateZombie {\n    IDLE,\n    PATROL,\n    CHASE,\n    ATTACK\n}"
                }
            ]
        },
        {
            "category": "3.2 Fitur Player (Controller, Fisika, & Combat)",
            "desc": "Menangani interaksi pemain dengan dunia game: pergerakan fisika, serangan pedang, i-frames, serta pertahanan dual-layer Health & Shield.",
            "scripts": [
                {
                    "name": "PlayerMovement.cs",
                    "path": "Assets/Scripts/Player/PlayerMovement.cs",
                    "guid": "52f1270fa8ccdd5449fbb5ac975682d5",
                    "attached": "GameObject 'Player' pada scene MainScene.unity",
                    "summary": "Pengendali utama pergerakan 2D pemain berbasis fisika Rigidbody2D dan penyerangan kontak dengan hitbox pedang.",
                    "logic": [
                        "Input Gerak: Menggunakan Unity New Input System via callback OnMove(InputValue) untuk menangkap vektor 2D.",
                        "Fisika FixedUpdate: Menggerakkan pemain dengan rb.linearVelocity = arahGerak.normalized * kecepatan. Pendekatan velocity langsung ini mengeliminasi tabrakan fisik liar dan bug karakter terpental mundur.",
                        "Orientasi Visual: Skala horizontal (transform.localScale.x) dibalik sesuai arah pergerakan (+x kanan, -x kiri) untuk merotasi sprite tanpa merusak hierarki child.",
                        "Mekanisme Serangan (Combat): OnAttack() atau Spasi/Klik Kiri memicu trigger Animator 'Attack' dan mengeksekusi Physics2D.OverlapCircleAll di sekitar attackPoint. Musuh ber-collider yang terkena lapisan enemyLayers akan menerima pengurangan darah via enemyHealth.TakeDamage(attackDamage).",
                        "Pengambilan Koin: OnTriggerEnter2D mendeteksi tag 'Coin', menambah skor lokal, menghancurkan koin, dan memanggil GameManager.Instance.AmbilKoin()."
                    ],
                    "code_snippet": "void FixedUpdate() {\n    rb.linearVelocity = arahGerak.normalized * kecepatan;\n}\nvoid MulaiSerang() {\n    Collider2D[] hitEnemies = Physics2D.OverlapCircleAll(attackPoint.position, attackRange, enemyLayers);\n    foreach (Collider2D enemy in hitEnemies) {\n        EnemyHealth eh = enemy.GetComponent<EnemyHealth>();\n        if (eh != null) eh.TakeDamage(attackDamage);\n    }\n}"
                },
                {
                    "name": "PlayerHealth.cs",
                    "path": "Assets/Scripts/Player/PlayerHealth.cs",
                    "guid": "536bf28dc387ae9409c77a49d14708ee",
                    "attached": "GameObject 'Player' pada scene MainScene.unity",
                    "summary": "Pengelola sistem ketahanan pemain dengan arsitektur dual-layer (Shield menyerap damage terlebih dahulu, dilanjutkan Health), regenerasi perisai otomatis, dan i-Frames.",
                    "logic": [
                        "Dual-Layer Damage Absorption: Saat TakeDamage() dipanggil, poin serangan dialokasikan terlebih dahulu untuk memotong currentShield. Hanya kelebihan damage yang belum terserap yang diteruskan ke currentHealth.",
                        "Regenerasi Perisai Otomatis: Coroutine RegenShieldRoutine() berjalan setelah jeda shieldRegenDelay (4 detik) tanpa serangan. Perisai pulih 1 poin per shieldRegenRate (0.5 detik). Setiap serangan baru otomatis me-reset coroutine ini.",
                        "Invulnerability Frames (i-Frames): Menjaga pemain dari damage beruntun (spam hits) selama iFrameDuration (1 detik). Coroutine DamageRoutine() menghasilkan efek visual berkedip merah transparan pada SpriteRenderer.",
                        "Kematian & GameOver: Jika currentHealth <= 0, komponen PlayerMovement dan Collider2D dinonaktifkan secara permanen, dilanjutkan notifikasi ke GameManager.Instance.PlayerKalah()."
                    ],
                    "code_snippet": "public void TakeDamage(int damage) {\n    if (isInvulnerable) return;\n    int sisa = damage;\n    if (currentShield > 0) {\n        if (currentShield >= sisa) { currentShield -= sisa; sisa = 0; }\n        else { sisa -= currentShield; currentShield = 0; }\n    }\n    if (sisa > 0) currentHealth -= sisa;\n    if (currentHealth <= 0) Die(); else StartCoroutine(DamageRoutine());\n}"
                }
            ]
        },
        {
            "category": "3.3 Fitur Enemies (AI, State Machine, & Combat)",
            "desc": "Logika musuh mencakup navigasi pengejaran target, eksekusi damage kontak, respon animasi kedip saat terkena hit, dan pelaporan eliminasi ke GameManager.",
            "scripts": [
                {
                    "name": "Enemy.cs",
                    "path": "Assets/Scripts/Enemies/Enemy.cs",
                    "guid": "0a7c7b099fe999c49bdc942c96ccf610",
                    "attached": "GameObject 'Orc' pada scene MainScene.unity",
                    "summary": "Base class musuh yang mengimplementasikan FSM (StateZombie) dan interface IDamageable.",
                    "logic": [
                        "FSM Update: Update() mengevaluasi jarak target ke Player di PeriksaTransisi(). State berpindah dinamis antara ATTACK, CHASE, dan PATROL.",
                        "Pengejaran Objek: Method Kejar() mengarahkan posisi musuh menggunakan Vector2.MoveTowards menuju koordinat transform pemain.",
                        "Polymorphism: Menyediakan method virtual void Serang() yang dapat di-override oleh varian musuh khusus.",
                        "Implementasi IDamageable: KenaDamage(int) mengontrol pengurangan HP dan menghancurkan GameObject musuh saat mati."
                    ],
                    "code_snippet": "public class Enemy : MonoBehaviour, IDamageable {\n    private void PeriksaTransisi() {\n        float jarak = JarakKePlayer();\n        if (jarak <= jarakSerang) state = StateZombie.ATTACK;\n        else if (jarak <= jarakDeteksi) state = StateZombie.CHASE;\n        else state = StateZombie.PATROL;\n    }\n    public virtual void Serang() { }\n}"
                },
                {
                    "name": "EnemyAI.cs",
                    "path": "Assets/Scripts/Enemies/EnemyAI.cs",
                    "guid": "66af829c1a9a88a40b543b90c0bf6c4e",
                    "attached": "4 Objek Orc di MainScene: 'Orc', 'Orc_Corridor_Sentry', 'Orc_North_Guard', 'Orc_South_Guard'",
                    "summary": "Penggerak AI fisik musuh Orc di scene dengan pelacakan pemain dan pemberian damage kontak berulang.",
                    "logic": [
                        "Pelacakan Target: Menemukan GameObject bertag 'Player' di Start(), menghitung vektor arah ternormalisasi di FixedUpdate().",
                        "Gerak Fisika: Mendorong Rigidbody2D melalui rb.linearVelocity = arah * speed.",
                        "Orientasi Visual (Flip X): Membalik spriteRenderer.flipX berdasarkan sumbu horizontal arah gerak.",
                        "Kontak Damage: Menangani tabrakan via OnTriggerEnter2D dan OnCollisionEnter2D, mengambil PlayerHealth dan memberikan contactDamage (1)."
                    ],
                    "code_snippet": "void FixedUpdate() {\n    if (playerTransform == null) return;\n    Vector2 arah = (playerTransform.position - transform.position).normalized;\n    rb.linearVelocity = arah * speed;\n    spriteRenderer.flipX = arah.x < -0.05f;\n}"
                },
                {
                    "name": "EnemyHealth.cs",
                    "path": "Assets/Scripts/Enemies/EnemyHealth.cs",
                    "guid": "6c8f8e1d6c61563498e59b97e1fd713b",
                    "attached": "4 Objek Orc di MainScene: 'Orc', 'Orc_Corridor_Sentry', 'Orc_North_Guard', 'Orc_South_Guard'",
                    "summary": "Pengelola kesehatan spesifik musuh yang terhubung langsung dengan sistem kondisi menang di GameManager.",
                    "logic": [
                        "Penerimaan Hit: TakeDamage() mengurangi currentHealth dan memicu coroutine BlinkRed() untuk feedback visual selama 0.1 detik.",
                        "Eliminasi Terintegrasi: Method Die() memanggil GameManager.Instance.MusuhKalah(this) untuk memperbarui hitungan musuh kalah, lalu memanggil Destroy(gameObject)."
                    ],
                    "code_snippet": "void Die() {\n    if (GameManager.Instance != null)\n        GameManager.Instance.MusuhKalah(this);\n    Destroy(gameObject);\n}"
                },
                {
                    "name": "IDamageable.cs",
                    "path": "Assets/Scripts/Enemies/IDamageable.cs",
                    "guid": "6168124a0e2f0714c94fb87ae0401ea8",
                    "attached": "Interface Abstraksi — Diimplementasikan oleh Enemy.cs",
                    "summary": "Kontrak interface OOP untuk entitas yang dapat menerima damage.",
                    "logic": [
                        "Menjamin decoupling antara kelas penyerang (attacker) dan penerima serangan (victim) tanpa perlu referensi kelas konkret."
                    ],
                    "code_snippet": "public interface IDamageable {\n    void KenaDamage(int jumlah);\n}"
                }
            ]
        },
        {
            "category": "3.4 Fitur Inventory & ScriptableObject Management",
            "desc": "Sistem penyimpanan item pemain berbasis data ScriptableObject, penumpukan kuantitas otomatis, seleksi slot, dan panel inspeksi.",
            "scripts": [
                {
                    "name": "InventoryManager.cs",
                    "path": "Assets/Scripts/Inventory/InventoryManager.cs",
                    "guid": "0e5901c77e4349a438911a30c9ad8afd",
                    "attached": "GameObject 'InventoryManager' pada scene MainScene.unity",
                    "summary": "Pusat pengendali sistem tas pemain, time-freeze saat membuka canvas, stacking logic, dan koordinasi UI slot.",
                    "logic": [
                        "Input Toggle & Pause: Menangkap input action 'Inventory'. Saat dibuka, InventoryCanvas aktif dan Time.timeScale disetel 0f (game dijeda). Saat ditutup, timeScale kembali ke 1f.",
                        "Auto-Wiring Slot: Start() mengumpulkan seluruh komponen ItemSlot di bawah InventoryCanvas menggunakan GetComponentsInChildren<ItemSlot>(true).",
                        "Smart Stacking Logic: Method AddItem(ItemDetails item) memprioritaskan slot yang sudah memuat item sejenis dan belum penuh (CanStackWith). Jika tidak ditemukan, item ditaruh di slot kosong pertama (IsEmpty).",
                        "Koordinasi Seleksi: SelectSlot() mematikan status slot lain (DesselectAllSlot), menyalakan visual highlight selectedPanel, dan memanggil detailsPanel.Show(itemDetails, quantity)."
                    ],
                    "code_snippet": "public void AddItem(ItemDetails item) {\n    for (int i = 0; i < itemSlot.Length; i++) {\n        if (itemSlot[i].CanStackWith(item.ItemName)) {\n            itemSlot[i].AddQuantity(item.Quantity);\n            return;\n        }\n    }\n    for (int i = 0; i < itemSlot.Length; i++) {\n        if (itemSlot[i].IsEmpty) {\n            itemSlot[i].AddItem(item);\n            return;\n        }\n    }\n}"
                },
                {
                    "name": "ItemDetails.cs",
                    "path": "Assets/Scripts/Inventory/ScriptableObjects/ItemDetails.cs",
                    "guid": "89a9f1aa238cd814daad3f6f4a332486",
                    "attached": "ScriptableObject Blueprint — Digunakan oleh ItemCoin.asset, ItemBlueCoin.asset, ItemPotion.asset",
                    "summary": "Definisi data murni item yang dapat dibuat sebagai aset independen di Project Window via CreateAssetMenu.",
                    "logic": [
                        "Data Enkapsulasi: Menyimpan itemName, quantity default, itemIcon (Sprite), dan description (TextArea).",
                        "Read-Only Properties: Seluruh data diekspos melalui lambda properties (ItemName => itemName) untuk menjaga integritas data saat runtime."
                    ],
                    "code_snippet": "[CreateAssetMenu(fileName = \"ItemDetails\", menuName = \"Scriptable Objects/ItemDetails\")]\npublic class ItemDetails : ScriptableObject {\n    [SerializeField] private string itemName;\n    [SerializeField] private int quantity = 1;\n    [SerializeField] private Sprite itemIcon;\n    [SerializeField, TextArea] private string description;\n}"
                },
                {
                    "name": "ItemSlot.cs",
                    "path": "Assets/Scripts/Inventory/ScriptableObjects/ItemSlot.cs",
                    "guid": "eea08762a2cbaef478991f41a9cccbec",
                    "attached": "6 Komponen pada GameObject: 'Item', 'Item (1)', 'Item (2)', 'Item (3)', 'Item (4)', 'Item (5)'",
                    "summary": "Representasi visual dan interaktif satu kotak inventaris dengan penanganan event klik mouse.",
                    "logic": [
                        "IPointerClickHandler: Menangkap klik mouse EventSystem. Klik kiri memanggil inventoryManager.SelectSlot(this).",
                        "Stacking Checker: CanStackWith(string) memastikan slot belum penuh (!isFull), tidak kosong (!IsEmpty), dan memiliki nama item identik.",
                        "Update Tampilan: AddQuantity(int) menambah jumlah, mengecek batas maxStackSize (99), serta memperbarui teks quantityText dan ikon gambar itemImage."
                    ],
                    "code_snippet": "public void OnPointerClick(PointerEventData eventData) {\n    if (eventData.button == PointerEventData.InputButton.Left) {\n        if (inventoryManager != null) inventoryManager.SelectSlot(this);\n    }\n}"
                },
                {
                    "name": "ItemDetailsPanel.cs",
                    "path": "Assets/Scripts/Inventory/ItemDetailsPanel.cs",
                    "guid": "438b63dbe7e63ff4b9d866b7f64c6c8b",
                    "attached": "GameObject 'itemDescription' pada scene MainScene.unity",
                    "summary": "Pengontrol panel inspeksi detail item terpilih pada sisi kanan antarmuka inventaris.",
                    "logic": [
                        "Self-Validation: ValidateReferences() mendeteksi nama GameObject untuk mengoreksi penempatan referensi teks yang tertukar secara otomatis.",
                        "Presentasi Data: Show(ItemDetails, int) menampilkan sprite icon, judul nama, kuantitas saat ini, serta teks penjelasan item.",
                        "Pembersihan: Clear() mengosongkan gambar dan teks saat slot kosong terpilih."
                    ],
                    "code_snippet": "public void Show(ItemDetails item, int quantity) {\n    if (item == null) { Clear(); return; }\n    itemImage.sprite = item.ItemIcon;\n    itemImage.enabled = true;\n    itemNameText.text = item.ItemName;\n    itemQuantityText.text = \"Quantity: \" + quantity;\n    itemDescriptionText.text = item.Description;\n}"
                },
                {
                    "name": "WorldItem.cs",
                    "path": "Assets/Scripts/Inventory/WorldItem.cs",
                    "guid": "6962d7bcbc9c0454aba6d056b8887467",
                    "attached": "GameObject 'Potion 1_0' pada scene MainScene.unity",
                    "summary": "Entitas fisik di dunia game (lantai dungeon) yang mengaitkan data ScriptableObject untuk dapat dipungut pemain.",
                    "logic": [
                        "Grabable Contract: Mengimplementasikan GrabableItem. Memasukkan itemData ke InventoryManager.Instance.AddItem(itemData).",
                        "Trigger Collision: OnTriggerEnter2D memeriksa tag 'Player' dan mengeksekusi Grab() lalu menghancurkan objek fisik dari scene."
                    ],
                    "code_snippet": "public void Grab() {\n    if (InventoryManager.Instance != null && itemData != null) {\n        InventoryManager.Instance.AddItem(itemData);\n        Destroy(gameObject);\n    }\n}"
                },
                {
                    "name": "GrabableItem.cs",
                    "path": "Assets/Scripts/Inventory/GrabableItem.cs",
                    "guid": "5c443c571bf13a445b283ee293cbdb95",
                    "attached": "Interface Abstraksi — Diimplementasikan oleh WorldItem.cs",
                    "summary": "Interface kontrak untuk semua objek yang dapat dipungut ke dalam inventaris.",
                    "logic": [
                        "Mendefinisikan method wajib void Grab();"
                    ],
                    "code_snippet": "public interface GrabableItem {\n    void Grab();\n}"
                }
            ]
        },
        {
            "category": "3.5 Fitur Events & Delegates",
            "desc": "Implementasi komunikasi decoupled antar objek menggunakan delegate dan pola Publisher-Subscriber (C# Action event).",
            "scripts": [
                {
                    "name": "BelajarDelegate.cs",
                    "path": "Assets/Events/BelajarDelegate.cs",
                    "guid": "89efa9a36339f5842bb4dfa8be57ed56",
                    "attached": "GameObject 'GameManager' pada scene MainScene.unity",
                    "summary": "Skrip pembelajaran dan pengujian konsep delegate C#: Single-cast, Multi-cast, dan System.Action.",
                    "logic": [
                        "Single-cast Delegate: Mengasosiasikan satu method ke delegate ContohDelegate.",
                        "Multicast Delegate: Menggabungkan beberapa method (PanggilHello + PanggilWorld) menggunakan operator +=.",
                        "System.Action: Menggunakan tipe standar System.Action bawaan .NET tanpa deklarasi delegate manual."
                    ],
                    "code_snippet": "void UjiDelegate2() {\n    ContohDelegate Halo = PanggilHello;\n    Halo += PanggilWorld;\n    Halo();\n}"
                },
                {
                    "name": "PemancarEvent.cs",
                    "path": "Assets/Events/PemancarEvent.cs",
                    "guid": "3222feba45e600749a452a1e379ad988",
                    "attached": "GameObject 'PemancarEvent_GO' pada scene MainScene.unity",
                    "summary": "Komponen Publisher yang menyiarkan event global saat tombol keyboard spasi ditekan.",
                    "logic": [
                        "Mendeklarasikan static event Action SaatTombolDitekan.",
                        "Pada Update(), mendeteksi Keyboard.current.spaceKey.wasPressedThisFrame dan memanggil SaatTombolDitekan?.Invoke() dengan aman."
                    ],
                    "code_snippet": "public static event Action SaatTombolDitekan;\nvoid Update() {\n    if (Keyboard.current != null && Keyboard.current.spaceKey.wasPressedThisFrame) {\n        SaatTombolDitekan?.Invoke();\n    }\n}"
                },
                {
                    "name": "PenerimaEvent.cs",
                    "path": "Assets/Events/PenerimaEvent.cs",
                    "guid": "16c1cdb7a2c73af4380a75684824ec15",
                    "attached": "GameObject 'Player' pada scene MainScene.unity",
                    "summary": "Komponen Subscriber yang mendengarkan event siaran dari PemancarEvent.",
                    "logic": [
                        "Lifecycle-safe Subscription: Berlangganan di OnEnable() dan berhenti berlangganan di OnDisable() untuk mencegah dangling pointer.",
                        "Method Respon() dieksekusi setiap kali event SaatTombolDitekan disiarkan."
                    ],
                    "code_snippet": "private void OnEnable() { PemancarEvent.SaatTombolDitekan += Respon; }\nprivate void OnDisable() { PemancarEvent.SaatTombolDitekan -= Respon; }\nvoid Respon() { Debug.Log(\"Tombol ditekan\"); }"
                }
            ]
        },
        {
            "category": "3.6 Skrip Khusus & Editor Tools",
            "desc": "Skrip penunjang pengembangan dungeon di Unity Editor serta skrip uji coba yang telah diisolasi.",
            "scripts": [
                {
                    "name": "DungeonMapBuilder.cs",
                    "path": "Assets/Editor/DungeonMapBuilder.cs",
                    "guid": "f8b5f05d7354b62449e982ae0503c5b4",
                    "attached": "Editor Window — Menu 'Tools/Dungeon Generator/Open Dungeon Window...'",
                    "summary": "Perkakas kustom Unity Editor untuk mengotomasi generasi peta dungeon, 2-layer tilemap ber-collider, penempatan koin, musuh, dan dekorasi.",
                    "logic": [
                        "Pemisahan Layer: Membangun Floor_Tilemap (tanpa collider) dan Walls_Tilemap (dilengkapi TilemapCollider2D & CompositeCollider2D).",
                        "Generasi Entitas: Menghasilkan koin terstruktur, musuh Orc patroli, obor (Torch), guci (Vase), dan ramuan di bawah hierarki '--- DUNGEON ENTITIES ---'.",
                        "Pembersihan Otomatis: Menyediakan tombol Clear Map untuk mereset seluruh entitas dungeon lama secara aman dengan fitur Undo bawaan Unity Editor."
                    ],
                    "code_snippet": "[MenuItem(\"Tools/Dungeon Generator/Generate Dungeon Map\", false, 1)]\npublic static void MenuGenerateMap() {\n    DungeonMapBuilder window = GetWindow<DungeonMapBuilder>(\"Dungeon Generator\");\n    window.ExecuteGeneration();\n}"
                },
                {
                    "name": "blyatman.cs",
                    "path": "Assets/Scripts/Trash/blyatman.cs",
                    "guid": "3cb291d69436a84459f261508f69009d",
                    "attached": "TIDAK TERPASANG (Dead Code / Eksperimen OOP diisolasi di folder Trash)",
                    "summary": "Contoh turunan dari Enemy yang meng-override method Serang() dengan pesan log 'blyatman throwing vodka'.",
                    "logic": [
                        "Mendemonstrasikan konsep Inheritance dan Method Overriding.",
                        "Karena tidak digunakan di scene maupun prefab manapun, file dipindahkan ke folder Scripts/Trash/ guna menjaga kebersihan arsitektur kode produksi tanpa menghapus riwayat pembelajaran."
                    ],
                    "code_snippet": "public class blyatman : Enemy {\n    public bool flag = true;\n    public override void Serang() {\n        Debug.Log(\"blyatman throwing vodka\");\n    }\n}"
                }
            ]
        }
    ]

    for sec in sections_detail:
        h_sec = doc.add_paragraph()
        h_sec.paragraph_format.space_before = Pt(12)
        h_sec.paragraph_format.space_after = Pt(2)
        r_sec = h_sec.add_run(sec["category"])
        r_sec.font.name = "Segoe UI"
        r_sec.font.size = Pt(12.5)
        r_sec.font.bold = True
        r_sec.font.color.rgb = STEEL_BLUE

        p_desc = doc.add_paragraph(sec["desc"])
        p_desc.paragraph_format.line_spacing = 1.15
        p_desc.paragraph_format.space_after = Pt(6)

        for s in sec["scripts"]:
            # Card table for each script
            sc_tbl = doc.add_table(rows=6, cols=2)
            sc_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
            set_table_borders(sc_tbl, color="D0D5DD", sz="4")

            fields = [
                ("Nama File Skrip", s["name"]),
                ("Lokasi Path File", s["path"]),
                ("Unity Asset GUID", s["guid"]),
                ("Attached GameObject / Penggunaan", s["attached"]),
                ("Ringkasan Fungsi & Peran", s["summary"]),
            ]

            for row_i, (k, val) in enumerate(fields):
                c0, c1 = sc_tbl.rows[row_i].cells[0], sc_tbl.rows[row_i].cells[1]
                c0.width = Inches(2.0)
                c1.width = Inches(4.5)
                set_cell_background(c0, "F4F6F9")
                set_cell_margins(c0, top=50, bottom=50, left=80, right=80)
                set_cell_margins(c1, top=50, bottom=50, left=80, right=80)
                
                pk = c0.paragraphs[0]
                pk.paragraph_format.line_spacing = 1.1
                rk = pk.add_run(k)
                rk.bold = True
                rk.font.size = Pt(8.5)
                rk.font.color.rgb = NAVY
                
                pv = c1.paragraphs[0]
                pv.paragraph_format.line_spacing = 1.1
                rv = pv.add_run(val)
                rv.font.size = Pt(8.5)
                if k == "Nama File Skrip":
                    rv.bold = True
                    rv.font.color.rgb = NAVY
                elif k == "Unity Asset GUID":
                    rv.font.name = "Consolas"
                    rv.font.size = Pt(8.0)
                elif "TIDAK TERPASANG" in val:
                    rv.font.color.rgb = RGBColor(0xC0, 0x00, 0x00)
                    rv.bold = True

            # Row 5: Detailed Logic bullet points
            c_bot0, c_bot1 = sc_tbl.rows[5].cells[0], sc_tbl.rows[5].cells[1]
            c_bot0.width = Inches(2.0)
            c_bot1.width = Inches(4.5)
            set_cell_background(c_bot0, "F4F6F9")
            set_cell_margins(c_bot0, top=60, bottom=60, left=80, right=80)
            set_cell_margins(c_bot1, top=60, bottom=60, left=80, right=80)
            
            p_lbl = c_bot0.paragraphs[0]
            r_lbl = p_lbl.add_run("Rincian Logika & Alur Eksekusi")
            r_lbl.bold = True
            r_lbl.font.size = Pt(8.5)
            r_lbl.font.color.rgb = NAVY
            
            p_log = c_bot1.paragraphs[0]
            p_log.paragraph_format.line_spacing = 1.1
            for l_idx, logic_item in enumerate(s["logic"]):
                if l_idx > 0:
                    p_log = c_bot1.add_paragraph()
                    p_log.paragraph_format.line_spacing = 1.1
                    p_log.paragraph_format.space_before = Pt(2)
                    p_log.paragraph_format.space_after = Pt(2)
                r_bullet = p_log.add_run("• ")
                r_bullet.bold = True
                r_bullet.font.color.rgb = STEEL_BLUE
                r_text = p_log.add_run(logic_item)
                r_text.font.size = Pt(8.5)

            doc.add_paragraph().paragraph_format.space_after = Pt(4)
            if "code_snippet" in s and s["code_snippet"]:
                add_code_block(doc, s["code_snippet"])

    # ==========================================================
    # 5. MATRIKS TRACEABILITY GAMEOBJECT & SCENE
    # ==========================================================
    h4 = doc.add_paragraph()
    h4.paragraph_format.space_before = Pt(14)
    h4.paragraph_format.space_after = Pt(6)
    r_h4 = h4.add_run("4. Matriks Keterikatan GameObject & Scene (Attachment Traceability)")
    r_h4.font.name = "Segoe UI"
    r_h4.font.size = Pt(15)
    r_h4.font.bold = True
    r_h4.font.color.rgb = NAVY

    p_mat = doc.add_paragraph(
        "Tabel berikut memetakan setiap GameObject di dalam 'MainScene.unity' terhadap komponen skrip yang melekat padanya, "
        "beserta fungsi peran dari GameObject tersebut dalam gameplay."
    )
    p_mat.paragraph_format.line_spacing = 1.15
    p_mat.paragraph_format.space_after = Pt(6)

    matrix_data = [
        ("GameManager", "MainScene", "GameManager.cs\nBelajarDelegate.cs", "Pusat pengendali logika permainan, skor koin, evaluasi kemenangan, game over, dan demonstrasi delegate."),
        ("Player", "MainScene", "PlayerMovement.cs\nPlayerHealth.cs\nPenerimaEvent.cs", "Entitas karakter utama yang dikendalikan pengguna, menerima damage musuh, dan mendengarkan event tombol."),
        ("Orc", "MainScene", "Enemy.cs\nEnemyAI.cs\nEnemyHealth.cs", "Musuh dasar dengan FSM (StateZombie), pengejaran target berbasis fisika, dan pelaporan eliminasi ke GameManager."),
        ("Orc_Corridor_Sentry", "MainScene", "EnemyAI.cs\nEnemyHealth.cs", "Musuh penjaga koridor dengan kecepatan gerak khusus, mengejar pemain saat melintasi lorong."),
        ("Orc_North_Guard", "MainScene", "EnemyAI.cs\nEnemyHealth.cs", "Musuh penjaga ruangan utara dungeon dengan health terisolasi."),
        ("Orc_South_Guard", "MainScene", "EnemyAI.cs\nEnemyHealth.cs", "Musuh penjaga ruangan selatan dungeon yang terintegrasi dengan perhitungan total musuh GameManager."),
        ("InventoryManager", "MainScene", "InventoryManager.cs", "Pengendali antarmuka inventaris, sistem slot stacking (maks 99), dan seleksi item aktif."),
        ("itemDescription", "MainScene", "ItemDetailsPanel.cs", "Panel informasi sisi kanan pada UI inventaris untuk menampilkan gambar, judul, jumlah, dan deskripsi item terpilih."),
        ("Potion 1_0", "MainScene", "WorldItem.cs", "Item ramuan fisik di lantai dungeon yang dapat dipungut (Grab) pemain ke dalam slot inventaris."),
        ("Item (Item Slot 1)", "MainScene", "ItemSlot.cs", "Slot inventaris pertama pada InventoryCanvas dengan listener klik IPointerClickHandler."),
        ("Item (1) s/d (5)", "MainScene", "ItemSlot.cs", "Slot inventaris ke-2 sampai ke-6 pada Grid antarmuka inventaris."),
        ("PemancarEvent_GO", "MainScene", "PemancarEvent.cs", "Objek publisher yang memancarkan event static SaatTombolDitekan saat tombol Spasi ditekan."),
        ("ItemCoin.asset\nItemBlueCoin.asset\nItemPotion.asset", "Project Assets", "ItemDetails.cs", "Aset data ScriptableObject mandiri yang menyimpan definisi nama, ikon sprite, dan teks deskripsi.")
    ]

    m_tbl = doc.add_table(rows=len(matrix_data) + 1, cols=4)
    m_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(m_tbl, color="D0D5DD", sz="4")

    m_headers = ["Nama GameObject / Aset", "Lokasi Scene / Wadah", "Komponen Skrip Melekat", "Peran & Fungsi Gameplay"]
    m_widths = [Inches(1.8), Inches(1.1), Inches(1.6), Inches(2.0)]

    for idx, h_text in enumerate(m_headers):
        c = m_tbl.rows[0].cells[idx]
        c.width = m_widths[idx]
        set_cell_background(c, "1F4E79")
        set_cell_margins(c, top=70, bottom=70, left=60, right=60)
        p = c.paragraphs[0]
        run = p.add_run(h_text)
        run.bold = True
        run.font.size = Pt(8.5)
        run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    for r_idx, row_data in enumerate(matrix_data):
        row = m_tbl.rows[r_idx + 1]
        bg = "F8FAFC" if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            c = row.cells[c_idx]
            c.width = m_widths[c_idx]
            set_cell_background(c, bg)
            set_cell_margins(c, top=50, bottom=50, left=60, right=60)
            p = c.paragraphs[0]
            p.paragraph_format.line_spacing = 1.05
            run = p.add_run(val)
            run.font.size = Pt(8.0)
            if c_idx == 0:
                run.bold = True
                run.font.color.rgb = NAVY
            elif c_idx == 2:
                run.font.name = "Consolas"
                run.font.size = Pt(7.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # ==========================================================
    # 6. KESIMPULAN & REKOMENDASI PENGEMBANGAN
    # ==========================================================
    h5 = doc.add_paragraph()
    h5.paragraph_format.space_before = Pt(14)
    h5.paragraph_format.space_after = Pt(6)
    r_h5 = h5.add_run("5. Kesimpulan & Rekomendasi Pemeliharaan Kode")
    r_h5.font.name = "Segoe UI"
    r_h5.font.size = Pt(15)
    r_h5.font.bold = True
    r_h5.font.color.rgb = NAVY

    conclusions = [
        ("Modularitas & Enkapsulasi Tinggi", "Pemisahan folder ke Core, Player, Enemies, dan Inventory secara drastis meningkatkan keterbacaan kode dan memudahkan pelacakan bug."),
        ("Pemanfaatan Fitur Unity 6 yang Idiomatis", "Penggunaan Rigidbody2D.linearVelocity menggantikan properti usang velocity, serta integrasi New Input System via InputValue dan Keyboard.current."),
        ("Penerapan Pola Data-Driven yang Efektif", "Pemisahan data item ke dalam ScriptableObject (ItemDetails) menghindari hardcoding properti item di dalam prefab."),
        ("Rekomendasi Pemeliharaan", "Hindari pemanggilan Object.FindObjectsByType pada Update frame. Caching referensi di Awake/Start atau menggunakan pendekatan event-driven terbukti lebih efisien bagi alokasi memori dan performa CPU.")
    ]

    for title, desc in conclusions:
        p_c = doc.add_paragraph()
        p_c.paragraph_format.line_spacing = 1.15
        p_c.paragraph_format.space_before = Pt(3)
        p_c.paragraph_format.space_after = Pt(3)
        r_num = p_c.add_run("✔ ")
        r_num.bold = True
        r_num.font.color.rgb = STEEL_BLUE
        r_t = p_c.add_run(f"{title}: ")
        r_t.bold = True
        r_t.font.color.rgb = NAVY
        r_d = p_c.add_run(desc)
        r_d.font.color.rgb = DARK_TEXT

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # Save Document
    target_dir = r"C:\Users\ASUS\Documents\Laporan_ProjectGame"
    os.makedirs(target_dir, exist_ok=True)
    out_path = os.path.join(target_dir, "Laporan_Analisis_Script.docx")
    doc.save(out_path)
    print(f"DOCUMENT_SAVED_SUCCESSFULLY: {out_path}")
    print(f"FILE_SIZE: {os.path.getsize(out_path)} bytes")

if __name__ == "__main__":
    build_report()
