using UnityEngine;

public class Arrow : MonoBehaviour
{
    [SerializeField] private float speed = 12f;
    [SerializeField] private int damage = 10; // Default damage panah
    [SerializeField] private float lifetime = 3f;

    private Vector2 direction;

    public void SetDamage(int dmg)
    {
        damage = dmg;
    }

    public void SetDirection(Vector2 dir)
    {
        direction = dir.normalized;

        // Rotasi arrow agar menghadap arah tembak
        float angle = Mathf.Atan2(direction.y, direction.x) * Mathf.Rad2Deg;
        transform.rotation = Quaternion.Euler(0f, 0f, angle);
    }

    void Start()
    {
        // Hancurkan otomatis setelah beberapa detik agar tidak menumpuk
        Destroy(gameObject, lifetime);
    }

    void Update()
    {
        // Gerakkan arrow sesuai arah yang ditentukan
        transform.position += (Vector3)(direction * speed * Time.deltaTime);
    }

    private void OnTriggerEnter2D(Collider2D collision)
    {
        // Abaikan Player sendiri
        if (collision.CompareTag("Player")) return;

        // Abaikan Koin dan item collectible agar tidak hancur kena panah
        if (collision.CompareTag("Coin") || collision.GetComponent<GrabableItem>() != null)
        {
            return;
        }

        // Jika mengenai musuh, beri damage lalu panah hancur
        if (collision.CompareTag("Enemy") || collision.gameObject.layer == 6)
        {
            EnemyHealth enemyHealth = collision.GetComponentInParent<EnemyHealth>();
            if (enemyHealth != null)
            {
                enemyHealth.TakeDamage(damage);
            }
            else
            {
                IDamageable damageable = collision.GetComponentInParent<IDamageable>();
                if (damageable != null)
                {
                    damageable.KenaDamage(damage);
                }
            }

            Destroy(gameObject);
            return;
        }

        // Jika mengenai obstacle atau dinding solid
        if (!collision.isTrigger)
        {
            Destroy(gameObject);
        }
    }
}
