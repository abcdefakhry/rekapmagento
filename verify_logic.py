import sys

def test_reconciliation_logic():
    print("Testing reconciliation logic...")
    
    # 1. Magento row calculation
    magento_rows = [
        {"tx_no": "AC26000176", "point": -120000},
        {"tx_no": "JSL070016002166", "point": 20000},
        {"tx_no": "JSL070016002167", "point": 60000},
        {"tx_no": "JSL070016002168", "point": 40000},
    ]
    
    rekap_bersih = []
    mag_lookup = {}
    for r in magento_rows:
        pt = r["point"]
        pt_pos = pt if pt > 0 else 0
        pt_neg = pt if pt < 0 else 0
        rekap_bersih.append((r["tx_no"], pt_pos, pt_neg))
        if r["tx_no"] not in mag_lookup:
            mag_lookup[r["tx_no"]] = {"pos": pt_pos, "neg": pt_neg}
            
    assert len(rekap_bersih) == 4
    assert mag_lookup["AC26000176"]["pos"] == 0
    assert mag_lookup["AC26000176"]["neg"] == -120000
    assert mag_lookup["JSL070016002166"]["pos"] == 20000
    assert mag_lookup["JSL070016002166"]["neg"] == 0
    print("✓ Magento & Rekap Bersih logic passed.")

    # 2. POS Non-member separation & Member reconciliation
    pos_rows = [
        {"nops": "AC26000176", "mbrps": "0512260059", "pointrpps": 0, "pointrp2ps": 120000},
        {"nops": "JSL070016002166", "mbrps": "0712260373", "pointrpps": 20000, "pointrp2ps": 0},
        {"nops": "JSL070016002167", "mbrps": "0712260373", "pointrpps": 60000, "pointrp2ps": 0},
        {"nops": "JSL990000000001", "mbrps": "0812345678", "pointrpps": 50000, "pointrp2ps": 0},
        {"nops": "JSL070016002168", "mbrps": "0712260374", "pointrpps": 80000, "pointrp2ps": 0},
        {"nops": "JSL000000000099", "mbrps": "9999999999", "pointrpps": 0, "pointrp2ps": 0},
        {"nops": "JSL000000000100", "mbrps": "9999999999", "pointrpps": 0, "pointrp2ps": 0},
    ]

    member_results = []
    non_member_results = []

    count_sama = 0
    count_tidak_sama = 0
    count_missing = 0

    for r in pos_rows:
        if str(r["mbrps"]).strip() == "9999999999":
            non_member_results.append(r)
            continue
            
        nops = r["nops"]
        rpps = r["pointrpps"]
        rp2ps = r["pointrp2ps"]
        
        if nops in mag_lookup:
            matched = mag_lookup[nops]
            pt_mag = matched["pos"] if rpps > 0 else matched["neg"]
        else:
            pt_mag = "Tidak ditemukan"
            
        if pt_mag == "Tidak ditemukan":
            status = "TRANSAKSI TIDAK DITEMUKAN"
            ket = "Tidak ada pada Magento"
            count_missing += 1
        else:
            num_mag = float(pt_mag)
            is_sama = (num_mag == rpps) or (abs(num_mag) == abs(rp2ps)) or (num_mag == rp2ps)
            if is_sama:
                status = "SAMA"
                ket = "Point cocok"
                count_sama += 1
            else:
                status = "TIDAK SAMA"
                ket = "Nilai berbeda"
                count_tidak_sama += 1
                
        member_results.append({
            "nops": nops,
            "pt_mag": pt_mag,
            "status": status,
            "ket": ket
        })

    assert len(non_member_results) == 2, f"Expected 2 non-member, got {len(non_member_results)}"
    assert len(member_results) == 5, f"Expected 5 member, got {len(member_results)}"
    assert count_sama == 3, f"Expected 3 SAMA, got {count_sama}"
    assert count_tidak_sama == 1, f"Expected 1 TIDAK SAMA, got {count_tidak_sama}"
    assert count_missing == 1, f"Expected 1 TRANSAKSI TIDAK DITEMUKAN, got {count_missing}"

    # Verify each specific case
    assert member_results[0]["status"] == "SAMA" and member_results[0]["ket"] == "Point cocok"
    assert member_results[1]["status"] == "SAMA" and member_results[1]["ket"] == "Point cocok"
    assert member_results[2]["status"] == "SAMA" and member_results[2]["ket"] == "Point cocok"
    assert member_results[3]["status"] == "TRANSAKSI TIDAK DITEMUKAN" and member_results[3]["ket"] == "Tidak ada pada Magento"
    assert member_results[4]["status"] == "TIDAK SAMA" and member_results[4]["ket"] == "Nilai berbeda"
    
    print("✓ Member separation and reconciliation logic verified 100% successfully!")
    print(f"Summary: Total Member={len(member_results)}, SAMA={count_sama}, TIDAK SAMA={count_tidak_sama}, TIDAK DITEMUKAN={count_missing}, Non Member={len(non_member_results)}")

if __name__ == "__main__":
    test_reconciliation_logic()
