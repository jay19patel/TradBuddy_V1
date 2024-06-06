from flask import Flask, render_template, request, redirect, url_for, session,flash
from flask_bcrypt import Bcrypt
from functools import wraps
from datetime import timedelta,datetime

from Broker.TradBuddyBroker import TradBuddyBroker

app = Flask(__name__)
bcrypt = Bcrypt(app)
app.secret_key = 'it_is_very_strong_password_123'
app.permanent_session_lifetime = timedelta(days=1)

tb_broker = TradBuddyBroker()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        profile_id = request.form['profile_id']
        profile_password = request.form['profile_password']

        # is_auth = tb_broker.profile_login(profile_id=profile_id, profile_password=profile_password)
        # is_auth = {"status":"Authenticated"}
        # if is_auth.get("status") == "Authenticated":
        if profile_id == "122333" and profile_password == "122333":
            # session['username'] = is_auth["body"]
            session['username'] = "Jay Patel"
            session['username'] = "Jay"
            session['profile_id'] = "123"
            print("Success Login")
            return redirect(url_for('home'))
        else:
            flash("Not Authenticated !", 'error')
            return render_template('Pages/login.html')
    
    return render_template('Pages/login.html')


@app.context_processor
def inject_accounts():
    list_data = tb_broker.account_list(query={})
    # list_data = []
    if "message" in list_data:
        flash("Please Relogin","error")
        return []
    else:
        return {'accounts_list': list_data}
        # return {'accounts_list': [1,2,3]}


@app.route('/')
def home():
    return render_template('Pages/home.html')


@app.route('/profile')
@login_required
def Profile():
    AccountData = tb_broker.account_list({})

    return render_template('Pages/accountProfile.html' ,AccountsDetails=AccountData)


@app.route('/logout')
@login_required
def logout():
    session.pop('username', None)
    session.pop('profile_id', None)
    return redirect(url_for('login'))


@app.route('/logs')
@login_required
def logs():

    with open('Records/StrategyManager.log', 'r') as file:
        log_content = file.read()

    return render_template('Pages/logs.html', log_content=log_content)



@app.route('/add_account' ,methods=['GET', 'POST'])
@login_required
def AddAccount():
     
    if request.method == 'POST':
        # Retrieve form data
        data = request.form
        account_balance = data.get('account_balance')
        max_trad = data.get('max_trade')
        description = data.get('description')
        selected_indices = request.form.getlist('trading_index[]')
        strategy_mapping = {}

        for index in selected_indices:
            strategy = request.form.get(f'strategy[{index}]')
            if strategy:
                formatted_index = f"NSE:{index}-INDEX"
                if strategy in strategy_mapping:
                    strategy_mapping[strategy].append(formatted_index)
                else:
                    strategy_mapping[strategy] = [formatted_index]
        strategies = strategy_mapping


        account_activation_status = data.get('account_activation_status')
        trailing_status = data.get('trailing_status')
        payment_status = data.get('payment_status')
        today_margin = data.get('today_margin')
        today_single_trade_margin = data.get('today_single_trade_margin')
        minimum_profit = data.get('minimum_profit')
        maximum_loss = data.get('maximum_loss')
        base_stoploss = data.get('base_stoploss')
        base_target = data.get('base_target')
        base_trailing_stoploss = data.get('base_trailing_stoploss')
        base_trailing_target = data.get('base_trailing_target')


    
        # Call function with optimized variables
        account_status = tb_broker.account_create(
            account_balance=account_balance,
            is_activate=account_activation_status,
            strategy=strategies,
            max_trad_per_day=max_trad,
            todays_margin=today_margin,
            todays_trad_margin=today_single_trade_margin,
            account_min_profile=minimum_profit,
            account_max_loss=maximum_loss,
            base_stoploss=base_stoploss,
            base_target=base_target,
            trailing_status=trailing_status,
            trailing_stoploss=base_trailing_stoploss,
            trailing_target=base_trailing_target,
            payment_status=payment_status,
            description=description
        )
        flash(account_status.get("message"), 'success')
        return redirect(f"/account_setting/{account_status.get('body')}")

     
    return render_template('Pages/add_account.html')

@app.route('/account_setting/<account>' ,methods=['GET', 'POST'])
@login_required
def AccountSetting(account):
    if request.method == 'POST':
        data = request.form
        update_data = {
            "account_balance": data.get('strategy'),
            "is_activate":data.get('account_activation_status'),
            "trad_indexs":data.getlist('trading_index[]'),
            "strategy":data.get('strategy'),
            "max_trad_per_day":data.get('max_trade'),
            "todays_margin":data.get('today_margin'),
            "todays_trad_margin":data.get('today_single_trade_margin'),
            "account_min_profile":data.get('minimum_profit'),
            "account_max_loss":data.get('maximum_loss'),
            "base_stoploss":data.get('base_stoploss'),
            "base_target":data.get('base_target'),
            "trailing_status":data.get('trailing_status'),
            "trailing_stoploss":data.get('base_trailing_stoploss'),
            "trailing_target":data.get('base_trailing_target'),
            "payment_status": data.get('payment_status'),
            "description": data.get('description'),
            "last_updated_datetime":datetime.now()
        }
        update_status = tb_broker.account_update(account,update_data)

        flash(update_status["message"],"")
        return redirect(f"/account_setting/{account}")


        
    account_data = tb_broker.account_get(account)
    if account_data["status"] == "Ok":
        accout_details = account_data["body"]
        accout_details['last_updated_datetime'] = accout_details['last_updated_datetime'].strftime('%Y-%m-%d %H:%M:%S')
    else:
        accout_details = None

    
    return render_template('Pages/accountSetting.html',account_data=accout_details)


@app.route('/account_delete/<account>')
@login_required
def AccountDelete(account):
    delete_status = tb_broker.account_delete(account)
    flash(delete_status["message"])
    return redirect(url_for('home'))


@app.route('/account_dashbord/<account>')
@login_required
def AccountDashbord(account):

    # print({"trad_status":"Close","date":datetime.today().strftime("%d-%m-%Y")})

    OpenTrades = tb_broker.order_get({"trad_status":"Open"})
    CloseTrades = tb_broker.order_get({"trad_status":"Close","date":datetime.today().strftime("%d-%m-%Y")})

    SummryData = tb_broker.generate_report(account)

    # print("OpenTrades----------------------------------------------")
    # print(OpenTrades)
    # print("CloseTrades---------------------------------------------")
    # print(CloseTrades)


#     OpenTrades = [
#     {'ID': 1, 'Symbol': 'AAPL', 'Buy Price': 150.25, 'SL Price': 155.50, 'Target Price': 500, 'Buy Datetime': '2024-04-15 10:00:00', 'Sell Datetime': '2024-04-15 12:00:00', 'Qnty': 100},
#     {'ID': 2, 'Symbol': 'GOOGL', 'Buy Price': 2500.75, 'SL Price': 2520.80, 'Target Price': 2000, 'Buy Datetime': '2024-04-15 11:00:00', 'Sell Datetime': '2024-04-15 13:00:00', 'Qnty': 50}
# ]
#     CloseTrades = [
#     {'ID': 3, 'Symbol': 'MSFT', 'Buy Price': 300.50, 'Sell Price': 295.25, 'PnL': -700, 'Buy Datetime': '2024-04-15 09:30:00', 'Sell Datetime': '2024-04-15 11:30:00', 'Qnty': 150},
#     {'ID': 4, 'Symbol': 'AMZN', 'Buy Price': 3500.25, 'Sell Price': 3550.80, 'PnL': 3000, 'Buy Datetime': '2024-04-15 10:30:00', 'Sell Datetime': '2024-04-15 12:30:00', 'Qnty': 40}
# ]

    print(SummryData['body'])

    SummryData = [{'CE_Amount_Loss': 0.0, 'CE_Amount_Profit': 0.0, 'CE_Loss': 0.0, 'CE_Profit': 0.0, 'PE_Amount_Loss': 0.0, 'PE_Amount_Profit': 0.0, 'PE_Loss': 0.0, 'PE_Profit': 0.0, 'Total_Tred': 0.0, 'Total_Tred_Amount': 0.0, 'trad_index': 'Over All'}]
   
    scorebords = [("Trades",0),("Open/Close",0),("Positive/Nagative ",0),("Win Rate",0),("Grow",0),("Account Balance",10000)]
    
    return render_template('Pages/accountDashbord.html',OpenTrades=OpenTrades,CloseTrades=CloseTrades,SummryData=SummryData,scorebords=scorebords)


@app.route('/update_trad')
@login_required
def UpdateTrad():
    updatetrad = {"name":1,"age":2}
    return render_template('Pages/UpdateTrad.html',updatetrad=updatetrad)

@app.route('/account_overview/<account>')
@login_required
def accountOverview(account):
    overviewData = []
    return render_template('Pages/accountOverview.html',overviewData=overviewData)


@app.route('/notification')
@login_required
def Notification():
    notifications = []
    return render_template('Pages/Notification.html',notifications=notifications)

@app.route('/account_tradbook/<account>')
@login_required
def AccountTradbook(account):
    tradbook = [
    {
        'Date': '2024-04-15',
        'ID': '1',
        'Symbol': 'AAPL',
        'Buy Price': '$150',
        'Sell Price': '$160',
        'PnL': -250,
        'Buy Datetime': '2024-04-01 09:00:00',
        'Sell Datetime': '2024-04-15 15:00:00',
        'Quantity': '10'
    },
    {
        'Date': '2024-04-14',
        'ID': '2',
        'Symbol': 'GOOGL',
        'Buy Price': '$2500',
        'Sell Price': '$2600',
        'PnL': 500,
        'Buy Datetime': '2024-04-01 10:00:00',
        'Sell Datetime': '2024-04-14 14:00:00',
        'Quantity': '5'
    },
    {
        'Date': '2024-04-13',
        'ID': '3',
        'Symbol': 'MSFT',
        'Buy Price': '$200',
        'Sell Price': '$220',
        'PnL': 200,
        'Buy Datetime': '2024-04-01 11:00:00',
        'Sell Datetime': '2024-04-13 13:00:00',
        'Quantity': '8'
    }
]

    return render_template('Pages/accountTradbook.html',tradbook=tradbook)



