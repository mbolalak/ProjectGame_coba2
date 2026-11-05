using System.Collections;
using UnityEngine;
using UnityEngine.UI; // 1. Wajib ada baris ini!

public class PlayerHealth : MonoBehaviour
{
    [Header("Health Settings")]
    [SerializeField] private int maxHealth = 5;
    private int currentHealth;

    [Header("UI Reference")]
    [SerializeField] private Slider healthSlider; // 2. Baris ini yang memunculkan kolom di Inspector!

    [Header("Invulnerability (i-Frames)")]
    [SerializeField] private float iFrameDuration = 1f;
    private bool isInvulnerable = false;

    private SpriteRenderer spriteRenderer;

    void Start()
    {
        currentHealth = maxHealth;
        spriteRenderer = GetComponent<SpriteRenderer>();

        // Setel batas dan nilai awal bar darah
        if (healthSlider != null)
        {
            healthSlider.minValue = 0;
            healthSlider.maxValue = maxHealth;
            healthSlider.value = currentHealth;
        }
    }

    public void TakeDamage(int damage)
    {
        if (isInvulnerable) return;

        currentHealth -= damage;
        Debug.Log("Player terkena serangan! Sisa HP: " + currentHealth);

        // Update nilai slider saat terkena damage
        if (healthSlider != null)
        {
            healthSlider.value = currentHealth;
        }

        if (currentHealth <= 0)
        {
            Die();
        }
        else
        {
            StartCoroutine(DamageRoutine());
        }
    }

    private IEnumerator DamageRoutine()
    {
        isInvulnerable = true;

        if (spriteRenderer != null)
        {
            for (int i = 0; i < 3; i++)
            {
                spriteRenderer.color = new Color(1f, 0.3f, 0.3f, 0.5f);
                yield return new WaitForSeconds(iFrameDuration / 6);
                spriteRenderer.color = Color.white;
                yield return new WaitForSeconds(iFrameDuration / 6);
            }
        }

        isInvulnerable = false;
    }

    void Die()
    {
        Debug.Log("Player Kalah / Game Over!");

        PlayerMovement movement = GetComponent<PlayerMovement>();
        if (movement != null) movement.enabled = false;

        Collider2D col = GetComponent<Collider2D>();
        if (col != null) col.enabled = false;
    }

    public int GetCurrentHealth() => currentHealth;
    public int GetMaxHealth() => maxHealth;
}