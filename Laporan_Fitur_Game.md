# LAPORAN ANALISIS FITUR PROYEK GAME: COINCOLLECTOR_HANANVICTOR

**Nama Proyek**: CoinCollector_HananVictor  
**Engine & Versi**: Unity 6 (6000.5.3f1)  
**Render Pipeline**: Universal Render Pipeline (URP 2D)  
**Platform Target**: Standalone Windows 64-bit  
**Tanggal Penyusunan**: 11 November 2026  

---

## DAFTAR ISI
1. [Ringkasan Eksekutif & Konsep Game](#1-ringkasan-eksekutif--konsep-game)
2. [Penerapan Prinsip Pemrograman Berorientasi Objek (OOP)](#2-penerapan-prinsip-pemrograman-berorientasi-objek-oop)
3. [Daftar & Penjelasan Rinci Fitur Game](#3-daftar--penjelasan-rinci-fitur-game)
   - [3.1. Sistem Kontrol & Pergerakan Pemain](#31-sistem-kontrol--pergerakan-pemain-player-movement)
   - [3.2. Sistem Tempur Jarak Dekat (Melee Combat)](#32-sistem-tempur-jarak-dekat-melee-combat)
   - [3.3. Sistem Tempur Jarak Jauh (Ranged Bow & Arrow)](#33-sistem-tempur-jarak-jauh-ranged-bow--arrow)
   - [3.4. Sistem Ketahanan: Health, Shield & i-Frames](#34-sistem-ketahanan-health-shield--i-frames)
   - [3.5. Sistem Kecerdasan Buatan Musuh (Enemy AI & State Machine)](#35-sistem-kecerdasan-buatan-musuh-enemy-ai--state-machine)
   - [3.6. Sistem Wave Spawner Otomatis & Intelijen Tilemap](#36-sistem-wave-spawner-otomatis--intelijen-tilemap)
   - [3.7. Sistem Inventori Data-Driven (ScriptableObject)](#37-sistem-inventori-data-driven-scriptableobject)
   - [3.8. Sistem Item Dunia & Kolektibel (World Items & Coins)](#38-sistem-item-dunia--kolektibel-world-items--coins)
   - [3.9. Sistem Game Manager & Siklus Permainan (Game Flow)](#39-sistem-game-manager--siklus-permainan-game-flow)
   - [3.10. Tooling Editor: Dungeon Map Generator](#310-tooling-editor-dungeon-map-generator)
   - [3.11. Sistem Arsitektur Event & Delegate](#311-sistem-arsitektur-event--delegate)
4. [Tabel Matriks Fitur, File & Skrip Terkait](#4-tabel-matriks-fitur-file--skrip-terkait)
5. [Kesimpulan](#5-kesimpulan)

---

## 1. Ringkasan Eksekutif & Konsep Game
**CoinCollector_HananVictor** adalah game aksi petualangan 2D top-down berlatar belakang ruang bawah tanah (*dungeon*). Pemain menjelajahi koridor dan ruangan dungeon, mengumpulkan koin dan item untuk meningkatkan skor, sambil bertahan hidup dari serbuan musuh Orc yang terus bermunculan.

Tujuan utama pemain adalah:
1. Bertahan hidup dari gelombang musuh selama durasi spawn aktif (1 menit).
2. Menghabisi seluruh musuh Orc yang tersisa di dungeon menggunakan kombinasi serangan pedang jarak dekat (*melee*) dan panah jarak jauh (*ranged*).
3. Mengumpulkan koin dan mengelola inventori item penunjang.

---

## 2. Penerapan Prinsip Pemrograman Berorientasi Objek (OOP)
Proyek ini mengimplementasikan 4 pilar utama OOP secara konsisten dalam struktur skrip C#:

| Pilar OOP | Implementasi pada Proyek | Skrip Terkait |
| :--- | :--- | :--- |
| **Abstraction** | Penggunaan interface `IDamageable` untuk menyeragamkan semua entitas yang dapat menerima damage, serta interface `GrabableItem` untuk semua objek yang dapat diambil. | `IDamageable.cs`, `GrabableItem.cs` |
| **Encapsulation** | Penggunaan modifier akses `protected` / `private` dengan atribut `[SerializeField]`, serta properti getter publik (`Speed`, `ContactDamage`, `CurrentState`, `ItemDetails`, dll.) untuk mencegah manipulasi data secara liar dari luar kelas. | `EnemyAI.cs`, `EnemyHealth.cs`, `PlayerHealth.cs`, `ItemSlot.cs` |
| **Inheritance** | Pewarisan kelas dasar `EnemyAI` ke sub-kelas khusus `OrcAI` yang mewarisi seluruh sistem navigasi, fisika, dan state machine musuh. | `EnemyAI.cs` $\rightarrow$ `OrcAI.cs` |
| **Polymorphism** | Penulisan method virtual `Serang(GameObject target)` dan `Hancur()` pada `EnemyAI` yang di-override pada `OrcAI` untuk mengubah perilaku serangan spesifik (menabrak player lalu langsung hancur). | `EnemyAI.cs`, `OrcAI.cs` |

---

## 3. Daftar & Penjelasan Rinci Fitur Game

### 3.1. Sistem Kontrol & Pergerakan Pemain (Player Movement)
* **File Terkait**:
  * Skrip: `Assets/Scripts/Player/PlayerMovement.cs`
  * Pengaturan Input: `Assets/Settings/InputSystem_Actions.inputactions`
  * Animasi: `Assets/Animations/Player/PlayerAnimatorController.controller`
* **Penjelasan Teknis**:
  * **Pergerakan 8 Arah Berbasis Fisika**: Menggunakan Unity *New Input System* dengan method pesan `OnMove(InputValue value)` untuk membaca input analog/tombol arah (WASD / Panah).
  * Pergerakan dieksekusi dalam `FixedUpdate()` dengan mengatur `rb.linearVelocity = arahGerak.normalized * kecepatan`, menghilangkan bug benturan liar dan pergerakan tersentak pada dinding.
  * **Auto-Flip Karakter**: Skala transform `transform.localScale` otomatis dibalik pada sumbu X berdasarkan arah `arahGerak.x`, sehingga karakter selalu menghadap ke arah jalannya.
  * **Transisi Animasi**: Parameter float `Speed` pada Animator diperbarui secara kontinu berdasarkan magnitude kuadrat pergerakan (`arahGerak.sqrMagnitude`) untuk memicu animasi *Player_Idle* dan *Player_Walk*.

---

### 3.2. Sistem Tempur Jarak Dekat (Melee Combat)
* **File Terkait**:
  * Skrip: `Assets/Scripts/Player/PlayerMovement.cs`
  * Animasi: Trigger parameter `Attack` pada `PlayerAnimatorController.controller`
* **Penjelasan Teknis**:
  * **Trigger Serangan**: Dapat dipicu menggunakan tombol Attack dari Input System, tombol **Spasi**, atau **Klik Kiri Mouse**.
  * **Sistem Cooldown**: Dibatasi oleh interval waktu `meleeCooldown` (1 detik) menggunakan perbandingan `Time.time < lastMeleeTime + meleeCooldown`.
  * **Deteksi Area Tebasan**: Menggunakan `Physics2D.OverlapCircleAll(attackPoint.position, attackRange, enemyLayers)`.
  * **Pemberian Kerusakan**: Musuh yang berada di dalam radius tebasan akan dipotong HP-nya melalui pemanggilan `EnemyHealth.TakeDamage(attackDamage)` atau `IDamageable.KenaDamage(attackDamage)`.
  * **Visualisasi Debug**: Method `OnDrawGizmosSelected()` menggambar lingkaran merah kawat pada scene view di sekitar `attackPoint` untuk mempermudah penyesuaian jangkauan tebasan di Inspector.

---

### 3.3. Sistem Tempur Jarak Jauh (Ranged Bow & Arrow)
* **File Terkait**:
  * Skrip: `Assets/Scripts/Player/PlayerMovement.cs`
  * Skrip Proyektil: `Assets/Scripts/Player/Arrow.cs`
  * Prefab: `Assets/Prefabs/ArrowProjectile.prefab`
* **Penjelasan Teknis**:
  * **Input & Bidikan**: Dipicu dengan **Klik Kanan Mouse**. Skrip menghitung vektor arah tembak dari `attackPoint` menuju koordinat kursor mouse di dunia game via `Camera.main.ScreenToWorldPoint(Mouse.current.position.ReadValue())`.
  * **Auto-Aim Character Facing**: Pemain otomatis membalikkan hadapannya menghadap ke arah bidikan kursor mouse saat menembakkan panah.
  * **Mekanika Proyektil Arrow**:
    * Panah diinstansiasi dengan rotasi yang diselaraskan secara otomatis (`Mathf.Atan2(direction.y, direction.x) * Mathf.Rad2Deg`).
    * Bergerak dengan kecepatan linier `12 unit/detik`.
    * Memiliki perlindungan pengecualian tabrakan (`tag == "Player"`, `tag == "Coin"`, dan `GrabableItem` diabaikan agar tidak menghancurkan koin atau item).
    * Memberikan kerusakan (10 damage) ke musuh yang terkena, lalu proyektil langsung hancur.
    * Hancur jika menabrak dinding dungeon solid (`!collision.isTrigger`).
    * Dilengkapi `lifetime` (3 detik) untuk mencegah penumpukan objek yang tidak mengenai target.

---

### 3.4. Sistem Ketahanan: Health, Shield & i-Frames
* **File Terkait**:
  * Skrip: `Assets/Scripts/Player/PlayerHealth.cs`
  * Interface: `Assets/Scripts/Enemies/IDamageable.cs`
  * Elemen UI: `HealthBar`, `HPText`, `ShieldBar`, `ShieldText` di bawah `HUDCanvas` pada `MainScene.unity`
* **Penjelasan Teknis**:
  * **Mekanisme Perisai Penahan Kerusakan (Shield Absorption)**:
    * Pemain memiliki 7 Health dan 5 Shield.
    * Saat serangan musuh masuk, Shield akan menyerap kerusakan terlebih dahulu.
    * Jika kerusakan melebihi sisa Shield, sisa kerusakan (*overflow damage*) baru akan memotong nilai Health.
  * **Regenerasi Perisai Otomatis (Shield Auto-Regeneration)**:
    * Coroutine `RegenShieldRoutine()` dimulai setelah jeda 4 detik (`shieldRegenDelay`) tanpa menerima serangan.
    * Perisai mengisi ulang 1 poin setiap 0.5 detik (`shieldRegenRate`) hingga penuh kembali.
  * **Masa Kebal Sementara (Invulnerability Frames / i-Frames)**:
    * Coroutine `DamageRoutine()` memberikan masa kebal selama 1 detik (`iFrameDuration`).
    * Disertai efek visual kedip merah transparan sebanyak 3 siklus untuk memberi indikasi visual yang jelas kepada pemain.
  * **Penanganan Kematian (`Die`)**:
    * Menonaktifkan komponen `PlayerMovement` dan `Collider2D` agar karakter tidak bisa digerakkan lagi.
    * Memanggil `GameManager.Instance.PlayerKalah()` untuk memicu Game Over.

---

### 3.5. Sistem Kecerdasan Buatan Musuh (Enemy AI & State Machine)
* **File Terkait**:
  * Base Class: `Assets/Scripts/Enemies/EnemyAI.cs`
  * Sub Class: `Assets/Scripts/Enemies/OrcAI.cs`
  * Enum: `Assets/Scripts/Core/StateZombie.cs`
  * Komponen HP Musuh: `Assets/Scripts/Enemies/EnemyHealth.cs`
  * Prefab: `Assets/Prefabs/OrcEnemy.prefab`
* **Penjelasan Teknis**:
  * **Finite State Machine (FSM)**:
    * Perilaku musuh diatur melalui enum `StateZombie`: `IDLE`, `PATROL`, `CHASE`, dan `ATTACK`.
    * Dalam state `CHASE`, musuh menghitung vektor arah ke pemain: `(playerTransform.position - transform.position).normalized * speed` dan secara otomatis membalikkan arah sprite renderer (`flipX`).
  * **Polymorphism Perilaku Serangan Orc (`OrcAI`)**:
    * Kelas `OrcAI` meng-override method `Serang(GameObject target)`.
    * Memanggil `base.Serang(target)` untuk mengurangi shield/health pemain sebesar `contactDamage`.
    * Jika `hancurSetelahMenyerang == true`, musuh langsung memanggil `Hancur()`, menghancurkan dirinya sendiri seketika sesuai aturan tugas game.
  * **Feedback Kerusakan Musuh (`EnemyHealth`)**:
    * Memiliki Max HP = 3.
    * Coroutine `BlinkRed()` mengubah warna sprite menjadi merah selama 0.1 detik saat terkena hit tebasan atau panah.
    * Saat HP $\le$ 0, memanggil `GameManager.Instance.MusuhKalah(this)` sebelum `Destroy(gameObject)`.

---

### 3.6. Sistem Wave Spawner Otomatis & Intelijen Tilemap
* **File Terkait**:
  * Skrip: `Assets/Scripts/Enemies/EnemySpawner.cs`
  * Prefab Musuh: `Assets/Prefabs/OrcEnemy.prefab`
  * Elemen Tilemap: `Floor_Tilemap`, `Walls_Tilemap`
* **Penjelasan Teknis**:
  * **Gelombang Pemunculan (Wave Spawner)**:
    * Memunculkan 3 unit Orc setiap interval 3 detik (`spawnInterval = 3f`, `jumlahPerWave = 3`).
  * **Batas Waktu Ketahanan (Survival Duration)**:
    * Spawner beroperasi dengan batas waktu 60 detik (1 menit). Setelah 60 detik tercapai, spawner otomatis dinonaktifkan (`spawnerAktif = false`).
  * **Pencegahan Spawn Cacat (Tilemap-Aware Positioning)**:
    * Skrip membaca cell bounds dari `Floor_Tilemap` dan mengumpulkan semua koordinat lantai yang valid.
    * Melakukan filter agar tidak memunculkan musuh di cell yang bertepatan dengan `Walls_Tilemap` atau memiliki collider solid (`obstacleLayers`).
    * Menentukan lokasi spawn di sekitar player dengan batas jarak aman (`minSpawnDistance = 3f` sampai `spawnRadius = 8f`) agar musuh tidak muncul tepat di atas posisi pemain.
    * Dilengkapi algoritma fallback ruangan jika tilemap tidak ditemukan di scene.
  * **Timer HUD**:
    * Menampilkan hitung mundur waktu spawn secara langsung di layar game.

---

### 3.7. Sistem Inventori Data-Driven (ScriptableObject)
* **File Terkait**:
  * Data Definition: `Assets/Scripts/Inventory/ScriptableObjects/ItemDetails.cs`
  * Data Assets:
    * `Assets/Scripts/Inventory/ScriptableObjects/ItemCoin.asset`
    * `Assets/Scripts/Inventory/ScriptableObjects/ItemBlueCoin.asset`
    * `Assets/Scripts/Inventory/ScriptableObjects/ItemPotion.asset`
  * Pengatur Slot: `Assets/Scripts/Inventory/ScriptableObjects/ItemSlot.cs`
  * Pengatur Inventori: `Assets/Scripts/Inventory/InventoryManager.cs`
  * Panel Detail: `Assets/Scripts/Inventory/ItemDetailsPanel.cs`
* **Penjelasan Teknis**:
  * **Arsitektur Data ScriptableObject**: Informasi item (nama, jumlah kuantitas awal, sprite ikon, dan teks deskripsi) tersimpan secara modular di luar scene sebagai aset.
  * **Buka / Tutup Inventori & Game Pause**:
    * Tombol **[E]** (melalui action "Inventory" pada Input System) digunakan untuk membuka atau menutup UI canvas inventori.
    * Saat inventori terbuka, waktu game dihentikan sementara (`Time.timeScale = 0f`), dan dilanjutkan kembali saat ditutup (`Time.timeScale = 1f`).
  * **Pengelompokan Slot & Penumpukan Item (Stacking)**:
    * Terdapat 16 slot inventori (`ItemSlot`).
    * Method `CanStackWith(itemName)` memeriksa apakah slot memiliki item yang sama dan belum penuh (`maxStackSize = 99`). Jika ya, kuantitas item akan digabungkan ke slot tersebut.
    * Jika tidak ada slot sejenis yang dapat ditumpuk, item dimasukkan ke slot kosong pertama (`IsEmpty`).
  * **Interaktivitas Klik & Panel Informasi**:
    * Implementasi interface `IPointerClickHandler` memungkinkan pemain mengeklik slot menggunakan mouse.
    * Klik kiri memanggil `SelectSlot(slot)`, mengaktifkan bingkai penanda (`selectedPanel`), dan mengirimkan data item ke `ItemDetailsPanel` untuk menampilkan gambar resolusi besar, nama, jumlah stok, dan deskripsi lengkap.

---

### 3.8. Sistem Item Dunia & Kolektibel (World Items & Coins)
* **File Terkait**:
  * Interface: `Assets/Scripts/Inventory/GrabableItem.cs`
  * Skrip Item Dunia: `Assets/Scripts/Inventory/WorldItem.cs`
  * Skrip Interaksi Koin: `PlayerMovement.OnTriggerEnter2D` & `GameManager.AmbilKoin`
* **Penjelasan Teknis**:
  * **Interface GrabableItem**: Menetapkan kontrak standar method `Grab()` untuk setiap objek di dunia game yang dapat dipungut.
  * **WorldItem Pickup**: Digunakan pada item obat (*Health Potion*) di dunia game. Menggunakan `OnTriggerEnter2D` untuk mendeteksi sentuhan pemain, memanggil `InventoryManager.Instance.AddItem(itemData)`, dan menghancurkan objek di scene.
  * **Koleksi Koin (Score & Inventory Sync)**:
    * Setiap koin memiliki tag `"Coin"` dan CircleCollider2D bertipe Trigger.
    * Saat pemain menyentuh koin: skor bertambah, koin di scene dihancurkan, dan data koin secara otomatis ditambahkan ke dalam inventori pemain melalui `GameManager.Instance.AmbilKoin()`.

---

### 3.9. Sistem Game Manager & Siklus Permainan (Game Flow)
* **File Terkait**:
  * Skrip: `Assets/Scripts/Core/GameManager.cs`
  * GameObject: `GameManager` pada `Assets/Scenes/MainScene.unity`
* **Penjelasan Teknis**:
  * **Singleton Pattern**: Menggunakan properti statis `public static GameManager Instance { get; private set; }` dengan perlindungan duplikasi objek pada method `Awake()`.
  * **Kondisi Menang (Victory)**:
    * `isGameWon` bernilai true saat: spawner musuh telah menyelesaikan durasi 60 detik (`EnemySpawner.Instance.IsSelesai()`) **DAN** jumlah musuh aktif di scene telah bernilai 0 (`activeCount <= 0`).
    * Mengaktifkan panel kemenangan `panelMenang` atau menampilkan pesan "VICTORY! Seluruh Musuh Telah Dikalahkan!".
  * **Kondisi Kalah (Game Over)**:
    * Dipicu ketika fungsi `PlayerKalah()` dipanggil oleh `PlayerHealth.Die()`.
    * Menampilkan panel kekalahan `panelKalah` dengan teks "GAME OVER! Kamu Telah Gugur".
  * **Sistem Restart Permainan**:
    * Pemain dapat menekan tombol **[R]** pada keyboard kapan saja saat kondisi `isGameOver` bernilai true.
    * Skrip mengembalikan skala waktu normal (`Time.timeScale = 1f`) dan memuat ulang scene aktif via `SceneManager.LoadScene(buildIndex)`.
  * **Fallback GUI**: Menyediakan method `OnGUI()` bawaan dengan tampilan box dan tombol "Main Lagi" otomatis apabila referensi UI Canvas belum dipasang di Inspector.

---

### 3.10. Tooling Editor: Dungeon Map Generator
* **File Terkait**:
  * Skrip Editor: `Assets/Editor/DungeonMapBuilder.cs`
  * Menu Editor: `Tools > Dungeon Generator > Open Dungeon Window...`
* **Penjelasan Teknis**:
  * **Jendela Kustom Unity Editor**: Membantu perancang game membuat layout level dungeon 2D siap pakai secara instan tanpa perlu menata tile satu per satu secara manual.
  * **Dua Layer Tilemap Otomatis**:
    * `Floor_Tilemap`: Menampung tile lantai walkable dengan sorting order 0.
    * `Walls_Tilemap`: Menampung tile tembok pembatas dengan sorting order 1, dilengkapi komponen `TilemapCollider2D` dan `CompositeCollider2D` (Rigidbody2D bertipe Static) untuk mencegah pemain dan musuh menembus dinding.
  * **Pilihan Layout**:
    1. *TwoRoomsWithCorridor*: Layout dua ruangan besar (Spawn Chamber & Treasure Room) yang dihubungkan oleh sebuah lorong koridor.
    2. *SingleEnclosedRoom*: Satu ruangan persegi dengan panjang dan lebar yang dapat dikonfigurasi melalui slider.
  * **Penataan Entitas Otomatis**:
    * Memasang koin dalam formasi garis sepanjang koridor dan formasi lingkaran di ruang harta.
    * Menempatkan musuh Orc di titik penjagaan strategis.
    * Meletakkan dekorasi obor dinding, guci hias, dan item potion.
    * Memindahkan posisi awal pemain langsung ke ruangan spawn.
  * **Fungsi Pembersih (Clear Dungeon)**: Menghapus tilemap dan seluruh entitas lama dalam sekali klik via `Undo.DestroyObjectImmediate` agar ramah terhadap history undo Unity.

---

### 3.11. Sistem Arsitektur Event & Delegate
* **File Terkait**:
  * `Assets/Events/PemancarEvent.cs`
  * `Assets/Events/PenerimaEvent.cs`
  * `Assets/Events/BelajarDelegate.cs`
* **Penjelasan Teknis**:
  * **Event-Driven Decoupling**:
    * `PemancarEvent.cs` mendeklarasikan `public static event Action SaatTombolDitekan;`. Saat tombol spasi ditekan, event dipancarkan melalui `SaatTombolDitekan?.Invoke()`.
    * `PenerimaEvent.cs` berlangganan event pada `OnEnable()` (`+= Respon`) dan berhenti berlangganan pada `OnDisable()` (`-= Respon`) untuk mencegah kebocoran memori (*memory leak*).
    * Pola ini memastikan pemancar input tidak perlu mengetahui siapa penerima aksinya (*loose coupling*).
  * **Pembelajaran Delegate**:
    * `BelajarDelegate.cs` mendemonstrasikan perbandingan antara *Single-Cast Delegate*, *Multicast Delegate* (menjalankan banyak fungsi secara berantai dengan operator `+=`), dan `System.Action`.

---

## 4. Tabel Matriks Fitur, File & Skrip Terkait

| No | Modul / Fitur | File Skrip Utama | File Dependensi / Aset Terkait | Peran Utama |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Player Movement** | `PlayerMovement.cs` | `InputSystem_Actions.inputactions`<br>`PlayerAnimatorController.controller` | Kontrol gerak 8 arah, auto-flip sprite, parameter animasi kecepatan, dan fisika velocity. |
| **2** | **Melee Combat** | `PlayerMovement.cs` | `EnemyHealth.cs`<br>`IDamageable.cs` | Deteksi serangan radius lingkaran di depan karakter, cooldown tebasan, dan pemberian damage. |
| **3** | **Ranged Combat** | `PlayerMovement.cs`<br>`Arrow.cs` | `ArrowProjectile.prefab` | Tembak panah ke posisi kursor mouse, orientasi sudut proyektil, damage, dan deteksi tabrakan. |
| **4** | **Health & Shield** | `PlayerHealth.cs` | `IDamageable.cs`<br>`HUDCanvas` (HealthBar, ShieldBar) | Penyerapan damage berlapis oleh perisai, auto-regenerasi shield, kebal sementara (i-frames), dan UI. |
| **5** | **Enemy AI & State** | `EnemyAI.cs`<br>`StateZombie.cs` | `MainScene.unity` | Base class AI musuh, navigasi pelacakan player, flip sprite, dan implementasi State Machine. |
| **6** | **Orc Specific Attack** | `OrcAI.cs` | `EnemyAI.cs`<br>`PlayerHealth.cs` | Polymorphism serang: memberikan damage tabrakan ke player lalu langsung meledak/hancur. |
| **7** | **Enemy Health** | `EnemyHealth.cs` | `IDamageable.cs`<br>`GameManager.cs` | Manajemen HP musuh, efek visual kedip merah saat kena hit, dan melapor ke GameManager saat mati. |
| **8** | **Wave Spawner** | `EnemySpawner.cs` | `OrcEnemy.prefab`<br>`Floor_Tilemap`<br>`Walls_Tilemap` | Memunculkan gelombang musuh (3 Orc / 3 detik), batas survival 60 detik, filter koordinat lantai dungeon. |
| **9** | **Item Data Asset** | `ItemDetails.cs` | `ItemCoin.asset`<br>`ItemBlueCoin.asset`<br>`ItemPotion.asset` | ScriptableObject blueprint untuk mendefinisikan nama, kuantitas awal, sprite ikon, dan deskripsi item. |
| **10** | **Inventory Manager** | `InventoryManager.cs` | `InventoryCanvas`<br>`ItemSlot.cs`<br>`ItemDetailsPanel.cs` | Buka-tutup inventori (tombol E), time freeze, penambahan item, seleksi slot, dan sistem stacking. |
| **11** | **Inventory Slot** | `ItemSlot.cs` | `ItemDetails.cs`<br>`QuantityText`<br>`SelectedPanel` | Menampilkan kuantitas dan icon di slot grid, handling klik mouse kiri/kanan, dan batas tumpukan (max 99). |
| **12** | **Item Detail View** | `ItemDetailsPanel.cs` | `InventoryCanvas` | Panel inspeksi yang menampilkan ikon besar, judul, jumlah, dan deskripsi lengkap item yang dipilih. |
| **13** | **World Items** | `WorldItem.cs`<br>`GrabableItem.cs` | `ItemPotion.asset` | Objek obat di dunia yang otomatis diambil dan masuk ke inventori saat disentuh pemain. |
| **14** | **Game Loop & Rules** | `GameManager.cs` | `HUDCanvas` (PanelMenang, PanelKalah)<br>`PlayerHealth.cs`<br>`EnemyHealth.cs` | Menghitung total koin & musuh, memvalidasi kondisi Menang (Victory) dan Kalah (Game Over), restart [R]. |
| **15** | **Level Generator** | `DungeonMapBuilder.cs` | `Set 1.png` (Spritesheet)<br>`MaterialKoin.mat` | Tool Unity Editor untuk men-generate layout map dungeon 2 layer Tilemap beserta collider dan entitas. |
| **16** | **Event Architecture** | `PemancarEvent.cs`<br>`PenerimaEvent.cs`<br>`BelajarDelegate.cs` | `MainScene.unity` | Pola arsitektur event decoupling menggunakan C# `event Action` dan studi kasus delegasi fungsi. |

---

## 5. Kesimpulan
Proyek game **CoinCollector_HananVictor** memiliki arsitektur yang solid dan terstruktur dengan rapi:
1. **Gameplay Lengkap**: Menggabungkan elemen aksi eksplorasi dungeon, pertarungan melee dan ranged, mekanisme survival perisai berlapis, dan manajemen inventori item.
2. **Kepatuhan Standar Pemrograman**: Memenuhi seluruh kaidah Object-Oriented Programming (OOP) meliputi Abstraction, Encapsulation, Inheritance, dan Polymorphism, serta didukung arsitektur modular berbasis ScriptableObject dan Event-Driven Programming.
3. **Produktivitas Editor**: Dilengkapi tool kustom (*DungeonMapBuilder*) yang mempermudah proses level design secara efisien langsung di Unity Editor.
