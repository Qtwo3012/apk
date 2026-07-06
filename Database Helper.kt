package com.example.rgbilling

import android.content.ContentValues
import android.content.Context
import android.database.sqlite.SQLiteDatabase
import android.database.sqlite.SQLiteOpenHelper

class DatabaseHelper(context: Context) :
    SQLiteOpenHelper(context, "rgbilling.db", null, 3) {

    override fun onCreate(db: SQLiteDatabase) {

        db.execSQL(
            """
            CREATE TABLE transaksi(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tanggal TEXT,
                ps TEXT,
                pelanggan TEXT,
                durasi INTEGER,
                total INTEGER
            )
            """.trimIndent()
        )

        db.execSQL(
            """
            CREATE TABLE produk(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama TEXT,
                kategori TEXT,
                modal INTEGER,
                jual INTEGER,
                stok INTEGER
            )
            """.trimIndent()
        )

        db.execSQL(
            """
            CREATE TABLE transaksi_kantin(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tanggal TEXT,
                produk TEXT,
                qty INTEGER,
                harga INTEGER,
                total INTEGER
            )
            """.trimIndent()
        )
    }

    override fun onUpgrade(
        db: SQLiteDatabase,
        oldVersion: Int,
        newVersion: Int
    ) {

        if (oldVersion < 2) {

            db.execSQL(
                """
                CREATE TABLE IF NOT EXISTS produk(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nama TEXT,
                    kategori TEXT,
                    modal INTEGER,
                    jual INTEGER,
                    stok INTEGER
                )
                """.trimIndent()
            )

        }

        if (oldVersion < 3) {

            db.execSQL(
                """
                CREATE TABLE IF NOT EXISTS transaksi_kantin(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    tanggal TEXT,
                    produk TEXT,
                    qty INTEGER,
                    harga INTEGER,
                    total INTEGER
                )
                """.trimIndent()
            )

        }

    }

    // =====================================
    // TRANSAKSI PS
    // =====================================

    fun simpan(
        tanggal: String,
        ps: String,
        pelanggan: String,
        durasi: Int,
        total: Int
    ) {

        val db = writableDatabase

        val values = ContentValues()

        values.put("tanggal", tanggal)
        values.put("ps", ps)
        values.put("pelanggan", pelanggan)
        values.put("durasi", durasi)
        values.put("total", total)

        db.insert("transaksi", null, values)

    }

    fun getTotalPendapatan(): Int {

        val db = readableDatabase

        val cursor = db.rawQuery(
            "SELECT IFNULL(SUM(total),0) FROM transaksi",
            null
        )

        var total = 0

        if (cursor.moveToFirst()) {
            total = cursor.getInt(0)
        }

        cursor.close()

        return total
    }

    fun getJumlahTransaksi(): Int {

        val db = readableDatabase

        val cursor = db.rawQuery(
            "SELECT COUNT(*) FROM transaksi",
            null
        )

        var jumlah = 0

        if (cursor.moveToFirst()) {
            jumlah = cursor.getInt(0)
        }

        cursor.close()

        return jumlah
    }

    // =====================================
    // PRODUK
    // =====================================
fun isiProdukDefault() {

    val db = writableDatabase

    val cursor = db.rawQuery(
        "SELECT COUNT(*) FROM produk",
        null
    )

    var jumlah = 0

    if (cursor.moveToFirst()) {
        jumlah = cursor.getInt(0)
    }

    cursor.close()

    if (jumlah > 0) return

    val daftar = arrayOf(

        arrayOf("🍫 Beng Beng", "Snack", 2500, 3000, 100),
        arrayOf("🍫 Chocolatos", "Snack", 1800, 2500, 100),

        arrayOf("🥤 Es Cekek", "Minuman", 3000, 5000, 100),
        arrayOf("🥤 Es Teh Jumbo", "Minuman", 2500, 4000, 100),

        arrayOf("☕ Good Day", "Kopi", 2500, 4000, 100),
        arrayOf("☕ Kapal Api", "Kopi", 1500, 3000, 100),
        arrayOf("☕ Torabika", "Kopi", 2500, 4000, 100),

        arrayOf("🥛 Milo", "Susu", 3500, 5000, 100),
        arrayOf("🥛 Susu", "Susu", 3000, 5000, 100),

        arrayOf("🍊 Nutrisari", "Minuman", 1500, 3000, 100),
        arrayOf("🥛 Nutrisari Susu", "Minuman", 2500, 4000, 100),

        arrayOf("🧋 Pop Ice Biasa", "Minuman", 2000, 4000, 100),
        arrayOf("🧋 Pop Ice Boba", "Minuman", 3500, 6000, 100)

    )

    for (item in daftar) {

        val values = ContentValues()

        values.put("nama", item[0] as String)
        values.put("kategori", item[1] as String)
        values.put("modal", item[2] as Int)
        values.put("jual", item[3] as Int)
        values.put("stok", item[4] as Int)

        db.insert("produk", null, values)
    }

}

    for (item in daftar) {

        val values = ContentValues()

        values.put("nama", item[0] as String)
        values.put("kategori", item[1] as String)
        values.put("modal", item[2] as Int)
        values.put("jual", item[3] as Int)
        values.put("stok", item[4] as Int)

        db.insert("produk", null, values)
    }

}
    
    fun tambahProduk(
        nama: String,
        kategori: String,
        modal: Int,
        jual: Int,
        stok: Int
    ) {

        val db = writableDatabase

        val values = ContentValues()

        values.put("nama", nama)
        values.put("kategori", kategori)
        values.put("modal", modal)
        values.put("jual", jual)
        values.put("stok", stok)

        db.insert("produk", null, values)

    }

    fun updateProduk(
        namaLama: String,
        namaBaru: String,
        kategori: String,
        modal: Int,
        jual: Int,
        stok: Int
    ) {

        val db = writableDatabase

        val values = ContentValues()

        values.put("nama", namaBaru)
        values.put("kategori", kategori)
        values.put("modal", modal)
        values.put("jual", jual)
        values.put("stok", stok)

        db.update(
            "produk",
            values,
            "nama=?",
            arrayOf(namaLama)
        )

    }

    fun hapusProduk(nama: String) {

        val db = writableDatabase

        db.delete(
            "produk",
            "nama=?",
            arrayOf(nama)
        )

    }

    fun getSemuaProduk(): ArrayList<Produk> {

        val list = ArrayList<Produk>()

        val db = readableDatabase

        val cursor = db.rawQuery(
            "SELECT nama, jual, stok FROM produk ORDER BY nama",
            null
        )

        while (cursor.moveToNext()) {

            list.add(
                Produk(
                    cursor.getString(0),
                    cursor.getInt(1),
                    cursor.getInt(2)
                )
            )

        }

        cursor.close()

        return list

    }

    fun getProduk(nama: String): Produk? {

        val db = readableDatabase

        val cursor = db.rawQuery(
            "SELECT nama, jual, stok FROM produk WHERE nama=?",
            arrayOf(nama)
        )

        var produk: Produk? = null

        if (cursor.moveToFirst()) {

            produk = Produk(
                cursor.getString(0),
                cursor.getInt(1),
                cursor.getInt(2)
            )

        }

        cursor.close()

        return produk

    }

    // =====================================
    // TRANSAKSI KANTIN
    // =====================================

    fun simpanTransaksiKantin(
        tanggal: String,
        produk: String,
        qty: Int,
        harga: Int,
        total: Int
    ) {

        val db = writableDatabase

        val values = ContentValues()

        values.put("tanggal", tanggal)
        values.put("produk", produk)
        values.put("qty", qty)
        values.put("harga", harga)
        values.put("total", total)

        db.insert("transaksi_kantin", null, values)

    }

    fun kurangiStok(
        nama: String,
        qty: Int
    ) {

        val db = writableDatabase

        db.execSQL(
           "UPDATE produk SET stok = stok - ? WHERE nama = ?",
           arrayOf(qty.toString(), nama)
)

    }

    fun getStok(
        nama: String
    ): Int {

        val db = readableDatabase

        val cursor = db.rawQuery(
            "SELECT stok FROM produk WHERE nama=?",
            arrayOf(nama)
        )

        var stok = 0

        if (cursor.moveToFirst()) {
            stok = cursor.getInt(0)
        }

        cursor.close()

        return stok

    }

    fun getTotalKantin(): Int {

        val db = readableDatabase

        val cursor = db.rawQuery(
            "SELECT IFNULL(SUM(total),0) FROM transaksi_kantin",
            null
        )

        var total = 0

        if (cursor.moveToFirst()) {
            total = cursor.getInt(0)
        }

        cursor.close()

        return total

    }

    fun getJumlahTransaksiKantin(): Int {

        val db = readableDatabase

        val cursor = db.rawQuery(
            "SELECT COUNT(*) FROM transaksi_kantin",
            null
        )

        var jumlah = 0

        if (cursor.moveToFirst()) {
            jumlah = cursor.getInt(0)
        }

        cursor.close()

        return jumlah

    }
    
    fun getRiwayatKantin(): ArrayList<String> {

    val list = ArrayList<String>()

    val db = readableDatabase

    val cursor = db.rawQuery(
        """
        SELECT tanggal,produk,qty,total
        FROM transaksi_kantin
        ORDER BY id DESC
        """.trimIndent(),
        null
    )

    while (cursor.moveToNext()) {

        list.add(
            cursor.getString(0) +
            "\n" +
            cursor.getString(1) +
            " x" +
            cursor.getInt(2) +
            "\nRp " +
            MoneyUtils.rupiah(cursor.getInt(3))
        )

    }

    cursor.close()

    return list

}

}
