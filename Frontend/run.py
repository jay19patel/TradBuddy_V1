from flask import Flask, render_template, request, redirect, url_for, session,flash
from functools import wraps
from datetime import timedelta,datetime
import json
from Broker.TradBuddyBroker import TradBuddyBroker

app = Flask(__name__)
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

# @app.errorhandler(Exception)
# def handle_exception(e):
#     flash(f"Something Wrong this Process You are redirecting : {e}")
#     return redirect(url_for('home'))

@app.route('/profile')
@login_required
def Profile():
    AccountData = tb_broker.account_list({})
    for accoun in AccountData:
        accoun['TotalTrads'] = len(tb_broker.orders_list(query={"account_id":accoun['account_id']}))
        accoun['TodaysTrads'] = len(tb_broker.orders_list(query={"account_id":accoun['account_id'],"date":datetime.today().strftime("%d-%m-%Y")}))
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

@app.route('/parameters')
@login_required
def parameters():
    try:
        with open('Records/strategies_results.json', 'r') as file:
            strategies_results = json.load(file)
    except (FileNotFoundError, IOError, json.JSONDecodeError) as e:
        print(f"Error reading strategies_results.json: {e}")
        strategies_results = None

    try:
        with open('Records/get_overview.json', 'r') as file:
            get_overview = json.load(file)
    except (FileNotFoundError, IOError, json.JSONDecodeError) as e:
        print(f"Error reading get_overview.json: {e}")
        get_overview = None

    if strategies_results:
        first_index = next(iter(strategies_results.values()))
        column_names = list(first_index.keys())
    else:
        column_names = []

    return render_template('Pages/parameters.html', strategies_results=strategies_results, get_overview=get_overview, column_names=column_names)



@app.route('/clear_logs', methods=['POST'])
@login_required
def clear_logs():
    log_file_path = 'Records/StrategyManager.log'
    
    # Clear the log file by truncating it
    open(log_file_path, 'w').close()
    
    # Redirect back to the logs page
    return redirect(url_for('logs'))


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
            account_min_profit=minimum_profit,
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
            "account_balance": float(data.get('strategy')),
            "is_activate":data.get('account_activation_status'),
            "trad_indexs":data.getlist('trading_index[]'),
            "strategy":data.get('strategy'),
            "max_trad_per_day":int(data.get('max_trade')),
            "todays_margin":float(data.get('today_margin')),
            "todays_trad_margin":float(data.get('today_single_trade_margin')),
            "account_min_profit":float(data.get('minimum_profit')),
            "account_max_loss":float(data.get('maximum_loss')),
            "base_stoploss":float(data.get('base_stoploss')),
            "base_target":float(data.get('base_target')),
            "trailing_status":data.get('trailing_status'),
            "trailing_stoploss":float(data.get('base_trailing_stoploss')),
            "trailing_target":float(data.get('base_trailing_target')),
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
    
    OpenTrades = tb_broker.orders_list({"trad_status":"Open","account_id":account})
    CloseTrades = tb_broker.orders_list({"trad_status":"Close","account_id":account,"date":datetime.today().strftime("%d-%m-%Y")})

    SummryData = tb_broker.generate_report(account,True)
    data = tb_broker.perform_analysis(account,True).get('body', {})

    scorebords = [
        ("Trades", data.get('Total Trades', 0)),
        ("Open/Close", f"{data.get('Open Trades', 0)}/{data.get('Closed Trades', 0)}"),
        ("Positive/Nagative", f"{data.get('Positive Trades', 0)}/{data.get('Nagative Trades', 0)}"),
        ("Win Rate", round(data.get('Win Ratio', 0), 2)),
        ("Grow", round(data.get('Total PnL', 0), 2)),
        ("Balance", round(tb_broker.account_get(account)['body']['account_balance'], 2))
    ]


    # scorebords = [("Trades",0),("Open/Close",0),("Positive/Nagative ",0),("Win Rate",0),("Grow",0),("Account Balance",10000)]
    
    return render_template('Pages/accountDashbord.html',OpenTrades=OpenTrades,CloseTrades=CloseTrades,SummryData=SummryData['body'],scorebords=scorebords)

@app.route('/update_trad/<order_id>', methods=['GET', 'POST'])
@login_required
def UpdateTrad(order_id):
    orderData = None

    if request.method == 'POST':
        stoploss_price = request.form['stoploss_price']
        target_price = request.form['target_price']

        update_status = tb_broker.order_update(order_id=order_id, query={"stoploss_price": stoploss_price, "target_price": target_price})
        flash(update_status)
        return redirect(url_for('UpdateTrad', order_id=order_id))  # Redirect to avoid form resubmission

    orderData = tb_broker.orders_get(query={"order_id": str(order_id)})
    return render_template('Pages/UpdateTrad.html', orderData=orderData)

@app.route('/account_overview/<account>')
@login_required
def accountOverview(account):
    overviewData = tb_broker.generate_report(account,False)['body']
    data = tb_broker.perform_analysis(account).get('body', {})

    scorebords = [
        ("Trades", data.get('Total Trades', 0)),
        ("Open/Close", f"{data.get('Open Trades', 0)}/{data.get('Closed Trades', 0)}"),
        ("Positive/Nagative", f"{data.get('Positive Trades', 0)}/{data.get('Nagative Trades', 0)}"),
        ("Win Rate", round(data.get('Win Ratio', 0), 2)),
        ("Grow", round(data.get('Total PnL', 0), 2)),
        ("Balance", round(tb_broker.account_get(account)['body']['account_balance'], 2))
    ]

    SummryData = tb_broker.daily_account_status(account) 
    return render_template('Pages/accountOverview.html',overviewData=overviewData,scorebords=scorebords,SummryData=SummryData)


@app.route('/notification')
@login_required
def Notification():
    notifications = []
    return render_template('Pages/Notification.html',notifications=notifications)

@app.route('/account_tradbook/<account>')
@login_required
def AccountTradbook(account):

    tradbook = tb_broker.order_book(account)
    print(tradbook)
    return render_template('Pages/accountTradbook.html',tradbook=tradbook['body'])



