using UnityEngine;
using UnityEngine.InputSystem;

public class PlayerMovement : MonoBehaviour
{
    public float kecepatan = 5f;
    private Vector2 arahGerak;
    public int skor = 0;

    // Referensi komponen pendukung
    private Animator anim;
    private SpriteRenderer spriteRenderer;

    void Start()
    {
        anim = GetComponent<Animator>();
        spriteRenderer = GetComponent<SpriteRenderer>();
    }

    void OnMove(InputValue value)
    {
        arahGerak = value.Get<Vector2>();
    }

    void Update()
    {
        // 1. Gerakkan objek
        Vector3 arah = new Vector3(arahGerak.x, arahGerak.y, 0);
        transform.position += arah * kecepatan * Time.deltaTime;

        // 2. Kirim nilai kecepatan ke Animator
        if (anim != null)
        {
            anim.SetFloat("Speed", arahGerak.sqrMagnitude);
        }

        // 3. Balik arah hadap karakter (kiri / kanan)
        if (arahGerak.x > 0.01f)
        {
            spriteRenderer.flipX = false; // Hadap kanan
        }
        else if (arahGerak.x < -0.01f)
        {
            spriteRenderer.flipX = true;  // Hadap kiri
        }
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