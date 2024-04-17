# import Anybody_LoadOutput.LoadOutput as LoadOutput
# import Anybody_Tools as LoadOutputTools

from Anybody_Package.Anybody_LoadOutput.LoadOutput import define_variables_to_load
from Anybody_Package.Anybody_LoadOutput.LoadOutput import load_simulation_cases
from Anybody_Package.Anybody_LoadOutput.LoadOutput import load_simulation
from Anybody_Package.Anybody_LoadOutput.LoadOutput import create_compared_simulations

from Anybody_Package.Anybody_LoadOutput.Tools import save_results_to_file
from Anybody_Package.Anybody_LoadOutput.Tools import array_to_dictionary

from Anybody_Package.Anybody_LoadOutput.LoadLiterature import load_literature_data
from Anybody_Package.Anybody_LoadOutput.LoadOutput import combine_simulation_cases

import numpy as np

import pandas as pd

# %% Setup des variables à charger

# Muscles
MuscleDictionary = {"Deltoideus lateral": ["deltoideus_lateral", "_part_", [1, 4]],
                    "Deltoideus posterior": ["deltoideus_posterior", "_part_", [1, 4]],
                    "Deltoideus anterior": ["deltoideus_anterior", "_part_", [1, 4]],
                    "Supraspinatus": ["supraspinatus", "_", [1, 6]],
                    "Infraspinatus": ["infraspinatus", "_", [1, 6]],
                    "Serratus anterior": ["serratus_anterior", "_", [1, 6]],
                    "Lower trapezius": ["trapezius_scapular", "_part_", [1, 3]],
                    "Middle trapezius": ["trapezius_scapular", "_part_", [4, 6]],
                    "Upper trapezius": ["trapezius_clavicular", "_part_", [1, 6]],
                    "Biceps brachii long head": ["biceps_brachii_caput_longum", "", []],
                    "Biceps brachii short head": ["biceps_brachii_caput_breve", "", []],
                    "Pectoralis major clavicular": ["pectoralis_major_clavicular", "_part_", [1, 5]],
                    "Pectoralis major sternal": ["pectoralis_major_thoracic", "_part_", [1, 10]],

                    "Pectoralis major": [["pectoralis_major_thoracic", "_part_", [1, 10]],
                                         ["pectoralis_major_clavicular", "_part_", [1, 5]]
                                         ],

                    "Pectoralis minor": ["pectoralis_minor", "_", [1, 3]],
                    "Latissimus dorsi": ["latissimus_dorsi", "_", [1, 11]],
                    "Triceps long head": ["Triceps_LH", "_", [1, 2]],
                    "Upper Subscapularis": ["subscapularis", "_", [1, 2]],
                    "Downward Subscapularis": ["subscapularis", "_", [3, 6]],
                    "Subscapularis": ["subscapularis", "_", [1, 6]],
                    "Teres minor": ["teres_minor", "_", [1, 6]],
                    "Teres major": ["teres_major", "_", [1, 6]],
                    "Rhomboideus": ["rhomboideus", "_", [1, 3]],
                    "Levator scapulae": ["levator_scapulae", "_", [1, 4]],
                    "Sternocleidomastoid clavicular": ["Sternocleidomastoid_caput_clavicular", "", []],
                    "Sternocleidomastoid sternum": ["Sternocleidomastoid_caput_Sternum", "", []],
                    "Coracobrachialis": ["coracobrachialis", "_", [1, 6]]
                    }

MuscleVariableDictionary = {"Fm": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "Fm", "VariableDescription": "Muscle force [N]"},
                            # "Ft": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "Ft", "VariableDescription": "Force musculaire totale [Newton]"},
                            # "Activity": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "CorrectedActivity", "VariableDescription": "Activité Musculaire [%]", "MultiplyFactor": 100, "combine_muscle_part_operations": ["max", "mean"]},

                            # "F origin": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "RefFrameOutput.F", "VariableDescription": "Force Musculaire à l'origine du muscle [N]", "select_matrix_line": 0,
                            #              "rotation_matrix_path": "Output.Seg.Scapula.AnatomicalFrame.ISB_Coord.Axes", "inverse_rotation": True, "SequenceComposantes": ["AP", "IS", "ML"],
                            #              "combine_muscle_part_operations": ["total", "mean"]},

                            # "F insertion": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "RefFrameOutput.F", "VariableDescription": "Force Musculaire à l'insertion du muscle [N]", "select_matrix_line": 1,
                            #                 "rotation_matrix_path": "Output.Seg.Scapula.AnatomicalFrame.ISB_Coord.Axes", "inverse_rotation": True, "SequenceComposantes": ["AP", "IS", "ML"],
                            #                 "combine_muscle_part_operations": ["total", "mean"]},

                            "MomentArm": {"MuscleFolderPath": "Output.Mus", "AnybodyVariableName": "MomentArm", "VariableDescription": "Muscle moment arm [mm]",
                                          "combine_muscle_part_operations": ["mean"], "MultiplyFactor": 1000}
                            }

# Variables
VariableDictionary_Flexion = {"Angle": {"VariablePath": "Output.Model.ModelEnvironmentConnection.Drivers.Angle", "VariableDescription": "Sagittal elevation [°]"},
                              "Reaction": {"VariablePath": "Output.Jnt.MyGlenoHumeralJoint.Constraints.Reaction.Fout", "VariableDescription": "glenohumeral reaction force [N]", "SequenceComposantes": ["AP", "IS", "ML"]},
                              }

VariableDictionary_Abduction = {"Angle": {"VariablePath": "Output.Model.ModelEnvironmentConnection.Drivers.Angle", "VariableDescription": "Coronal elevation [°]"},
                                "Reaction": {"VariablePath": "Output.Jnt.MyGlenoHumeralJoint.Constraints.Reaction.Fout", "VariableDescription": "glenohumeral reaction force [N]", "SequenceComposantes": ["AP", "IS", "ML"]},
                                }

VariableDictionary_Scapular = {"Angle": {"VariablePath": "Output.Model.ModelEnvironmentConnection.Drivers.Angle", "VariableDescription": "Scapular elevation [°]"},
                               "Reaction": {"VariablePath": "Output.Jnt.MyGlenoHumeralJoint.Constraints.Reaction.Fout", "VariableDescription": "glenohumeral reaction force [N]", "SequenceComposantes": ["AP", "IS", "ML"]},
                               }


# Constantes (si un fichier AnyFileOut contenant des constantes est créé en même temps que le fichier h5)
# Constantes
ConstantsDictionary = {"AnybodyFileOutPath": "Main.Study.FileOut",  # CHEMIN D'ACCÈS ANYBODY DE L'OBJET AnyFileOut
                       "Paramètres de simulation": ["Case", "MuscleRecruitment", "nStep", "tEnd", "GHReactions", "Movement"],
                       "Mannequin": ["GlenohumeralFlexion", "GlenohumeralAbduction", "GlenohumeralExternalRotation"]
                       }


VariableDictionary_Flexion = define_variables_to_load(VariableDictionary_Flexion, MuscleDictionary, MuscleVariableDictionary, ConstantsDictionary)
VariableDictionary_Abduction = define_variables_to_load(VariableDictionary_Abduction, MuscleDictionary, MuscleVariableDictionary, ConstantsDictionary)
VariableDictionary_Scapular = define_variables_to_load(VariableDictionary_Scapular, MuscleDictionary, MuscleVariableDictionary, ConstantsDictionary)


# %% Chargement des fichiers .h5

"""Chemin d'accès au dossier où sont sauvegardes les fichiers h5"""
SaveDataDir = r"Results"

# Chemin d'accès au dossier dans lequel les fichiers doivent être sauvegardés
SaveSimulationsDirectory = "Saved Simulations"

MovementType_list = ["CoronalElevation", "ScapularElevation", "SagitalElevation"]

# glenoid_lateralisation_offset_list = [-10, -5, 0, 5]
# glenoid_superior_offset_list = [-6, -4, -2, 0]
# glenoid_lateral_offset = [0, 5, 10, 15]

glenoid_lateralisation_offset_list = [-10, 5]
glenoid_superior_offset_list = [-6, 0]
glenoid_lateral_offset_list = [0, 15]

Files_Abduction = []
Files_Scapular = []
Files_Flexion = []

CaseNames = []

for humeral_lateral_offset in glenoid_lateral_offset_list:
    for glenoid_lateral_offset in glenoid_lateralisation_offset_list:

        for glenoid_superior_offset in glenoid_superior_offset_list:

            # Nom des simulations
            CaseNames.append(f"Hum : {humeral_lateral_offset} Lat ; Glen : {glenoid_lateral_offset} Lat, {glenoid_superior_offset} Sup")

            # Nom des fichiers par mouvements
            Files_Abduction.append(f"CoronalElevation_humLat_{humeral_lateral_offset}_glenLat_{glenoid_lateral_offset}_glenSup_{glenoid_superior_offset}")
            Files_Scapular.append(f"ScapularElevation_humLat_{humeral_lateral_offset}_glenLat_{glenoid_lateral_offset}_glenSup_{glenoid_superior_offset}")
            Files_Flexion.append(f"SagitalElevation_humLat_{humeral_lateral_offset}_glenLat_{glenoid_lateral_offset}_glenSup_{glenoid_superior_offset}")

Results_Abduction = load_simulation_cases(SaveDataDir, Files_Abduction, CaseNames, VariableDictionary_Abduction)
Results_Scapular = load_simulation_cases(SaveDataDir, Files_Scapular, CaseNames, VariableDictionary_Scapular)
Results_Flexion = load_simulation_cases(SaveDataDir, Files_Flexion, CaseNames, VariableDictionary_Flexion)

Results = {"CoronalElevation": Results_Abduction, "ScapularElevation": Results_Scapular, "SagitalElevation": Results_Flexion}

# Ration d'instabilité
for movement in MovementType_list:
    for case in CaseNames:
        current_result = Results[movement][case]

        reactions = current_result["Reaction"]
        current_result["IR"] = {"SequenceComposantes": ["Total"], "Description": "Instability ratio"}
        current_result["IR"]["Total"] = reactions["IS"] / reactions["ML"]

# Sauvegarde des résultats dans des fichiers .pkl
save_results_to_file(Results_Flexion, SaveSimulationsDirectory, "Results_Flexion")
save_results_to_file(Results_Abduction, SaveSimulationsDirectory, "Results_Abduction")
save_results_to_file(Results_Scapular, SaveSimulationsDirectory, "Results_Scapular")

# %% Sauvegarde des dictionnaires de variables

# # Chemin d'accès au dossier dans lequel les fichiers doivent être sauvegardés
SaveVariablesDirectory = "Saved VariablesDictionary"

save_results_to_file(VariableDictionary_Flexion, SaveVariablesDirectory, "VariableDictionary_Flexion")

# %% Chargement du fichier excel de littérature

# # Informations about the excel file
# file_name = "Template_importation_littérature"
# directory_path = "Anybody_Package/Template"

# # Loads the excel
# Results_Literature = load_literature_data(file_name, directory_path)

# # Saves it to a .pkl file
# save_results_to_file(Results_Literature, SaveSimulationsDirectory, "Results_Literature")

# %% Combiner des cas de simulations

# combine_cases = {"cas_13": ["cas_1", "cas_3"],
#                  "cas_24": ["cas_2", "cas_4"],
#                  "cas_5": ["cas_5"]
#                  }

# # moyenne des cas de simulations
# combined_results = combine_simulation_cases(Results, combine_cases, "mean")

# # Saves it to a .pkl file
# save_results_to_file(combined_results, SaveSimulationsDirectory, "combined_results")


