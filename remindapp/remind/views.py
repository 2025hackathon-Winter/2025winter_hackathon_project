from django.shortcuts import render,get_object_or_404,redirect
from pathlib import Path
from django.http import HttpResponse
from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from .models import CustomUsers,MyGoods
from .forms import *
from django.contrib.auth import authenticate, login as auth_login,get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
import logging
from django.views import View
from remind.models import MyGoods
from datetime import datetime,timedelta


logger = logging.getLogger(__name__)
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
        logger.debug(f"{user.uuid}")

        all_goods = MyGoods.objects.all()
        user_goods = MyGoods.objects.filter(uid=user_id)

        daily_goods = user_goods.filter(category="日用品")  # "日用品"のカテゴリを取得
        food_goods = user_goods.filter(category="食品")  # "食料"のカテゴリを取得
        other_goods = user_goods.filter(category="その他")  # "その他"のカテゴリを取得
        logger.debug(f"{daily_goods},{food_goods},{other_goods}")
        return render(request,'menu.html', {'goods_items':all_goods, 'daily_goods': daily_goods,'food_goods': food_goods,'other_goods': other_goods})

    def post(self, request):
        # ユーザー情報を変数に格納する
        user = CustomUsers.objects.get(mailaddress=request.user)
        user_id = user.uuid
        logger.debug(f"{user}")

        # ユーザーIDを取得
        find_uid = CustomUsers.objects.filter(uuid=user_id).first()
        logger.debug(f"{find_uid}")

        new_item = request.POST.get("regist_item")
        logger.debug(f"{new_item}")  

        # 入力された物品がテーブルに存在するか確認
        find_new_item = MyGoods.objects.filter(goods_name=new_item).first()

        if find_new_item:
            error_message = f"{find_new_item}はすでに管理物品一覧に存在します。値の更新を行ってください。"

            all_goods = MyGoods.objects.all()
            user_goods = MyGoods.objects.filter(uid=find_uid.uuid)

            daily_goods = user_goods.filter(category="日用品")
            food_goods = user_goods.filter(category="食料")
            other_goods = user_goods.filter(category="その他")
            return render(request, 'menu.html', {
                'goods_items': all_goods,
                'daily_goods': daily_goods,
                'food_goods': food_goods,
                'other_goods': other_goods,
                'error_message': error_message  # エラーメッセージを渡す
            })

        else:
            # カテゴリを取得する
            find_origin_item = DefaultGoods.objects.filter(name=new_item).first()

            if find_origin_item is None:
                error_message = f"{new_item}はデフォルト物品に存在しません。新規物品登録を行ってください。"

                all_goods = MyGoods.objects.all()
                user_goods = MyGoods.objects.filter(uid=find_uid.uuid)

                daily_goods = user_goods.filter(category="日用品")
                food_goods = user_goods.filter(category="食料")
                other_goods = user_goods.filter(category="その他")
                return render(request, 'menu.html', {
                    'goods_items': all_goods,
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
        return redirect('remind:menu')
    
# 新規物品登録　2025/2/16 うっちゃん追加
class MyitemsAdd(View):
    template_name = 'new-item-add.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        logger.debug(f"通ったよ")  

        item_name = request.POST.get('item_name')
        item_default_term = request.POST.get('item_defltterm',4)
        # item_default_term = int(item_default_term) 
        item_category = request.POST.get("category")
        logger.debug(f"{item_name},{item_default_term},{item_category}")  

        # 入力された物品がテーブルに存在するか確認
        item = DefaultGoods.objects.filter(name=item_name).first()

        if item:
            context = {'error_message': '商品がすでに存在しています。'}
            return render(request, self.template_name, context)
        
        else:
            logger.debug(f"{item_name},{item_default_term},{item_category}")  

            # 新しい物品をデータベースに保存
            new_item = DefaultGoods(name=item_name,
                                    default_term=item_default_term,
                                    category=item_category)
            new_item.save()
            # 成功したらメニュー画面へ
            return render(request,'menu.html', {'new_regist_items':new_item})   
            # return redirect('remind:menu')


# 設定画面　2025/2/16 うっちゃん追加
@login_required
def settings_page(request):
    return render(request, 'setting.html')

@login_required
def update_default_term(request):
     #return HttpResponse(f"Logged in user: {request.user.mailaddress}")
    user = request.user # 現在ログインしているユーザーを取得

    user_goods = MyGoods.objects.filter(uid=user.id)

    if request.method == 'POST':
        defaultform = DefaultTermForm(request.POST, instance=user)
        if defaultform.is_valid():
            default_term = defaultform.cleaned_data['default_term']
            defaultform.save()

            user_goods.update(next_purchase_term=default_term)

            #MyGoods.objects.filter(uid=user.id).update(next_purchase_term=default_term)

            return redirect('remind:menu')

    context = {
        'user_goods': user_goods
    }

    return redirect('remind:settings')


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

            goods.next_purchase_date = new_purchase_date + datetime.timedelta(weeks=new_next_purchase_term)

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

