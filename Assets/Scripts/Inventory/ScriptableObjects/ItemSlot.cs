using UnityEngine;
using TMPro;
using UnityEngine.UI;
using UnityEngine.EventSystems;

public class ItemSlot : MonoBehaviour, IPointerClickHandler
{
    // Item Data
    public string itemName;
    public int itemQuantity;
    public Sprite itemIcon;
    public bool isFull;

    // Simpan data ScriptableObject & Properti untuk InventoryManager
    [SerializeField] private ItemDetails itemDetails;
    public ItemDetails ItemDetails => itemDetails;
    public bool IsEmpty => itemDetails == null || itemQuantity == 0;

    // Item Slot UI
    [SerializeField] private TMP_Text quantityText;
    [SerializeField] private Image itemImage;
    [SerializeField] private int maxStackSize = 99;

    // Selected Item
    [SerializeField] public GameObject selectedPanel;
    public bool isItemSelected;

    public InventoryManager inventoryManager;

    private void Awake()
    {
        // Auto-heal / perbaiki referensi jika kosong atau salah sambung akibat copy-paste
        if (selectedPanel == null || selectedPanel.transform.parent != transform)
        {
            Transform childPanel = transform.Find("SelectedPanel");
            if (childPanel != null)
            {
                selectedPanel = childPanel.gameObject;
            }
        }

        if (quantityText == null)
        {
            quantityText = GetComponentInChildren<TMP_Text>(true);
        }

        if (itemImage == null)
        {
            itemImage = GetComponent<Image>();
        }
    }

    public void Start()
    {
        inventoryManager = FindAnyObjectByType<InventoryManager>();
    }

    public void AddItem(ItemDetails item)
    {
        itemDetails = item;
        itemName = item.ItemName;
        itemIcon = item.ItemIcon;
        AddQuantity(item.Quantity);
    }

    // Check conditions for stacking items in the same slot
    public bool CanStackWith(string otherItemName)
    {
        return !isFull && !IsEmpty && itemName == otherItemName;
    }

    public void AddQuantity(int amount)
    {
        itemQuantity += amount;
        isFull = itemQuantity >= maxStackSize;
        
        if (quantityText != null)
        {
            quantityText.text = itemQuantity.ToString();
            quantityText.enabled = true;
        }

        if (itemImage != null)
        {
            itemImage.sprite = itemIcon;
            itemImage.enabled = true;
        }
    }

    public void OnPointerClick(PointerEventData eventData)
    {
        if (eventData.button == PointerEventData.InputButton.Left)
        {
            LeftClick();
        }
        
        if (eventData.button == PointerEventData.InputButton.Right)
        {
            RightClick();
        }
    }

    private void LeftClick()
{
    Debug.Log("Left Clicked on " + (IsEmpty ? "Empty Slot" : itemName));

    if (inventoryManager != null)
    {
        inventoryManager.SelectSlot(this);
    }
}

    private void RightClick()
    {
        Debug.Log("Right Clicked on " + itemName);
    }
}