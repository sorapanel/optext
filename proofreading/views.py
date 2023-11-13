from django.shortcuts import render
import urllib.request
import urllib.parse
import json
import requests
import environ

env = environ.Env()
environ.Env.read_env('.env')

# Create your views here.
def proofMain(request):
    #A3RTのAPI取得
    API='https://api.a3rt.recruit.co.jp/proofreading/v2/typo'
    KEY=env('PROOF_KEY')

    #status:初期は0、正常値は1,異常値は2
    #input:入力データ, check:出力データ
    #suggests:正解候補を格納した配列
    status = 0
    input = ''
    check = ''
    suggests = []

    #POST時
    if request.method == 'POST':
        #formからの値取得
        prevtext = request.POST.get('prevtext', None)
        if prevtext is not None:
            values = {
            'apikey': KEY,
            'sentence':prevtext,
            'sensitivity':"medium",
            }
            #パラメータの暗号化
            params = urllib.parse.urlencode(values)
            #リクエストURL作成
            url = API + "?" + params
            #リクエスト結果取得
            r = requests.get(url)
            #rを辞書型へ
            data = json.loads(r.text)

            if data['status'] == 0: #stutas: 0検索なし, 1正常, 2異常
                status = 1
            else:
                status = 2

            print(data['status'])

            try:#正解候補の配列作成
                for alert in data['alerts']:
                    str = alert['word'] + '→' + alert['suggestions'][0] + 'または' + alert['suggestions'][1] + 'または' + alert['suggestions'][2]
                    suggests.append(str)

                print('alerts')
                input = data['inputSentence']
                check = data['checkedSentence']

            except:
                print('異常なし')

        else:
            print('prevtext is None')

    #コンテキスト
    context = {
        'status':status,
        'input':input,
        'check':check,
        'suggests':suggests,
    }

    return render(request, 'proofreading/proof_main.html', context)