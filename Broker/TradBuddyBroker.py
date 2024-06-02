# Create Own Broker for paper trading as well as Store Trad Historys import pandas as pd 
from werkzeug.security import generate_password_hash, check_password_hash
import pandas as pd

# --------------------[Custom Imports]------------------------
import os
import pymongo
from dotenv import load_dotenv
load_dotenv()

def DBConnection_for_Broker():
    try:
        db_client = os.getenv("MONGODB_STRING")
        verion = 2
        mongo_connection = pymongo.MongoClient(db_client)[f'TradBuddy_V{verion}_Worker_1']
        account_collection = mongo_connection.get_collection("Account")
        notifications_collection = mongo_connection.get_collection("Notifications")
        orders_collection = mongo_connection.get_collection("Orders")
        transactions_collection = mongo_connection.get_collection("Transactions")
        print("Database connection established successfully")
        return transactions_collection, account_collection, notifications_collection, orders_collection,mongo_connection
    except Exception as e:
        print(f"Failed to establish database connection: {e}")
        return None, None, None, None, None

import datetime 
import random

def create_uuid(name):
    randint = random.randint(111, 999)
    mytimestampstr = str(datetime.datetime.now().timestamp()).replace(".", "")
    myuuid = f"{name}-{mytimestampstr}{randint}"
    return myuuid

def tbCurrentTimestamp():
    return datetime.datetime.now()

class TradBuddyBroker:
    def __init__(self):
        self.transactions_collection, self.account_collection, self.notifications_collection, self.orders_collection, self.mongo_connection = DBConnection_for_Broker()
        self.isAuthenticated = False
        

    def account_create(self, **data):
        try:
            account_id = f"ACC-{str(self.account_collection.count_documents({}) + 1).zfill(3)}"
            accountSchema = {
                    "account_id": account_id,
                    "account_balance": data.get("account_balance") or 100000,
                    "is_activate": data.get("is_activate", True),
                    "strategy": data.get("strategy", {}),
                    "max_trad_per_day": data.get("max_trad_per_day", 10),
                    "todays_margin":(data.get("todays_margin", float(0))),
                    "todays_trad_margin": (data.get("todays_trad_margin", float(0))),
                    "account_min_profile": (data.get("account_min_profile", float(0))),
                    "account_max_loss": (data.get("account_max_loss", float(0))),
                    "base_stoploss": (data.get("base_stoploss", float(0))),
                    "base_target": (data.get("base_target", float(0))),
                    "trailing_status": data.get("trailing_status", True),
                    "trailing_stoploss": (data.get("trailing_stoploss", float(0))),
                    "trailing_target": (data.get("trailing_target", float(0))),
                    "payment_status": data.get("payment_status", "Paper Trad"),
                    "description": data.get("description", ""),
                    "last_updated_datetime": tbCurrentTimestamp()
                }

            self.account_collection.insert_one(accountSchema)
            return {
                "message": f"account_create [{account_id}]: success - Account created successfully.",
                "body": account_id,
                "status": "Ok"
            }
        except Exception as e:
            return {
                "message": "account_create: fail - Failed to create account.",
                "body": str(e),
                "status": "Fail"
            }

    def account_update(self, account_id, update_data):
        try:
            print(update_data,"update_data")
            result = self.account_collection.update_one({"account_id": "ACC-001"}, {"$set": update_data})
            if result.modified_count:
                return {
                    "message": f"account_update [{account_id}]: success - Account updated successfully.",
                    "body": None,
                    "status": "Ok"
                }
            else:
                return {
                    "message": "account_update: fail - No matching account found for update.",
                    "body": None,
                    "status": "Fail"
                }
        except Exception as e:
            return {
                "message": "account_update: fail - Failed to update account.",
                "body": str(e),
                "status": "Fail"
            }

    def account_get(self, account_id):
        try:
            result = self.account_collection.find_one({"account_id": account_id})
            del result["_id"]
            return {
                "message": f"account_get [{account_id}]: success - Account retrieved successfully.",
                "body": result,
                "status": "Ok"
            }
        except Exception as e:
            return {
                "message": f"account_get [{account_id}]: fail - Failed to get account.",
                "body": str(e),
                "status": "Fail"
            }
        
    def account_list(self):
        result = self.account_collection.find({})
        if result:
            return list(result)
        return []


    def account_delete(self, account_id):
        try:
            result = self.account_collection.delete_one({"account_id": account_id})
            if result.deleted_count:
                return {
                    "message": f"account_delete [{account_id}]: success - Account deleted successfully.",
                    "body": None,
                    "status": "Ok"
                }
            else:
                return {
                    "message": "account_delete: fail - No matching account found for deletion.",
                    "body": None,
                    "status": "Fail"
                }
        except Exception as e:
            return {
                "message": "account_delete: fail - Failed to delete account.",
                "body": str(e),
                "status": "Fail"
            }

    def account_transaction_create(self, transaction_type, amount, account_id, notes=""):
        try:
            account_data = self.account_collection.find_one({"profile_id": self.profile_id, "account_id": account_id})
            if not account_data:
                return {
                    "message": f"account_transaction: fail - Account not found for profile: {self.profile_id} and account: {account_id}",
                    "body": None,
                    "status": "Fail"
                }

            if transaction_type == "deposit":
                self.account_collection.update_one({"_id": account_data["_id"]}, {"$inc": {"account_balance": amount}})
                return {
                    "message": f"account_transaction: success - {amount} is deposited in account: {account_id} for profile: {self.profile_id}",
                    "body": None,
                    "status": "Ok"
                }

            elif transaction_type == "withdraw":
                if account_data["account_balance"] >= amount:
                    self.account_collection.update_one({"_id": account_data["_id"]}, {"$inc": {"account_balance": -amount}})
                    return {
                        "message": f"account_transaction: success - {amount} is withdrawn from account: {account_id} for profile: {self.profile_id}",
                        "body": None,
                        "status": "Ok"
                    }
                else:
                    return {
                        "message": f"account_transaction: fail - Insufficient balance in account: {account_id} for profile: {self.profile_id}",
                        "body": None,
                        "status": 400
                    }
            else:
                return {
                    "message": "account_transaction: fail - Select proper transaction type.",
                    "body": None,
                    "status": 400
                }

        except Exception as e:
            return {
                "message": "account_transaction: fail - Failed to perform account transaction.",
                "body": str(e),
                "status": "Fail"
            }
        finally :
            transaction_id = create_uuid("ACC-TRAN")
            transaction_schema = {
                "transaction_id": transaction_id,
                "profile_id": self.profile_id,
                "account_id": account_id,
                "type": transaction_type.capitalize(),
                "amount": amount,
                "datetime": tbCurrentTimestamp(),
                "notes": notes
            }
            # Insert transaction data into the collection
            self.transactions_collection.insert_one(transaction_schema)
            return {
                "message": f"account_transaction: success - Account transaction successful, Transaction ID: {transaction_id}",
                "body": None,
                "status": "Ok"
            }
        
    def account_transaction_view(self,account_id):
        try:
            account_data = self.account_collection.find({"profile_id": self.profile_id, "account_id": account_id})
            del account_data["_id"]
            return {
                "message": "account_transactions: sucess.",
                "body": account_data,
                "status": 200
            }
        except Exception as e:
            return {
                "message": "account_transaction: fail - Select proper transaction type.",
                "body": e,
                "status": 400
            }
 

    def order_place(self, **data):
        try:
            order_id = create_uuid("ORD")
            isBuyMargin = data.get("buyprice") * data.get("qnty")
            order_schema = {
                "order_id": order_id,
                "account_id": data.get("account_id"),
                "strategy": data.get("strategy"),
                "date": tbCurrentTimestamp().strftime("%d-%m-%Y"),
                "trad_status": "Open",
                "trad_type": data.get("type", "Buy"),
                "trad_index": data.get("trad_index"),
                "trad_side": data.get("trad_side"),
                "trigger_price": data.get("trigger_price"),
                "option_symbol": data.get("option_symbol"),
                "qnty": data.get("qnty"),
                "buy_price": data.get("buyprice"),
                "sell_price": None,
                "stoploss_price": data.get("sl_price"),
                "target_price": data.get("target_price"),
                "buy_datetime": tbCurrentTimestamp(),
                "sell_datetime": None,
                "buy_margin": isBuyMargin,
                "sell_margin": None,
                "trailing_count":0,
                "pnl_status": None,
                "pnl": None,
                "notes": data.get("notes")
            }
            account = self.account_collection.find_one({"account_id": data["account_id"]})
            if not account:
                return {
                    "message": f"order_place: fail - Failed to place order: Account not found.",
                    "body": None,
                    "status": "Fail"
                }

            if account.get("account_balance", 0) < isBuyMargin:
                return {
                    "message": f"order_place: fail - Failed to place order: Insufficient balance in the Account ID: {data['account_id']} Require Balance is More then {isBuyMargin}",
                    "body": None,
                    "status": 400
                }

            self.orders_collection.insert_one(order_schema)
            self.account_collection.update_one({"account_id": data["account_id"]}, {"$inc": {"account_balance": -isBuyMargin}})
            return {
                "message": f"order_place [{order_id}]: success - Order placed successfully.",
                "body": order_id,
                "status": "Ok"
            }

        except Exception as e:
            return {
                "message": "order_place: fail - Failed to place order.",
                "body": str(e),
                "status": "Fail"
            }
        
    def order_update(self,order_id,query):
        try:
            self.orders_collection.update_one({"order_id": order_id}, {"$set": query})
            return {
                        "message": f"order_update [{order_id}]: success - Order Update successfully",
                        "body": None,
                        "status": "Ok"
                    }
        except Exception as e:
            return {
                "message": "order_update: fail - Failed to update the order.",
                "body": str(e),
                "status": "Fail"
            }

    def order_close(self, account_id, order_id, sell_price):
        try:
            order = self.orders_collection.find_one({"order_id": order_id, "account_id": account_id})
            if order:
                isSellMargin = float(order.get("qnty") * sell_price)
                isPnl = isSellMargin - order.get("buy_margin")
                update_data = {
                    "trad_status": "Close",
                    "sell_price": sell_price,
                    "sell_datetime": tbCurrentTimestamp(),
                    "sell_margin": isSellMargin,
                    "pnl_status": "Profit" if isPnl >= 1 else "Loss",
                    "pnl": isPnl
                }
                # Update order document
                result_order = self.orders_collection.update_one({"order_id": order_id, "account_id": account_id}, {"$set": update_data})
                result_account = self.account_collection.update_one({"account_id": account_id}, {"$inc": {"account_balance": isSellMargin}})

                if result_order.modified_count > 0 and result_account.modified_count > 0:
                    return {
                        "message": f"order_close [{order_id}]: success - Order closed successfully with PNL: {isPnl}",
                        "body": None,
                        "status": "Ok"
                    }
                else:
                    return {
                        "message": "order_close: fail - Failed to close the order.",
                        "body": None,
                        "status": "Fail"
                    }
            else:
                return {
                    "message": "order_close: fail - Order not found.",
                    "body": None,
                    "status": 404
                }
        except Exception as e:
            return {
                "message": "order_close: fail - Failed to close the order.",
                "body": str(e),
                "status": "Fail"
            }


        
    def order_opens(self):
        try:
            order_book = self.orders_collection.find({"trad_status": "Open"})
            return list(order_book)
        except:
            return None

    def order_get(self,query):
        try:
            order_book = self.orders_collection.find(query)
            return list(order_book)
        except:
            return None

    def order_book(self, account_id):
        try:
            order_book = self.orders_collection.find_one({"account_id": account_id})
            del order_book["_id"]
            return {
                "message": "order_book: success - Order book retrieved successfully.",
                "body": order_book,
                "status": "Ok"
            }
        except Exception as e:
            return {
                "message": f"order_book: fail - Failed to get order book.",
                "body": str(e),
                "status": "Fail"
            }

    def generate_report(self, account_id):
        try:
            order_book = self.orders_collection.find({"account_id": account_id, "trad_status": "Close"})
            if order_book:
                df = pd.DataFrame(order_book)
                count_df_group = df.groupby(['trad_index', 'trad_side', 'pnl_status']).size().reset_index(name='Total Trades')
                count_df = count_df_group.pivot_table(index='trad_index', columns=['trad_side', 'pnl_status'], values='Total Trades', aggfunc='sum', fill_value=0)
                count_df.columns = ['_'.join(col) for col in count_df.columns.values]
                count_df['Total_Tred'] = count_df.sum(axis=1)
                count_df.reset_index(inplace=True)

                amount_df_group = df.groupby(['trad_index', 'trad_side', 'pnl_status'])['pnl'].sum().reset_index(name='Total PnL Grow')
                amount_df = amount_df_group.pivot_table(index='trad_index', columns=['trad_side', 'pnl_status'], values='Total PnL Grow', aggfunc='sum', fill_value=0)
                amount_df.columns = ['_Amount_'.join(col) for col in amount_df.columns.values]
                amount_df['Total_Tred_Amount'] = amount_df.sum(axis=1)

                merged_df = pd.merge(count_df, amount_df, on='trad_index', how='outer').fillna(0)
                columns_to_add = ['CE_Loss', 'PE_Loss', 'PE_Profit', 'CE_Profit', 'CE_Amount_Loss', 'PE_Amount_Loss', 'PE_Amount_Profit', 'CE_Amount_Profit']
                merged_df = merged_df.reindex(columns=merged_df.columns.union(columns_to_add), fill_value=0)
                merged_df['Total_Tred'] = merged_df[['CE_Loss', 'PE_Loss', 'PE_Profit', 'CE_Profit']].sum(axis=1)
                merged_df['Total_Tred_Amount'] = merged_df[['CE_Amount_Loss', 'PE_Amount_Loss', 'PE_Amount_Profit', 'CE_Amount_Profit']].sum(axis=1)

                total_row = merged_df.sum(numeric_only=True)
                total_row['trad_index'] = 'Over All'
                total_df = pd.DataFrame([total_row])
                output = pd.concat([merged_df, total_df], ignore_index=True).to_dict('records')
                return {
                    "message": "generate_report: success - Report generated successfully.",
                    "body": output,
                    "status": "Ok"
                }
            else:
                return {
                    "message": "generate_report: fail - Order book has no values.",
                    "body": None,
                    "status": "Fail"
                }
        except Exception as e:
            return {
                "message": "generate_report: fail - Failed to generate report.",
                "body": str(e),
                "status": "Fail"
            }
    
    def perform_analysis(self, account_id): # Daily data analysis
        try:
            order_book = self.orders_collection.find({"account_id": account_id})
            alldf = pd.DataFrame(order_book)
            total_trades = alldf.shape[0]
            total_open_list = alldf[alldf["trad_status"] == "Open"]
            total_close_list = alldf[alldf["trad_status"] == "Close"]

            closed_trades = total_close_list.shape[0]
            open_trades = total_open_list.shape[0]
            total_pnl = sum(total_close_list["pnl"])
            pnl_per_trade = total_pnl / closed_trades if closed_trades > 0 else 0
            win_ratio = (total_close_list[total_close_list["pnl"] > 0].shape[0] / closed_trades) * 100 if closed_trades > 0 else 0

            analysis = {
                "Total Trades": total_trades,
                "Closed Trades": closed_trades,
                "Open Trades": open_trades,
                "Total PnL": total_pnl,
                "PnL per trade": pnl_per_trade,
                "Win Ratio": win_ratio
            }

            return {
                "message": "perform_analysis: success - Analysis performed successfully.",
                "body": analysis,
                "status": "Ok"
            }
        except Exception as e:
            return {
                "message": "perform_analysis: fail - Failed to perform analysis.",
                "body": str(e),
                "status": "Fail"
            }














