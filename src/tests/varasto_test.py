import unittest
from varasto import Varasto


class TestVarasto(unittest.TestCase):
    def setUp(self):
        self.varasto = Varasto(10)

    def test_konstruktori_luo_tyhjan_varaston(self):
        # https://docs.python.org/3/library/unittest.html#unittest.TestCase.assertAlmostEqual
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_uudella_varastolla_oikea_tilavuus(self):
        self.assertAlmostEqual(self.varasto.tilavuus, 10)

    def test_lisays_lisaa_saldoa(self):
        self.varasto.lisaa_varastoon(8)

        self.assertAlmostEqual(self.varasto.saldo, 8)

    def test_lisays_lisaa_pienentaa_vapaata_tilaa(self):
        self.varasto.lisaa_varastoon(8)

        # vapaata tilaa pitäisi vielä olla tilavuus-lisättävä määrä eli 2
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 2)

    def test_ottaminen_palauttaa_oikean_maaran(self):
        self.varasto.lisaa_varastoon(8)

        saatu_maara = self.varasto.ota_varastosta(2)

        self.assertAlmostEqual(saatu_maara, 2)

    def test_ottaminen_lisaa_tilaa(self):
        self.varasto.lisaa_varastoon(8)

        self.varasto.ota_varastosta(2)

        # varastossa pitäisi olla tilaa 10 - 8 + 2 eli 4
        self.assertAlmostEqual(self.varasto.paljonko_mahtuu(), 4)

    def test_negatiivinen_lisays_ei_muuta_saldoa(self):
        self.varasto.lisaa_varastoon(-5)
        self.assertAlmostEqual(self.varasto.saldo, 0)

    def test_negatiivinen_otto_palauttaa_nolla(self):
        self.varasto.lisaa_varastoon(8)
        saatu_maara = self.varasto.ota_varastosta(-2)
        self.assertAlmostEqual(saatu_maara, 0)

    def test_otto_yli_saldon_palauttaa_koko_saldon(self):
        self.varasto.lisaa_varastoon(5)
        saatu_maara = self.varasto.ota_varastosta(10)
        self.assertAlmostEqual(saatu_maara, 5)  # Palauttaa kaikki, mitä voidaan ottaa
        self.assertAlmostEqual(self.varasto.saldo, 0)  # Saldo on nyt 0

    def test_lisaa_varastoon_yli_tilavuuden(self):
        self.varasto.lisaa_varastoon(15)  # Yritetään lisätä enemmän kuin tilavuus
        self.assertAlmostEqual(self.varasto.saldo, 10)  # Saldo ei saa ylittää tilavuutta

    def test_ota_varastosta_yli_saldon(self):
        self.varasto.lisaa_varastoon(5)
        saatu = self.varasto.ota_varastosta(10)  # Yritetään ottaa enemmän kuin saldo
        self.assertAlmostEqual(saatu, 5)  # Palauttaa kaiken, mitä voidaan
        self.assertAlmostEqual(self.varasto.saldo, 0)  # Saldo on nyt 0

    def test_str_metodi_palauttaa_oikean_merkkijonon(self):
        self.varasto.lisaa_varastoon(3)
        self.assertEqual(str(self.varasto), "saldo = 3, vielä tilaa 7")

    def test_konstruktori_negatiivisella_tilavuudella(self):
        v = Varasto(-5)
        self.assertAlmostEqual(v.tilavuus, 0)

    def test_konstruktori_alkusaldo_yli_tilavuuden(self):
        v = Varasto(5, 10)
        self.assertAlmostEqual(v.saldo, 5)
    def test_konstruktori_negatiivisella_alkusaldolla(self):
        v = Varasto(5, -3)
        self.assertAlmostEqual(v.saldo, 0)
