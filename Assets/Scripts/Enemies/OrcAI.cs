using UnityEngine;

/// <summary>
/// DERIVED CLASS: OrcAI mewarisi EnemyAI (INHERITANCE).
/// 
/// Mengimplementasikan POLYMORPHISM:
/// Meng-override method virtual Serang() dari EnemyAI agar memenuhi ketentuan
/// Soal PAS poin 1.b:
/// "Memiliki Musuh yang digenerate secara otomatis dengan behaviour:
///  a. Bisa bergerak menyerang player.
///  b. Ketika sudah menyerang musuh akan hancur."
/// </summary>
public class OrcAI : EnemyAI
{
    [Header("Orc Special Behaviour (Ketentuan PAS)")]
    [SerializeField] private bool hancurSetelahMenyerang = true;

    /// <summary>
    /// POLYMORPHISM: Override dari EnemyAI.Serang
    /// Memberikan damage ke Player, lalu langsung menghancurkan diri musuh.
    /// </summary>
    public override void Serang(GameObject target)
    {
        // 1. Jalankan logika serang dasar dari base class (mengurangi HP/Shield player)
        base.Serang(target);

        // 2. Ketentuan Soal PAS poin 1.b: "Ketika sudah menyerang musuh akan hancur"
        if (hancurSetelahMenyerang)
        {
            Debug.Log($"💥 [OrcAI] {gameObject.name} menabrak Player dan langsung hancur sesuai ketentuan PAS!");
            Hancur();
        }
    }
}
