using System.Collections.Generic;
using UnityEditor;
using UnityEngine;

public class DungeonMapBuilder : EditorWindow
{
    private const string ROOT_NAME = "--- DUNGEON MAP ---";

    [MenuItem("Tools/Dungeon Generator/Open Dungeon Window...", false, 0)]
    public static void ShowWindow()
    {
        GetWindow<DungeonMapBuilder>("Dungeon Generator");
    }

    private void OnGUI()
    {
        GUILayout.Space(10);
        EditorGUILayout.LabelField("Dungeon Room Generator", EditorStyles.boldLabel);
        EditorGUILayout.HelpBox("Klik tombol di bawah untuk membangun ruangan dungeon secara otomatis (lantai rapi, dinding ber-collider, koin tertata, dan Orc).", MessageType.Info);

        GUILayout.Space(10);
        if (GUILayout.Button("🏰 Generate Dungeon Map", GUILayout.Height(40)))
        {
            GenerateMap();
        }

        GUILayout.Space(5);
        if (GUILayout.Button("🗑️ Clear Generated Map", GUILayout.Height(30)))
        {
            ClearMap();
        }
    }

    [MenuItem("Tools/Dungeon Generator/Generate Dungeon Map", false, 1)]
    public static void GenerateMap()
    {
        ClearMap();

        // 1. Root GameObject
        GameObject root = new GameObject(ROOT_NAME);
        Undo.RegisterCreatedObjectUndo(root, "Generate Dungeon Map");

        GameObject floorContainer = new GameObject("1_Floors");
        floorContainer.transform.SetParent(root.transform);

        GameObject wallContainer = new GameObject("2_Walls (With Colliders)");
        wallContainer.transform.SetParent(root.transform);

        GameObject decorContainer = new GameObject("3_Decorations");
        decorContainer.transform.SetParent(root.transform);

        GameObject coinContainer = new GameObject("4_Coins");
        coinContainer.transform.SetParent(root.transform);

        GameObject enemyContainer = new GameObject("5_Enemies");
        enemyContainer.transform.SetParent(root.transform);

        // Assets
        Sprite floorSprite = LoadSubSprite("Assets/Sprites/Dungeon Gathering Free Version/Set 1.1.png", "Set 1.1_0");
        if (floorSprite == null) floorSprite = LoadFirstSprite("Assets/Sprites/Dungeon Gathering Free Version/Set 1.png");

        Sprite wallSprite = LoadSubSprite("Assets/Sprites/Dungeon Gathering Free Version/Set 1.0.png", "Set 1.0_0");
        if (wallSprite == null) wallSprite = AssetDatabase.GetBuiltinExtraResource<Sprite>("UI/Skin/Background.psd");

        Sprite coinSprite = LoadSubSprite("Assets/Sprites/Dungeon Gathering Free Version/Coin Sheet.png", "Coin Sheet_0");
        if (coinSprite == null) coinSprite = LoadFirstSprite("Assets/Sprites/Dungeon Gathering Free Version/Coins.png");

        Material coinMaterial = AssetDatabase.LoadAssetAtPath<Material>("Assets/MaterialKoin.mat");

        Sprite orcSprite = LoadSubSprite("Assets/Sprites/Characters(100x100 split)/Orc/Orc/Orc_Idle.png", "Orc_Idle_0");
        if (orcSprite == null) orcSprite = LoadFirstSprite("Assets/Sprites/Characters(100x100 split)/Orc/Orc/Orc.png");

        Sprite torchSprite = LoadSubSprite("Assets/Sprites/Dungeon Gathering Free Version/Torch Yellow.png", "Torch Yellow_0");
        Sprite potionSprite = LoadSubSprite("Assets/Sprites/Dungeon Gathering Free Version/Potion 1.png", "Potion 1_0");
        Sprite vaseSprite = LoadSubSprite("Assets/Sprites/Dungeon Gathering Free Version/Vase Shine Anim.png", "Vase Shine Anim_0");
        Sprite pillarSprite = LoadSubSprite("Assets/Sprites/Dungeon Gathering Free Version/Structure.png", "Structure_0");

        // 2. Build Floor Areas
        // Room 1 (Spawn Chamber): center (-15.5, 0), size (7, 9)
        CreateFloorArea("Floor_Room1_Spawn", new Vector2(-15.5f, 0f), new Vector2(7f, 9f), floorSprite, floorContainer.transform);

        // Corridor: center (-10.0, 0), size (4, 3.2)
        CreateFloorArea("Floor_Corridor", new Vector2(-10.0f, 0f), new Vector2(4f, 3.2f), floorSprite, floorContainer.transform);

        // Room 2 (Boss & Treasure Room): center (-4.5, 0), size (7f, 9.6f)
        CreateFloorArea("Floor_Room2_Treasure", new Vector2(-4.5f, 0f), new Vector2(7f, 9.6f), floorSprite, floorContainer.transform);

        // 3. Build Perimeter & Interior Walls with Solid BoxCollider2D
        Color wallColor = new Color(0.85f, 0.85f, 0.9f, 1f);

        // --- Room 1 Walls ---
        CreateWall("Wall_Room1_West", new Vector2(-19.3f, 0f), new Vector2(0.8f, 9.8f), wallSprite, wallColor, wallContainer.transform);
        CreateWall("Wall_Room1_North", new Vector2(-15.5f, 4.8f), new Vector2(7.2f, 0.8f), wallSprite, wallColor, wallContainer.transform);
        CreateWall("Wall_Room1_South", new Vector2(-15.5f, -4.8f), new Vector2(7.2f, 0.8f), wallSprite, wallColor, wallContainer.transform);

        // Partition between Room 1 & Corridor
        CreateWall("Wall_Partition_R1_North", new Vector2(-12.0f, 3.3f), new Vector2(0.8f, 2.4f), wallSprite, wallColor, wallContainer.transform);
        CreateWall("Wall_Partition_R1_South", new Vector2(-12.0f, -3.3f), new Vector2(0.8f, 2.4f), wallSprite, wallColor, wallContainer.transform);

        // --- Corridor Walls ---
        CreateWall("Wall_Corridor_North", new Vector2(-10.0f, 1.9f), new Vector2(3.6f, 0.6f), wallSprite, wallColor, wallContainer.transform);
        CreateWall("Wall_Corridor_South", new Vector2(-10.0f, -1.9f), new Vector2(3.6f, 0.6f), wallSprite, wallColor, wallContainer.transform);

        // Partition between Corridor & Room 2
        CreateWall("Wall_Partition_R2_North", new Vector2(-8.0f, 3.5f), new Vector2(0.8f, 2.8f), wallSprite, wallColor, wallContainer.transform);
        CreateWall("Wall_Partition_R2_South", new Vector2(-8.0f, -3.5f), new Vector2(0.8f, 2.8f), wallSprite, wallColor, wallContainer.transform);

        // --- Room 2 Walls ---
        CreateWall("Wall_Room2_North", new Vector2(-4.5f, 5.1f), new Vector2(7.8f, 0.8f), wallSprite, wallColor, wallContainer.transform);
        CreateWall("Wall_Room2_South", new Vector2(-4.5f, -5.1f), new Vector2(7.8f, 0.8f), wallSprite, wallColor, wallContainer.transform);
        CreateWall("Wall_Room2_East", new Vector2(-0.7f, 0f), new Vector2(0.8f, 10.4f), wallSprite, wallColor, wallContainer.transform);

        // Interior Tactical Pillars in Room 2 (Provide combat cover)
        CreateWall("Pillar_NW", new Vector2(-6.0f, 2.2f), new Vector2(0.9f, 0.9f), pillarSprite != null ? pillarSprite : wallSprite, Color.white, wallContainer.transform);
        CreateWall("Pillar_SW", new Vector2(-6.0f, -2.2f), new Vector2(0.9f, 0.9f), pillarSprite != null ? pillarSprite : wallSprite, Color.white, wallContainer.transform);
        CreateWall("Pillar_NE", new Vector2(-3.0f, 2.2f), new Vector2(0.9f, 0.9f), pillarSprite != null ? pillarSprite : wallSprite, Color.white, wallContainer.transform);
        CreateWall("Pillar_SE", new Vector2(-3.0f, -2.2f), new Vector2(0.9f, 0.9f), pillarSprite != null ? pillarSprite : wallSprite, Color.white, wallContainer.transform);

        // 4. Decorations (Torches, Vases, Potions)
        if (torchSprite != null)
        {
            CreateDecor("Torch_R1_1", new Vector2(-17.0f, 4.4f), torchSprite, decorContainer.transform, 1.2f);
            CreateDecor("Torch_R1_2", new Vector2(-14.0f, 4.4f), torchSprite, decorContainer.transform, 1.2f);
            CreateDecor("Torch_Corr_N", new Vector2(-10.0f, 1.6f), torchSprite, decorContainer.transform, 1.0f);
            CreateDecor("Torch_Corr_S", new Vector2(-10.0f, -1.6f), torchSprite, decorContainer.transform, 1.0f);
            CreateDecor("Torch_R2_N1", new Vector2(-6.0f, 4.7f), torchSprite, decorContainer.transform, 1.2f);
            CreateDecor("Torch_R2_N2", new Vector2(-3.0f, 4.7f), torchSprite, decorContainer.transform, 1.2f);
        }

        if (vaseSprite != null)
        {
            CreateDecor("Vase_R1_SW", new Vector2(-18.5f, -4.0f), vaseSprite, decorContainer.transform, 1.5f);
            CreateDecor("Vase_R1_NW", new Vector2(-18.5f, 4.0f), vaseSprite, decorContainer.transform, 1.5f);
            CreateDecor("Vase_R2_NE", new Vector2(-1.5f, 4.2f), vaseSprite, decorContainer.transform, 1.5f);
            CreateDecor("Vase_R2_SE", new Vector2(-1.5f, -4.2f), vaseSprite, decorContainer.transform, 1.5f);
        }

        if (potionSprite != null)
        {
            CreateDecor("Potion_Collectible", new Vector2(-18.3f, 0f), potionSprite, decorContainer.transform, 1.2f);
        }

        // 5. Coins (Neatly Arranged)
        // Trail along the corridor (5 coins)
        for (int i = 0; i < 5; i++)
        {
            float x = -11.6f + i * 0.8f;
            CreateCoin($"Coin_Corridor_{i + 1}", new Vector2(x, 0f), coinSprite, coinMaterial, coinContainer.transform);
        }

        // Circular Treasure Formation in Room 2 (8 coins around center, 1 special center)
        Vector2 centerR2 = new Vector2(-4.5f, 0f);
        int ringCoins = 8;
        float radius = 1.3f;
        for (int i = 0; i < ringCoins; i++)
        {
            float angle = i * (Mathf.PI * 2f / ringCoins);
            Vector2 pos = centerR2 + new Vector2(Mathf.Cos(angle) * radius, Mathf.Sin(angle) * radius);
            CreateCoin($"Coin_Ring_{i + 1}", pos, coinSprite, coinMaterial, coinContainer.transform);
        }
        CreateCoin("Coin_Treasure_Center", centerR2, coinSprite, coinMaterial, coinContainer.transform, 1.3f);

        // 6. Enemies (Orcs) in Strategic Guard Positions
        CreateOrc("Orc_Corridor_Sentry", new Vector2(-8.8f, 0f), orcSprite, enemyContainer.transform, 2.0f);
        CreateOrc("Orc_North_Guard", new Vector2(-4.5f, 2.8f), orcSprite, enemyContainer.transform, 2.4f);
        CreateOrc("Orc_South_Guard", new Vector2(-4.5f, -2.8f), orcSprite, enemyContainer.transform, 2.4f);

        // 7. Reposition Player into Room 1 spawn point
        GameObject player = GameObject.FindGameObjectWithTag("Player");
        if (player != null)
        {
            Undo.RecordObject(player.transform, "Position Player");
            player.transform.position = new Vector3(-16.0f, 0f, 0f);
            Debug.Log("Pemain diposisikan ke Spawn Room: (-16, 0)");
        }

        // Deactivate old placeholder stretched walls if present
        DeactivateOldWall("wall");
        DeactivateOldWall("wall (1)");
        DeactivateOldWall("wall (2)");
        DeactivateOldWall("wall (3)");

        // Deactivate old scattered coins so the new ones are cleanly counted
        DeactivateOldObject("Coin");
        DeactivateOldObject("Coin (1)");
        DeactivateOldObject("Coin (2)");
        DeactivateOldObject("Coin (3)");
        DeactivateOldObject("Coin (4)");

        // Deactivate old placeholder Orcs if present
        GameObject[] oldOrcs = Object.FindObjectsByType<GameObject>(FindObjectsInactive.Include);
        foreach (var obj in oldOrcs)
        {
            if (obj.name == "Orc" && obj.transform.parent == null)
            {
                Undo.RecordObject(obj, "Deactivate Old Orc");
                obj.SetActive(false);
            }
        }

        UnityEditor.SceneManagement.EditorSceneManager.MarkSceneDirty(
            UnityEditor.SceneManagement.EditorSceneManager.GetActiveScene()
        );

        Selection.activeGameObject = root;
        Debug.Log("✅ Layout Ruangan Dungeon Berhasil Dibangun dengan Rapi!");
    }

    [MenuItem("Tools/Dungeon Generator/Clear Generated Map", false, 2)]
    public static void ClearMap()
    {
        GameObject existing = GameObject.Find(ROOT_NAME);
        if (existing != null)
        {
            Undo.DestroyObjectImmediate(existing);
            Debug.Log("Dungeon sebelumnya telah dibersihkan.");
        }
    }

    private static void CreateFloorArea(string name, Vector2 pos, Vector2 size, Sprite sprite, Transform parent)
    {
        GameObject floor = new GameObject(name);
        floor.transform.SetParent(parent);
        floor.transform.position = new Vector3(pos.x, pos.y, 0f);

        SpriteRenderer sr = floor.AddComponent<SpriteRenderer>();
        sr.sprite = sprite;
        sr.sortingOrder = -10;
        sr.color = new Color(0.9f, 0.9f, 0.95f, 1f);

        if (sprite != null)
        {
            sr.drawMode = SpriteDrawMode.Tiled;
            sr.size = size;
        }
        else
        {
            floor.transform.localScale = new Vector3(size.x, size.y, 1f);
        }
    }

    private static void CreateWall(string name, Vector2 pos, Vector2 size, Sprite sprite, Color color, Transform parent)
    {
        GameObject wall = new GameObject(name);
        wall.transform.SetParent(parent);
        wall.transform.position = new Vector3(pos.x, pos.y, 0f);

        SpriteRenderer sr = wall.AddComponent<SpriteRenderer>();
        sr.sprite = sprite;
        sr.color = color;
        sr.sortingOrder = 5;

        if (sprite != null)
        {
            sr.drawMode = SpriteDrawMode.Tiled;
            sr.size = size;
        }
        else
        {
            wall.transform.localScale = new Vector3(size.x, size.y, 1f);
        }

        BoxCollider2D col = wall.AddComponent<BoxCollider2D>();
        col.size = size;
    }

    private static void CreateDecor(string name, Vector2 pos, Sprite sprite, Transform parent, float scale = 1f)
    {
        GameObject decor = new GameObject(name);
        decor.transform.SetParent(parent);
        decor.transform.position = new Vector3(pos.x, pos.y, 0f);
        decor.transform.localScale = Vector3.one * scale;

        SpriteRenderer sr = decor.AddComponent<SpriteRenderer>();
        sr.sprite = sprite;
        sr.sortingOrder = 6;
    }

    private static void CreateCoin(string name, Vector2 pos, Sprite sprite, Material mat, Transform parent, float scale = 1f)
    {
        GameObject coin = new GameObject(name);
        coin.tag = "Coin";
        coin.transform.SetParent(parent);
        coin.transform.position = new Vector3(pos.x, pos.y, 0f);
        coin.transform.localScale = Vector3.one * scale;

        SpriteRenderer sr = coin.AddComponent<SpriteRenderer>();
        sr.sprite = sprite;
        if (mat != null) sr.material = mat;
        sr.sortingOrder = 2;

        CircleCollider2D col = coin.AddComponent<CircleCollider2D>();
        col.isTrigger = true;
        col.radius = 0.45f;
    }

    private static void CreateOrc(string name, Vector2 pos, Sprite sprite, Transform parent, float speed)
    {
        GameObject orc = new GameObject(name);
        orc.tag = "Enemy";
        orc.layer = 6; // Enemy layer
        orc.transform.SetParent(parent);
        orc.transform.position = new Vector3(pos.x, pos.y, 0f);
        orc.transform.localScale = new Vector3(1f, 1f, 1f);

        SpriteRenderer sr = orc.AddComponent<SpriteRenderer>();
        sr.sprite = sprite;
        sr.sortingOrder = 4;

        Rigidbody2D rb = orc.AddComponent<Rigidbody2D>();
        rb.gravityScale = 0f;
        rb.constraints = RigidbodyConstraints2D.FreezeRotation;

        BoxCollider2D col = orc.AddComponent<BoxCollider2D>();
        col.size = new Vector2(0.8f, 0.9f);

        EnemyAI ai = orc.AddComponent<EnemyAI>();
        // Set private fields via SerializedObject to maintain values properly
        SerializedObject soAI = new SerializedObject(ai);
        soAI.FindProperty("speed").floatValue = speed;
        soAI.FindProperty("contactDamage").intValue = 1;
        soAI.ApplyModifiedPropertiesWithoutUndo();

        orc.AddComponent<EnemyHealth>();
    }

    private static Sprite LoadSubSprite(string assetPath, string spriteName)
    {
        Object[] assets = AssetDatabase.LoadAllAssetsAtPath(assetPath);
        foreach (Object obj in assets)
        {
            if (obj is Sprite s && s.name == spriteName) return s;
        }
        return null;
    }

    private static Sprite LoadFirstSprite(string assetPath)
    {
        Object[] assets = AssetDatabase.LoadAllAssetsAtPath(assetPath);
        foreach (Object obj in assets)
        {
            if (obj is Sprite s) return s;
        }
        return AssetDatabase.LoadAssetAtPath<Sprite>(assetPath);
    }

    private static void DeactivateOldWall(string name)
    {
        GameObject obj = GameObject.Find(name);
        if (obj != null && obj.transform.parent == null)
        {
            Undo.RecordObject(obj, "Deactivate Placeholder Wall");
            obj.SetActive(false);
        }
    }

    private static void DeactivateOldObject(string name)
    {
        GameObject obj = GameObject.Find(name);
        if (obj != null && obj.transform.parent == null)
        {
            Undo.RecordObject(obj, "Deactivate Old Object");
            obj.SetActive(false);
        }
    }
}
