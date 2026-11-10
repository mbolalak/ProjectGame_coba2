using UnityEngine;
using UnityEngine.InputSystem;

public class PlayerMovement : MonoBehaviour
{
    public float kecepatan = 5f;
    private Vector2 arahGerak;
    public int skor = 0;

    [Header("Combat Settings")]
    [SerializeField] private Transform attackPoint; // Titik ujung pedang
    [SerializeField] private float attackRange = 0.5f; // Jarak jangkauan tebasan
    [SerializeField] private LayerMask enemyLayers; // Layer khusus musuh
    [SerializeField] private int attackDamage = 10; // Melee Damage

    [Header("Ranged Combat (Arrow)")]
    [SerializeField] private GameObject arrowPrefab; // Prefab panah
    [SerializeField] private int arrowDamage = 10;   // Arrow Damage (Damage Panah)

    [Header("Cooldown Settings")]
    [SerializeField] private float meleeCooldown = 1f;   // Cooldown melee 1 detik
    [SerializeField] private float rangedCooldown = 1f;  // Cooldown tembak panah 1 detik
    private float lastMeleeTime = -999f;
    private float lastRangedTime = -999f;

    // Referensi Komponen
    private Rigidbody2D rb; // <-- Variabel ini yang sebelumnya belum ada
    private Animator anim;
    private SpriteRenderer spriteRenderer;

    void Start()
    {
        rb = GetComponent<Rigidbody2D>();
        anim = GetComponent<Animator>();
        spriteRenderer = GetComponent<SpriteRenderer>();
    }

    void OnMove(InputValue value)
    {
        arahGerak = value.Get<Vector2>();
    }

    void OnAttack()
    {
        MulaiSerang();
    }

    void Update()
    {
        // Parameter Animator
        if (anim != null)
        {
            anim.SetFloat("Speed", arahGerak.sqrMagnitude);
        }

        // Balik hadap karakter (kiri / kanan)
        if (arahGerak.x > 0.01f)
        {
            transform.localScale = new Vector3(Mathf.Abs(transform.localScale.x), transform.localScale.y, transform.localScale.z);
        }
        else if (arahGerak.x < -0.01f)
        {
            transform.localScale = new Vector3(-Mathf.Abs(transform.localScale.x), transform.localScale.y, transform.localScale.z);
        }

        // Cadangan input langsung (Spasi atau Klik Kiri untuk Melee)
        if ((Keyboard.current != null && Keyboard.current.spaceKey.wasPressedThisFrame) ||
            (Mouse.current != null && Mouse.current.leftButton.wasPressedThisFrame))
        {
            MulaiSerang();
        }

        // Input Klik Kanan untuk Menembak Arrow
        if (Mouse.current != null && Mouse.current.rightButton.wasPressedThisFrame)
        {
            TembakArrow();
        }
    }

    void FixedUpdate()
    {
        // Pergerakan murni fisika: otomatis mengatasi tabrakan liar & player mundur sendiri
        rb.linearVelocity = arahGerak.normalized * kecepatan;
    }

    void MulaiSerang()
    {
        // Cek cooldown melee attack 1 detik
        if (Time.time < lastMeleeTime + meleeCooldown)
        {
            return;
        }

        lastMeleeTime = Time.time;

        if (anim != null)
        {
            anim.SetTrigger("Attack");
        }

        // Deteksi musuh di depan Player
        if (attackPoint != null)
        {
            Collider2D[] hitEnemies = (enemyLayers.value != 0)
                ? Physics2D.OverlapCircleAll(attackPoint.position, attackRange, enemyLayers)
                : Physics2D.OverlapCircleAll(attackPoint.position, attackRange);

            foreach (Collider2D enemy in hitEnemies)
            {
                if (!enemy.CompareTag("Enemy") && enemy.gameObject.layer != 6) continue;

                EnemyHealth enemyHealth = enemy.GetComponentInParent<EnemyHealth>();
                if (enemyHealth != null)
                {
                    enemyHealth.TakeDamage(attackDamage);
                    continue;
                }

                IDamageable damageable = enemy.GetComponentInParent<IDamageable>();
                if (damageable != null)
                {
                    damageable.KenaDamage(attackDamage);
                }
            }
        }
    }

    void TembakArrow()
    {
        // Cek cooldown tembak arrow 1 detik
        if (Time.time < lastRangedTime + rangedCooldown)
        {
            return;
        }

        lastRangedTime = Time.time;

        // Tentukan posisi awal panah
        Vector3 spawnPos = (attackPoint != null) ? attackPoint.position : transform.position;

        // Hitung arah menuju kursor mouse
        Vector2 shootDir = (transform.localScale.x >= 0) ? Vector2.right : Vector2.left;
        if (Mouse.current != null && Camera.main != null)
        {
            Vector3 mouseScreenPos = Mouse.current.position.ReadValue();
            mouseScreenPos.z = -Camera.main.transform.position.z;
            Vector3 mouseWorldPos = Camera.main.ScreenToWorldPoint(mouseScreenPos);
            Vector2 delta = (mouseWorldPos - spawnPos);
            if (delta.sqrMagnitude > 0.01f)
            {
                shootDir = delta.normalized;
            }
        }

        // Balik hadap Player sesuai arah tembakan mouse
        if (shootDir.x > 0.05f)
        {
            transform.localScale = new Vector3(Mathf.Abs(transform.localScale.x), transform.localScale.y, transform.localScale.z);
        }
        else if (shootDir.x < -0.05f)
        {
            transform.localScale = new Vector3(-Mathf.Abs(transform.localScale.x), transform.localScale.y, transform.localScale.z);
        }

        // Munculkan prefab panah
        if (arrowPrefab != null)
        {
            GameObject arrowObj = Instantiate(arrowPrefab, spawnPos, Quaternion.identity);
            Arrow arrow = arrowObj.GetComponent<Arrow>();
            if (arrow != null)
            {
                arrow.SetDirection(shootDir);
                arrow.SetDamage(arrowDamage > 0 ? arrowDamage : attackDamage);
            }
            Debug.Log($"🏹 [Player] Tembak arrow (Damage: {(arrowDamage > 0 ? arrowDamage : attackDamage)}) ke arah: {shootDir}");
        }
        else
        {
            Debug.LogWarning("[PlayerMovement] arrowPrefab belum dipasang di Inspector!", this);
        }
    }

    private void OnDrawGizmosSelected()
    {
        if (attackPoint == null) return;
        Gizmos.color = Color.red;
        Gizmos.DrawWireSphere(attackPoint.position, attackRange);
    }

    void OnTriggerEnter2D(Collider2D other)
    {
        if (other.CompareTag("Coin"))
        {
            SpriteRenderer coinSprite = other.GetComponent<SpriteRenderer>();
            Sprite icon = (coinSprite != null) ? coinSprite.sprite : null;

            Destroy(other.gameObject);
            
            skor++;
            Debug.Log("Skor Kamu Saat Ini: " + skor);

            GameManager gm = FindAnyObjectByType<GameManager>();
            if (gm != null)
            {
                gm.AmbilKoin(icon);
            }
        }
    }
}