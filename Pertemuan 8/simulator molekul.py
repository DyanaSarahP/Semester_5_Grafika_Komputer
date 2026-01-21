"""
SIMULATOR MOLEKUL 3D INTERAKTIF
Menggunakan Ursina Engine
Author: [DyanaSarah]

KONTROL:
- Mouse: Drag untuk rotasi view
- 1-5: Ganti molekul (H2O, CO2, NH3, CH4, O2)
- R: Reset view
- A: Toggle auto-rotate
- P: Toggle proyeksi (Perspektif/Ortogonal)
- Arrow Keys: Rotasi manual
- Scroll: Zoom in/out
- G: Toggle grid
- ESC: Keluar
"""

from ursina import *

# Data molekul
molekul_data = {
    'H2O': {
        'nama': 'Air (H2O)',
        'atoms': [
            {'element': 'O', 'pos': (0, 0, 0), 'color': color.red, 'scale': 0.6},
            {'element': 'H', 'pos': (0.76, 0.59, 0), 'color': color.white, 'scale': 0.4},
            {'element': 'H', 'pos': (-0.76, 0.59, 0), 'color': color.white, 'scale': 0.4}
        ],
        'bonds': [(0, 1), (0, 2)],
        'info': 'Molekul air: 2 Hidrogen + 1 Oksigen',
        'struktur': 'Bengkok (Bent)',
        'massa': '18.015 g/mol',
        'sudut': '104.5 derajat'
    },
    'CO2': {
        'nama': 'Karbon Dioksida (CO2)',
        'atoms': [
            {'element': 'C', 'pos': (0, 0, 0), 'color': color.gray, 'scale': 0.5},
            {'element': 'O', 'pos': (1.2, 0, 0), 'color': color.red, 'scale': 0.6},
            {'element': 'O', 'pos': (-1.2, 0, 0), 'color': color.red, 'scale': 0.6}
        ],
        'bonds': [(0, 1), (0, 2)],
        'info': 'Gas rumah kaca dengan ikatan rangkap dua',
        'struktur': 'Linear',
        'massa': '44.01 g/mol',
        'sudut': '180 derajat'
    },
    'NH3': {
        'nama': 'Amonia (NH3)',
        'atoms': [
            {'element': 'N', 'pos': (0, 0, 0), 'color': color.blue, 'scale': 0.55},
            {'element': 'H', 'pos': (0.94, 0.33, 0), 'color': color.white, 'scale': 0.4},
            {'element': 'H', 'pos': (-0.47, 0.33, 0.82), 'color': color.white, 'scale': 0.4},
            {'element': 'H', 'pos': (-0.47, 0.33, -0.82), 'color': color.white, 'scale': 0.4}
        ],
        'bonds': [(0, 1), (0, 2), (0, 3)],
        'info': 'Basa lemah dengan bau menyengat',
        'struktur': 'Piramida Trigonal',
        'massa': '17.031 g/mol',
        'sudut': '107 derajat'
    },
    'CH4': {
        'nama': 'Metana (CH4)',
        'atoms': [
            {'element': 'C', 'pos': (0, 0, 0), 'color': color.gray, 'scale': 0.5},
            {'element': 'H', 'pos': (0.63, 0.63, 0.63), 'color': color.white, 'scale': 0.4},
            {'element': 'H', 'pos': (-0.63, -0.63, 0.63), 'color': color.white, 'scale': 0.4},
            {'element': 'H', 'pos': (-0.63, 0.63, -0.63), 'color': color.white, 'scale': 0.4},
            {'element': 'H', 'pos': (0.63, -0.63, -0.63), 'color': color.white, 'scale': 0.4}
        ],
        'bonds': [(0, 1), (0, 2), (0, 3), (0, 4)],
        'info': 'Komponen utama gas alam',
        'struktur': 'Tetrahedral',
        'massa': '16.043 g/mol',
        'sudut': '109.5 derajat'
    },
    'O2': {
        'nama': 'Oksigen (O2)',
        'atoms': [
            {'element': 'O', 'pos': (0.6, 0, 0), 'color': color.red, 'scale': 0.6},
            {'element': 'O', 'pos': (-0.6, 0, 0), 'color': color.red, 'scale': 0.6}
        ],
        'bonds': [(0, 1)],
        'info': 'Essential untuk respirasi aerobik',
        'struktur': 'Linear',
        'massa': '31.998 g/mol',
        'sudut': '180 derajat'
    }
}

# Inisialisasi Ursina
app = Ursina()
window.title = 'Simulator Molekul 3D - Ursina Engine'
window.borderless = False
window.fullscreen = False
window.exit_button.visible = False
window.fps_counter.enabled = False

# Variabel global
current_molecule = 'H2O'
auto_rotate = True
show_grid = True
molecule_group = Entity()
atoms_list = []
bonds_list = []
labels_list = []

# Setup camera
camera.position = (0, 0, -8)
camera.rotation_x = 0
camera.rotation_y = 0

# Fungsi untuk membuat bond (ikatan)
def create_bond(pos1, pos2):
    # Hitung arah dan jarak
    direction = Vec3(pos2[0] - pos1[0], pos2[1] - pos1[1], pos2[2] - pos1[2])
    distance = direction.length()
    
    # Buat cylinder
    bond = Entity(
        model='cylinder',
        color=color.light_gray,
        scale=(0.1, distance, 0.1),
        position=((pos1[0] + pos2[0])/2, (pos1[1] + pos2[1])/2, (pos1[2] + pos2[2])/2),
        parent=molecule_group
    )
    
    # Rotasi cylinder agar menghadap dari pos1 ke pos2
    bond.look_at(Vec3(pos2[0], pos2[1], pos2[2]))
    bond.rotation_x += 90
    
    return bond

# Fungsi untuk membuat molekul
def create_molecule(mol_key):
    global atoms_list, bonds_list, labels_list, molecule_group
    
    # Hapus molekul lama
    for atom in atoms_list:
        destroy(atom)
    for bond in bonds_list:
        destroy(bond)
    for label in labels_list:
        destroy(label)
    
    atoms_list = []
    bonds_list = []
    labels_list = []
    
    mol = molekul_data[mol_key]
    
    # Buat bonds dulu (biar di belakang)
    for bond_idx in mol['bonds']:
        atom1 = mol['atoms'][bond_idx[0]]
        atom2 = mol['atoms'][bond_idx[1]]
        bond = create_bond(atom1['pos'], atom2['pos'])
        bonds_list.append(bond)
    
    # Buat atoms
    for atom_data in mol['atoms']:
        atom = Entity(
            model='sphere',
            color=atom_data['color'],
            scale=atom_data['scale'],
            position=atom_data['pos'],
            parent=molecule_group
        )
        atoms_list.append(atom)
        
        # Label untuk atom
        label = Text(
            text=atom_data['element'],
            position=(atom_data['pos'][0], atom_data['pos'][1] + atom_data['scale'] + 0.3, atom_data['pos'][2]),
            scale=2,
            color=color.yellow,
            origin=(0, 0),
            parent=molecule_group,
            billboard=True
        )
        labels_list.append(label)
    
    update_ui()

# UI Panel Kiri (Proyeksi & Transformasi)
panel_left = Entity(
    model='quad',
    color=color.rgba(0, 100, 50, 200),
    scale=(0.48, 0.28),
    position=(-0.61, 0.36),
    z=1,
    parent=camera.ui
)

ui_title = Text(
    text='PROYEKSI: PERSPEKTIF',
    position=(-0.85, 0.46),
    scale=1.5,
    color=color.rgb(100, 255, 200),
    origin=(-0.5, 0.5),
    parent=camera.ui
)

ui_objek = Text(
    text='Objek: Air (H2O)',
    position=(-0.85, 0.42),
    scale=1.0,
    color=color.white,
    origin=(-0.5, 0.5),
    parent=camera.ui
)

ui_translasi = Text(
    text='1. TRANSLASI: (0, 0, 0)',
    position=(-0.85, 0.37),
    scale=0.8,
    color=color.rgb(100, 200, 255),
    origin=(-0.5, 0.5),
    parent=camera.ui
)

ui_rotasi = Text(
    text='2. ROTASI: X=0° Y=0° Z=0°',
    position=(-0.85, 0.34),
    scale=0.8,
    color=color.rgb(255, 150, 100),
    origin=(-0.5, 0.5),
    parent=camera.ui
)

ui_skala = Text(
    text='3. SKALA: 1.00x',
    position=(-0.85, 0.31),
    scale=0.8,
    color=color.rgb(255, 200, 100),
    origin=(-0.5, 0.5),
    parent=camera.ui
)

ui_refleksi = Text(
    text='4. REFLEKSI: X=1 Y=1 Z=1',
    position=(-0.85, 0.28),
    scale=0.8,
    color=color.rgb(150, 150, 255),
    origin=(-0.5, 0.5),
    parent=camera.ui
)

ui_keyboard1 = Text(
    text='Keyboard: Arrow=Rot | 1-5=Molekul | +/-=Zoom',
    position=(-0.85, 0.24),
    scale=0.7,
    color=color.rgb(180, 180, 180),
    origin=(-0.5, 0.5),
    parent=camera.ui
)

ui_keyboard2 = Text(
    text='R=Reset | P=Proyeksi | G=Grid | A/Space=AutoRot',
    position=(-0.85, 0.22),
    scale=0.7,
    color=color.rgb(180, 180, 180),
    origin=(-0.5, 0.5),
    parent=camera.ui
)

# UI Panel Kanan (Info Molekul)
panel_right = Entity(
    model='quad',
    color=color.rgba(80, 50, 0, 200),
    scale=(0.4, 0.32),
    position=(0.60, 0.34),
    z=1,
    parent=camera.ui
)

ui_info_title = Text(
    text='INFO MOLEKUL',
    position=(0.42, 0.46),
    scale=1.5,
    color=color.rgb(255, 200, 100),
    origin=(-0.5, 0.5),
    parent=camera.ui
)

ui_nama = Text(
    text='Air (H2O)',
    position=(0.42, 0.42),
    scale=1.2,
    color=color.white,
    origin=(-0.5, 0.5),
    parent=camera.ui
)

ui_struktur = Text(
    text='Struktur: Bengkok (Bent)',
    position=(0.42, 0.38),
    scale=0.8,
    color=color.rgb(200, 200, 200),
    origin=(-0.5, 0.5),
    parent=camera.ui
)

ui_sudut = Text(
    text='Sudut: 104.5 derajat',
    position=(0.42, 0.35),
    scale=0.8,
    color=color.rgb(200, 200, 200),
    origin=(-0.5, 0.5),
    parent=camera.ui
)

ui_massa = Text(
    text='Massa: 18.015 g/mol',
    position=(0.42, 0.32),
    scale=0.8,
    color=color.rgb(200, 200, 200),
    origin=(-0.5, 0.5),
    parent=camera.ui
)

ui_komposisi = Text(
    text='Atom: 3 | Ikatan: 2',
    position=(0.42, 0.29),
    scale=0.8,
    color=color.rgb(200, 200, 200),
    origin=(-0.5, 0.5),
    parent=camera.ui
)

ui_deskripsi = Text(
    text='Molekul air: 2 Hidrogen + 1 Oksigen',
    position=(0.42, 0.25),
    scale=0.7,
    color=color.rgb(180, 255, 180),
    origin=(-0.5, 0.5),
    parent=camera.ui
)

ui_hint = Text(
    text='Tekan 1-5 untuk ganti molekul',
    position=(0.42, 0.21),
    scale=0.7,
    color=color.rgb(150, 150, 150),
    origin=(-0.5, 0.5),
    parent=camera.ui
)

ui_autorot = Text(
    text='Auto-Rotate: ON',
    position=(0.42, 0.18),
    scale=0.8,
    color=color.rgb(100, 255, 100),
    origin=(-0.5, 0.5),
    parent=camera.ui
)

# Status bar bawah
panel_bottom = Entity(
    model='quad',
    color=color.rgba(30, 30, 30, 230),
    scale=(2, 0.05),
    position=(0, -0.475),
    z=1,
    parent=camera.ui
)

ui_status = Text(
    text='Molekul: Air (H2O) | Proyeksi: PERSPEKTIF | Grid: ON | Auto-Rotate: ON',
    position=(0, -0.47),
    scale=0.8,
    color=color.rgb(200, 200, 200),
    origin=(0, 0),
    parent=camera.ui
)

# Grid
grid_entity = Entity(model=Grid(20, 20), scale=10, rotation_x=90, color=color.rgba(100, 100, 100, 50))

# Fungsi untuk update UI
def update_ui():
    mol = molekul_data[current_molecule]
    ui_objek.text = f'Objek: {mol["nama"]}'
    ui_rotasi.text = f'2. ROTASI: X={int(molecule_group.rotation_x)}° Y={int(molecule_group.rotation_y)}° Z={int(molecule_group.rotation_z)}°'
    ui_skala.text = f'3. SKALA: {molecule_group.scale_x:.2f}x'
    
    ui_nama.text = mol['nama']
    ui_struktur.text = f'Struktur: {mol["struktur"]}'
    ui_sudut.text = f'Sudut: {mol["sudut"]}'
    ui_massa.text = f'Massa: {mol["massa"]}'
    ui_komposisi.text = f'Atom: {len(mol["atoms"])} | Ikatan: {len(mol["bonds"])}'
    ui_deskripsi.text = mol['info']
    
    ui_autorot.text = f'Auto-Rotate: {"ON" if auto_rotate else "OFF"}'
    ui_autorot.color = color.rgb(100, 255, 100) if auto_rotate else color.rgb(255, 100, 100)
    
    proj_mode = 'PERSPEKTIF' if camera.fov != 0 else 'ORTOGONAL'
    ui_title.text = f'PROYEKSI: {proj_mode}'
    
    ui_status.text = f'Molekul: {mol["nama"]} | Proyeksi: {proj_mode} | Grid: {"ON" if grid_entity.enabled else "OFF"} | Auto-Rotate: {"ON" if auto_rotate else "OFF"}'

# Input handling
def input(key):
    global current_molecule, auto_rotate, show_grid
    
    # Ganti molekul
    if key == '1':
        current_molecule = 'H2O'
        create_molecule(current_molecule)
    elif key == '2':
        current_molecule = 'CO2'
        create_molecule(current_molecule)
    elif key == '3':
        current_molecule = 'NH3'
        create_molecule(current_molecule)
    elif key == '4':
        current_molecule = 'CH4'
        create_molecule(current_molecule)
    elif key == '5':
        current_molecule = 'O2'
        create_molecule(current_molecule)
    
    # Rotasi manual
    elif key == 'left arrow':
        molecule_group.rotation_y -= 5
        update_ui()
    elif key == 'right arrow':
        molecule_group.rotation_y += 5
        update_ui()
    elif key == 'up arrow':
        molecule_group.rotation_x -= 5
        update_ui()
    elif key == 'down arrow':
        molecule_group.rotation_x += 5
        update_ui()
    
    # Zoom
    elif key == '+' or key == '=':
        molecule_group.scale *= 1.1
        update_ui()
    elif key == '-':
        molecule_group.scale *= 0.9
        update_ui()
    
    # Reset
    elif key == 'r':
        molecule_group.rotation = (0, 0, 0)
        molecule_group.scale = 1
        update_ui()
    
    # Toggle auto-rotate
    elif key == 'a' or key == 'space':
        auto_rotate = not auto_rotate
        update_ui()
    
    # Toggle proyeksi
    elif key == 'p':
        if camera.fov == 90:
            camera.fov = 0  # Orthographic
        else:
            camera.fov = 90  # Perspective
        update_ui()
    
    # Toggle grid
    elif key == 'g':
        grid_entity.enabled = not grid_entity.enabled
        update_ui()
    
    # Scroll zoom
    elif key == 'scroll up':
        molecule_group.scale *= 1.05
        update_ui()
    elif key == 'scroll down':
        molecule_group.scale *= 0.95
        update_ui()

# Update loop
def update():
    if auto_rotate:
        molecule_group.rotation_y += 20 * time.dt
        if int(time.time() * 2) % 2 == 0:  # Update UI setiap 0.5 detik
            update_ui()

# Buat molekul awal
create_molecule(current_molecule)

# Print info
print("="*60)
print("SIMULATOR MOLEKUL 3D - URSINA ENGINE")
print("="*60)
print("Program siap! Kontrol ada di window.")
print("="*60)

# Run aplikasi
app.run()