"""
Implementation of process word checker
"""

from spacy.matcher import PhraseMatcher

from python_requirements_inspector import constants
from python_requirements_inspector.text_processor import TextProcessor
from python_requirements_inspector.type_definitions import MatcherId

# initialize list of process words
process_word_list_en: list[str] = []

process_word_list_de = [
    "Auswählen",
    "Abbilden",
    "Ablehnen",
    "Ableiten",
    "Abrufen",
    "Abschliessen",
    "Adressieren",
    "Aktivieren",
    "Aktualisieren",
    "Analysieren",
    "Anbieten",
    "Anfordern",
    "Anpassen",
    "Anstossen",
    "Anzeigen ",
    "Aufbereiten",
    "Auflisten",
    "Aufzeichnen",
    "Ausführen",
    "Ausgeben",
    "Aushändigen",
    "Ausrechnen",
    "Ausschalten",
    "Ausschliessen",
    "Austauschen",
    "Auswechseln",
    "Auswerten",
    "Bearbeiten",
    "Beenden",
    "Beginnen",
    "Benachrichtigen",
    "Berechnen",
    "Bereitstellen",
    "Berücksichtigen",
    "Bestellen",
    "Bestimmen",
    "Bewirtschaften",
    "Deaktivieren",
    "Definieren",
    "Dokumentieren",
    "Duplizieren",
    "Durchführen",
    "Einbetten",
    "Einhalten",
    "Einschalten",
    "Empfangen",
    "Empfehlen",
    "Entfernen",
    "Entziehen",
    "Erfassen",
    "Erfüllen",
    "Erhalten",
    "Erkennen",
    "Erlauben",
    "Ermöglichen",
    "Errechnen",
    "Ersetzen",
    "Erstellen",
    "Exportieren",
    "Extrapolation",
    "Feinjustieren",
    "Festlegen",
    "Festschreiben",
    "Fortsetzen",
    "Freigeben",
    "Genehmigen",
    "Gestatten",
    "Gewährleisten",
    "Glätten",
    "Identifizieren",
    "Importieren",
    "Informieren",
    "Initiieren",
    "Integrieren",
    "Kategorisierung",
    "Kennen",
    "Klassifizieren",
    "Kontrollieren",
    "Kopieren",
    "Korrigieren",
    "Lokalisieren",
    "Löschen",
    "Lösen",
    "Miteinbeziehen",
    "Modifizieren",
    "Mutieren",
    "Nachführen",
    "Nivellieren",
    "Optimieren",
    "Orten",
    "Persistieren",
    "Planen",
    "Plausibilisieren",
    "Prognostizieren",
    "Prüfen",
    "Realisieren",
    "Rechnen",
    "Reservieren",
    "Schätzen",
    "Schützen",
    "Senden",
    "Setzen",
    "Sichern",
    "Sicherstellen",
    "Speichern",
    "Starten",
    "Steuern",
    "Stornieren",
    "Suchen",
    "Terminieren",
    "Testen",
    "Transferieren",
    "Triggern",
    "Umsetzen",
    "Unterstützen",
    "Untersuchen",
    "Verarbeiten",
    "Verbessern",
    "Verfügbar machen",
    "Verhindern",
    "Verifizieren",
    "Verknüpfen",
    "Vermeiden",
    "Verrechnen",
    "Vervielfältigen",
    "Verwalten",
    "Verwerfen",
    "Visualisieren",
    "Vollziehen",
    "Voraussagen",
    "Vorschlagen",
    "Warnen",
    "Wegnehmen",
    "Weiterleiten",
    "Zulassen",
    "Zuordnen",
    "Zusammenführen",
    "Zuteilen",
    "Zuweisen",
    "auf die Probe stellen",
    "melden",
    "verständigen",
    "zur Verfügung stellen",
    "Ändern",
    "Übergeben",
    "Übertragen",
    "Überwachen",
]


class ProcessWordChecker:
    """
    A class for analyzing the presence of process words in sentences.
    """

    def __init__(self, text_processor: TextProcessor):
        """
        Initializes a ProcessWordChecker object.

        Parameters:
            text_processor (TextProcessor): An instance of the TextProcessor class for text processing.

        """

        self.__text_processor = text_processor

        # Language-specific initialization
        lang = text_processor.get_language()
        if lang == constants.ENGLISH:
            process_word_list = process_word_list_en
        elif lang == constants.GERMAN:
            process_word_list = process_word_list_de
        else:
            raise ValueError(f"Unsupported language: {lang}")

        self.__process_word_matcher = PhraseMatcher(text_processor.get_vocab(), attr="LEMMA")
        patterns = [text_processor.tokenize(name) for name in text_processor.lemmatize_list(process_word_list)]
        self.__process_word_matcher.add(MatcherId.PROCESSWORD_MATCHER_ID.value, patterns)

    def check_sentence(self, sent: str) -> tuple[int, str]:
        """
        Checks if a sentence contains any process words (defined in the process word list).

        Parameters:
            sent (str): The sentence to be analyzed.

        Returns:
            tuple: A tuples with detected findings in the sentence. The tuple contains:
                - Finding count (int)
                - Finding description (str)

        """

        # make the sentence lowercase to ensure detection is case-insensitive
        text = sent.lower()
        doc = self.__text_processor.tokenize(text)

        # get the matched lowercase lemmas
        matches = self.__process_word_matcher(doc, as_spans=True)

        finding_desc = ""
        finding_count = len(matches)

        for match in matches:
            finding_desc += f" {match}"

        return finding_count, finding_desc
