from django.shortcuts import render,get_object_or_404,redirect
from pathlib import Path
from django.http import HttpResponse
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from .models import CustomUsers,MyGoods
from .forms import *
from django.contrib.auth import authenticate, login as auth_login,get_user_model,update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import logging
from django.views import View
from remind.models import MyGoods
from datetime import datetime,timedelta
# LINE連携
import requests
from django.http import JsonResponse


logger = logging.getLogger("remind") 
# def helloworldfunction(reqest):
#     returnedobject = HttpResponse('<h1>hello world</h1>')
#     return returnedobject

# 2025/2/1 うっちゃん追加　ログイン成功後ルーティング
def index(request):    # ブラウザからアクセスがあった時の処理
    return HttpResponse("Hello, world. You're at the polls index.")

# ログイン機能　2025/2/16 うっちゃん追加 
User = get_user_model()

class CustomAuthenticationForm(AuthenticationForm):
    def clean(self):
        email = self.cleaned_data.get("username")  # フォームの入力を `email` に変更
        password = self.cleaned_data.get("password")

        if email and password:
            try:
                user = User.objects.get(mailaddress=email)
            except User.DoesNotExist:
                self.add_error("username", "このメールアドレスは登録されていません。")
                return
            
            user = authenticate(mailaddress=email, password=password)
            if user is None:
                self.add_error("password", "パスワードが間違っています。")
            else:
                # ユーザーが認証された場合のみ、ログインを進める
                if user.is_active:  # 必要に応じて有効なユーザーか確認
                    auth_login(self.request, user)
                else:
                    self.add_error("username", "このユーザーは無効です。")

        return self.cleaned_data

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    authentication_form = CustomAuthenticationForm

class CustomLogoutView(LogoutView):
    next_page = '/login/'


class MenuView(View):
    def get(self, request):
        user = CustomUsers.objects.get(mailaddress=request.user.mailaddress)
        user_id = user.uuid
        logger.debug(f"{user.uuid}がログインしていますよ")

        # all goodsで取ると他のユーザーのアイテムも取ってしまう 
        # all_goods = MyGoods.objects.all()

        # 2/26 うっちゃん 修正（本当にすみませんでした！）
        # # 次回購入期限順、最近買った順での並び替え
        # sort_symbols = {"sort_next_purchase":["",""],"sort_recent_purchase":["",""]}
        # if request.GET.get("sort") == "sort-next-purchase" or request.GET.get("sort") == "sort-next-purchase-ASC":
        #     user_goods = MyGoods.objects.filter(uid=user_id).order_by('next_purchase_date')
        #     sort_symbols["sort_next_purchase"] = ["-DESC","↑"]
        # elif request.GET.get("sort") == "sort-next-purchase-DESC":
        #     user_goods = MyGoods.objects.filter(uid=user_id).order_by('-next_purchase_date')
        #     sort_symbols["sort_next_purchase"] = ["-ASC","↓"]
        # elif request.GET.get("sort") == "sort-recent-purchase" or request.GET.get("sort") == "sort-recent-purchase-ASC":
        #     user_goods = MyGoods.objects.filter(uid=user_id).order_by('purchase_date')
        #     sort_symbols["sort_recent_purchase"] = ["-DESC","↑"]
        # elif request.GET.get("sort") == "sort-recent-purchase-DESC":
        #     user_goods = MyGoods.objects.filter(uid=user_id).order_by('-purchase_date')
        #     sort_symbols["sort_recent_purchase"] = ["-ASC","↓"]
        # else :
        user_goods = MyGoods.objects.filter(uid=user_id)

        daily_goods = user_goods.filter(category="日用品")  # "日用品"のカテゴリを取得
        food_goods = user_goods.filter(category="食品")  # "食料"のカテゴリを取得
        other_goods = user_goods.filter(category="その他")  # "その他"のカテゴリを取得
        new_regist_item = request.session.pop("new_regist_item", None) # セッションから新規追加アイテム名を取得し、使っていたセッションを削除
        tab_label = request.session.pop("tab_label", None) # セッションから新規追加アイテム名を取得し、使っていたセッションを削除
        logger.debug(f"{daily_goods},{food_goods},{other_goods}")
        return render(request,'menu.html', {'goods_items':user_goods, 
                                            'daily_goods': daily_goods,
                                            'food_goods': food_goods,
                                            'other_goods': other_goods,
                                            'new_regist_item': new_regist_item,
                                            'tab_label' : tab_label})
                                            # 'sort_symbols' : sort_symbols

    def post(self, request):
        # 入力された物品がテーブルに存在するか確認
        new_item = request.POST.get("item_name")
        logger.debug(f"{new_item}")
        find_new_item = MyGoods.objects.filter(goods_name=new_item).first()

        # ユーザー情報を変数に格納する
        user = CustomUsers.objects.get(mailaddress=request.user)
        user_id = user.uuid
        logger.debug(f"{user}")

        # ユーザーIDを取得
        find_uid = CustomUsers.objects.filter(uuid=user_id).first()
        logger.debug(f"{find_uid}")

        # 物品が入力されたか確認
        if not new_item:
            error_message = f"物品名を入力してください。"
            user_goods = MyGoods.objects.filter(uid=find_uid.uuid)
            daily_goods = user_goods.filter(category="日用品")
            food_goods = user_goods.filter(category="食料")
            other_goods = user_goods.filter(category="その他")
            return render(request, 'menu.html', {
                'goods_items': user_goods,
                'daily_goods': daily_goods,
                'food_goods': food_goods,
                'other_goods': other_goods,
                'error_message': error_message  # エラーメッセージを渡す
            })

        # MyGoodsに登録されている場合エラー
        if find_new_item:
            error_message = f"{find_new_item}はすでに管理物品一覧に存在します。値の更新を行ってください。"

            # all goodsで取ると他のユーザーのアイテムも取ってしまう 
            # all_goods = MyGoods.objects.all()
            user_goods = MyGoods.objects.filter(uid=find_uid.uuid)

            daily_goods = user_goods.filter(category="日用品")
            food_goods = user_goods.filter(category="食料")
            other_goods = user_goods.filter(category="その他")
            return render(request, 'menu.html', {
                'goods_items': user_goods,
                'daily_goods': daily_goods,
                'food_goods': food_goods,
                'other_goods': other_goods,
                'error_message': error_message  # エラーメッセージを渡す
            })

        else:
            # カテゴリを取得する
            find_origin_item = RegistGoods.objects.filter(name=new_item).first()

            if find_origin_item is None:
                error_message = f"{new_item}はデフォルト物品に存在しません。新規物品登録を行ってください。"

                # all goodsで取ると他のユーザーのアイテムも取ってしまう 
                # all_goods = MyGoods.objects.all()
                user_goods = MyGoods.objects.filter(uid=find_uid.uuid)

                daily_goods = user_goods.filter(category="日用品")
                food_goods = user_goods.filter(category="食料")
                other_goods = user_goods.filter(category="その他")
                return render(request, 'menu.html', {
                    'goods_items': user_goods,
                    'daily_goods': daily_goods,
                    'food_goods': food_goods,
                    'other_goods': other_goods,
                    'error_message': error_message  # エラーメッセージを渡す
                })
            else:
                next_purchase_date = int(find_origin_item.default_term)*7
                
                # 新しい物品をデータベースに保存
                new_item = MyGoods(uid=find_uid,
                                goods_id=find_origin_item.id,                  
                                goods_name=new_item,
                                category=find_origin_item.get_category_display(),
                                purchase_date=datetime.today(),
                                next_purchase_date=datetime.today()+timedelta(days=int(find_origin_item.default_term)*7),
                                next_purchase_term=find_origin_item.default_term,
                                first_term=find_origin_item.default_term
                                )
                new_item.save()
                # 成功したらメニュー画面へ
                return redirect('remind:menu')

# return redirect("remind:menu")  # リダイレクトして再表示

# 買ったボタン押下
class BoughtItem(View):
    template_name = 'menu.html'

    def post(self,request):
        item_id = request.POST.get('item_id')
        find_item = get_object_or_404(MyGoods, id=item_id)
        find_item.purchase_date = datetime.today()
        find_item.expire_date = None
        find_item.save()
        request.session['tab_label'] = request.POST.get('tab_label')  # セッションに保存
        return redirect('remind:menu')

# 延長ボタン押下
class ExtendItem(View):
    template_name = 'menu.html'

    def post(self,request):
        item_id = request.POST.get('item_id')
        find_item = get_object_or_404(MyGoods, id=item_id)
        find_item_term = find_item.next_purchase_term
        find_item.next_purchase_date = find_item.next_purchase_date+timedelta(find_item_term*7)
        logger.debug(f"{find_item.next_purchase_date}")  
        find_item.save()
        request.session['tab_label'] = request.POST.get('tab_label')  # セッションに保存
        return redirect('remind:menu')
    
# 新規物品登録　2025/2/16 うっちゃん追加
class MyitemsAdd(View):
    template_name = 'new-item-add.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        logger.debug(f"通ったよ")  

        item_name = request.POST.get('item_name')
        item_default_term = request.POST.get('default_term',4)
        # item_default_term = int(item_default_term) 
        item_category = request.POST.get("category")
        logger.debug(f"{item_name},{item_default_term},{item_category}")  

        if " " in item_name or "　" in item_name:  # スペースを含む場合はエラー
            logger.debug(f"Error: item_name contains spaces")
            context = {'error_message': '商品を入力してください。'}
            return render(request, self.template_name, context)
                
        # 入力された物品がテーブルに存在するか確認
        item = RegistGoods.objects.filter(name=item_name).first()

        if item:
            context = {'error_message': '商品がすでに存在しています。'}
            return render(request, self.template_name, context)
        
        else:
            logger.debug(f"{item_name},{item_default_term},{item_category}")  

            # 新しい物品をデータベースに保存
            new_item = RegistGoods(name=item_name,
                                    default_term=item_default_term,
                                    category=item_category)
            new_item.save()
            # 成功したらメニュー画面へ
            # return render(request,'menu.html', {'new_regist_items':new_item})   
            request.session['new_regist_item'] = item_name  # セッションに保存
            return redirect('remind:menu')


# 設定画面　2025/2/16 うっちゃん追加
@login_required
def settings_page(request):
    user = CustomUsers.objects.get(mailaddress=request.user.mailaddress)
    before_mailaddress = user.mailaddress  # 現在のメールアドレス
    logger.debug(f"before_mailaddress: {before_mailaddress}")
    return render(request, 'setting.html', {'before_mailaddress': before_mailaddress})

# 次回購入までの期間の一括設定
@login_required
def update_default_term(request):
     #return HttpResponse(f"Logged in user: {request.user.mailaddress}")
    user = request.user # 現在ログインしているユーザーを取得

    #user_goods = MyGoods.objects.filter(uid=request.user)

    if request.method == 'POST':
        defaultform = DefaultTermForm(request.POST, instance=user)
        if defaultform.is_valid():
            default_term = defaultform.cleaned_data['default_term']
            defaultform.save()

            #user_goods.update(next_purchase_term=default_term)

            MyGoods.objects.filter(uid=request.user).update(next_purchase_term=default_term)

            return redirect('remind:menu')

    return redirect('remind:settings')

# 期間の初期化
def reset_default_term(request):    
    if request.method == 'POST':
        default_term = request.POST.get('default_term')
        if default_term == '0':
            logger.debug("期間を初期化しました。")
            user = CustomUsers.objects.get(mailaddress=request.user.mailaddress)
            user_id = user.uuid
            logger.debug(f"{user_id}はこれだよ")
            # usersの期間を更新する
            CustomUsers.objects.filter(uuid=user_id).update(default_term=0)

            # 自分で登録した物品の期間を更新する
            goods_list = MyGoods.objects.filter(uid=user_id)
            for goods in goods_list:
                new_first_term = goods.first_term
                goods.next_purchase_term = new_first_term
                goods.save()
        return redirect('remind:settings')

# メールアドレス・パスワードの変更
@login_required
def change_personal_info(request):
    if request.method == 'POST':
     if request.method == 'POST':
        new_email = request.POST.get('email')
        new_password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        try:
            user = CustomUsers.objects.get(mailaddress=request.user.mailaddress)

            # フラグを用意（どちらも変更しない場合に備える）
            email_updated = False
            password_updated = False

            # メールアドレスの変更処理
            if new_email and new_email != user.mailaddress:
                user.mailaddress = new_email
                email_updated = True

            # パスワードの変更処理
            if new_password:
                if new_password == confirm_password:
                    user.set_password(new_password)
                    password_updated = True
                else:
                    logger.error("パスワードが一致しません")
                    messages.error(request, f"パスワードが一致しません")
                    return redirect('remind:change_personal_info')

            # 変更があった場合のみ保存
            if email_updated or password_updated:
                user.save()

                if password_updated:
                    # セッションの認証情報を更新（ログアウトされないように）
                    update_session_auth_hash(request, user)

                logger.debug(f"ユーザー情報を更新しました: {new_email if email_updated else 'メール変更なし'}")
                messages.error(request, f"アカウント情報を更新しました")

            return redirect('remind:settings')

        except CustomUsers.DoesNotExist:
            logger.error("ユーザーが見つかりませんでした")
            messages.error(request, f"ユーザー情報の取得に失敗しました")
            return redirect('remind:settings')

    return redirect('remind:settings')

# お問い合わせ
def Inquiry(request):
    return render(request,'inquiry.html')

# モーダル編集    
def editmodal(request):
    if request.method == 'POST':
        goods_id = request.POST.get('goods_id')
        goods_instance = get_object_or_404(MyGoods, id=goods_id, uid=request.user)

        form = ModalForm(request.POST, instance=goods_instance)
        if form.is_valid():
            goods = form.save(commit=False)

            new_purchase_date = form.cleaned_data['purchase_date']
            new_next_purchase_term = form.cleaned_data['next_purchase_term']

            goods.next_purchase_date = new_purchase_date + timedelta(weeks=new_next_purchase_term)

            goods.save()
            return redirect('remind:menu')

    return redirect('remind:menu')


# サインアップ　2025/2/13 MANA追記
class UserCreateView(CreateView):
    model = CustomUsers
    form_class = CustomUsersCreationForm
    template_name = 'registration/signup.html'
    success_url = reverse_lazy('remind:login')
    

class HelloWorldClass(TemplateView):
    template_name = 'base.html'

# LINE連携
def send_line_notify(request):
    LINE_NOTIFY_TOKEN = "YOUR_ACCESS_TOKEN"
    message = "Djangoからの通知です！"
    
    url = "https://notify-api.line.me/api/notify"
    headers = {"Authorization": f"Bearer {LINE_NOTIFY_TOKEN}"}
    data = {"message": message}

    response = requests.post(url, headers=headers, data=data)
    
    if response.status_code == 200:
        return JsonResponse({"status": "success", "message": "通知を送信しました"})
    else:
        return JsonResponse({"status": "error", "message": response.text})