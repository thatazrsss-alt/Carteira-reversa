#!/usr/bin/env python3
"""Serve a Carteira Reversa v18 locally. Python 3, no pip dependencies."""
import argparse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from functools import partial
import webbrowser

ROOT=Path(__file__).resolve().parent
HTML=ROOT/"Carteira_Reversa_Gerencial_v18_Producao_Data_FillRate.html"
def main():
    a=argparse.ArgumentParser(description="Carteira Reversa v18")
    a.add_argument("--port",type=int,default=0)
    a.add_argument("--no-browser",action="store_true")
    a.add_argument("--check",action="store_true")
    opt=a.parse_args()
    if not HTML.exists():
        raise SystemExit("Arquivo HTML ausente. Baixe o HTML na mesma pasta deste script.")
    if opt.check:
        assert "function convertOrderBalances()" in HTML.read_text(encoding="utf-8")
        print("OK: Carteira Reversa v18.")
        return
    handler=partial(SimpleHTTPRequestHandler,directory=str(ROOT))
    with ThreadingHTTPServer(("127.0.0.1",opt.port),handler) as server:
        url=f"http://127.0.0.1:{server.server_port}/{HTML.name}"
        print("Carteira Reversa v18: "+url+"\nCtrl+C para encerrar.")
        if not opt.no_browser:webbrowser.open(url)
        try:server.serve_forever()
        except KeyboardInterrupt:pass
if __name__=="__main__":main()
