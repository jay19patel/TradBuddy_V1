

from MicroScripts.AdjustmentTheory.app import save_expiry_index_price_after_3_pm


save_expiry_index_price_after_3_pm()
import schedule
import time
while True:
    schedule.run_pending()
    time.sleep(1)