from django.shortcuts import render
import requests
from django.http import JsonResponse
from datetime import datetime
import random


def index(request):
    return render(request, "uncommon/index.html",{
    })

def searchflight(request):

    display = False

    if request.method == "POST":

        display = True

        user_input = request.POST.get('location-input')
        dateFrom_unformatted = request.POST.get('start_date')
        dateTo_unformatted = request.POST.get('end_date')
        budget = int(request.POST.get('budget'))
        budget_depart = int(budget)
        
        dateFrom_step = datetime.strptime(dateFrom_unformatted, "%Y-%m-%d")
        dateFrom = dateFrom_step.strftime("%d/%m/%Y")

        dateTo_step = datetime.strptime(dateTo_unformatted, "%Y-%m-%d")
        dateTo = dateTo_step.strftime("%d/%m/%Y")

        url = f'https://api.tequila.kiwi.com/v2/search?fly_from={user_input}&dateFrom={dateFrom}&dateTo={dateFrom}&price_to={budget_depart}&limit=100000'

        headers = {"apikey": "gGgmMRbcNFUZRWqo9Akg8HKtKgT5hmUJ"}

        response = requests.get(url, headers=headers)

        data = response.json()

        no_go = [
            "ATL", "PEK", "DXB", "LAX", "HND", "ORD", "LHR", "HKG", "PVG", "CDG",
            "DFW", "CGK", "CAN", "JFK", "AMS", "SIN", "ICN", "DEL", "FRA", "IST",
            "CGH", "BKK", "DEN", "SFO", "KUL", "MAD", "BCN", "LAS", "SEA", "CTU",
            "MEX", "YYZ", "SZX", "PHX", "SYD", "MUC", "MCO", "CLT", "PTY", "IAH",
            "YYC", "BOM", "FCO", "GRU", "MNL", "BNE", "PHL", "ZRH", "EWR", "MSP",
            "YUL", "GMP", "GIG", "AKL", "SLC", "CAI", "LGW", "NRT", "BRU", "DUB",
            "FLL", "PMI", "KMG", "DUS", "BWI", "SHA", "RUH", "CPH", "OTP", "MAN",
            "CUN", "SVO", "CSX", "HGH", "HAM", "NCE", "ATH", "IST", "TUN", "STR",
            "SAW", "MCT", "HAN", "OSL", "CMH", "PMO", "DOH", "CTA", "BHX", "MAA",
            "KIX", "VIE", "SSA", "VCP", "DAL", "ABJ", "MRS", "BLR", "GDL", "TLV",
            "BEG", "KWI", "JED", "BOD", "GVA", "LIS", "BNA", "NCE", "YVR", "MCI",
            "MEL", "LED", "BAH", "TLN", "NUE", "JNB", "KGL", "TPE", "GIG", "KBP",
            "KWI", "DPS", "MAN", "ARN", "KUL", "SIN", "MEX", "KRR", "GDL", "SJC",
            "SAL", "FUK", "IST", "MGA", "SXF", "LIM", "KIX", "INV", "NBO", "KEF",
            "CEB", "AUS", "GDL", "SNA", "SKG", "AMS", "OSA", "GVA", "MUC", "BUD",
            "CNS", "SVQ", "MYR", "KBP", "LIS", "HKT", "CUN", "OPO", "LCY", "JED",
            "BGI", "BUD", "ROB", "TRS", "GLA", "LFT", "TRN", "MCO", "INN", "NAP",
            "LOS", "COK", "SAW", "GOT", "EBB", "CNF", "TLS", "JAX", "VCP", "PVG",
            "SGN", "BHD", "HAJ", "SJJ", "DAC", "SKP", "MUC", "LYS", "EBL", "SDJ",
            "TFS", "STR", "PSA", "CTA", "JED", "NOU", "TFS", "BTV", "BVA", "CAI",
            "NTE", "LFT", "AAE", "TSN", "PRG", "POS", "UIO", "HNA", "CAG", "LWO",
            "SCL", "EVN", "GYD", "LCG", "MRS", "CMN", "LIS", "CMH", "ZAZ", "PRG",
            "MED", "MRU", "KUL", "GRR", "ALG", "KSD", "GZT", "POA", "NCE", "LPI",
            "YUL", "PMI", "MID", "DPS", "FAT", "BRI", "LPA", "JUB", "BCN", "CWL",
            "GOA", "VVI", "KLU", "UFA", "CUN", "HRE", "MAD", "MAH", "ORH", "WAS",
            "TLL", "TFS", "AZO", "RDM", "FUE", "MAN", "FKB", "MLA", "LPA", "DUR",
            "JRO", "BRE", "STR", "SCQ", "AGP", "JAX", "SOF", "NNG", "AJA", "LNZ",
            "BUD", "KEF", "TXL", "BKK", "LAS", "MRS", "TTN", "LUX", "KUF", "TXL",
            "DLM", "FMO", "EBB", "GOJ", "AOI", "PIA", "CJU", "MIA", "VVI", "KIV",
            "GOT", "KJA", "BRN", "GVA", "AYT", "YYZ", "ACE", "LAN", "NWI", "PIK"
        ]

        def find():
            possible = []
            output_data = {}
            for i in data['data']:
                if i['route'][0]['cityCodeTo'] not in no_go:
                    possible.append(i['route'][0]['id'])
            
            list_length = len(possible)
            rd_num = random.randint(0, list_length-1)
            user_destination = possible[rd_num]

            for i in data['data']:
                if i['route'][0]['id'] == user_destination:
                    output_data = i 
            return output_data


        try:
            find()
        except ValueError:
            return render(request, "uncommon/index.html",{
            "error": "Try Tweaking your query a little :)"
        })


        booking_first = find()
        booking_token = booking_first['deep_link']
        cityTo_data = booking_first['cityTo']
        price_data = booking_first['price']

        return render(request, "uncommon/index.html",{
            "booking_token": booking_token,
            "cityTo": cityTo_data,
            "price_data": price_data,
            "display": display
        })

    return render(request, "uncommon/index.html")