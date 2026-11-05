using UnityEngine;

#if UNITY_EDITOR
using UnityEditor;
#endif

public class DungeonGenerator : MonoBehaviour
{
    [Header("Generator Action")]
    [Tooltip("Klik kanan pada komponen ini lalu pilih 'Generate Dungeon Map' atau gunakan menu Tools")]
    public bool infoOnly;

#if UNITY_EDITOR
    [ContextMenu("Generate Dungeon Map Now")]
    public void GenerateDungeonFromInspector()
    {
        DungeonMapBuilder.GenerateMap();
    }

    [ContextMenu("Clear Dungeon Map")]
    public void ClearDungeonFromInspector()
    {
        DungeonMapBuilder.ClearMap();
    }
#endif
}

#if UNITY_EDITOR
[CustomEditor(typeof(DungeonGenerator))]
public class DungeonGeneratorEditor : Editor
{
    public override void OnInspectorGUI()
    {
        DrawDefaultInspector();

        DungeonGenerator generator = (DungeonGenerator)target;

        EditorGUILayout.Space(10);
        EditorGUILayout.HelpBox("Klik tombol di bawah ini untuk membangun ruangan dungeon secara otomatis lengkap dengan lantai, dinding ber-collider, koin tertata, dan musuh Orc.", MessageType.Info);

        EditorGUILayout.BeginHorizontal();
        if (GUILayout.Button("🏰 Generate Dungeon Map", GUILayout.Height(35)))
        {
            DungeonMapBuilder.GenerateMap();
        }

        if (GUILayout.Button("🗑️ Clear Map", GUILayout.Height(35)))
        {
            DungeonMapBuilder.ClearMap();
        }
        EditorGUILayout.EndHorizontal();
    }
}
#endif
