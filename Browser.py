import sys
import os
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QToolBar, QLineEdit, QTabWidget, QToolButton, QAction, QPushButton, QLabel
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings

GITHUB_REPO = 'https://github.com/RapChapter/Browser'
LOCAL_VERSION_FILE = 'version.txt'
REMOTE_VERSION_FILE = f'{GITHUB_REPO}/raw/main/version.txt'
UPDATE_SCRIPT = 'update.py'
CURRENT_VERSION = '0.9.9'

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Eigen Browser')
        self.setGeometry(100, 100, 1200, 800)

        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('https://www.google.com'))
        self.setCentralWidget(self.browser)

        self.browser.settings().setAttribute(QWebEngineSettings.PluginsEnabled, True)
        self.browser.settings().setAttribute(QWebEngineSettings.FullScreenSupportEnabled, True)
        self.browser.settings().setAttribute(QWebEngineSettings.JavascriptCanOpenWindows, True)
        self.browser.settings().setAttribute(QWebEngineSettings.JavascriptCanAccessClipboard, True)
        self.browser.settings().setAttribute(QWebEngineSettings.AllowRunningInsecureContent, True)
        self.browser.settings().setAttribute(QWebEngineSettings.AllowGeolocationOnInsecureOrigins, True)

        # Toolbar für Standardfunktionen
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        back_button = QToolButton()
        back_button.setText('←')
        back_button.clicked.connect(self.browser.back)
        self.toolbar.addWidget(back_button)

        forward_button = QToolButton()
        forward_button.setText('→')
        forward_button.clicked.connect(self.browser.forward)
        self.toolbar.addWidget(forward_button)

        reload_button = QToolButton()
        reload_button.setText('⟳')
        reload_button.clicked.connect(self.browser.reload)
        self.toolbar.addWidget(reload_button)

        home_button = QToolButton()
        home_button.setText('⌂')
        home_button.clicked.connect(self.navigate_home)
        self.toolbar.addWidget(home_button)

        # URL-Leiste
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.toolbar.addWidget(self.url_bar)

        self.browser.urlChanged.connect(self.update_url)

        # Tab-Widget
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.tabs.tabBarDoubleClicked.connect(self.open_new_tab)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.addTab(self.browser, 'Home')

        self.setCentralWidget(self.tabs)

        # Neue Tab-Taste
        self.new_tab_button = QPushButton('+')
        self.new_tab_button.clicked.connect(self.open_new_tab)
        self.toolbar.addWidget(self.new_tab_button)

        # Lesezeichen-Leiste
        self.bookmarks_bar = QToolBar('Bookmarks')
        self.addToolBar(Qt.BottomToolBarArea, self.bookmarks_bar)
        self.bookmarks = ['https://www.google.com']
        self.load_bookmarks()

        # Versionsanzeige
        self.version_label = QLabel(f'Version: {CURRENT_VERSION}')
        self.toolbar.addWidget(self.version_label)

        self.check_for_updates()

    def navigate_home(self):
        self.browser.setUrl(QUrl('https://www.google.com'))

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith('http'):
            url = 'http://' + url
        self.browser.setUrl(QUrl(url))

    def update_url(self, q):
        self.url_bar.setText(q.toString())

    def open_new_tab(self, i=None):
        new_browser = QWebEngineView()
        new_browser.setUrl(QUrl('https://www.google.com'))
        self.tabs.addTab(new_browser, 'New Tab')
        self.tabs.setCurrentWidget(new_browser)
        new_browser.urlChanged.connect(lambda q, browser=new_browser: self.update_tab_title(q, browser))

    def close_current_tab(self, i):
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)

    def current_tab_changed(self, i):
        q = self.tabs.currentWidget().url()
        self.update_url(q)

    def update_tab_title(self, q, browser):
        index = self.tabs.indexOf(browser)
        self.tabs.setTabText(index, browser.page().title())

    def load_bookmarks(self):
        for bookmark in self.bookmarks:
            bookmark_action = QAction(bookmark, self)
            bookmark_action.triggered.connect(lambda checked, url=bookmark: self.browser.setUrl(QUrl(url)))
            self.bookmarks_bar.addAction(bookmark_action)

    def check_for_updates(self):
        try:
            local_version = self.read_local_version()
            remote_version = self.fetch_remote_version()
            if self.is_newer_version(remote_version, local_version):
                self.update_browser()
        except Exception as e:
            print(f'Fehler bei der Überprüfung auf Updates: {e}')

    def read_local_version(self):
        with open(LOCAL_VERSION_FILE, 'r') as file:
            return file.read().strip()

    def fetch_remote_version(self):
        response = requests.get(REMOTE_VERSION_FILE)
        response.raise_for_status()
        return response.text.strip()

    def is_newer_version(self, remote_version, local_version):
        return remote_version > local_version

    def update_browser(self):
        os.system(f'python {UPDATE_SCRIPT}')

if __name__ == '__main__':
    # Speichern Sie die aktuelle Version in der Version-Datei
    with open(LOCAL_VERSION_FILE, 'w') as file:
        file.write(CURRENT_VERSION)

    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())
