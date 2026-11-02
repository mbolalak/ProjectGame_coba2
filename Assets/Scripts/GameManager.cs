using UnityEngine;
using TMPro;

public class GameManager : MonoBehaviour
{
    public int totalKoin;
    private int koinTerkumpul = 0;

    [Header("UI References")]
    public TextMeshProUGUI teksSkor;
    public GameObject teksMenang;

    [Header("Item Data")]
    public ItemDetails coinData; 

    void Start()
    {
        totalKoin = GameObject.FindGameObjectsWithTag("Coin").Length;

        if (teksMenang != null) 
        {
            teksMenang.SetActive(false);
        }
        
        UpdateSkorUI();
    }

    public void AmbilKoin(Sprite icon = null)
    {
        koinTerkumpul++;
        UpdateSkorUI();

        // Kirim data ScriptableObject ItemCoin ke InventoryManager


        
        if (InventoryManager.Instance != null && coinData != null)
        {
            InventoryManager.Instance.AddItem(coinData);
        }

        if (koinTerkumpul == totalKoin)
        {
            Menang();
        }
    }

    void UpdateSkorUI()
    {
        if (teksSkor != null)
        {
            teksSkor.text = "Skor: " + koinTerkumpul;
        }
    }

    void Menang()
    {
        Debug.Log("KAMU MENANG!");

        if (teksMenang != null)
        {
            teksMenang.SetActive(true);
        }
    }
}