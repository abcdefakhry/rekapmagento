def test_member_reconciliation():
    print("Testing Member reconciliation logic...")

    # Sample Magento Data
    magento_raw = [
        {"lac_no": 512250002, "name": "FIKRI RAMAD", "point": 0},
        {"lac_no": "0422250013", "name": "ISWANDI HAI", "point": 0},
        {"lac_no": "0115000001", "name": "PATRESIA SONDRA SIAGIAN", "point": 0},
        {"lac_no": "0115000020", "name": "ROSSA BELLA", "point": 0},
        {"lac_no": "0115000021", "name": "ROBBI TAREHMANGUN", "point": 0}, # POS has point 60000 -> Point berbeda
        {"lac_no": "0115000025", "name": "FERDINAL CIU BASCO (DI MAGENTO)", "point": 40000}, # Name beda in POS
        {"lac_no": "BANJAR2917", "name": "FIRDAUS SA", "point": 0},
    ]

    # Normalize Magento LAC No (Key)
    def normalize_lac(val):
        s = str(val).strip()
        if s.isdigit():
            return s.zfill(10)
        return s

    mag_lookup = {}
    for r in magento_raw:
        key = normalize_lac(r["lac_no"])
        mag_lookup[key] = {
            "name": r["name"],
            "point": float(r["point"])
        }

    assert normalize_lac(512250002) == "0512250002"
    assert normalize_lac("BANJAR2917") == "BANJAR2917"
    assert "0115000001" in mag_lookup

    # Sample POS Data
    pos_raw = [
        {"kdmbr": "0115000001", "nmmbr": "PATRESIA SONDRA SIAGIAN", "poinmbr": 0}, # Data sesuai
        {"kdmbr": "0115000020", "nmmbr": "rossa bella", "poinmbr": 0}, # Data sesuai (case insensitive)
        {"kdmbr": "0115000021", "nmmbr": "ROBBI TAREHMANGUN", "poinmbr": 60000}, # Point berbeda
        {"kdmbr": "0115000025", "nmmbr": "FERDINAL CIU BASCO", "poinmbr": 40000}, # Nama berbeda
        {"kdmbr": "0115999999", "nmmbr": "MEMBER TIDAK DI MAGENTO", "poinmbr": 10000}, # Tidak ditemukan
        {"kdmbr": "0115000001", "nmmbr": "PATRESIA SONDRA SIAGIAN", "poinmbr": 0}, # DUPLIKAT kdmbr
    ]

    # Calculate frequencies for duplicate check
    freq = {}
    for r in pos_raw:
        k = str(r["kdmbr"]).strip()
        freq[k] = freq.get(k, 0) + 1

    results = []
    stat_total = len(pos_raw)
    stat_sesuai = 0
    stat_nama_beda = 0
    stat_point_beda = 0
    stat_missing = 0

    for r in pos_raw:
        kdmbr = str(r["kdmbr"]).strip()
        nmmbr = str(r["nmmbr"]).strip()
        poinmbr = float(r["poinmbr"])

        lac_key = normalize_lac(kdmbr)

        # Lookup
        if lac_key in mag_lookup:
            matched = mag_lookup[lac_key]
            nama_magento = matched["name"]
            point_magento = matched["point"]
        else:
            nama_magento = "LAC No TIDAK DITEMUKAN DI MAGENTO"
            point_magento = "LAC No TIDAK DITEMUKAN DI MAGENTO"

        # Hasil Nama
        if nama_magento == "LAC No TIDAK DITEMUKAN DI MAGENTO":
            hasil_nama = "LAC No TIDAK DITEMUKAN"
        elif nmmbr.upper() == str(nama_magento).strip().upper():
            hasil_nama = "SESUAI"
        else:
            hasil_nama = "TIDAK SESUAI"

        # Hasil Point
        if point_magento == "LAC No TIDAK DITEMUKAN DI MAGENTO":
            hasil_point = "LAC No TIDAK DITEMUKAN"
        elif round(poinmbr, 2) == round(float(point_magento), 2):
            hasil_point = "SAMA"
        else:
            hasil_point = "TIDAK SAMA"

        # Validasi Ganda
        if nama_magento == "LAC No TIDAK DITEMUKAN DI MAGENTO":
            validasi_ganda = "LAC No TIDAK DITEMUKAN"
        elif hasil_nama == "SESUAI":
            validasi_ganda = "VALID (LAC No & Nama cocok)"
        else:
            validasi_ganda = "PERLU DICEK MANUAL (LAC No ketemu tapi Nama beda)"

        # Keterangan
        if hasil_nama == "LAC No TIDAK DITEMUKAN":
            keterangan = "Tidak ditemukan di Magento"
            stat_missing += 1
        elif hasil_nama == "SESUAI" and hasil_point == "SAMA":
            keterangan = "Data sesuai"
            stat_sesuai += 1
        elif hasil_nama == "TIDAK SESUAI" and hasil_point == "SAMA":
            keterangan = "Nama berbeda - perlu dicek"
            stat_nama_beda += 1
        elif hasil_nama == "SESUAI" and hasil_point == "TIDAK SAMA":
            keterangan = "Point berbeda"
            stat_point_beda += 1
        else:
            keterangan = "Nama dan Point berbeda - perlu dicek"
            stat_nama_beda += 1
            stat_point_beda += 1

        # Cek Duplikat
        cek_duplikat = "DUPLIKAT" if freq[kdmbr] > 1 else "TIDAK DUPLIKAT"

        results.append({
            "kdmbr": kdmbr,
            "hasil_nama": hasil_nama,
            "hasil_point": hasil_point,
            "validasi_ganda": validasi_ganda,
            "keterangan": keterangan,
            "cek_duplikat": cek_duplikat
        })

    assert results[0]["keterangan"] == "Data sesuai" and results[0]["cek_duplikat"] == "DUPLIKAT"
    assert results[1]["keterangan"] == "Data sesuai"
    assert results[2]["keterangan"] == "Point berbeda" and results[2]["hasil_point"] == "TIDAK SAMA"
    assert results[3]["keterangan"] == "Nama berbeda - perlu dicek" and results[3]["hasil_nama"] == "TIDAK SESUAI"
    assert results[4]["keterangan"] == "Tidak ditemukan di Magento" and results[4]["hasil_nama"] == "LAC No TIDAK DITEMUKAN"
    assert results[5]["cek_duplikat"] == "DUPLIKAT"

    print("✓ All Member reconciliation rules verified successfully!")
    print(f"Stats: Total={stat_total}, Sesuai={stat_sesuai}, Nama Beda={stat_nama_beda}, Point Beda={stat_point_beda}, Missing={stat_missing}")

if __name__ == "__main__":
    test_member_reconciliation()
