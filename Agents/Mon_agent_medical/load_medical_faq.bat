@echo off
echo ============================================
echo   Chargement des FAQ du Cabinet Medical
echo ============================================
echo.
echo Ces FAQ contiennent les informations SPECIFIQUES
echo au cabinet (horaires, medecins, tarifs, etc.)
echo.

echo Horaires...
parlant-qna add -q "Quels sont les horaires du cabinet ?" -q "Le cabinet est ouvert quand ?" -a "Notre cabinet est ouvert Lundi-Vendredi 8h30-19h, Samedi 9h-13h. Ferme dimanche et jours feries. Urgences: composez le 15 ou +33-1-23-45-67-89."

echo Equipe medicale...
parlant-qna add -q "Qui sont les medecins du cabinet ?" -q "Quelles specialites disponibles ?" -a "Dr. Sophie Martin (medecine generale, Lun-Mer-Ven), Dr. Thomas Dupont (cardiologie, Mar-Jeu), Dr. Claire Leblanc (pediatrie, Lun-Sam), Mme Nathalie Rousseau (infirmiere, tous les jours)."

echo Politique annulation...
parlant-qna add -q "Comment annuler un rendez-vous ?" -q "Quelle est votre politique d'annulation ?" -a "Annulation gratuite si plus de 24h avant. Entre 24h-2h: 20 euros. Moins de 2h: 50 euros. Annulez en ligne sur cabinet-martin-sante.fr, par tel +33-1-23-45-67-89 ou email contact@cabinet-martin-sante.fr"

echo Tarifs...
parlant-qna add -q "Quels sont vos tarifs ?" -q "Combien coute une consultation ?" -a "Medecine generale: 25 euros (rembourse 70 pourcent). Cardiologie: 50 euros. Pediatrie: 30 euros (100 pourcent pour moins 16 ans). Tiers payant accepte pour CMU, ALD, enfants."

echo Contact et acces...
parlant-qna add -q "Comment vous contacter ?" -q "Ou etes-vous situes ?" -a "Cabinet Medical Martin, 12 Avenue de la Sante, 75015 Paris. Tel: +33-1-23-45-67-89. Metro ligne 12 Convention. Acces PMR disponible."

echo.
echo ============================================
echo   FAQ du cabinet chargees avec succes !
echo ============================================
echo.
echo Verifiez avec: parlant-qna list
pause
