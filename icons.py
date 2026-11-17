"""Pictogrammes SVG (viewBox 0 0 64 64, trait currentColor).
Chaque page de service choisit une clé de ce dictionnaire dans son front matter (icon:)."""

ICONS = {
    # Porte d'entrée avec poignée et serrure
    "door": '<rect x="16" y="6" width="32" height="52" rx="2"/><path d="M10 58h44"/><circle cx="41" cy="33" r="2.5"/><path d="M41 38v4"/><path d="M22 12h20v16H22z" opacity=".45"/>',
    # Cadenas classique
    "lock": '<rect x="14" y="28" width="36" height="28" rx="4"/><path d="M22 28v-8a10 10 0 0 1 20 0v8"/><circle cx="32" cy="40" r="3.5"/><path d="M32 43.5V49"/>',
    # Coupe de cylindre avec goupilles
    "pins": '<rect x="8" y="22" width="48" height="22" rx="11"/><path d="M8 33h48" opacity=".4"/><path d="M18 14v14M26 14v10M34 14v16M42 14v12"/><circle cx="18" cy="31" r="1.6"/><circle cx="26" cy="27" r="1.6"/><circle cx="34" cy="33" r="1.6"/><circle cx="42" cy="29" r="1.6"/>',
    # Clé à panneton
    "key": '<circle cx="18" cy="32" r="10"/><circle cx="18" cy="32" r="3.5"/><path d="M28 32h28v6M48 32v5M42 32v7M36 32v4"/>',
    # Deux clés (reproduction)
    "keys": '<circle cx="16" cy="24" r="8"/><path d="M24 24h24v5M42 24v4M36 24v6"/><circle cx="22" cy="42" r="8" opacity=".55"/><path d="M30 42h24v5M48 42v4M42 42v6" opacity=".55"/>',
    # Pêne dormant
    "deadbolt": '<rect x="10" y="12" width="20" height="40" rx="3"/><circle cx="20" cy="26" r="5"/><path d="M20 22v8"/><rect x="30" y="38" width="22" height="8" rx="1.5"/><path d="M52 34v16" opacity=".5"/>',
    # Serrure connectée avec ondes
    "smartlock": '<rect x="18" y="10" width="22" height="44" rx="5"/><circle cx="29" cy="24" r="5"/><path d="M25 38h8M25 44h8"/><path d="M46 20a10 10 0 0 1 0 14M51 15a17 17 0 0 1 0 24"/>',
    # Clavier à code
    "keypad": '<rect x="16" y="6" width="32" height="52" rx="4"/><circle cx="25" cy="18" r="2"/><circle cx="32" cy="18" r="2"/><circle cx="39" cy="18" r="2"/><circle cx="25" cy="27" r="2"/><circle cx="32" cy="27" r="2"/><circle cx="39" cy="27" r="2"/><circle cx="25" cy="36" r="2"/><circle cx="32" cy="36" r="2"/><circle cx="39" cy="36" r="2"/><path d="M26 47h12"/>',
    # Serrure et clé plate (réparation)
    "repair": '<rect x="10" y="24" width="26" height="30" rx="3"/><circle cx="23" cy="36" r="3"/><path d="M23 39v6"/><path d="M38 26l14-14a5 5 0 0 1 7 7L45 33" /><path d="M36 30l6 6"/>',
    # Clé cassée
    "brokenkey": '<circle cx="14" cy="32" r="8"/><path d="M22 32h12"/><path d="M34 28l3 4-3 4"/><path d="M42 28l-3 4 3 4" /><path d="M42 32h16v5M52 32v4"/>',
    # Porte coulissante
    "sliding": '<rect x="6" y="10" width="52" height="44" rx="2"/><path d="M32 10v44"/><path d="M14 18h12v28H14z" opacity=".4"/><path d="M38 32h-4M44 32l6 0M47 29l3 3-3 3"/>',
    # Fenêtre
    "window": '<rect x="10" y="8" width="44" height="48" rx="2"/><path d="M10 32h44M32 8v48"/><rect x="28" y="28" width="8" height="8" rx="1.5"/>',
    # Boîte aux lettres américaine
    "mailbox": '<path d="M12 48V28a12 12 0 0 1 24 0v20z"/><path d="M36 28h16v20H36"/><path d="M24 48v10"/><path d="M44 20v-8h8v5h-8"/><circle cx="24" cy="38" r="2"/>',
    # Maison et clé (emménagement)
    "house": '<path d="M8 30L32 10l24 20"/><path d="M14 26v28h36V26"/><path d="M27 54V40h10v14"/><circle cx="46" cy="16" r="0"/>',
    # Bouclier (après effraction)
    "shield": '<path d="M32 6l20 8v14c0 14-9 24-20 30C21 52 12 42 12 28V14z"/><path d="M24 31l6 6 11-12"/>',
    # Bouclier + cadenas (haute sécurité)
    "shieldlock": '<path d="M32 6l20 8v14c0 14-9 24-20 30C21 52 12 42 12 28V14z"/><rect x="24" y="28" width="16" height="13" rx="2"/><path d="M27 28v-4a5 5 0 0 1 10 0v4"/>',
    # Voiture
    "car": '<path d="M8 40v-7l6-12h36l6 12v7a3 3 0 0 1-3 3H11a3 3 0 0 1-3-3z"/><path d="M14 33h36"/><circle cx="19" cy="43" r="5"/><circle cx="45" cy="43" r="5"/><path d="M22 21l-3 12M42 21l3 12" opacity=".4"/>',
    # Clé de voiture à tête
    "carkey": '<rect x="8" y="20" width="22" height="24" rx="7"/><circle cx="19" cy="28" r="2"/><circle cx="19" cy="36" r="2"/><path d="M30 32h24l2 3-2 3h-6l-2-3-2 3h-4l-2-3-2 3h-6"/>',
    # Puce de transpondeur
    "chip": '<rect x="18" y="18" width="28" height="28" rx="3"/><rect x="26" y="26" width="12" height="12" rx="1.5"/><path d="M24 12v6M32 12v6M40 12v6M24 46v6M32 46v6M40 46v6M12 24h6M12 32h6M12 40h6M46 24h6M46 32h6M46 40h6"/>',
    # Télécommande (key fob)
    "fob": '<rect x="20" y="6" width="24" height="44" rx="11"/><circle cx="32" cy="18" r="4"/><path d="M27 30h10M27 37h10"/><path d="M32 50v8"/><circle cx="32" cy="58" r="0"/>',
    # Contacteur de démarrage
    "ignition": '<circle cx="32" cy="32" r="22"/><circle cx="32" cy="32" r="9"/><path d="M32 23v18" /><path d="M32 6v5M32 53v5M6 32h5M53 32h5" opacity=".5"/>',
    # Coffre de voiture
    "trunk": '<path d="M8 42v-6l10-12h20l8 8h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H10a2 2 0 0 1-2-2z"/><circle cx="18" cy="44" r="5"/><circle cx="46" cy="44" r="5"/><path d="M46 32l8-12" /><circle cx="51" cy="38" r="1.5"/>',
    # Vitrine de commerce
    "store": '<path d="M8 22l4-12h40l4 12z"/><path d="M8 22c0 4 4 6 8 6s8-2 8-6c0 4 4 6 8 6s8-2 8-6c0 4 4 6 8 6s8-2 8-6"/><path d="M12 28v26h40V28"/><path d="M26 54V38h12v16"/>',
    # Porte commerciale vitrée
    "commercialdoor": '<rect x="10" y="6" width="44" height="52" rx="1.5"/><path d="M32 6v52"/><path d="M14 10h14v44H14zM36 10h14v44H36z" opacity=".35"/><path d="M27 26v12M37 26v12"/>',
    # Ferme-porte hydraulique
    "closer": '<path d="M6 12h52"/><rect x="10" y="12" width="24" height="9" rx="2"/><path d="M30 17l14 10 10-15"/><path d="M8 21v37" opacity=".4"/><path d="M14 58h40" opacity=".4"/>',
    # Barre antipanique
    "panicbar": '<rect x="12" y="6" width="40" height="52" rx="1.5"/><rect x="16" y="28" width="32" height="7" rx="3.5"/><path d="M22 35v4M42 35v4"/><path d="M38 18l6 4-6 4" opacity=".5"/>',
    # Badge de contrôle d'accès
    "badge": '<rect x="10" y="14" width="26" height="38" rx="3"/><circle cx="23" cy="27" r="5"/><path d="M16 42a7 7 0 0 1 14 0"/><path d="M42 24a10 10 0 0 1 0 16M48 18a18 18 0 0 1 0 28"/>',
    # Passe-partout (une clé, plusieurs serrures)
    "masterkey": '<circle cx="14" cy="16" r="7"/><path d="M21 16h20v4M35 16v4"/><rect x="8" y="38" width="12" height="16" rx="2"/><rect x="26" y="38" width="12" height="16" rx="2"/><rect x="44" y="38" width="12" height="16" rx="2"/><path d="M14 23v8M32 22v9h18v4M14 31h18M32 31v4" opacity=".5"/>',
    # Coffre-fort avec molette
    "safe": '<rect x="8" y="8" width="48" height="44" rx="3"/><rect x="14" y="14" width="36" height="32" rx="2" opacity=".45"/><circle cx="32" cy="30" r="8"/><path d="M32 22v3M40 30h-3M32 38v-3M24 30h3"/><path d="M14 52v5M50 52v5"/>',
    # Coffre-fort ancré au sol
    "safeinstall": '<rect x="14" y="10" width="36" height="36" rx="3"/><circle cx="32" cy="27" r="6"/><path d="M44 22v10"/><path d="M6 54h52"/><path d="M20 46v8M44 46v8"/><path d="M26 50h-6M44 50h-6" opacity=".5"/>',
    # Horloge 24 h
    "clock": '<circle cx="32" cy="32" r="24"/><path d="M32 18v14l9 6"/><path d="M32 8v3M56 32h-3M32 56v-3M8 32h3" opacity=".5"/>',

    # Étiquette de prix
    "tag": '<path d="M8 30V10a2 2 0 0 1 2-2h20l26 26-22 22z"/><circle cx="20" cy="20" r="4"/><path d="M30 38l8-8M26 34l4 4" opacity=".5"/>',
    # Livre ouvert (blog)
    "book": '<path d="M32 16c-6-5-14-6-24-5v38c10-1 18 0 24 5 6-5 14-6 24-5V11c-10-1-18 0-24 5z"/><path d="M32 16v38"/><path d="M14 22h10M14 30h10M40 22h10M40 30h10" opacity=".5"/>',
    # Bulle de discussion (contact)
    "chat": '<path d="M10 14h44v28H30l-12 10V42h-8z"/><circle cx="22" cy="28" r="2"/><circle cx="32" cy="28" r="2"/><circle cx="42" cy="28" r="2"/>',
    # Point d'interrogation (FAQ)
    "question": '<circle cx="32" cy="32" r="24"/><path d="M24 25a8 8 0 1 1 11 7.4c-2 .9-3 2.4-3 4.6v2"/><circle cx="32" cy="46" r="1.6"/>',
    # Personnes (à propos)
    "people": '<circle cx="24" cy="22" r="8"/><path d="M8 52a16 16 0 0 1 32 0"/><circle cx="44" cy="24" r="6" opacity=".6"/><path d="M40 38a13 13 0 0 1 17 14" opacity=".6"/>',
    # Valise à code
    "luggage": '<rect x="14" y="18" width="36" height="38" rx="4"/><path d="M24 18v-8h16v8"/><path d="M14 30h36" opacity=".5"/><rect x="26" y="36" width="12" height="8" rx="1.5"/>',
}
