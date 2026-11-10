using UnityEngine;

public class EnemyHealth : MonoBehaviour, IDamageable
{
    [SerializeField] private int maxHealth = 3;
    private int currentHealth;

    private void Awake()
    {
        currentHealth = maxHealth;
    }

    void Start()
    {
        // Pastikan currentHealth selalu terisi jika belum di Awake
        if (currentHealth <= 0)
        {
            currentHealth = maxHealth;
        }
    }

    // Implementasi IDamageable
    public void KenaDamage(int jumlah)
    {
        TakeDamage(jumlah);
    }

    public void TakeDamage(int damage)
    {
        currentHealth -= damage;
        Debug.Log(gameObject.name + " terkena damage! Sisa HP: " + currentHealth);

        // Efek visual singkat (opsional: kedip merah saat kena hit)
        StartCoroutine(BlinkRed());

        if (currentHealth <= 0)
        {
            Die();
        }
    }

    private System.Collections.IEnumerator BlinkRed()
    {
        SpriteRenderer sr = GetComponent<SpriteRenderer>();
        if (sr != null)
        {
            sr.color = Color.red;
            yield return new WaitForSeconds(0.1f);
            sr.color = Color.white;
        }
    }

    void Die()
    {
        Debug.Log(gameObject.name + " Mati!");

        // Beritahu GameManager bahwa musuh ini kalah
        if (GameManager.Instance != null)
        {
            GameManager.Instance.MusuhKalah(this);
        }
        else
        {
            GameManager gm = FindAnyObjectByType<GameManager>();
            if (gm != null) gm.MusuhKalah(this);
        }

        Destroy(gameObject);
    }
}