import gi
gi.require_version('Gtk', '4.0')
gi.require_version('WebKit', '6.0')
from gi.repository import Gtk, Gdk, WebKit


class Browser(Gtk.ApplicationWindow):
    def __init__(self, app):
        super(Browser, self).__init__(application=app)
        self.set_title('BudgetButlerWeb')
        self.maximize()
        self.webview = WebKit.WebView()

        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_child(self.webview)
        
        self.webview.load_uri("file:///home/sebastian/git/BudgetButlerWeb/butler_offline_boot_screen/loading/loading.html")

        self.set_child(scrolled_window)


def on_activate(app):
    browser = Browser(app)
    browser.present()


if __name__ == "__main__":
    app = Gtk.Application()
    app.connect('activate', on_activate)
    app.run(None)
    
    
