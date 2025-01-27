import sys
import pandas as pd
from obspy import UTCDateTime
from datetime import datetime, timedelta
from obspy.clients.fdsn import Client


class CheckingSignal(object):
    def __init__(self):
        self.blank = []
        self.gaps = []
    
    def run(self):
        station = pd.read_csv('/home/sysop/bin/template.txt', delim_whitespace=True, header=None)
        
        client = Client(
            "https://geof.bmkg.go.id",
            user="pgn",
            password="InfoPgn!&#2"
        )

        now = datetime.now()
        t0 = UTCDateTime(now - timedelta(hours=7, minutes=30))
        t1 = UTCDateTime(now - timedelta(hours=7))

        for index, row in station.iterrows():
            print(row[0], row[1], row[2], row[3])
            try:
                if row[2] == "Null":
                    st = client.get_waveforms(row[0], row[1], "", row[3], t0, t1)
                else:
                    st = client.get_waveforms(row[0], row[1], row[2], row[3], t0, t1)
            except:
                self.blank.append(row[1])
                continue

            if st.get_gaps():
                self.gaps.append(row[1])

        txt = f"Update {datetime.now()}\n\n"
        txt += "Blank\n"
        for item in self.blank:
            txt += "%s\n" % item

        txt += "\nGaps\n"
        for item in self.gaps:
            txt += "%s\n" % item

        file = open("/home/sysop/current/www/checklist.txt", "w")
        file.write(txt)
        file.close()

        return True

def main():
    app = CheckingSignal()
    return app.run()

if __name__ == "__main__":
    sys.exit(main())