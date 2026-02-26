# ==========================================
# OBSERVER — Esempio reale: Event-driven UI
# ==========================================
# In un'interfaccia grafica, un componente (es. un bottone) è il
# Subject. Quando l'utente interagisce con esso, diversi Observer
# reagiscono in modo indipendente: aggiornare la UI, scrivere
# un log, tracciare analytics, ecc.
#
# Il bottone non sa CHI lo osserva né COSA fanno gli observer.
# Sa solo che deve chiamare il loro metodo su_evento().
# Questo è esattamente come funzionano i framework UI moderni
# (React, Vue, Qt, Tkinter, WPF…).

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime


# ==========================================
# EVENTO — dati associati a un'interazione
# ==========================================

@dataclass
class Evento:
    """Descrive un'interazione dell'utente con un componente UI."""
    tipo: str                   # "click", "input", "submit"
    sorgente: str               # nome del componente che ha generato l'evento
    dati: dict = field(default_factory=dict)
    timestamp: str = field(default_factory=lambda: datetime.now().strftime("%H:%M:%S"))


# ==========================================
# OBSERVER — interfaccia comune
# ==========================================

class EventListener(ABC):
    """Chiunque voglia reagire a eventi UI implementa questa interfaccia."""

    @abstractmethod
    def su_evento(self, evento: Evento) -> None:
        ...


# ==========================================
# SUBJECT — componente UI generico
# Da notare che avremmo potuto creare direttamente un Subject specifico (tipo un bottone), 
# ma in questo modo possiamo riutilizzare la logica di gestione dei listener per 
# qualsiasi componente UI.
# ==========================================

class ComponenteUI:
    """Subject: un componente dell'interfaccia che emette eventi."""

    def __init__(self, nome: str):
        self.nome = nome
        self._listener: dict[str, list[EventListener]] = {}

    def registra(self, tipo_evento: str, listener: EventListener) -> None:
        """Registra un listener per un tipo di evento specifico."""
        if tipo_evento not in self._listener:
            self._listener[tipo_evento] = []
        self._listener[tipo_evento].append(listener)

    def rimuovi(self, tipo_evento: str, listener: EventListener) -> None:
        """Rimuove un listener da un tipo di evento."""
        if tipo_evento in self._listener:
            self._listener[tipo_evento].remove(listener)

    def _emetti(self, tipo_evento: str, dati: dict | None = None) -> None:
        """Notifica tutti i listener registrati per questo tipo di evento."""
        evento = Evento(tipo=tipo_evento, sorgente=self.nome, dati=dati or {})
        for listener in self._listener.get(tipo_evento, []):
            listener.su_evento(evento)


# ==========================================
# COMPONENTI UI CONCRETI
# ==========================================

class Bottone(ComponenteUI):
    """Un bottone cliccabile."""

    # Da notare che la classe Bottone nel sup "metodo principale" o comunque nel metodo
    # legato al pattern observer si limita a:
        # 1. fare l'operazione specifica del bottone (es. click), in questo caso un semplice print
        # 2. chiamare _emetti() per notificare tutti i listener registrati a questo evento
    # Il bottone NON si preoccupa di chi sono i listener, di cosa fanno, di come reagiscono, ecc.
    def click(self) -> None:
        print(f"\n[{self.nome}] 🖱️ Click!")
        self._emetti("click")


class CampoTesto(ComponenteUI):
    """Un campo di input testuale."""

    def __init__(self, nome: str):
        super().__init__(nome)
        self.valore = ""

    def scrivi(self, testo: str) -> None:
        self.valore = testo
        print(f"\n[{self.nome}] ⌨️ Testo inserito: '{testo}'")
        self._emetti("input", {"valore": testo})


class Form(ComponenteUI):
    """Un form che può essere inviato."""

    def __init__(self, nome: str):
        super().__init__(nome)
        self.campi: dict[str, str] = {}

    def imposta_campo(self, chiave: str, valore: str) -> None:
        self.campi[chiave] = valore

    def invia(self) -> None:
        print(f"\n[{self.nome}] 📨 Form inviato con dati: {self.campi}")
        self._emetti("submit", dict(self.campi))


# ==========================================
# OBSERVER CONCRETI
# ==========================================
# Ogni observer reagisce a modo suo. Il componente UI non sa
# nulla di loro — chiama su_evento() e basta.

class Logger(EventListener):
    """Scrive ogni evento in un log (simula scrittura su file)."""

    def __init__(self):
        self.log: list[str] = []

    def su_evento(self, evento: Evento) -> None:
        riga = f"[{evento.timestamp}] {evento.tipo.upper()} su '{evento.sorgente}'"
        self.log.append(riga)
        print(f"  📝 Logger: {riga}")


class Analytics(EventListener):
    """Conta le interazioni per tipo (simula un sistema di tracking)."""

    def __init__(self):
        self.contatori: dict[str, int] = {}

    def su_evento(self, evento: Evento) -> None:
        chiave = f"{evento.sorgente}:{evento.tipo}"
        self.contatori[chiave] = self.contatori.get(chiave, 0) + 1
        print(f"  📊 Analytics: {chiave} → {self.contatori[chiave]} volta/e")


class Validatore(EventListener):
    """Controlla che un campo non sia vuoto (validazione in tempo reale)."""

    def su_evento(self, evento: Evento) -> None:
        valore = evento.dati.get("valore", "")
        if valore.strip():
            print(f"  ✅ Validatore: '{evento.sorgente}' → OK")
        else:
            print(f"  ❌ Validatore: '{evento.sorgente}' → campo vuoto!")


class AggiornamentoUI(EventListener):
    """Simula l'aggiornamento di un elemento della UI."""

    def __init__(self, elemento: str):
        self.elemento = elemento

    def su_evento(self, evento: Evento) -> None:
        if evento.tipo == "submit":
            print(f"  🔄 UI: '{self.elemento}' aggiornato con i dati del form")
        elif evento.tipo == "click":
            print(f"  🔄 UI: '{self.elemento}' reagisce al click")


# ==========================================
# UTILIZZO
# ==========================================

if __name__ == "__main__":

    # --- Observer condivisi ---
    logger = Logger()
    analytics = Analytics()
    validatore = Validatore()
    aggiorna_tabella = AggiornamentoUI("Tabella utenti")

    # --- Componenti UI ---
    btn_salva = Bottone("Bottone Salva")
    campo_nome = CampoTesto("Campo Nome")
    form_registrazione = Form("Form Registrazione")

    # --- Registrazione listener (chi ascolta cosa) ---
    btn_salva.registra("click", logger)
    btn_salva.registra("click", analytics)
    btn_salva.registra("click", aggiorna_tabella)

    campo_nome.registra("input", logger)
    campo_nome.registra("input", analytics)
    campo_nome.registra("input", validatore)

    form_registrazione.registra("submit", logger)
    form_registrazione.registra("submit", analytics)
    form_registrazione.registra("submit", aggiorna_tabella)

    print("=" * 50)
    print("  EVENT-DRIVEN UI — Observer Pattern")
    print("=" * 50)

    # ---- 1. Click sul bottone → 3 observer reagiscono ----
    btn_salva.click()

    # ---- 2. Input nel campo testo → validazione in tempo reale ----
    campo_nome.scrivi("Mario Rossi")
    campo_nome.scrivi("")           # validazione fallisce

    # ---- 3. Submit del form ----
    form_registrazione.imposta_campo("nome", "Mario Rossi")
    form_registrazione.imposta_campo("email", "mario@example.com")
    form_registrazione.invia()

    # ---- 4. Secondo click (analytics conta) ----
    btn_salva.click()

    # ---- 5. Rimozione di un listener ----
    print("\n--- Rimuovo il Logger dal bottone ---")
    btn_salva.rimuovi("click", logger)
    btn_salva.click()               # il logger NON reagisce più

