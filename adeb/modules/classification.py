import pandas as pd

# ==============================
# 🛍️ Dictionnaires de classification
# ==============================

pret_a_porter = ["ASOS", "ZALANDO", "H&M", "MANGO", "KIABI", "BERSHKA", "ZARA", "CELIO", "UNIQLO", "PRIMARK", "SHEIN"]

restaurants = ["MCDO", "MCDONALD", "BURGER KING", "KFC", "QUICK", "SUBWAY"]

transport = ["SNCF", "UBER", "RATP", "BOLT", "FREE NOW"]

sante = ["DOCTOLIB", "PHARMACIE", "PHARMA", "MEDECIN", "MEDECINS", "DENTISTE", "OPTIQUE", "LABORATOIRE"]
consultations_medicales = ["DOCTOLIB", "MEDECIN", "MEDECINS", "GENERALISTE", "SPECIALISTE", "DENTISTE", "KINE", "KINÉ", "OSTEO", "OSTEOPATHE"]
pharmacies = ["PHARMACIE", "PHARMA", "PARAPHARMACIE"]
optique = ["OPTIQUE", "OPTICIEN", "KRYS", "AFFLELOU", "GENERALE D OPTIQUE", "GRANDOPTICAL"]
laboratoires = ["LABORATOIRE", "BIOGROUP", "CERBALLIANCE", "ANALYSE MEDICALE"]

# ==============================
# 🧹 Nettoyage des montants
# ==============================

def nettoyer_montant(serie):
    return pd.to_numeric(
        serie.astype(str)
        .str.replace(" ", "", regex=False)
        .str.replace(",", ".", regex=False)
        .str.replace("€", "", regex=False)
        .str.strip(),
        errors="coerce"
    )


# ==============================
# 🧠 Classification Adeb Finance
# ==============================

def mapper_adeb(row):

    category = str(row.get("category", "")).strip()
    parent = str(row.get("categoryParent", "")).strip()
    label = str(row.get("label", "")).upper()
    amount = row.get("amount", 0)

    # 💰 Revenus
    if amount > 0:
        if "Allocation" in parent:
            return "Revenus", "Allocations", "Allocations familiales"

        if "Salaire" in category or "Revenus du travail" in parent:
            return "Revenus", "Salaire", "Salaire fixe"

        return "Revenus", "Autres revenus", "Virement reçu"

    # 🌱 Épargne
    if "REVOLUT" in label:
        return "Epargne", "Sécurité", "Epargne Revolut"

    # 🕌 Baraka
    if parent == "Cadeaux et solidarité":
        return "Baraka", "Sadaqa", category

    if "Famille" in parent:
        return "Baraka", "Aide familiale", category

    # 👕 Prêt-à-porter
    if any(mot in label for mot in pret_a_porter):
        return "Dépenses", "Vie quotidienne", "Vêtements et accessoires"

    # 🍔 Restaurants
    if any(mot in label for mot in restaurants):
        return "Dépenses", "Loisirs & sorties", "Restaurants"

    # 🚆 Transport
    if any(mot in label for mot in transport):
        return "Dépenses", "Transports", "Transport"

    # 🏠 Logement
    if parent == "Logement":
        return "Dépenses", "Logement", category

    # 📱 Factures
    if parent == "Abonnements & téléphonie":
        return "Dépenses", "Factures", category

    # 🛒 Vie quotidienne
    if parent == "Vie quotidienne":
        if category == "Alimentation":
            return "Dépenses", "Vie quotidienne", "Alimentation"

        return "Dépenses", "Vie quotidienne", category

    # ✈️ Voyages & transports
    if parent == "Voyages & Transports":
        return "Dépenses", "Transports", category

    # 🎉 Loisirs
    if parent == "Loisirs et sorties":
        return "Dépenses", "Loisirs & sorties", category

    # 💼 Services
    if parent == "Services financiers & professionnels":
        return "Dépenses", "Imprévus", category
    
    # Santé
    if any(mot in label for mot in consultations_medicales):
        return "Dépenses", "Santé", "Consultation médicale"

    if any(mot in label for mot in pharmacies):
        return "Dépenses", "Santé", "Pharmacie"

    if any(mot in label for mot in optique):
        return "Dépenses", "Santé", "Optique"

    if any(mot in label for mot in laboratoires):
        return "Dépenses", "Santé", "Analyses médicales"

    if parent == "Santé":
        return "Dépenses", "Santé", category if category else "Santé"

    # ❓ Non catégorisé
    return "Dépenses", "Imprévus", "Non catégorisé"
    
