import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QWidget, QTabWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.setCentralWidget(self.tabs)

        self.create_navigation_bar()
        self.add_new_tab(QUrl('http://www.google.com'), 'Homepage')

        self.setStyleSheet("""
                           
            QMainWindow {
                background-color: #f0f0f0;
            }
                           
            QTabWidget::pane {
                border: 1px solid #ccc;
                padding: 5px;
                margin: 5px;
            }
                           
            QTabWidget::tab-bar {
                alignment: left;
            }
                           
            QTabBar::tab {
                background-color: #f0f0f0;
                border: 1px solid #ccc;
                padding: 2px;
            }
                           
            QTabBar::tab:selected, QTabBar::tab:hover {
                background-color: #e0e0e0;
            }
                           
            QPushButton, QTabBar::tab {
                background-color: #4CAF50;
                color: white;
                border: none;
                text-decoration: none;
                font-size: 22px;
                width: 60px;
                height: 36px;
                border-radius: 5px;
            }
                           
            QTabBar::tab{
                width: 140px;
                font-size: 14px;
                padding: 10px 10px;
                height: 20px;
            }
                           
            QPushButton:hover, QTabBar::tab:selected, QTabBar::tab:hover {
                background-color: #499cbf;
            }
                           
             QLineEdit {
                border-radius: 7px;
                padding: 10px;
                margin: 0 10px;
                font-size: 16px;
                background-color: #ECEFF7;
                color: #212121;
                border: 1px solid #5A5A5A;
            }
                           
        """)

        self.showMaximized()

    def create_navigation_bar(self):
        nav_bar = QWidget()
        nav_layout = QHBoxLayout()
        nav_bar.setLayout(nav_layout)
        nav_bar.setFixedHeight(60)

        self.back_button = QPushButton('←')
        self.back_button.clicked.connect(self.go_back)
        nav_layout.addWidget(self.back_button)

        self.forward_button = QPushButton('→')
        self.forward_button.clicked.connect(self.go_forward)
        nav_layout.addWidget(self.forward_button)

        self.reload_button = QPushButton('⟳')
        self.reload_button.clicked.connect(self.reload_page)
        nav_layout.addWidget(self.reload_button)

        self.new_tab_button = QPushButton('+')
        self.new_tab_button.clicked.connect(self.add_new_tab)
        nav_layout.addWidget(self.new_tab_button)

        self.close_tab_button = QPushButton('×')
        self.close_tab_button.clicked.connect(self.close_current_tab)
        nav_layout.addWidget(self.close_tab_button)

        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Enter URL or search term...")
        self.search_bar.returnPressed.connect(self.navigate_to_url)
        nav_layout.addWidget(self.search_bar)

        nav_layout.setSpacing(10)
        nav_layout.setAlignment(Qt.AlignLeft)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(nav_bar)
        main_layout.addWidget(self.tabs)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def add_new_tab(self, qurl=None, label="Blank"):
        if not qurl:
            qurl = QUrl('http://www.google.com')
        browser = QWebEngineView()
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, label)

        self.tabs.setCurrentIndex(i)

        browser.urlChanged.connect(lambda qurl, browser=browser:
            self.update_title(browser, qurl))
        browser.loadFinished.connect(lambda _, i=i, browser=browser:
            self.tabs.setTabText(i, browser.page().title()))

    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab()

    def current_tab_changed(self, i):
        if self.tabs.widget(i):
            qurl = self.tabs.currentWidget().url()
            self.update_title(self.tabs.currentWidget(), qurl)
            self.search_bar.setText(qurl.toString() if qurl else "")
            self.search_bar.setCursorPosition(0)

    def close_tab(self, i):
        if self.tabs.count() < 2:
            return

        self.tabs.removeTab(i)

    def close_current_tab(self):
        current_index = self.tabs.currentIndex()
        self.close_tab(current_index)

    def update_title(self, browser, q):
        if browser != self.tabs.currentWidget():
            return

        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle("% s - Web Browser" % title)

    def navigate_to_url(self):
        qurl = QUrl(self.search_bar.text())
        if qurl.scheme() == "":
            qurl.setScheme("http")

        self.tabs.currentWidget().setUrl(qurl)

    def go_back(self):
        self.tabs.currentWidget().back()

    def go_forward(self):
        self.tabs.currentWidget().forward()

    def reload_page(self):
        self.tabs.currentWidget().reload()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    QApplication.setApplicationName("Web Browser")
    window = Browser()
    window.show()
    sys.exit(app.exec_())