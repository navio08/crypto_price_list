import os
import sys

import pytest

from data.response import response

CURRENT_FOLDER = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(CURRENT_FOLDER, ".."))

from aggregator import aggregate  # noqa: E402


class TestAggregate:
    def test_aggregate_noFormatgiven(self):
        result = aggregate(
            response, "041b19fc72b54e3ca142edb666d00807", "6077b1382ad84783a3f205b6f647239d"
        )
        assert (
            result
            == '{"columns":["crypto","prices","rank"],"data":[["BTC",29166.0953591331,1.0],["ETH",1861.9882005559,2.0],["USDT",0.9996858298,3.0],["XRP",0.7133587879,4.0],["BNB",239.9067212408,5.0],["USDC",0.9999038419,6.0],["DOGE",0.077384616,8.0],["ADA",0.3062827482,9.0],["SOL",24.8655444645,10.0],["TRX",0.0822459683,11.0],["MATIC",0.7149187231,12.0],["LTC",90.0757071196,13.0],["DOT",5.1997919515,14.0],["WBTC",29176.4950836844,16.0],["BCH",242.230818049,15.0],["SHIB",0.0000077601,18.0],["DAI",0.9989147194,20.0],["AVAX",13.0858307742,19.0],["TON",1.3165723234,17.0],["XLM",0.1581460742,22.0],["LINK",7.9229698211,23.0],["BUSD",0.999756123,24.0],["LEO",3.9886344426,25.0],["UNI",5.8164721562,21.0],["ATOM",8.8806504444,27.0],["XMR",161.516190322,28.0],["TUSD",0.9989244443,26.0],["OKB",42.9110694148,30.0],["ETC",18.0832748527,29.0],["FIL",4.3287825924,31.0],["ICP",4.0688818511,32.0],["MNT",0.5277571237,33.0],["HBAR",0.0517564793,35.0],["LDO",1.9075231243,34.0],["APT",6.9517069758,37.0],["ARB",1.1751338672,38.0],["CRO",0.0587599535,36.0],["VET",0.0184023401,41.0],["NEAR",1.3535811186,42.0],["QNT",101.488124019,39.0],["MKR",1163.6280250864,44.0],["AAVE",71.947735466,45.0],["OP",1.496944404,46.0],["GRT",0.1106556589,47.0],["ALGO",0.1096213683,51.0],["XDC",0.0610361502,52.0],["AXS",5.9962512392,59.0],["EGLD",32.2694519084,54.0],["STX",0.5941812748,53.0],["SAND",0.4220519438,57.0],["EOS",0.7353304214,56.0],["THETA",0.7893629096,58.0],["IMX",0.7256391273,60.0],["SNX",2.8585482135,50.0],["XTZ",0.8030820602,62.0],["APE",1.9936089503,64.0],["USDD",0.998019931,61.0],["MANA",0.3826548806,65.0],["FTM",0.2415042283,67.0],["BSV",34.8677064763,66.0],["RNDR",1.7563074553,68.0],["INJ",7.974859085,69.0],["CRV",0.7256465339,71.0],["NEO",8.6522740906,72.0],["FLOW",0.5783004197,73.0],["RPL",29.9074529855,75.0],["KAVA",0.8879365552,76.0],["XEC",0.000029514,78.0],["KCS",5.8537051262,80.0],["USDP",0.9942382285,43.0],["CHZ",0.0766607342,83.0],["COMP",69.913904892,89.0],["CFX",0.1709081257,87.0],["PEPE",0.0000013323,82.0],["GALA",0.0232193557,77.0],["KLAY",0.1607657426,85.0],["GMX",55.5138004636,86.0],["ZEC",29.7590330528,null],["PAXG",1940.0532905714,84.0],["XAUT",1948.5982550238,91.0],["MIOTA",0.1723733581,null],["LUNC",0.0000805381,88.0],["BTT",0.0000004728,94.0],["FXS",6.0509528041,93.0],["HT",2.6763888905,96.0],["CSPR",0.0381258583,97.0],["GT",4.2345160916,74.0],["MINA",0.4381494749,98.0],["SUI",0.6267169039,null],["TWT",0.8991988056,100.0],["AR",5.5989823237,null],["NEXO",0.6412554156,null],["DASH",31.4476106869,null],["GUSD",0.9775535187,79.0],["WOO",0.1995440013,null],["ZIL",0.0205881439,null],["DYDX",2.0354052117,null],["CAKE",1.4885364208,null],["RUNE",0.9267860385,null],["1INCH",0.302936677,null],["STETH",null,7.0],["BIT",null,40.0],["FRAX",null,48.0],["RETH",null,49.0],["WBT",null,55.0],["KAS",null,63.0],["BGB",null,70.0],["XRD",null,81.0],["IOTA",null,90.0],["SPA",null,92.0],["FRXETH",null,95.0],["FLEX",null,99.0]]}'
        )

    def test_aggregate_jsonFormatgiven(self):
        result = aggregate(
            response,
            "041b19fc72b54e3ca142edb666d00807",
            "6077b1382ad84783a3f205b6f647239d",
            "json",
        )
        assert (
            result
            == '{"columns":["crypto","prices","rank"],"data":[["BTC",29166.0953591331,1.0],["ETH",1861.9882005559,2.0],["USDT",0.9996858298,3.0],["XRP",0.7133587879,4.0],["BNB",239.9067212408,5.0],["USDC",0.9999038419,6.0],["DOGE",0.077384616,8.0],["ADA",0.3062827482,9.0],["SOL",24.8655444645,10.0],["TRX",0.0822459683,11.0],["MATIC",0.7149187231,12.0],["LTC",90.0757071196,13.0],["DOT",5.1997919515,14.0],["WBTC",29176.4950836844,16.0],["BCH",242.230818049,15.0],["SHIB",0.0000077601,18.0],["DAI",0.9989147194,20.0],["AVAX",13.0858307742,19.0],["TON",1.3165723234,17.0],["XLM",0.1581460742,22.0],["LINK",7.9229698211,23.0],["BUSD",0.999756123,24.0],["LEO",3.9886344426,25.0],["UNI",5.8164721562,21.0],["ATOM",8.8806504444,27.0],["XMR",161.516190322,28.0],["TUSD",0.9989244443,26.0],["OKB",42.9110694148,30.0],["ETC",18.0832748527,29.0],["FIL",4.3287825924,31.0],["ICP",4.0688818511,32.0],["MNT",0.5277571237,33.0],["HBAR",0.0517564793,35.0],["LDO",1.9075231243,34.0],["APT",6.9517069758,37.0],["ARB",1.1751338672,38.0],["CRO",0.0587599535,36.0],["VET",0.0184023401,41.0],["NEAR",1.3535811186,42.0],["QNT",101.488124019,39.0],["MKR",1163.6280250864,44.0],["AAVE",71.947735466,45.0],["OP",1.496944404,46.0],["GRT",0.1106556589,47.0],["ALGO",0.1096213683,51.0],["XDC",0.0610361502,52.0],["AXS",5.9962512392,59.0],["EGLD",32.2694519084,54.0],["STX",0.5941812748,53.0],["SAND",0.4220519438,57.0],["EOS",0.7353304214,56.0],["THETA",0.7893629096,58.0],["IMX",0.7256391273,60.0],["SNX",2.8585482135,50.0],["XTZ",0.8030820602,62.0],["APE",1.9936089503,64.0],["USDD",0.998019931,61.0],["MANA",0.3826548806,65.0],["FTM",0.2415042283,67.0],["BSV",34.8677064763,66.0],["RNDR",1.7563074553,68.0],["INJ",7.974859085,69.0],["CRV",0.7256465339,71.0],["NEO",8.6522740906,72.0],["FLOW",0.5783004197,73.0],["RPL",29.9074529855,75.0],["KAVA",0.8879365552,76.0],["XEC",0.000029514,78.0],["KCS",5.8537051262,80.0],["USDP",0.9942382285,43.0],["CHZ",0.0766607342,83.0],["COMP",69.913904892,89.0],["CFX",0.1709081257,87.0],["PEPE",0.0000013323,82.0],["GALA",0.0232193557,77.0],["KLAY",0.1607657426,85.0],["GMX",55.5138004636,86.0],["ZEC",29.7590330528,null],["PAXG",1940.0532905714,84.0],["XAUT",1948.5982550238,91.0],["MIOTA",0.1723733581,null],["LUNC",0.0000805381,88.0],["BTT",0.0000004728,94.0],["FXS",6.0509528041,93.0],["HT",2.6763888905,96.0],["CSPR",0.0381258583,97.0],["GT",4.2345160916,74.0],["MINA",0.4381494749,98.0],["SUI",0.6267169039,null],["TWT",0.8991988056,100.0],["AR",5.5989823237,null],["NEXO",0.6412554156,null],["DASH",31.4476106869,null],["GUSD",0.9775535187,79.0],["WOO",0.1995440013,null],["ZIL",0.0205881439,null],["DYDX",2.0354052117,null],["CAKE",1.4885364208,null],["RUNE",0.9267860385,null],["1INCH",0.302936677,null],["STETH",null,7.0],["BIT",null,40.0],["FRAX",null,48.0],["RETH",null,49.0],["WBT",null,55.0],["KAS",null,63.0],["BGB",null,70.0],["XRD",null,81.0],["IOTA",null,90.0],["SPA",null,92.0],["FRXETH",null,95.0],["FLEX",null,99.0]]}'
        )

    def test_aggregate_csvFormatgiven(self):
        result = aggregate(
            response, "041b19fc72b54e3ca142edb666d00807", "6077b1382ad84783a3f205b6f647239d", "csv"
        )
        assert (
            result
            == "crypto,prices,rank\nBTC,29166.095359133065,1.0\nETH,1861.9882005559157,2.0\nUSDT,0.9996858298096042,3.0\nXRP,0.7133587879270377,4.0\nBNB,239.90672124078282,5.0\nUSDC,0.9999038418869547,6.0\nDOGE,0.07738461598326471,8.0\nADA,0.3062827481665035,9.0\nSOL,24.865544464543575,10.0\nTRX,0.08224596829479353,11.0\nMATIC,0.7149187231492828,12.0\nLTC,90.0757071196006,13.0\nDOT,5.199791951483896,14.0\nWBTC,29176.495083684375,16.0\nBCH,242.2308180490328,15.0\nSHIB,7.760142274564844e-06,18.0\nDAI,0.9989147193936121,20.0\nAVAX,13.08583077415222,19.0\nTON,1.3165723233966404,17.0\nXLM,0.15814607423035565,22.0\nLINK,7.922969821074524,23.0\nBUSD,0.9997561229551233,24.0\nLEO,3.988634442587706,25.0\nUNI,5.816472156189671,21.0\nATOM,8.880650444398565,27.0\nXMR,161.5161903219573,28.0\nTUSD,0.9989244442716319,26.0\nOKB,42.91106941484826,30.0\nETC,18.08327485269589,29.0\nFIL,4.328782592377962,31.0\nICP,4.068881851067634,32.0\nMNT,0.5277571236748989,33.0\nHBAR,0.05175647925709867,35.0\nLDO,1.9075231243375552,34.0\nAPT,6.951706975829222,37.0\nARB,1.1751338671612086,38.0\nCRO,0.058759953465994975,36.0\nVET,0.018402340093960152,41.0\nNEAR,1.3535811186423103,42.0\nQNT,101.48812401902406,39.0\nMKR,1163.6280250864486,44.0\nAAVE,71.94773546596902,45.0\nOP,1.4969444040310773,46.0\nGRT,0.11065565892625846,47.0\nALGO,0.10962136827178036,51.0\nXDC,0.061036150153936,52.0\nAXS,5.996251239187839,59.0\nEGLD,32.26945190839988,54.0\nSTX,0.5941812748295195,53.0\nSAND,0.4220519437725733,57.0\nEOS,0.7353304214069482,56.0\nTHETA,0.7893629096326653,58.0\nIMX,0.7256391272506485,60.0\nSNX,2.858548213513626,50.0\nXTZ,0.803082060206176,62.0\nAPE,1.9936089503208128,64.0\nUSDD,0.9980199310225882,61.0\nMANA,0.3826548806195512,65.0\nFTM,0.2415042282546504,67.0\nBSV,34.86770647629037,66.0\nRNDR,1.7563074553217595,68.0\nINJ,7.974859084956745,69.0\nCRV,0.7256465339396626,71.0\nNEO,8.65227409056827,72.0\nFLOW,0.5783004196580793,73.0\nRPL,29.907452985533062,75.0\nKAVA,0.8879365551580658,76.0\nXEC,2.9513976415545846e-05,78.0\nKCS,5.853705126248594,80.0\nUSDP,0.994238228486914,43.0\nCHZ,0.07666073421972316,83.0\nCOMP,69.91390489195607,89.0\nCFX,0.1709081257305117,87.0\nPEPE,1.332297302685621e-06,82.0\nGALA,0.023219355716394774,77.0\nKLAY,0.16076574255638518,85.0\nGMX,55.51380046362859,86.0\nZEC,29.7590330527887,\nPAXG,1940.0532905714188,84.0\nXAUT,1948.5982550237584,91.0\nMIOTA,0.17237335808375231,\nLUNC,8.053807500627499e-05,88.0\nBTT,4.7278433517986435e-07,94.0\nFXS,6.050952804124752,93.0\nHT,2.6763888905306104,96.0\nCSPR,0.03812585825526857,97.0\nGT,4.234516091630688,74.0\nMINA,0.4381494749165184,98.0\nSUI,0.6267169039009561,\nTWT,0.8991988055698741,100.0\nAR,5.598982323710338,\nNEXO,0.6412554156148605,\nDASH,31.447610686891558,\nGUSD,0.9775535186774271,79.0\nWOO,0.19954400126710603,\nZIL,0.020588143937551446,\nDYDX,2.03540521167746,\nCAKE,1.4885364207512732,\nRUNE,0.9267860385215537,\n1INCH,0.30293667704510197,\nSTETH,,7.0\nBIT,,40.0\nFRAX,,48.0\nRETH,,49.0\nWBT,,55.0\nKAS,,63.0\nBGB,,70.0\nXRD,,81.0\nIOTA,,90.0\nSPA,,92.0\nFRXETH,,95.0\nFLEX,,99.0\n"
        )

    def test_aggregate_wrongFormatgiven(self):
        with pytest.raises(AssertionError) as error:
            aggregate(
                response,
                "041b19fc72b54e3ca142edb666d00807",
                "6077b1382ad84783a3f205b6f647239d",
                "xml",
            )
        assert str(error.value) == "Wrong Format xml"