import sys
import pickle
from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QCheckBox, QLabel, QTabWidget, QScrollArea, QFormLayout, QFrame

Sections = [
    'Basic Principles',
    'Neuroradiology',
    'Chest',
    'Breast Radiology',
    'Cardiac Radiology',
    'Vascular and Interventional Radiology',
    'Gastrointestinal Tract',
    'Genitourinary Tract',
    'Ultrasonography',
    'Musculoskeletal Radiology',
    'Pediatric Radiology',
    'Nuclear Radiology'
]

ChapterCounts = [
    1, 8, 8, 6, 7, 12, 7, 3, 5, 10, 6, 10
]

Chapters = [
    ('I. Diagnostic Imaging Methods', 26),
    # -----
    ('II. Introduction to Brain Imaging', 21),
    ('II. Craniofacial Trauma', 28),
    ('II. Cerebrovascular Disease', 32),
    ('II. CNS Neoplasms and Tumor-like Masses', 29),
    ('II. CNS Infections', 34),
    ('II. White Matter and Neurodegenerative Diseases', 26),
    ('II. Head and Neck Imaging', 27),
    ('II. Spine Imaging', 39),
    # -----
    ('III. Methods of Examination, Normal Anatomy...', 46),
    ('III. Mediastinum and Hila', 34),
    ('III. Pulmonary Vascular Disease', 17),
    ('III. Pulmonary Neoplasms and Neoplastic-like Conditions', 33),
    ('III. Pulmonary Infection', 24),
    ('III. Diffuse Lung Disease', 37),
    ('III. Airways Disease and Emphysema', 20),
    ('III. Pleura, Chest Wall, Diaphragm....', 35),
    # -----
    ('IV. Normal Anatomy and Histopathology', 18),
    ('IV. Imaging the Screening Patient', 14),
    ('IV. Imaging the Diagnostic Patient', 13),
    ('IV. Breast Imaging Reporting and Data System', 21),
    ('IV. Breast Magnetic Resonance Imaging', 22),
    ('IV. Image-Guided Breast Procedures', 24),
    # -----
    ('V. Introduction to Cardiac Anatomy, Physiology, and Imaging Techniques', 21),
    ('V. Coronary Artery Anomalies and Disease', 37),
    ('V. Cardiac Masses', 21),
    ('V. Valvular Diseaes', 21),
    ('V. Nonischemic Cardiomyopathies', 15),
    ('V. Imaging of the Pericardium', 26),
    ('V. Thoracic Aorta', 33),
    # -----
    ('VI. Medications in Interventional Radiology', 9),
    ('VI. Basics of Angiography and Arterial Disease – (Angiography)', 13),
    ('VI. Peripheral Arterial Disease', 14),
    ('VI. Central Venous Catheters', 7),
    ('VI. Chronic Venous Disease and Deep Vein Thrombosis', 12),
    ('VI. Pulmonary Embolism', 17),
    ('VI. Gastrointestinal Interventions', 22),
    ('VI. Genitourinary Interventions', 12),
    ('VI. Portal Hypertension', 13),
    ('VI. Interventional Radiology in the Diagnosis and Management of Post Liver and Kidney Transplant Complications', 20),
    ('VI. Image-Guided Needle Biopsies and Personalized Medicine', 15),
    ('VI. Interventional Management of Hepatic Malignancies: General Concepts From Anatomy to Practice', 22),
    # -----
    ('VII. Abdomen and Pelvis', 19),
    ('VII. Liver, Biliary Tree, and Gallbladder', 28),
    ('VII. Pancreas and Spleen', 15),
    ('VII. Pharynx and Esophagus', 18),
    ('VII. Stomach and Duodenum', 13),
    ('VII. Mesenteric Small Bowel', 15),
    ('VII. Colon and Appendix', 16),
    # -----
    ('VIII. Adrenal Glands and Kidneys', 21),
    ('VIII. Pelvicalyceal System, Ureters, Bladder, and Urethra', 19),
    ('VIII. Genital Tract—CT, MR, and Radiographic Imaging', 20),
    # -----
    ('IX. Abdomen Ultrasound', 26),
    ('IX. Genital Tract and Bladder Ultrasound', 24),
    ('IX. Obstetric Ultrasound', 28),
    ('IX. Chest, Thyroid, Parathyroid, and Neonatal Brain Ultrasound', 18),
    ('IX. Vascular Ultrasound', 26),
    # -----
    ('X. Benign Lucent Bone Lesions', 20),
    ('X. Malignant Bone and Soft Tissue Tumors', 15),
    ('X. Skeletal Trauma', 29),
    ('X. Arthritis', 24),
    ('X. Metabolic Bone Disease', 11),
    ('X. Skeletal “Don’t Touch” Lesions', 11),
    ('X. Miscellaneous Bone Lesions', 8),
    ('X. Magnetic Resonance Imaging of the Knee', 12),
    ('X. Magnetic Resonance Imaging of the Shoulder', 8),
    ('X. Magnetic Resonance Imaging of the Foot and Ankle', 12),
    # -----
    ('XI. Imaging Children—What You Need to Know', 4),
    ('XI. Pediatric Neuroradiology', 27),
    ('XI. Pediatric Chest', 23),
    ('XI. Congenital and Pediatric Heart Disease', 13),
    ('XI. Abdomen', 36),
    ('XI. Pediatric MSK', 45),
    # -----
    ('XII. Introduction to Nuclear Medicine', 5),
    ('XII. Essential Science of Nuclear Medicine', 19),
    ('XII. Gastrointestinal, Liver–Spleen, and Hepatobiliary Scintigraph', 12),
    ('XII. Pulmonary Scintigraphy', 17),
    ('XII. Skeletal System Scintigraphy', 13),
    ('XII. Endocrine Gland Scintigraphy', 15),
    ('XII. Cardiovascular System Scintigraphy', 12),
    ('XII. Nuclear Brain Imaging', 11),
    ('XII. Scintigraphic Diagnosis of Inflammation and Infection', 12),
    ('XII. Positron Emission Tomography', 29),
]


save_file = 'checkbox_states.pkl'

class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.total_sum = sum([chapter[1] for chapter in Chapters])
        self.checked_sum = 0
        self.layout = QVBoxLayout()
        self.tab_widget = QTabWidget()
        self.checkboxes = {}
        self.layout.addWidget(self.tab_widget)

        self.line = QFrame()
        self.line.setGeometry(QRect(60, 110, 751, 40))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.layout.addWidget(self.line)

        self.label1 = QLabel(self)
        self.label2 = QLabel(self)
        self.layout.addWidget(self.label1)
        self.layout.addWidget(self.label2)

        self.populate_tabs()
        self.setLayout(self.layout)
        self.load_states()
        self.update_labels()

    def populate_tabs(self):
        chapter_index = 0
        chapter_offset = 0
        for section in Sections:
            scroll_area = QScrollArea()
            form_layout = QFormLayout()

            chapter_count = ChapterCounts[chapter_index]
            for chapter in Chapters[chapter_offset:chapter_count+chapter_offset]:
                checkbox = QCheckBox(chapter[0], self)
                checkbox.stateChanged.connect(self.update_labels)
                form_layout.addWidget(checkbox)
                self.checkboxes[checkbox] = chapter[1]

            chapter_offset += chapter_count
            chapter_index += 1
            section_widget = QWidget()
            section_widget.setLayout(form_layout)
            scroll_area.setWidget(section_widget)
            scroll_area.setWidgetResizable(True)
            self.tab_widget.addTab(scroll_area, section)

    def update_labels(self):
        self.checked_sum = sum([val for cb, val in self.checkboxes.items() if cb.isChecked()])
        self.label1.setText(f'Pages Read: {self.checked_sum} out of {self.total_sum}')
        percentage = (self.checked_sum / self.total_sum) * 100 if self.total_sum != 0 else 0
        self.label2.setText(f'Book Completion: {percentage:.2f}%')
        self.save_states()

    def save_states(self):
        states = {cb.text(): cb.isChecked() for cb in self.checkboxes}
        with open(save_file, 'wb') as f:
            pickle.dump(states, f)

    def load_states(self):
        try:
            with open(save_file, 'rb') as f:
                states = pickle.load(f)
                for cb in self.checkboxes:
                    cb.setChecked(states.get(cb.text(), False))
        except FileNotFoundError:
            pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.show()
    sys.exit(app.exec_())
