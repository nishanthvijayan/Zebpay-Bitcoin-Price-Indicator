import os
import json
from gi.repository import Gtk, GLib
try: 
       from gi.repository import AppIndicator3 as AppIndicator  
except:  
       from gi.repository import AppIndicator
from urllib2 import urlopen,Request


class BitcoinPriceMonitor:
    def __init__(self):

        self.ind = AppIndicator.Indicator.new(
                            "indicator-btc-india",
                            os.path.dirname(os.path.realpath(__file__)) + "/bitcoin.png",
                            AppIndicator.IndicatorCategory.SYSTEM_SERVICES)


        self.ind.set_status (AppIndicator.IndicatorStatus.ACTIVE)

        self.menu = Gtk.Menu()

        # menu item for quiting the indicator
        item = Gtk.MenuItem()
        item.set_label("Exit                      ")
        item.connect("activate", self.handler_menu_exit )
        item.show()
        self.menu.append(item)

        self.menu.show()
        self.ind.set_menu(self.menu)

        self.handler_timeout()

        # then start updating every 5 minutes
        GLib.timeout_add_seconds(60*5, self.handler_timeout)

    def handler_menu_exit(self, evt):
        Gtk.main_quit()

    def handler_timeout(self):
        # This will be called every minute by the GLib.timeout.
        # Resets the time counter if the user has been idle for too long
        req = Request('https://api.coinsecure.in/v1/exchange/ticker')
        req.add_header('User-agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:37.0) Gecko/20100101 Firefox/37.0')
        try:
            data = json.load(urlopen(req))
            buy_price = int(data['message']['ask'])/100
            sell_price = int(data['message']['bid'])/100
            status_message = "Buy: " + str(buy_price) + "   Sell: " + str(sell_price) 
            self.ind.set_label(status_message, "")
        except Exception, e:
            print str(e)
            self.ind.set_label("!", "")
        return True

    def main(self):
        Gtk.main()

if __name__ == "__main__":
    ind = BitcoinPriceMonitor()
    ind.main()
