from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .models import Balance, Item, HistoryBalance, Feedback
from .forms import BalanceForm, ItemForm, InitialSavingsForm, ProfilePictureForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template import loader


def registerPage(request):          
    if request.method=='POST':  
        uname=request.POST.get('username')
        email=request.POST.get('email')
        pass1=request.POST.get('password')
      
        if User.objects.filter(username=uname).exists() or User.objects.filter(email=email).exists():
            messages.error(request,"Username/Email is already taken ")
            return redirect('register')
        else:
            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            return redirect('login')
    return render (request,'register.html')

def logoutPage(request):
    logout(request) 
    return redirect ('home')  


@login_required(login_url='login')        
def index(request):
   
    if not request.user.is_authenticated:
        return redirect('login')
        
    balance, created = Balance.objects.get_or_create(user=request.user)
    items = Item.objects.filter(user=request.user)
    history_data = HistoryBalance.objects.filter(user=request.user)
    
    return render(request, 'index1.html', {'items': items,'balance': balance.amount,'initial_savings': balance.savings,'balance': balance,'historydatas': history_data}) 
    

def loginPage(request):
        if request.method == 'POST': 
            username = request.POST.get('username')
            pass1 = request.POST.get('password')
 
            User = authenticate(request,username=username,password=pass1) 
            if User is not None:
                login(request,User) 
                return redirect('home')
            else:   
                messages.error(request,"Invalid Credentials!")
                return redirect("login")      
                      
        return render (request,'login.html')  

@login_required(login_url='login') 
def search_items(request):
    balance, created = Balance.objects.get_or_create(user=request.user)
    items = Item.objects.filter(user=request.user)
    history_data = HistoryBalance.objects.filter(user=request.user)
    
    if request.method == 'POST':
        search_query = request.POST.get('searched')
        items = Item.objects.filter(name__icontains=search_query,user=request.user) 
        
    else:
        return redirect('home')   
    
    return render(request, 'index1.html', {'items': items, 'search_query': search_query,'initial_savings': balance.savings,
                                           'balance': balance,'historydatas': history_data})
@login_required(login_url='login') 
def add_savings(request):
    balance, created = Balance.objects.get_or_create(user=request.user)
    items = Item.objects.filter(user=request.user)
    history_data = HistoryBalance.objects.filter(user=request.user)
    
    if request.method == 'POST':
        savings_form = InitialSavingsForm(request.POST, balance)
        if savings_form.is_valid():
                    new_savings = savings_form.cleaned_data['savings']
                    if new_savings < 0:
                        messages.error(request, "Invalid Input!")
                        return redirect('home') 
                    else:
                        if new_savings > balance.amount:
                            messages.error(request, "Insufficient Balance!")
                            return redirect('home') 
                        else:
                            balance.amount -= new_savings
                            balance.savings += new_savings
                            balance.save()  
                            success_message = f"₱{new_savings} was added to your Savings!"
                            messages.success(request, success_message)
                            
                            HistoryBalance.objects.create(
                            user=request.user,
                            amount_history = balance.amount,
                            amount_added = new_savings,
                            type = "ADD SAVINGS",
                            )
                            
                        return redirect('home')
            
    else:  
         savings_form = InitialSavingsForm()
         return redirect('home')
    return render(request, 'index1.html', {'balance': balance,'initial_savings': balance.savings,'items': items,'historydatas': history_data})

def withdraw(request):
    balance, created = Balance.objects.get_or_create(user=request.user)
    items = Item.objects.filter(user=request.user)
    history_data = HistoryBalance.objects.filter(user=request.user)
    if request.method == 'POST':
        savings_form = InitialSavingsForm(request.POST, balance)
        if savings_form.is_valid():
                    withdraw = savings_form.cleaned_data['savings']
                    if withdraw < 0:
                        messages.error(request, "Invalid Input!")
                        return redirect('home') 
                    else:
                        if withdraw > balance.savings:
                            messages.error(request, "Insufficient Savings!")
                            return redirect('home') 
                        else:
                            balance.savings -= withdraw
                            balance.amount += withdraw
                            balance.save()  
                            success_message = f"₱{withdraw} was added to your Balance!"
                            messages.success(request, success_message)
                            
                            HistoryBalance.objects.create(
                            user=request.user,
                            amount_history = balance.amount,
                            amount_added = withdraw,
                            type = "WITHDRAW",
                            )
                        return redirect('home')
                
    else:  
         savings_form = InitialSavingsForm()
         return redirect('home')
    return render(request, 'index1.html',{'balance': balance,'initial_savings': balance.savings,'items': items,'historydatas':history_data})

@login_required(login_url='login') 
def add_balance(request):
    balance, created = Balance.objects.get_or_create(user=request.user)
    items = Item.objects.filter(user=request.user)
    history_data = HistoryBalance.objects.filter(user=request.user)
    if request.method == 'POST':
        balance_form = BalanceForm(request.POST, balance)

        if balance_form.is_valid():
                    new_balance = balance_form.cleaned_data['amount']
                    if new_balance < 0:
                        messages.error(request, "Invalid Input!")
                        return redirect('home') 
                    else:
                        balance.amount += new_balance 
                        balance.save()  
                        HistoryBalance.objects.create(
                            user=request.user,
                            amount_history = balance.amount,
                            amount_added = new_balance,
                            type = "ADD BALANCE",
                            )
                        success_message = f"₱{new_balance} was added to your balance!"
                        messages.success(request, success_message)
                        return redirect('home') 
    else:  
        balance_form = BalanceForm(instance=balance)
        return redirect('home')
                             
    return render(request, 'index1.html',{'balance': balance,'initial_savings': balance.savings,'items': items,'historydatas':history_data})

def deduct_balance(request):
    balance, created = Balance.objects.get_or_create(user=request.user)
    items = Item.objects.filter(user=request.user)
    history_data = HistoryBalance.objects.filter(user=request.user)
    if request.method == 'POST':
        balance_form = BalanceForm(request.POST, balance)

        if balance_form.is_valid():
                    ded_balance = balance_form.cleaned_data['amount']
                    if ded_balance < 0:
                        messages.error(request, "Invalid Input!")
                        return redirect('home') 
                    else:
                        if balance.amount < ded_balance:
                            messages.error(request, "Insufficient Balance!")
                            return redirect('home') 
                        else:
                            balance.amount -= ded_balance 
                            balance.save()  
                            HistoryBalance.objects.create(
                            user=request.user,
                            amount_history = balance.amount,
                            amount_added = ded_balance,
                            type = "DEDUCT BALANCE",
                            )
                            success_message = f"₱{ded_balance} was Deducted from your balance!"
                            messages.success(request, success_message)
                            return redirect('home') 
    else:  
        balance_form = BalanceForm(instance=balance)
        return redirect('home')
           
    return render(request, 'index1.html',{'balance': balance,'initial_savings': balance.savings,'items': items,'historydatas':history_data})

@login_required(login_url='login') 
def add_items(request):
    balance, created = Balance.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        item_form = ItemForm(request.POST)
     
        if item_form.is_valid():
            item = item_form.save(commit=False)
            item.user = request.user
            item_name = item_form.cleaned_data['name']
            item_price = item_form.cleaned_data['price']

            
                        
            if item_price <= balance.amount:
                item.price2 = item_price
                item.save()
                balance.amount -= item_price
                balance.save()
                
                HistoryBalance.objects.create(
                            user=request.user,
                            amount_history = balance.amount,
                            amount_added = item_price,
                            type = "ITEM",
                            )
                
                success_message = f"Expense {item_name} was added to Expenses!"
                messages.success(request, success_message)
                return redirect ('home')
                
            else:
                error_message = f"Insufficient Balance!"
                messages.error(request, error_message)
                return redirect ('home')
             
    else:  
        item_form = ItemForm()
        return redirect('home')
    return render(request, 'index1.html')

def update_items(request,item_id):
    balance, created = Balance.objects.get_or_create(user=request.user)
    upitems = Item.objects.get(pk=item_id,user=request.user)
    upitems.price2 = upitems.price
   
    if request.method == 'POST':
            new_name = request.POST.get("ItemName")
            upitems.price_str = request.POST.get("ItemPrice") 
            new_desc = request.POST.get("Desc")
            upitems.price = int(upitems.price_str)
            
            if upitems.price < 0:
                messages.error(request, "Invalid Input!")
                return redirect('home')
            if upitems.name != new_name:
                upitems.name = new_name
                upitems.save()
                
            if upitems.desc != new_desc:
                upitems.desc = new_desc 
                upitems.save()

            if upitems.name != new_name or upitems.desc != new_desc or upitems.price != upitems.price2:
                upitems.name = new_name
                upitems.desc = new_desc
                
                if upitems.price < upitems.price2:
                    price_changed =  upitems.price -upitems.price2 
                    price_difference = balance.amount - price_changed
                    if price_difference > 0:
                        upitems.save()
                        balance.amount -=price_changed
                        balance.save()
                        HistoryBalance.objects.create(
                                    user=request.user,
                                    amount_history = balance.amount,
                                    amount_added = price_changed,
                                    type = "ITEM EDIT",
                                    )
                        return redirect('home')

                    else:
                        error_message = f"Insufficient Balance!"
                        messages.error(request, error_message)
                        return redirect('home')
                    
                elif upitems.price > upitems.price2:
                    price_changed = upitems.price - upitems.price2
                    price_difference = balance.amount - price_changed
                    if price_difference >= 0:
                        upitems.save()
                        balance.amount -= price_changed
                        balance.save()
                        HistoryBalance.objects.create(
                                    user=request.user,
                                    amount_history = balance.amount,
                                    amount_added = price_changed,
                                    type = "ITEM EDIT",
                                    )
                        return redirect('home')
                    else:
                        error_message = f"Insufficient Balance!"
                        messages.error(request, error_message)
                        return redirect('home')

            
            
            if upitems.price < upitems.price2:
                price_changed =  upitems.price -upitems.price2 
                price_difference = balance.amount - price_changed
                if price_difference > 0:
                    upitems.save()
                    balance.amount -=price_changed
                    balance.save()
                    HistoryBalance.objects.create(
                                user=request.user,
                                amount_history = balance.amount,
                                amount_added = price_changed,
                                type = "ITEM EDIT",
                                )
                    return redirect('home')

                else:
                    error_message = f"Insufficient Balance!"
                    messages.error(request, error_message)
                    return redirect('home')
                
            elif upitems.price > upitems.price2:
                price_changed = upitems.price - upitems.price2
                price_difference = balance.amount - price_changed
                if price_difference >= 0:
                    upitems.save()
                    balance.amount -= price_changed
                    balance.save()
                    HistoryBalance.objects.create(
                                user=request.user,
                                amount_history = balance.amount,
                                amount_added = price_changed,
                                type = "ITEM EDIT",
                                )
                    return redirect('home')
                else:
                    error_message = f"Insufficient Balance!"
                    messages.error(request, error_message)
                    return redirect('home')
            else:
                return redirect('home')

    return render(request, 'index1.html',{'upitems':upitems})
def delete_items(request, item_id):
    items = Item.objects.get(pk=item_id,user=request.user)
    items.delete()
    
    return redirect ('home') 
@login_required(login_url='login') 
def add_profile(request):
    balance = Balance.objects.get(user=request.user)
    if request.method == 'POST':
        profile_form = ProfilePictureForm(request.POST, request.FILES, instance=request.user.balance)   
        if profile_form.is_valid():
            profile_form.save()
            return redirect('home')
    else:  
        profile_form = ProfilePictureForm(instance=balance)
        return redirect('home')
       
    return render(request, 'index1.html')

def aboutPage(request):
    return render(request,'about.html')
 
def contactPage(request):
    if request.method=='POST':  
        fullname=request.POST.get('fullname')
        email=request.POST.get('email')
        message=request.POST.get('message')

        mess = Feedback.objects.create(fullname=fullname, email=email, message=message)
        mess.save
        return redirect('contact')
    return render(request,'contact.html')
  
def deleterecord(request):
    balance = Balance.objects.get(user=request.user)
    items = Item.objects.filter(user=request.user)
    history = HistoryBalance.objects.filter(user=request.user)   
          
    history.delete()
    items.delete()
    
    balance.amount = 0
    balance.savings = 0
    balance.save()
    
    return redirect('home')
 