using UnityEngine;

/// <summary>
/// BASE CLASS: EnemyAI
/// Fondasi kecerdasan buatan musuh yang menerapkan pilar OOP:
/// - Encapsulation: Variabel protected & private dengan property accessor.
/// - State Machine: Mengintegrasikan StateZombie (IDLE, PATROL, CHASE, ATTACK).
/// - Polymorphism: Menyediakan method virtual (Serang, KejarPlayer, Hancur)
///   yang dapat di-override oleh kelas turunan spesifik.
/// </summary>
[RequireComponent(typeof(Rigidbody2D))]
public class EnemyAI : MonoBehaviour
{
    [Header("Pergerakan & Serangan")]
    [SerializeField] protected float speed = 2.5f;
    [SerializeField] protected int contactDamage = 1;

    [Header("State Machine")]
    [SerializeField] protected StateZombie currentState = StateZombie.CHASE;

    protected Transform playerTransform;
    protected Rigidbody2D rb;
    protected SpriteRenderer spriteRenderer;
    protected bool sudahMenyerang = false;

    // Encapsulation (Getters)
    public float Speed => speed;
    public int ContactDamage => contactDamage;
    public StateZombie CurrentState => currentState;

    protected virtual void Awake()
    {
        rb = GetComponent<Rigidbody2D>();
        spriteRenderer = GetComponent<SpriteRenderer>();
    }

    protected virtual void Start()
    {
        // Cari objek Player di scene secara otomatis
        GameObject playerObj = GameObject.FindGameObjectWithTag("Player");
        if (playerObj != null)
        {
            playerTransform = playerObj.transform;
        }
    }

    protected virtual void FixedUpdate()
    {
        if (playerTransform == null || sudahMenyerang) return;

        UpdateStateMachine();
    }

    /// <summary>
    /// Menjalankan perilaku musuh berdasarkan State Machine
    /// </summary>
    protected virtual void UpdateStateMachine()
    {
        switch (currentState)
        {
            case StateZombie.IDLE:
                PerilakuIdle();
                break;
            case StateZombie.PATROL:
                PerilakuPatrol();
                break;
            case StateZombie.CHASE:
                PerilakuChase();
                break;
            case StateZombie.ATTACK:
                PerilakuAttack();
                break;
        }
    }

    protected virtual void PerilakuIdle()
    {
        if (rb != null) rb.linearVelocity = Vector2.zero;
    }

    protected virtual void PerilakuPatrol()
    {
        // Perilaku patroli dasar (jika diperlukan)
    }

    protected virtual void PerilakuChase()
    {
        KejarPlayer();
    }

    protected virtual void PerilakuAttack()
    {
        // Sedang mengeksekusi serangan
    }

    /// <summary>
    /// Logika pergerakan mengejar Player dan membalik arah badan (Flip X)
    /// </summary>
    public virtual void KejarPlayer()
    {
        if (playerTransform == null || rb == null) return;

        Vector2 arah = (playerTransform.position - transform.position).normalized;
        rb.linearVelocity = arah * speed;

        if (spriteRenderer != null)
        {
            if (arah.x > 0.05f)
            {
                spriteRenderer.flipX = false;
            }
            else if (arah.x < -0.05f)
            {
                spriteRenderer.flipX = true;
            }
        }
    }

    protected virtual void OnTriggerEnter2D(Collider2D collision)
    {
        if (collision.CompareTag("Player"))
        {
            Serang(collision.gameObject);
        }
    }

    protected virtual void OnCollisionEnter2D(Collision2D collision)
    {
        if (collision.gameObject.CompareTag("Player"))
        {
            Serang(collision.gameObject);
        }
    }

    /// <summary>
    /// POLYMORPHISM: Method virtual yang di-override oleh kelas turunan
    /// (misal OrcAI) untuk menentukan perilaku serangan yang berbeda.
    /// </summary>
    public virtual void Serang(GameObject target)
    {
        if (sudahMenyerang) return;
        sudahMenyerang = true;
        currentState = StateZombie.ATTACK;

        PlayerHealth playerHealth = target.GetComponent<PlayerHealth>();
        if (playerHealth != null)
        {
            playerHealth.TakeDamage(contactDamage);
            Debug.Log($"💥 [{gameObject.name}] menyerang Player! Memberikan damage {contactDamage}.");
        }
    }

    /// <summary>
    /// Menghancurkan musuh dan melaporkan kekalahan ke GameManager
    /// </summary>
    public virtual void Hancur()
    {
        EnemyHealth enemyHealth = GetComponent<EnemyHealth>();
        if (enemyHealth != null)
        {
            if (GameManager.Instance != null)
            {
                GameManager.Instance.MusuhKalah(enemyHealth);
            }
            else
            {
                GameManager gm = FindAnyObjectByType<GameManager>();
                if (gm != null) gm.MusuhKalah(enemyHealth);
            }
        }

        Destroy(gameObject);
    }
}
