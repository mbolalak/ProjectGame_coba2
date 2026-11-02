using UnityEngine;
using UnityEngine.UI;
using TMPro;

// Controls the right-side panel (InventoryDetails) of the inventory.
// It draws the details of the item the player has selected.
public class ItemDetailsPanel : MonoBehaviour
{
    [SerializeField] private Image itemImage;
    [SerializeField] private TMP_Text itemNameText;
    [SerializeField] private TMP_Text itemQuantityText;
    [SerializeField] private TMP_Text itemDescriptionText;

    // Show the details of the selected item.
    // quantity is the stack size currently stored in the slot.
    public void Show(ItemDetails item, int quantity)
    {
        if (item == null)
        {
            Clear();
            return;
        }

        itemImage.sprite = item.ItemIcon;
        itemImage.enabled = true;
        itemNameText.text = item.ItemName;
        itemQuantityText.text = "Quantity: " + quantity;
        itemDescriptionText.text = item.Description;
    }

    // Empty the panel, used when the selected slot has no item.
    public void Clear()
    {
        itemImage.sprite = null;
        itemImage.enabled = false;
        itemNameText.text = "";
        itemQuantityText.text = "";
        itemDescriptionText.text = "";
    }
}
