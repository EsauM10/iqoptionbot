from typing import Any
import webbrowser

from flask import Flask, jsonify, render_template, request, redirect
from flask_socketio import SocketIO

from iqoptionbot.api.repository import Repository
from iqoptionbot.api.services.bot import BotHandler
from iqoptionbot.api.events import FrontendChannels

app = Flask(__name__)
socketio    = SocketIO(app)
repository  = Repository()
frontend    = FrontendChannels(socketio)
bot_handler = BotHandler(frontend, repository)


@app.route('/', methods=['GET'])
def index():
    if(bot_handler.is_connected):
        return redirect('/dashboard')
    return redirect('/login')


@app.route('/login', methods=['GET'])
def login_page():
    if(bot_handler.is_connected):
        return redirect('/dashboard') 
    return render_template('login/login.html')


@app.route('/login', methods=['POST'])
def handle_login():
    try:
        json  = request.get_json()
        email = str(json['email'])
        password = str(json['password'])
        bot_handler.connect(email, password)
        return jsonify({'content': 'Logged In'}), 200

    except Exception as ex:
        return jsonify({'error': f'{ex}'}), 500


@app.route('/dashboard', methods=['GET'])
def dashboard():
    if(not bot_handler.is_connected):
        return redirect('/login')
    return render_template('dashboard/index.html')


# ================================== Events ================================== #
@socketio.on('alerts')
def handle_alerts(data: dict[str, Any]):
    method = str(data['method'])
    payload: dict[str, Any] = data['payload']

    if(method == 'POST'):
        asset_name = str(payload['asset_name'])
        price = float(payload['price'])
        alert = repository.create_alert(asset_name, price)
        frontend.add_alert(alert)
    elif(method == 'DELETE'):
        alert_id = int(payload['alert_id'])
        repository.delete_alert(alert_id)
        frontend.delete_alert(alert_id)


@socketio.on('connect')
@bot_handler.login_required
def on_connect(): 
    open_assets = bot_handler.exchange.get_open_assets(option='turbo', filter='open')
    account_balance = bot_handler.exchange.balance()
    repository.create_assets(open_assets)
    repository.update_selected_asset(open_assets[0]['name'])

    frontend.update_open_assets(repository.selected_asset, repository.get_open_assets_names())
    frontend.update_account_balance(account_balance)


@socketio.on('home')
@bot_handler.login_required
def home_page():
    asset = repository.get_asset_by_name(repository.selected_asset)
    asset.price = bot_handler.exchange.get_current_price(asset.name)
    frontend.update_open_assets(repository.selected_asset, repository.get_open_assets_names())
    frontend.update_transactions(repository.transactions)
    frontend.update_asset_data(asset)
    frontend.update_asset_alerts(asset)


@socketio.on('settings')
@bot_handler.login_required
def settings_page(data: dict[str, Any]):
    method = str(data['method'])
    payload: dict[str, Any] = data['payload']
    
    if(method == 'GET'):
        account_mode = bot_handler.exchange.get_account_mode()
        frontend.update_setup(account_mode, repository.setup)
    elif(method == 'PUT'):
        account_mode = str(payload['account_mode'])
        if(account_mode == 'PRACTICE' or account_mode == 'REAL'):
            bot_handler.exchange.change_account(account_mode)
            frontend.update_balance(bot_handler.exchange.balance())
        repository.setup.set_money(float(payload['money_amount']))
        repository.setup.stopgain    = float(payload['stop_win'])
        repository.setup.stoploss    = float(payload['stop_loss'])
        repository.setup.martingales = int(payload['martingales'])
        repository.setup.soros       = int(payload['soros'])
        frontend.push_notification('info', message='Setup atualizado')


@socketio.on('updateSelectedAsset')
def update_selected_asset(asset_name: str):
    asset = repository.get_asset_by_name(asset_name)
    asset.price = bot_handler.exchange.get_current_price(asset.name)
    frontend.update_asset_data(asset)
    frontend.update_asset_alerts(asset)


@socketio.on('startBot')
def start_bot(asset_name: str):
    bot_handler.start(asset_name)


@socketio.on('stopBot')
def stop_bot():
    bot_handler.stop()
    

@socketio.on_error()
def error_handler(e):
    bot_handler.stop()
    print(f'[{type(e)}]', e)


# ============================================================================ #
def run_app(port: int = 5000):
    debug = False
    
    if(not debug):
        webbrowser.open(f'http://localhost:{port}')
    socketio.run(app, port=port, debug=debug, use_reloader=debug, log_output=True)

if(__name__=='__main__'):
    run_app()
