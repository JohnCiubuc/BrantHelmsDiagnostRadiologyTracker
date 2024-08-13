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
    ('IV. ', 35),
    ('IV. ', 35),
    ('IV. ', 35),
    ('IV. ', 35),
    ('IV. ', 35),
    ('IV. ', 35),
    # -----
    ('V. ', 35),
    ('V. ', 35),
    ('V. ', 35),
    ('V. ', 35),
    ('V. ', 35),
    ('V. ', 35),
    ('V. ', 35),
    # -----
    ('VI. ', 35),
    ('VI. ', 35),
    ('VI. ', 35),
    ('VI. ', 35),
    ('VI. ', 35),
    ('VI. ', 35),
    ('VI. ', 35),
    ('VI. ', 35),
    ('VI. ', 35),
    ('VI. ', 35),
    ('VI. ', 35),
    ('VI. ', 35),
    # -----
    ('VII. ', 35),
    ('VII. ', 35),
    ('VII. ', 35),
    ('VII. ', 35),
    ('VII. ', 35),
    ('VII. ', 35),
    ('VII. ', 35),
    # -----
    ('VIII. ', 35),
    ('VIII. ', 35),
    ('VIII. ', 35),
    # -----
    ('IX. ', 35),
    ('IX. ', 35),
    ('IX. ', 35),
    ('IX. ', 35),
    ('IX. ', 35),
    # -----
    ('X. ', 35),
    ('X. ', 35),
    ('X. ', 35),
    ('X. ', 35),
    ('X. ', 35),
    ('X. ', 35),
    ('X. ', 35),
    ('X. ', 35),
    ('X. ', 35),
    ('X. ', 35),
    # -----
    ('XI. ', 35),
    ('XI. ', 35),
    ('XI. ', 35),
    ('XI. ', 35),
    ('XI. ', 35),
    ('XI. ', 35),
    # -----
    ('XII. ', 35),
    ('XII. ', 35),
    ('XII. ', 35),
    ('XII. ', 35),
    ('XII. ', 35),
    ('XII. ', 35),
    ('XII. ', 35),
    ('XII. ', 35),
    ('XII. ', 35),
    ('XII. ', 35),
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
