#!/bin/bash
# Script pour charger les FAQ SPÉCIFIQUES du cabinet médical dans parlant-qna

echo "🏥 Chargement des FAQ du Cabinet Médical..."
echo ""
echo "💡 Ces FAQ contiennent les informations SPÉCIFIQUES au cabinet"
echo "   (horaires, médecins, tarifs, etc.)"
echo ""

# Horaires
parlant-qna add \
  -q "Quels sont les horaires du cabinet ?" \
  -q "Le cabinet est ouvert quand ?" \
  -a "Notre cabinet est ouvert Lundi-Vendredi 8h30-19h, Samedi 9h-13h. Fermé dimanche et jours fériés. Urgences: composez le 15 ou +33-1-23-45-67-89."

echo "✅ Horaires ajoutés"

# Équipe médicale
parlant-qna add \
  -q "Qui sont les médecins du cabinet ?" \
  -q "Quelles spécialités sont disponibles ?" \
  -a "Dr. Sophie Martin (médecine générale, Lun-Mer-Ven), Dr. Thomas Dupont (cardiologie, Mar-Jeu), Dr. Claire Leblanc (pédiatrie, Lun-Sam), Mme Nathalie Rousseau (infirmière, tous les jours)."

echo "✅ Équipe médicale ajoutée"

# Politique annulation
parlant-qna add \
  -q "Comment annuler un rendez-vous ?" \
  -q "Quelle est votre politique d'annulation ?" \
  -a "Annulation gratuite si >24h avant. Entre 24h-2h: 20€. <2h: 50€. Annulez sur cabinet-martin-sante.fr, par tél +33-1-23-45-67-89 ou email contact@cabinet-martin-sante.fr"

echo "✅ Politique annulation ajoutée"

# Tarifs
parlant-qna add \
  -q "Quels sont vos tarifs ?" \
  -q "Combien coûte une consultation ?" \
  -a "Médecine générale: 25€ (remboursé 70%). Cardiologie: 50€. Pédiatrie: 30€ (100% pour -16 ans). Tiers payant accepté pour CMU, ALD, enfants."

echo "✅ Tarifs ajoutés"

# Contact et accès
parlant-qna add \
  -q "Comment vous contacter ?" \
  -q "Où êtes-vous situés ?" \
  -a "Cabinet Médical Martin, 12 Avenue de la Santé, 75015 Paris. Tél: +33-1-23-45-67-89. Métro ligne 12 Convention. Accès PMR disponible."

echo "✅ Contact et accès ajoutés"

echo ""
echo "🎉 Toutes les FAQ du cabinet ont été chargées !"
echo "📋 Vérifiez avec: parlant-qna list"
