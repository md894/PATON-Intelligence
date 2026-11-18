"""Public-source comparisons and FELYA validation hypotheses."""

TASKS = {
    "teleoperation": {
        "title": ("Teleoperate a robotic hand", "Roboterhand fernsteuern"),
        "entries": ("B01", "C10", "C11", "B02"),
        "question": (
            "Compare setup, grasp accuracy and repeatability. Distinguish camera input, vibration and active force feedback.",
            "Einrichtung, Greifgenauigkeit und Wiederholbarkeit vergleichen. Kameraeingabe, Vibration und aktives Kraftfeedback unterscheiden.",
        ),
    },
    "demonstrations": {
        "title": ("Capture robot-learning demonstrations", "Demonstrationen für Roboterlernen erfassen"),
        "entries": ("C09", "B12", "C12", "B04"),
        "question": (
            "Compare synchronized motion and contact data, export formats and usable demonstrations per hour.",
            "Synchronisierte Bewegungs- und Kontaktdaten, Exportformate und brauchbare Demonstrationen pro Stunde vergleichen.",
        ),
    },
    "contact": {
        "title": ("Return contact to the operator", "Kontakt an die Bedienperson rückmelden"),
        "entries": ("C10", "C11", "T13", "T17"),
        "question": (
            "Trace contact from the robot sensor to the operator. Compare sensing, fingertip vibration and applied force as separate capabilities.",
            "Kontakt vom Robotersensor bis zur Bedienperson verfolgen. Sensorik, Fingerspitzenvibration und ausgeübte Kraft getrennt vergleichen.",
        ),
    },
}

READINESS = (
    ("orca_control", "ORCA finger control", "ORCA-Fingersteuerung", "strategy_public",
     "FELYA publicly describes wearable robot control. Record the exact PATON prototype and ORCA setup, then run the camera comparison.",
     "FELYA beschreibt tragbare Robotersteuerung öffentlich. PATON-Prototyp und ORCA-Aufbau festhalten und den Kameravergleich durchführen."),
    ("demonstration_export", "Demonstration recording and export", "Aufzeichnung und Export von Demonstrationen", "strategy_unverified",
     "Record a timed sequence, export it and verify that joint samples, timestamps and metadata can be replayed.",
     "Eine zeitlich erfasste Sequenz exportieren und prüfen, ob Gelenkdaten, Zeitstempel und Metadaten abgespielt werden können."),
    ("contact_feedback", "Robot contact returned to the operator", "Rückmeldung von Roboterkontakt an die Bedienperson", "strategy_public",
     "FELYA describes physical feedback as a product direction. Test the sensor-to-operator loop for the exact ORCA configuration and measure latency.",
     "FELYA beschreibt physisches Feedback als Produktziel. Den Sensor-Feedback-Kreis in der konkreten ORCA-Konfiguration testen und die Latenz messen."),
)

BUYERS = {
    "orca": (
        ("Robotics development lab", "Robotik-Entwicklungslabor"),
        ("Robotics engineer", "Robotikingenieurin oder -ingenieur"),
        ("Lab lead or engineering manager", "Labor- oder Entwicklungsleitung"),
        ("Camera input or manual joint controls", "Kameraeingabe oder manuelle Gelenksteuerung"),
        ("Reduce setup time for repeatable grasps", "Einrichtungszeit für wiederholbare Greifvorgänge senken"),
    ),
    "learning": (
        ("Robot-learning team", "Team für Roboterlernen"),
        ("Data collection operator or ML engineer", "Datenerfassung oder ML-Entwicklung"),
        ("Physical AI program lead", "Leitung eines Physical-AI-Programms"),
        ("Data glove, XR input or manual teaching", "Datenhandschuh, XR-Eingabe oder manuelles Einlernen"),
        ("Increase usable demonstrations per hour", "Brauchbare Demonstrationen pro Stunde erhöhen"),
    ),
    "industrial": (
        ("Industrial automation integrator", "Industrieautomatisierungs-Integrator"),
        ("Teleoperation or commissioning engineer", "Teleoperations- oder Inbetriebnahmetechnik"),
        ("Automation project lead", "Leitung des Automatisierungsprojekts"),
        ("Camera-guided remote control or a fixed controller", "Kameragestützte Fernsteuerung oder stationäres Bediengerät"),
        ("Reduce contact errors in a selected handling task", "Kontaktfehler bei einer ausgewählten Handhabungsaufgabe senken"),
    ),
}

SIGNALS = (
    ("B13", "2026-10-20", (
        "Track which manual manufacturing tasks are selected and what an integrator would need for a pilot.",
        "Beobachten, welche manuellen Fertigungsaufgaben ausgewählt werden und was ein Integrator für einen Pilotversuch benötigt.",
    )),
    ("C09", None, (
        "Benchmark the demonstration workflow and confirm data formats and access with the supplier.",
        "Demonstrationsablauf vergleichen und Datenformate sowie Zugang beim Anbieter klären.",
    )),
    ("C11", None, (
        "Benchmark active finger feedback and review the documented ROS and Python integration paths.",
        "Aktives Fingerfeedback vergleichen und die dokumentierten Integrationswege für ROS und Python prüfen.",
    )),
    ("C10", None, (
        "Use AE01 as a vibration benchmark. Its specification lists five fingertip vibration motors.",
        "AE01 als Vibrationsvergleich nutzen. Die Spezifikation nennt fünf Vibrationsmotoren an den Fingerspitzen.",
    )),
)
