using System.Collections.Generic;
using UnityEngine;
using UnityEngine.Tilemaps;
using TMPro;

public class EnemySpawner : MonoBehaviour
{
    [Header("Spawner Settings")]
    [SerializeField] private GameObject orcPrefab;          // Prefab Orc yang akan di-spawn
    [SerializeField] private float spawnInterval = 3f;      // Spawn setiap 3 detik
    [SerializeField] private int jumlahPerWave = 3;         // 3 Orc per wave
    [SerializeField] private float durasiSpawn = 60f;       // Berhenti spawn setelah 60 detik (1 menit)

    [Header("Dungeon Boundary & Tilemap")]
    [SerializeField] private Tilemap floorTilemap;          // Tilemap lantai dungeon (area yang boleh di-spawn)
    [SerializeField] private Tilemap wallsTilemap;          // Tilemap dinding dungeon (area yang dilarang)
    [SerializeField] private LayerMask obstacleLayers;      // Layer collider dinding / rintangan

    [Header("Spawn Distance")]
    [SerializeField] private float spawnRadius = 8f;        // Jarak radius maksimal spawn dari player
    [SerializeField] private float minSpawnDistance = 3f;   // Jarak minimal dari player agar tidak spawn tepat di atas player

    [Header("UI Timer (Opsional)")]
    [SerializeField] private TextMeshProUGUI timerText;     // Teks UI untuk menampilkan sisa waktu spawn

    public static EnemySpawner Instance { get; private set; }

    private float timerSpawn;           // Hitung mundur interval spawn
    private float waktuBerjalan;        // Total waktu yang sudah berjalan
    private bool spawnerAktif = true;   // Apakah spawner masih aktif
    private Transform playerTransform;

    // Kumpulan titik lantai yang valid & berada di dalam dungeon
    private List<Vector3> validDungeonPositions = new List<Vector3>();

    private void Awake()
    {
        if (Instance != null && Instance != this)
        {
            Destroy(gameObject);
        }
        else
        {
            Instance = this;
        }
    }

    void Start()
    {
        // Cari Player di scene
        GameObject playerObj = GameObject.FindGameObjectWithTag("Player");
        if (playerObj != null)
        {
            playerTransform = playerObj.transform;
        }

        // Cari Tilemaps dungeon jika belum di-assign di Inspector
        if (floorTilemap == null)
        {
            GameObject floorObj = GameObject.Find("Floor_Tilemap");
            if (floorObj != null) floorTilemap = floorObj.GetComponent<Tilemap>();
        }

        if (wallsTilemap == null)
        {
            GameObject wallsObj = GameObject.Find("Walls_Tilemap");
            if (wallsObj != null) wallsTilemap = wallsObj.GetComponent<Tilemap>();
        }

        // Kumpulkan semua koordinat lantai di dalam dungeon
        KumpulkanPosisiLantaiDungeon();

        timerSpawn = spawnInterval;
        waktuBerjalan = 0f;

        UpdateTimerUI();
    }

    private void KumpulkanPosisiLantaiDungeon()
    {
        validDungeonPositions.Clear();

        if (floorTilemap != null)
        {
            BoundsInt bounds = floorTilemap.cellBounds;
            foreach (Vector3Int cell in bounds.allPositionsWithin)
            {
                if (floorTilemap.HasTile(cell))
                {
                    // Lewati cell jika cell tersebut memiliki tile dinding
                    if (wallsTilemap != null && wallsTilemap.HasTile(cell))
                    {
                        continue;
                    }

                    Vector3 worldPos = floorTilemap.GetCellCenterWorld(cell);

                    // Cek apakah ada collider solid yang menempati posisi ini
                    Collider2D hit = (obstacleLayers.value != 0)
                        ? Physics2D.OverlapCircle(worldPos, 0.35f, obstacleLayers)
                        : Physics2D.OverlapCircle(worldPos, 0.35f);

                    if (hit != null && !hit.isTrigger && !hit.CompareTag("Coin") && !hit.CompareTag("Player") && !hit.CompareTag("Enemy"))
                    {
                        continue;
                    }

                    validDungeonPositions.Add(worldPos);
                }
            }
        }

        // Fallback jika Floor_Tilemap tidak ditemukan di scene: gunakan koordinat dungeon bawaan
        if (validDungeonPositions.Count == 0)
        {
            GenerateFallbackDungeonPositions();
        }

        Debug.Log($"🏰 [EnemySpawner] Berhasil mendaftarkan {validDungeonPositions.Count} titik lantai valid di dalam dungeon.");
    }

    private void GenerateFallbackDungeonPositions()
    {
        // Ruangan 1 (Spawn Chamber): X [-16.5 s/d -12.5], Y [-3.5 s/d 3.5]
        for (float x = -16.5f; x <= -12.5f; x += 1f)
        {
            for (float y = -3.5f; y <= 3.5f; y += 1f)
            {
                validDungeonPositions.Add(new Vector3(x, y, 0f));
            }
        }

        // Lorong (Corridor): X [-10.5 s/d -7.5], Y = 0.5f
        for (float x = -10.5f; x <= -7.5f; x += 1f)
        {
            validDungeonPositions.Add(new Vector3(x, 0.5f, 0f));
        }

        // Ruangan 2 (Boss/Treasure): X [-5.5 s/d -1.5], Y [-4.5 s/d 4.5]
        for (float x = -5.5f; x <= -1.5f; x += 1f)
        {
            for (float y = -4.5f; y <= 4.5f; y += 1f)
            {
                validDungeonPositions.Add(new Vector3(x, y, 0f));
            }
        }
    }

    void Update()
    {
        // Jangan lakukan apa-apa jika game sudah selesai
        if (GameManager.Instance != null && GameManager.Instance.isGameOver) return;

        if (!spawnerAktif) return;

        // Tambah waktu berjalan
        waktuBerjalan += Time.deltaTime;

        // Cek apakah sudah melewati batas durasi spawn (1 menit)
        if (waktuBerjalan >= durasiSpawn)
        {
            spawnerAktif = false;
            Debug.Log("⏱️ [EnemySpawner] Waktu spawn habis! Tidak ada lagi musuh yang akan muncul.");
            UpdateTimerUI();

            if (GameManager.Instance != null)
            {
                GameManager.Instance.CekKondisiMenang();
            }
            return;
        }

        // Hitung mundur interval spawn
        timerSpawn -= Time.deltaTime;
        if (timerSpawn <= 0f)
        {
            SpawnWave();
            timerSpawn = spawnInterval; // Reset timer
        }

        UpdateTimerUI();
    }

    private void SpawnWave()
    {
        if (orcPrefab == null)
        {
            Debug.LogError("[EnemySpawner] Orc Prefab belum di-assign di Inspector!", this);
            return;
        }

        for (int i = 0; i < jumlahPerWave; i++)
        {
            Vector3 posisiSpawn = GetRandomSpawnPosition();
            GameObject orc = Instantiate(orcPrefab, posisiSpawn, Quaternion.identity);
            orc.name = "Orc_Spawned_" + System.DateTime.Now.Ticks;

            Debug.Log($"👹 [EnemySpawner] Orc muncul di dalam dungeon: {posisiSpawn}");
        }

        // Update hitungan total musuh di GameManager
        if (GameManager.Instance != null)
        {
            GameManager.Instance.HitungTotalMusuh();
        }
    }

    private Vector3 GetRandomSpawnPosition()
    {
        if (validDungeonPositions.Count == 0)
        {
            return (playerTransform != null) ? playerTransform.position : transform.position;
        }

        Vector3 playerPos = (playerTransform != null) ? playerTransform.position : transform.position;

        // 1. Prioritaskan posisi lantai dungeon yang berada di sekitar player (dalam radius wajar)
        List<Vector3> kandidatRadius = new List<Vector3>();
        foreach (Vector3 pos in validDungeonPositions)
        {
            float dist = Vector2.Distance(playerPos, pos);
            if (dist >= minSpawnDistance && dist <= spawnRadius)
            {
                kandidatRadius.Add(pos);
            }
        }

        if (kandidatRadius.Count > 0)
        {
            return kandidatRadius[Random.Range(0, kandidatRadius.Count)];
        }

        // 2. Jika tidak ada yang pas di radius, pilih lantai dungeon mana saja yang berjarak >= minSpawnDistance dari player
        List<Vector3> kandidatJauh = new List<Vector3>();
        foreach (Vector3 pos in validDungeonPositions)
        {
            float dist = Vector2.Distance(playerPos, pos);
            if (dist >= minSpawnDistance)
            {
                kandidatJauh.Add(pos);
            }
        }

        if (kandidatJauh.Count > 0)
        {
            return kandidatJauh[Random.Range(0, kandidatJauh.Count)];
        }

        // 3. Fallback: ambil posisi lantai dungeon mana saja secara acak
        return validDungeonPositions[Random.Range(0, validDungeonPositions.Count)];
    }

    private void UpdateTimerUI()
    {
        if (timerText == null) return;

        if (!spawnerAktif)
        {
            timerText.text = "Spawn: Selesai!";
            timerText.color = Color.green;
        }
        else
        {
            float sisaWaktu = Mathf.Max(0f, durasiSpawn - waktuBerjalan);
            int menit = Mathf.FloorToInt(sisaWaktu / 60f);
            int detik = Mathf.FloorToInt(sisaWaktu % 60f);
            timerText.text = $"Spawn: {menit:00}:{detik:00}";
        }
    }

    private void OnGUI()
    {
        // Jika game over, jangan tampilkan timer
        if (GameManager.Instance != null && GameManager.Instance.isGameOver) return;

        // Tampilkan HUD timer otomatis di bagian atas layar jika timerText tidak dipasang
        if (timerText == null)
        {
            GUIStyle boxStyle = new GUIStyle(GUI.skin.box);
            boxStyle.fontSize = 14;
            boxStyle.fontStyle = FontStyle.Bold;
            boxStyle.alignment = TextAnchor.MiddleCenter;

            float w = 260;
            float h = 34;
            float x = (Screen.width - w) / 2;
            float y = 12;

            if (spawnerAktif)
            {
                float sisaWaktu = Mathf.Max(0f, durasiSpawn - waktuBerjalan);
                int menit = Mathf.FloorToInt(sisaWaktu / 60f);
                int detik = Mathf.FloorToInt(sisaWaktu % 60f);
                GUI.color = new Color(1f, 0.92f, 0.35f, 0.95f);
                GUI.Box(new Rect(x, y, w, h), $"⏱️ Spawn Musuh: {menit:00}:{detik:00} (Tiap 3s: 3 Orc)", boxStyle);
            }
            else
            {
                GUI.color = new Color(0.3f, 1f, 0.45f, 0.95f);
                GUI.Box(new Rect(x, y, w, h), "⏱️ Spawn Selesai (Batas 1 Menit Habis)", boxStyle);
            }

            GUI.color = Color.white;
        }
    }

    // Gizmos untuk memvisualisasikan area lantai dungeon yang boleh di-spawn di Scene View
    private void OnDrawGizmosSelected()
    {
        if (validDungeonPositions != null && validDungeonPositions.Count > 0)
        {
            Gizmos.color = new Color(0f, 1f, 0.4f, 0.3f);
            foreach (Vector3 pos in validDungeonPositions)
            {
                Gizmos.DrawWireCube(pos, Vector3.one * 0.8f);
            }
        }

        Vector3 center = (playerTransform != null) ? playerTransform.position : transform.position;

        Gizmos.color = new Color(1f, 0f, 0f, 0.25f);
        Gizmos.DrawWireSphere(center, spawnRadius);

        Gizmos.color = new Color(1f, 1f, 0f, 0.25f);
        Gizmos.DrawWireSphere(center, minSpawnDistance);
    }

    /// <summary>Apakah spawner sudah berhenti memunculkan musuh?</summary>
    public bool IsSelesai() => !spawnerAktif;
}
