from django.shortcuts import render
import urllib.request
import urllib.parse
import json
import requests
import environ

env = environ.Env()
environ.Env.read_env('.env')

# Create your views here.
def summaryMain(request):
    #A3RTのAPI取得
    API='https://api.a3rt.recruit.co.jp/text_summarization/v1'
    KEY=env('SUMMARY_KEY')

    #status:初期は0、正常値は1,異常値は2
    #input:入力データ, output:出力データ
    status = 0
    input = ''
    output = []

    #POST時
    if request.method == 'POST':
        #formからの値取得
        prevtext = request.POST.get('prevtext', None)
        #letter_count:要約する文字数によって指定するlinenumberの数を変えるための変数
        letter_count = request.POST.get('count', None)
        if prevtext is not None:
            if letter_count is not None:
                if letter_count == "200":
                    linenumber = 1
                elif letter_count == "400":
                    linenumber = 2
                elif letter_count == "600":
                    linenumber = 3
                elif letter_count == "800":
                    linenumber = 4
                else:
                    linenumber = 1

                values = {
                'apikey': KEY,
                'sentences':prevtext,
                'linenumber':linenumber,
                }
                # #パラメータの暗号化
                params = urllib.parse.urlencode(values)
                # #リクエスト結果取得
                r = requests.post(API, data=params)
                #rを辞書型へ
                data = json.loads(r.text)

                print(data['status'])

                #data['status']: 0:ok, 1000~1500:異常終了
                if data['status'] == 0:
                    status = 1
                    input = prevtext
                    i=0
                    while i < linenumber:
                        output.append(data['summary'][i]) 
                        i += 1
                else:
                    status = 2
                    input = prevtext
                    output.append('要約できませんでした。要約したい文章の長さが元文章よりも長い場合は要約できません。')
            else:
                print('letter_count is None')
            
        else:
            print('prevtext is None')

    print(output)

    for a in output:
        print(a)

    #コンテキスト
    context = {
        'status':status,
        'input':input,
        'output':output,
    }

    return render(request, 'summarization/summary_main.html', context)