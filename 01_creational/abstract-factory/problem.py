# ==========================================
# IL PROBLEMA CHE L'ABSTRACT FACTORY RISOLVE
# ==========================================
# Il Factory Method gestiva UN solo tipo di prodotto.
# Ora immaginiamo di avere DUE tipi di prodotti correlati: A e B.
# Come nel Factory Method usiamo X, Y, Z — ma ora non sono prodotti singoli,
# sono FAMIGLIE: ogni famiglia ha la propria variante di A e di B,
# e le varianti della stessa famiglia DEVONO essere usate insieme.
#
#   Famiglia X:  ProdottoAX  +  ProdottoBX   ✅ compatibili
#   Famiglia Y:  ProdottoAY  +  ProdottoBY   ✅ compatibili
#   ProdottoAX  +  ProdottoBY               ❌ incompatibili!
#
# Senza Abstract Factory, è il CLIENT a dover gestire manualmente
# questa compatibilità — con tutti i rischi che ne conseguono.

# ==========================================
# PRODOTTI CONCRETI — tipo A (una per famiglia)
# ==========================================
# Nemmeno un'interfaccia comune: ogni classe espone il proprio metodo
# con nome diverso, rendendo l'interscambiabilità impossibile.

class ProdottoAX:
    def operazione_specifica_ax(self) -> str:
        return "Risultato del Prodotto A della famiglia X"

class ProdottoAY:
    def operazione_specifica_ay(self) -> str:
        return "Risultato del Prodotto A della famiglia Y"

class ProdottoAZ:
    def operazione_specifica_az(self) -> str:
        return "Risultato del Prodotto A della famiglia Z"

# ==========================================
# PRODOTTI CONCRETI — tipo B (una per famiglia)
# ==========================================

class ProdottoBX:
    def comportamento_bx(self) -> str:
        return "Risultato del Prodotto B della famiglia X"

class ProdottoBY:
    def comportamento_by(self) -> str:
        return "Risultato del Prodotto B della famiglia Y"

class ProdottoBZ:
    def comportamento_bz(self) -> str:
        return "Risultato del Prodotto B della famiglia Z"

# ==========================================
# IL PROBLEMA: IL CLIENT CHE GESTISCE TUTTO
# ==========================================
class ApplicazioneClient:
    def esegui_logica(self, famiglia: str):
        print(f"Client: costruisco i prodotti della famiglia '{famiglia}'")

        # PROBLEMA 1: il client conosce TUTTE le classi concrete di entrambi i tipi.
        # PROBLEMA 2: deve ricordare lui quali varianti sono compatibili tra loro.
        #             Se sbaglia (es. AX con BY), nessuno lo avvisa — bug silenzioso.
        # PROBLEMA 3: aggiungere la famiglia W significa modificare questo blocco.
        if famiglia == "X":
            a = ProdottoAX()
            b = ProdottoBX()
            risultato_a = a.operazione_specifica_ax()   # nome metodo diverso!
            risultato_b = b.comportamento_bx()           # nome metodo diverso!
        elif famiglia == "Y":
            a = ProdottoAY()
            b = ProdottoBY()
            risultato_a = a.operazione_specifica_ay()
            risultato_b = b.comportamento_by()
        elif famiglia == "Z":
            a = ProdottoAZ()
            b = ProdottoBZ()
            risultato_a = a.operazione_specifica_az()
            risultato_b = b.comportamento_bz()
        else:
            raise ValueError(f"Famiglia '{famiglia}' sconosciuta!")

        print(f"  → {risultato_a}")
        print(f"  → {risultato_b}")

# ==========================================
# UTILIZZO
# ==========================================
# I problemi visibili:
#  • Il client dipende da 6 classi concrete (AX, AY, AZ, BX, BY, BZ).
#  • La compatibilità tra A e B è garantita SOLO dalla disciplina del programmatore.
#  • Aggiungere la famiglia W richiede di toccare questo file.
if __name__ == "__main__":
    app = ApplicazioneClient()
    app.esegui_logica("X")
    app.esegui_logica("Y")
    app.esegui_logica("Z")

    # Nessuno impedisce di fare questo errore — il codice gira ugualmente:
    # a = ProdottoAX()
    # b = ProdottoBY()   ← famiglia sbagliata! bug silenzioso.